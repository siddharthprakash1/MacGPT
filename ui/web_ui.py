"""
Web UI for macOS MCP Server
Simple Flask-based chat interface
"""

from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import json
import sys
from core.ollama_client import OllamaClient, load_config

app = Flask(__name__)
CORS(app)

# Global client instance
config = load_config()
client = OllamaClient(config)

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html', 
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
        # Track tool executions
        tool_executions = []
        original_execute = client.mcp_server.execute_tool
        
        def tracked_execute(tool_name, parameters):
            # Print status for long-running tools
            long_running_tools = {
                'test_download_speed': 'Testing download speed (20-30 seconds)...',
                'test_upload_speed': 'Testing upload speed (10-15 seconds)...',
                'start_time_machine_backup': 'Starting Time Machine backup...',
                'download_file': f"Downloading file...",
                'compress_files': 'Compressing files...',
                'extract_archive': 'Extracting archive...',
                'web_scrape': 'Scraping website...',
                'convert_video_format': 'Converting video (this may take a while)...',
                'brew_install': f"Installing {parameters.get('package', 'package')} via Homebrew...",
                'brew_upgrade': 'Upgrading packages...',
                'npm_install_global': f"Installing {parameters.get('package', 'package')} globally...",
                'pip_install': f"Installing {parameters.get('package', 'package')}...",
            }
            
            if tool_name in long_running_tools:
                print(f"\n🔄 {long_running_tools[tool_name]}", flush=True)
            
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
    global client
    client.reset_conversation()
    client.set_system_prompt(
        "You are a helpful assistant with access to macOS system tools. "
        "When users ask you to perform system tasks, use the available tools to help them."
    )
    return jsonify({'success': True, 'message': 'Conversation reset'})

@app.route('/api/tools', methods=['GET'])
def list_tools():
    """List available tools"""
    tools = []
    for name, tool in client.mcp_server.tools.items():
        tools.append({
            'name': name,
            'description': tool['description']
        })
    return jsonify({'tools': tools})

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
