# System Architecture

A deep dive into how the macOS AI Commander is built, designed, and operates.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
├─────────────────────┬───────────────────────────────────────────┤
│   CLI Interface     │         Web UI (Flask)                    │
│   - Voice Input     │         - REST API                        │
│   - Voice Output    │         - WebSocket (future)              │
│   - Text I/O        │         - Beautiful UI                    │
└──────────┬──────────┴───────────────┬───────────────────────────┘
           │                          │
           └──────────────┬───────────┘
                          │
           ┌──────────────▼──────────────┐
           │    Ollama Client Layer      │
           │  - Conversation Management  │
           │  - Tool Calling Logic       │
           │  - Model Communication      │
           └──────────────┬──────────────┘
                          │
           ┌──────────────▼──────────────┐
           │      MCP Server Layer       │
           │  - Tool Registration        │
           │  - Tool Execution           │
           │  - Parameter Validation     │
           └──────────────┬──────────────┘
                          │
           ┌──────────────▼──────────────┐
           │      Tool Modules Layer     │
           │  - 189 Implementation       │
           │  - Category-based           │
           │  - Modular Design           │
           └──────────────┬──────────────┘
                          │
           ┌──────────────▼──────────────┐
           │    macOS System APIs        │
           │  - AppleScript              │
           │  - PyObjC                   │
           │  - Shell Commands           │
           │  - System Libraries         │
           └─────────────────────────────┘
```

## 📦 Core Components

### 1. **Ollama Client** (`core/ollama_client.py`)

**Purpose**: Interface between user and AI model

**Key Responsibilities**:
- Manage conversation history
- Format requests to Ollama API
- Parse AI responses
- Detect and execute tool calls
- Handle voice input/output (CLI mode)

**Data Flow**:
```python
User Input → Ollama Client → Ollama API → AI Model
                ↓
         Tool Detection
                ↓
         MCP Server → Tool Execution
                ↓
         Response Formatting → User
```

**Key Methods**:
```python
class OllamaClient:
    def chat_with_tools(message: str) -> dict:
        """Send message to AI and handle tool calls"""
        
    def execute_tool_call(tool_call: dict) -> dict:
        """Execute detected tool and return result"""
        
    def listen_voice() -> str:
        """Capture and transcribe voice input"""
        
    def speak_text(text: str):
        """Convert text to speech output"""
```

### 2. **MCP Server** (`core/mcp_server.py`)

**Purpose**: Tool registry and execution engine

**Key Responsibilities**:
- Register all available tools
- Validate tool parameters
- Execute tool functions
- Handle errors gracefully
- Return structured results

**Tool Definition Structure**:
```python
{
    "tool_name": {
        "description": "What the tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param1"]
        },
        "function": actual_python_function
    }
}
```

**Execution Flow**:
```
Tool Call Request
    ↓
Parameter Validation
    ↓
Function Lookup
    ↓
Execute with Error Handling
    ↓
Format Result
    ↓
Return to Ollama Client
```

### 3. **Tool Registry** (`tools/advanced_tool_registry.py`)

**Purpose**: Central hub for all tool definitions

**Organization**:
```python
ADVANCED_TOOLS = {
    # Window Management (9 tools)
    "snap_window_left": {...},
    "maximize_window": {...},
    
    # File Operations (10 tools)
    "compress_files": {...},
    "extract_archive": {...},
    
    # Web Tools (14 tools)
    "web_scrape": {...},
    "test_download_speed": {...},
    
    # ... 156+ more tools
}
```

**Tool Categories**:
1. **Basic Tools** (7) - Notifications, clipboard, screenshots
2. **Window Management** (9) - Snap, resize, move windows
3. **File Operations** (10) - Compress, move, rename files
4. **Advanced Clipboard** (7) - History, images, append
5. **Screen & Media** (8) - Recording, image conversion
6. **Display Control** (6) - Night shift, resolution
7. **Package Management** (16) - Brew, npm, pip
8. **Keyboard & Mouse** (9) - Type text, click, move
9. **Time Machine** (8) - Backup management
10. **AirDrop & Handoff** (6) - File sharing
11. **Database Tools** (11) - Query Postgres, MySQL, etc.
12. **Web Tools** (14) - Scrape, download, speed test
13. **App Integrations** (32) - Safari, Chrome, VS Code, etc.
14. **Quick Tools** (10) - Fast system operations
15. **Advanced Tools** (32) - File ops, notes, music, etc.

### 4. **Tool Implementations** (`tools/*.py`)

Each category has its own module:

**Example: Window Management** (`tools/window_management.py`)
```python
def snap_window_left(app_name: str = None) -> dict:
    """Snap window to left half of screen"""
    try:
        # Get screen dimensions
        screen_width, screen_height = get_screen_size()
        
        # Calculate left half position
        x, y, width, height = 0, 0, screen_width // 2, screen_height
        
        # Execute AppleScript
        script = f'''
            tell application "{app_name}"
                activate
                tell application "System Events"
                    set position of window 1 to {{{x}, {y}}}
                    set size of window 1 to {{{width}, {height}}}
                end tell
            end tell
        '''
        
        subprocess.run(['osascript', '-e', script], check=True)
        
        return {"success": True, "message": f"Snapped {app_name} to left"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## 🔄 Request Flow

### Complete Request Lifecycle

```
1. USER INPUT
   CLI: "snap chrome to the left"
   Web: POST /api/chat {"message": "snap chrome to the left"}
        ↓
2. OLLAMA CLIENT
   - Add to conversation history
   - Format request with tools list
   - Send to Ollama API
        ↓
3. OLLAMA API
   - Process with AI model
   - Analyze intent
   - Generate tool calls
        ↓
4. AI MODEL RESPONSE
   {
     "message": "I'll snap Chrome to the left side",
     "tool_calls": [
       {
         "function": {
           "name": "snap_window_left",
           "arguments": {"app_name": "Google Chrome"}
         }
       }
     ]
   }
        ↓
5. OLLAMA CLIENT (Tool Execution)
   - Parse tool_calls
   - For each tool:
        ↓
6. MCP SERVER
   - Validate tool exists
   - Validate parameters
   - Look up function
        ↓
7. TOOL EXECUTION
   - Execute snap_window_left("Google Chrome")
   - Uses AppleScript via subprocess
   - macOS moves window
        ↓
8. RESULT COLLECTION
   {
     "success": True,
     "message": "Snapped Google Chrome to left"
   }
        ↓
9. RESPONSE FORMATTING
   - Add tool result to conversation
   - AI generates final response
   - Format for user
        ↓
10. USER OUTPUT
    CLI: ✅ "Chrome is now on the left half"
    Web: Display tool execution card + AI response
```

## 🧠 AI Integration

### Model Context Protocol (MCP)

**What is MCP?**
A standardized way to describe tools/functions to AI models:

```json
{
  "type": "function",
  "function": {
    "name": "send_notification",
    "description": "Send macOS notification",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "message": {"type": "string"}
      },
      "required": ["title", "message"]
    }
  }
}
```

**Why MCP?**
- ✅ Standardized tool definitions
- ✅ Any AI model can understand
- ✅ Easy to add new tools
- ✅ Self-documenting
- ✅ Type-safe parameter passing

### Ollama Integration

**Communication Protocol**: HTTP REST API

**Endpoint**: `POST http://localhost:11434/api/chat`

**Request Format**:
```json
{
  "model": "gpt-oss:20b",
  "messages": [
    {"role": "system", "content": "You are a macOS assistant..."},
    {"role": "user", "content": "snap chrome left"},
    {"role": "assistant", "content": "I'll do that", "tool_calls": [...]},
    {"role": "tool", "content": "{\"success\": true}"}
  ],
  "tools": [...list of all tools...],
  "stream": false
}
```

**Response Format**:
```json
{
  "message": {
    "role": "assistant",
    "content": "Done!",
    "tool_calls": [
      {
        "function": {
          "name": "snap_window_left",
          "arguments": "{\"app_name\":\"Chrome\"}"
        }
      }
    ]
  }
}
```

### Conversation Management

**Memory Structure**:
```python
conversation_history = [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User message 1"},
    {"role": "assistant", "content": "AI response 1"},
    {"role": "tool", "content": "Tool result 1"},
    {"role": "user", "content": "User message 2"},
    # ... continues
]
```

**Benefits**:
- Context awareness across commands
- Follow-up questions work naturally
- Tool results inform next responses
- Multi-step workflows possible

## 🎨 Web UI Architecture

### Frontend Stack
- **HTML5** - Structure
- **CSS3** - Styling with animations
- **Vanilla JavaScript** - No framework overhead

### Backend Stack
- **Flask** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin requests

### Communication

**REST API Endpoints**:
```python
POST /api/chat
    Request: {"message": "user message"}
    Response: {
        "success": True,
        "response": "AI response",
        "tool_executions": [
            {
                "tool": "tool_name",
                "params": {...},
                "result": {...}
            }
        ]
    }

POST /api/reset
    Request: {}
    Response: {"success": True}

GET /api/tools
    Response: {
        "tools": [
            {"name": "tool_name", "description": "..."}
        ]
    }

GET /api/config
    Response: {
        "model": "gpt-oss:20b",
        "tool_count": 189
    }
```

### UI Features

**Animations**:
- Message slide-in effects
- Tool card expand animations
- Loading spinners with progress bars
- Smooth scrolling
- Hover effects on all interactive elements
- Ripple effects on buttons

**Glassmorphism Design**:
```css
background: rgba(42, 42, 52, 0.9);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.1);
```

**Responsive Layout**:
- Mobile-friendly
- Adaptive message widths
- Touch-optimized controls

## 🎤 Voice Integration

### Voice Input (CLI Only)

**Technology**: Vosk (offline speech recognition)

**Why Vosk?**
- ✅ Completely offline
- ✅ Fast transcription
- ✅ No API keys required
- ✅ Compatible with Python 3.14
- ✅ Low resource usage

**Implementation**:
```python
import vosk
import sounddevice as sd

def listen_voice():
    model = vosk.Model("model")  # Downloads ~40MB model
    rec = vosk.KaldiRecognizer(model, 16000)
    
    with sd.RawInputStream(samplerate=16000, channels=1):
        while True:
            data = audio_queue.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result['text']
```

### Voice Output (CLI Only)

**Technology**: macOS built-in `say` command

**Implementation**:
```python
def speak_text(text: str, voice: str = "Samantha"):
    subprocess.run(['say', '-v', voice, text])
```

**Available Voices**:
- Samantha (Female, US)
- Alex (Male, US)
- Victoria (Female, UK)
- Daniel (Male, UK)

## 🔧 Tool Development

### Adding a New Tool

**Step 1**: Implement function in appropriate module

```python
# tools/your_category.py
def your_new_tool(param1: str, param2: int = 10) -> dict:
    """
    Brief description of what tool does
    
    Args:
        param1: Description
        param2: Description (default: 10)
    
    Returns:
        dict with success/error and results
    """
    try:
        # Your implementation
        result = do_something(param1, param2)
        
        return {
            "success": True,
            "result": result,
            "message": "Operation successful"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

**Step 2**: Register in `advanced_tool_registry.py`

```python
from tools.your_category import your_new_tool

ADVANCED_TOOLS = {
    "your_new_tool": {
        "description": "Brief description for AI",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "What this parameter does"
                },
                "param2": {
                    "type": "integer",
                    "description": "What this parameter does"
                }
            },
            "required": ["param1"]  # param2 is optional
        },
        "function": your_new_tool
    }
}
```

**Step 3**: Enable in `config.json`

```json
{
  "tools": {
    "enabled": [
      "your_new_tool"
    ]
  }
}
```

### Tool Best Practices

1. **Always return dict** with `success` key
2. **Handle all exceptions** gracefully
3. **Provide clear error messages**
4. **Use type hints** for parameters
5. **Document well** - AI reads descriptions
6. **Test edge cases**
7. **Keep operations atomic** - one tool, one action
8. **Timeout long operations**
9. **Log important actions**
10. **Return useful metadata**

## 🔐 Security Considerations

### Permission Model

**macOS Permissions Required**:
```
Accessibility → Window management, system control
Automation → Application control
Microphone → Voice input (CLI only)
Files & Folders → File operations
```

**Principle of Least Privilege**:
- Only request needed permissions
- Users can deny specific permissions
- System degrades gracefully

### Input Validation

**Parameter Validation**:
```python
def validate_params(tool_def: dict, params: dict):
    required = tool_def['parameters'].get('required', [])
    for param in required:
        if param not in params:
            raise ValueError(f"Missing required param: {param}")
```

**Path Sanitization**:
```python
def safe_path(path: str) -> str:
    # Resolve to absolute path
    # Check if within allowed directories
    # Prevent directory traversal
    return os.path.abspath(path)
```

### Local-Only Processing

- ✅ **No cloud APIs** - Everything runs locally
- ✅ **No telemetry** - No data collection
- ✅ **No external calls** - Except user-initiated web tools
- ✅ **Open source** - Fully auditable code

## 📊 Performance Optimization

### Model Selection

**Trade-offs**:
| Model | Params | Speed | RAM | Quality |
|-------|--------|-------|-----|---------|
| qwen2.5:3b | 3B | Fast | 4GB | Good |
| mistral | 7B | Medium | 6GB | Better |
| gpt-oss:20b | 20B | Slow | 16GB | Best |

### Caching Strategies

**Tool Registry Caching**:
```python
# Load once at startup
tools = get_enabled_tools(config)
# Reuse for all requests
```

**Conversation History Pruning**:
```python
# Keep only last N messages
if len(history) > MAX_HISTORY:
    history = history[-MAX_HISTORY:]
```

### Async Operations (Future)

**Potential Improvements**:
- Parallel tool execution
- Streaming responses
- Background tasks
- WebSocket updates

## 🧪 Testing Strategy

### Unit Tests (Recommended Addition)

```python
# tests/test_window_management.py
def test_snap_window_left():
    result = snap_window_left("Safari")
    assert result["success"] == True
```

### Integration Tests

```python
# tests/test_integration.py
def test_full_flow():
    client = OllamaClient(config)
    response = client.chat("snap chrome left")
    assert "chrome" in response.lower()
```

### Manual Testing Checklist

- [ ] All 189 tools execute without errors
- [ ] Voice input works correctly
- [ ] Voice output is clear
- [ ] Web UI loads and responds
- [ ] Tool results display properly
- [ ] Error handling works
- [ ] Conversation history maintained
- [ ] Config changes apply

## 📈 Future Enhancements

### Planned Features

1. **Workflow System** - Chain multiple tools
2. **Scheduled Tasks** - Cron-like automation
3. **Custom Tools** - User-defined functions
4. **Plugin System** - Third-party extensions
5. **Mobile App** - iOS companion
6. **Shortcuts Integration** - macOS Shortcuts support
7. **Multi-language** - i18n support
8. **Analytics Dashboard** - Usage statistics
9. **Cloud Sync** - Optional config backup
10. **Team Features** - Shared workflows

### Technical Debt

- Add comprehensive unit tests
- Implement proper logging framework
- Add rate limiting to API
- Implement request queuing
- Add telemetry (opt-in)
- Performance profiling
- Memory leak testing
- Security audit

## 🤝 Contributing

Want to add features? See `CONTRIBUTING.md` for:
- Code style guidelines
- PR process
- Testing requirements
- Documentation standards

---

**Questions?** Open an issue or check other docs! 🚀

