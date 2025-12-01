"""
Web UI for macOS MCP Server
OPTIMIZED Flask-based chat interface
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import sys
from core.ollama_client import OllamaClient, load_config, get_system_prompt_with_memory
from core.memory import get_memory

app = Flask(__name__)
CORS(app)

# Global client instance
config = load_config()
client = OllamaClient(config)

# Set optimized system prompt on startup
client.set_system_prompt(get_system_prompt_with_memory())

# Pre-cache tools list for /api/tools endpoint
_cached_tools_list = None

def get_cached_tools():
    """Get cached tools list for API"""
    global _cached_tools_list
    if _cached_tools_list is None:
        _cached_tools_list = [
            {'name': name, 'description': tool['description']}
            for name, tool in client.mcp_server.tools.items()
        ]
    return _cached_tools_list


@app.route('/')
def index():
    """Serve the modern chat interface"""
    return render_template('index_modern.html', 
                         model=config['ollama']['model'],
                         tool_count=len(client.mcp_server.tools))


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with tool execution tracking"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Track tool executions efficiently
        tool_executions = []
        original_execute = client.mcp_server.execute_tool
        
        def tracked_execute(tool_name, parameters):
            result = original_execute(tool_name, parameters)
            tool_executions.append({
                'tool': tool_name,
                'params': parameters,
                'result': result
            })
            return result
        
        # Temporarily replace execute method
        client.mcp_server.execute_tool = tracked_execute
        
        # Get response from Ollama
        response = client.chat(message)
        
        # Restore original method
        client.mcp_server.execute_tool = original_execute
        
        return jsonify({
            'success': True,
            'response': response.get('message', {}).get('content', ''),
            'tool_executions': tool_executions,
            'model': config['ollama']['model']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation history"""
    client.reset_conversation()
    client.set_system_prompt(get_system_prompt_with_memory())
    return jsonify({'success': True, 'message': 'Conversation reset'})


@app.route('/api/memory', methods=['GET'])
def get_memories():
    """Get all agent memories"""
    memory = get_memory()
    return jsonify(memory.get_stats())


@app.route('/api/tools', methods=['GET'])
def list_tools():
    """List available tools (cached)"""
    return jsonify({'tools': get_cached_tools()})


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify({
        'model': config['ollama']['model'],
        'endpoint': config['ollama']['endpoint'],
        'temperature': config['ollama']['temperature'],
        'tool_count': len(client.mcp_server.tools)
    })


# Web UI is started via start_web.py launcher
