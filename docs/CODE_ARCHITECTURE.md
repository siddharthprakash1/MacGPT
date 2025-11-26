# Code Architecture

## Overview

This project implements a Model Context Protocol (MCP) server that enables Ollama-powered AI models to control macOS through function calling. The architecture is modular with clear separation between tools, server logic, and AI integration.

## Core Components

### 1. Tools Layer

#### `tools.py` - Basic Tools (7 tools)
Foundation tools for macOS interaction:

```python
TOOLS = {
    "send_notification": {
        "description": "...",
        "parameters": {...},
        "function": send_notification
    },
    # ... other tools
}

def get_enabled_tools(config):
    """Merges basic and advanced tools, filters by config"""
    all_tools = {**TOOLS, **ADVANCED_TOOLS}
    return filter_by_config(all_tools, config)
```

**Implements**:
- `send_notification()` - Uses osascript for macOS notifications
- `clipboard_read/write()` - Uses pbpaste/pbcopy commands
- `text_to_speech()` - Uses macOS `say` command
- `take_screenshot()` - Uses `screencapture` command
- `spotlight_search()` - Uses `mdfind` for Spotlight
- `get_system_info()` - Uses `scutil`, `uptime`, `df` commands

#### `advanced_tools.py` - Advanced Tools (15 tools)
Extended functionality for file operations, apps, notes, processes:

```python
def read_file(filepath, lines=None):
    """Read file with optional line limit"""
    path = Path(filepath).expanduser()
    with open(path, 'r') as f:
        content = f.read() if not lines else ''.join(f.readlines()[:lines])
    return {"success": True, "content": content}
```

**Key Functions**:
- File operations: `read_file`, `write_file`, `list_files`, `create_directory`
- Apps: `close_application`, `list_running_apps`
- Apple ecosystem: `create_note`, `search_notes`, `create_reminder`
- Process management: `list_processes`, `kill_process`
- Media: `control_music`, `get_current_song`
- Network: `get_network_info`
- Shell: `run_shell_command` (with timeout safety)

Uses:
- `subprocess.run()` for shell commands
- `Path` from pathlib for file operations
- AppleScript via osascript for Apple apps

#### `smart_helpers.py` - Smart Resolution
Intelligent app name and URL handling:

```python
APP_ALIASES = {
    "brave": "Brave Browser",
    "vscode": "Visual Studio Code",
    "chrome": "Google Chrome",
    # ... 39+ aliases
}

def resolve_app_name(app_name):
    """Convert user-friendly names to macOS app names"""
    return APP_ALIASES.get(app_name.lower(), app_name)

def open_application_smart(app_name):
    """Open app with automatic name resolution"""
    resolved = resolve_app_name(app_name)
    subprocess.run(['open', '-a', resolved])
```

**Features**:
- App alias resolution (39+ common app names)
- `open_youtube_video()` - Creates YouTube search URLs
- `smart_search()` - Multi-platform search (Google, GitHub, etc.)
- `open_url_smart()` - Auto-adds https://, resolves browser names
- `get_available_apps()` - Lists installed applications

#### `advanced_tool_registry.py` - Tool Definitions
Registry of all tools with MCP-compatible schemas:

```python
ADVANCED_TOOLS = {
    "read_file": {
        "description": "Read contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "..."},
                "lines": {"type": "integer", "description": "..."}
            },
            "required": ["filepath"]
        },
        "function": read_file
    },
    # ... 28 more tools
}

# Merge workflow tools
from workflow_runner import WORKFLOW_TOOLS
ADVANCED_TOOLS.update(WORKFLOW_TOOLS)
```

**Structure**:
- Each tool has: description, JSON Schema parameters, function reference
- Tools imported from `advanced_tools.py` and `smart_helpers.py`
- Workflow tools imported from `workflow_runner.py`

### 2. Server Layer

#### `mcp_server.py` - MCP Protocol Server
Implements the Model Context Protocol over stdio:

```python
class MCPServer:
    def __init__(self, config):
        self.config = config
        self.tools = get_enabled_tools(config)
    
    def list_tools(self):
        """Return MCP-formatted tool list"""
        return [{
            "name": name,
            "description": tool["description"],
            "inputSchema": tool["parameters"]
        } for name, tool in self.tools.items()]
    
    def execute_tool(self, tool_name, parameters):
        """Execute a tool and return result"""
        function = self.tools[tool_name]["function"]
        return function(**parameters)
    
    def handle_request(self, request):
        """Handle JSON-RPC request"""
        method = request.get('method')
        if method == 'initialize':
            return {"protocolVersion": "0.1.0", ...}
        elif method == 'tools/list':
            return {"tools": self.list_tools()}
        elif method == 'tools/call':
            return self.execute_tool(...)
    
    def run_stdio(self):
        """Main loop: read JSON-RPC from stdin, write to stdout"""
        for line in sys.stdin:
            request = json.loads(line)
            response = self.handle_request(request)
            print(json.dumps({"jsonrpc": "2.0", "result": response}))
```

**Protocol**:
- JSON-RPC 2.0 over stdio
- Methods: `initialize`, `tools/list`, `tools/call`
- Reads from stdin, writes to stdout
- Error handling with proper JSON-RPC error codes

### 3. AI Integration Layer

#### `ollama_client.py` - Ollama Integration
Connects Ollama models to MCP tools with conversation management:

```python
class OllamaClient:
    def __init__(self, config):
        self.model = config['ollama']['model']
        self.endpoint = config['ollama']['endpoint']
        self.mcp_server = MCPServer(config)
        self.conversation_history = []
    
    def get_tools_for_ollama(self):
        """Convert MCP tools to Ollama format"""
        return [{
            "type": "function",
            "function": {
                "name": name,
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        } for name, tool in self.mcp_server.tools.items()]
    
    def chat(self, message):
        """Send message to Ollama with tool support"""
        self.conversation_history.append({"role": "user", "content": message})
        
        response = requests.post(f"{self.endpoint}/api/chat", json={
            "model": self.model,
            "messages": self.conversation_history,
            "tools": self.get_tools_for_ollama(),
            "stream": False
        })
        
        result = response.json()
        tool_calls = result['message'].get('tool_calls', [])
        
        if tool_calls:
            # Execute each tool call
            for tool_call in tool_calls:
                tool_result = self.mcp_server.execute_tool(
                    tool_call['function']['name'],
                    tool_call['function']['arguments']
                )
            
            # Add tool results to conversation
            self.conversation_history.append({"role": "tool", "content": ...})
            
            # Get final response from model
            return self.chat("")
        
        return result
```

**Features**:
- Automatic tool call detection and execution
- Conversation history management
- Tool call loop (model can chain multiple tools)
- Graceful fallback for models without tool support
- System prompt configuration

**Interactive Mode**:
```python
def interactive_mode():
    """REPL interface for chatting with Ollama"""
    client = OllamaClient(config)
    
    while True:
        user_input = input("You: ")
        if user_input in ['quit', 'exit']:
            break
        
        response = client.chat(user_input)
        print(f"Assistant: {response['message']['content']}")
```

### 4. Workflow System

#### `workflow_runner.py` - Workflow Execution
Execute predefined automation sequences:

```python
class WorkflowRunner:
    def __init__(self):
        self.workflows = json.load(open('workflows.json'))
        self.all_tools = {**TOOLS, **ADVANCED_TOOLS}
    
    def run_workflow(self, workflow_id):
        """Execute workflow steps sequentially"""
        workflow = self.workflows[workflow_id]
        results = []
        
        for step in workflow['steps']:
            tool_name = step['tool']
            params = step.get('params', {})
            
            function = self.all_tools[tool_name]['function']
            result = function(**params)
            results.append(result)
        
        return {"success": True, "results": results}

# Exposed as tools
def list_workflows():
    return WorkflowRunner().list_workflows()

def run_workflow(workflow_id):
    return WorkflowRunner().run_workflow(workflow_id)
```

#### `workflows.json` - Workflow Definitions
```json
{
  "morning_routine": {
    "name": "Morning Routine",
    "steps": [
      {"tool": "get_system_info"},
      {"tool": "get_network_info"},
      {"tool": "send_notification", "params": {"title": "Good Morning!"}}
    ]
  }
}
```

### 5. Configuration

#### `config.json`
```json
{
  "server": {
    "name": "macos-integration",
    "version": "0.1.0"
  },
  "ollama": {
    "model": "gpt-oss:20b",
    "endpoint": "http://localhost:11434",
    "temperature": 0.7
  },
  "tools": {
    "enabled": ["send_notification", "clipboard_read", ...]
  }
}
```

**Loading**:
```python
def load_config(path='config.json'):
    with open(path) as f:
        return json.load(f)
```

## Data Flow

### User Request → Tool Execution

```
User: "Open brave and take a screenshot"
    ↓
OllamaClient.chat()
    ↓
POST to Ollama API with tools list
    ↓
Ollama model returns tool_calls:
  1. open_application(app_name="brave")
  2. take_screenshot()
    ↓
For each tool_call:
  MCPServer.execute_tool(name, params)
    ↓
  smart_helpers.open_application_smart("brave")
    → resolves to "Brave Browser"
    → subprocess.run(['open', '-a', 'Brave Browser'])
    ↓
  tools.take_screenshot()
    → subprocess.run(['screencapture', filepath])
    ↓
Tool results → Ollama for final response
    ↓
Assistant: "I've opened Brave and taken a screenshot..."
```

## Key Design Patterns

### 1. Tool Registry Pattern
All tools follow consistent structure:
```python
{
    "description": "Human-readable description",
    "parameters": {JSON Schema},
    "function": callable
}
```

### 2. Smart Resolution
User input → Alias resolution → Actual value:
```python
"brave" → resolve_app_name() → "Brave Browser"
"github.com" → add_protocol() → "https://github.com"
```

### 3. Error Handling
All tools return consistent format:
```python
{"success": True, "data": ...}  # Success
{"success": False, "error": ...}  # Failure
```

### 4. Modular Loading
```python
# Base tools always loaded
from tools import TOOLS

# Advanced tools conditionally loaded
try:
    from advanced_tool_registry import ADVANCED_TOOLS
    all_tools = {**TOOLS, **ADVANCED_TOOLS}
except ImportError:
    all_tools = TOOLS
```

## Security Considerations

1. **Shell Command Timeout**: `run_shell_command` has 30s timeout
2. **File Operations**: Path expansion via `Path.expanduser()` for user home directory
3. **Process Management**: Requires explicit PID (no wildcard killing)
4. **Sandboxing**: File operations scoped to user directory
5. **No Credential Storage**: No sensitive data in config

## Extension Points

### Adding New Tools

1. **Implement function** in `advanced_tools.py`:
```python
def my_new_tool(param1, param2):
    """Tool description"""
    # Implementation
    return {"success": True, "result": ...}
```

2. **Register in** `advanced_tool_registry.py`:
```python
ADVANCED_TOOLS["my_new_tool"] = {
    "description": "...",
    "parameters": {...},
    "function": my_new_tool
}
```

3. **Enable in** `config.json`:
```json
{"tools": {"enabled": ["my_new_tool", ...]}}
```

### Adding Workflows

Edit `workflows.json`:
```json
{
  "my_workflow": {
    "name": "My Custom Workflow",
    "description": "...",
    "steps": [
      {"tool": "tool_name", "params": {...}},
      {"tool": "another_tool"}
    ]
  }
}
```

## Testing

### Unit Testing
```python
# test_tools.py
def test_notification():
    result = TOOLS['send_notification']['function'](
        title="Test",
        message="Hello"
    )
    assert result['success'] == True
```

### Integration Testing
```bash
# Test all tools
python test_tools.py

# Test specific workflow
python examples.py workflow
```

## Dependencies

- **pyobjc** - macOS native API access
- **requests** - HTTP client for Ollama API
- **pathlib** - File path manipulation
- **subprocess** - Shell command execution
- **json** - Configuration and protocol
- **urllib.parse** - URL manipulation

## Performance

- Tool execution: ~100-500ms (varies by tool)
- Ollama response: 2-10s (depends on model size)
- Model loading: One-time ~5-15s (cached after first use)
- Total round-trip: ~3-12s for simple requests

## Future Enhancements

Potential additions:
- Calendar integration
- Mail automation
- Safari/Chrome tab control
- System preferences modification
- Finder window manipulation
- Voice recognition triggers
- Scheduled task execution
- Tool result caching

