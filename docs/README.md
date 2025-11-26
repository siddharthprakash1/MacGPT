# macOS MCP Server with Ollama

A powerful Model Context Protocol (MCP) server that gives AI models control over your macOS system. Built with Python and integrated with Ollama for local AI processing with **189 powerful tools**.

## Quick Setup

```bash
# 1. Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Pull Ollama model (if needed)
ollama pull gpt-oss:20b

# 3. Start the system
python start_cli.py   # For CLI with voice control
# OR
python start_web.py   # For Web UI on http://localhost:7889
```

## Project Structure

```
LocalMCP/
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
├── start_cli.py        # CLI launcher (with voice!)
├── start_web.py        # Web UI launcher
├── core/               # Core system modules
│   ├── mcp_server.py   # MCP protocol implementation
│   ├── ollama_client.py # Ollama integration
│   └── tools.py        # Basic tools registry
├── tools/              # All tool implementations (16 modules)
│   ├── advanced_tool_registry.py  # Main tool registry
│   ├── window_management.py
│   ├── file_operations.py
│   ├── clipboard_advanced.py
│   ├── screen_media.py
│   ├── display_control.py
│   ├── package_manager.py
│   ├── keyboard_mouse.py
│   ├── backup_tools.py
│   ├── airdrop_handoff.py
│   ├── database_tools.py
│   ├── web_tools.py
│   └── ... (and more)
├── ui/                 # Web interface
│   ├── web_ui.py
│   └── templates/
└── docs/               # Documentation
    ├── README.md
    └── CODE_ARCHITECTURE.md
```

## Requirements

- macOS 10.15+
- Python 3.8+
- [Ollama](https://ollama.ai) installed and running
- Model that supports tool calling (gpt-oss:20b, mistral, llama3.1, qwen2.5)

## Configuration

Edit `config.json`:

```json
{
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

## Available Tools (29 Total)

### System & Notifications
- **send_notification** - Send macOS notifications
- **get_system_info** - Get OS version, disk usage, uptime
- **get_network_info** - Check WiFi name and IP address

### Clipboard
- **clipboard_read** - Read clipboard content
- **clipboard_write** - Write text to clipboard

### Files & Directories
- **read_file** - Read any file
- **write_file** - Create or edit files (overwrite/append)
- **list_files** - Browse directories with glob patterns
- **create_directory** - Create folders with parent directories

### Applications (Smart Name Resolution!)
- **open_application** - Launch apps (supports aliases: brave→Brave Browser, vscode→Visual Studio Code)
- **close_application** - Close apps gracefully or force quit
- **list_running_apps** - See all running applications
- **get_available_apps** - List installed applications

### Apple Ecosystem
- **create_note** - Create notes in Apple Notes
- **search_notes** - Search notes by content
- **create_reminder** - Set reminders with due dates

### Media
- **text_to_speech** - Speak text with customizable voice
- **take_screenshot** - Capture screen/window/selection
- **control_music** - Play/pause/next/previous (Music/Spotify)
- **get_current_song** - Get currently playing track

### Web & Search
- **open_url** - Open URLs (auto-adds https://, supports browser aliases)
- **open_youtube** - Search and open YouTube videos
- **smart_search** - Search Google, GitHub, YouTube, StackOverflow, Reddit, Wikipedia, Maps
- **spotlight_search** - Find files using Spotlight

### Process Management
- **list_processes** - Monitor processes with CPU/memory usage
- **kill_process** - Terminate processes by PID

### Workflows
- **list_workflows** - Show predefined workflows
- **run_workflow** - Execute automation workflows (morning_routine, focus_mode, dev_setup, end_of_day)

### Advanced
- **run_shell_command** - Execute shell commands (30s timeout)

## Usage Examples

### Basic Operations
```
You: Send me a notification saying "Hello"
You: What's on my clipboard?
You: Take a screenshot
You: Tell me about my system
```

### Smart App Names (No exact names needed!)
```
You: Open brave
You: Launch vscode
You: Start spotify
You: Open chrome and terminal
```

### YouTube Integration
```
You: Play lo-fi music on YouTube in brave
You: Search YouTube for Python tutorials
You: Open YouTube and find cat videos in chrome
```

### File Operations
```
You: Create a file ~/Desktop/todo.txt with my tasks
You: Read ~/Desktop/notes.txt
You: List all Python files in ~/Projects
You: Create a directory ~/Desktop/NewProject
```

### Apple Notes & Reminders
```
You: Create a note called "Meeting Notes" with today's agenda
You: Search my notes for "password"
You: Remind me to call Mom tomorrow at 3pm
You: Create a reminder for team meeting on Friday 10am
```

### Smart Search
```
You: Search GitHub for awesome-python
You: Google search for machine learning tutorials
You: Look up React hooks on StackOverflow
You: Find coffee shops on Maps
```

### Multi-Step Automation
```
You: Open vscode and terminal, create a directory ~/Desktop/MyProject, 
     and create a README.md file with a project description
```

```
You: Take a screenshot, create a note with today's tasks, 
     and remind me to review it tonight at 8pm
```

```
You: Check my system info, network status, running apps, 
     and create a summary note with all this information
```

### Workflows
```
You: Run my morning routine
You: Start focus mode
You: Set up my development environment
You: List available workflows
```

## Predefined Workflows

Edit `workflows.json` to customize:

- **morning_routine** - System check, network info, motivational notification
- **focus_mode** - Close distracting apps, open work tools, start music
- **dev_setup** - Open VS Code, Terminal, localhost browser
- **end_of_day** - Screenshot, system summary note

## Smart Features

### App Name Aliases (39+)
No need for exact names!

**Browsers**: brave, chrome, firefox, safari, edge, opera  
**Dev Tools**: vscode, vs code, code, pycharm, sublime, terminal  
**Apps**: slack, discord, zoom, spotify, music, notes, mail  
**Office**: word, excel, powerpoint, keynote, pages

### Auto URL Formatting
```
You: Open github.com in brave
→ Automatically adds https://
→ Resolves "brave" to "Brave Browser"
```

## Testing

```bash
# Test all tools
python test_tools.py

# Test specific tool
python test_tools.py send_notification

# Run example workflows
python examples.py notifications
python examples.py workflow
```

## Usage Modes

### 1. Interactive Chat (Recommended)
```bash
python ollama_client.py
```
Natural conversation with AI that executes tools automatically.

### 2. MCP Server (stdio)
```bash
python mcp_server.py
```
Standard MCP protocol server for integration with other clients.

### 3. Python API
```python
from tools import send_notification, take_screenshot

send_notification(title="Hi", message="Hello!")
screenshot = take_screenshot(filename="capture.png")
```

## Model Compatibility

**Works with tool calling** ✅:
- gpt-oss:20b (recommended, 20B params)
- mistral:latest (7B params)
- llama3.1:8b
- qwen2.5:3b (fast)
- llama3.2

**No tool support** ❌:
- gemma2, gemma3 series

## Troubleshooting

### Ollama not running
```bash
ollama serve
```

### Model doesn't support tools
```bash
ollama pull gpt-oss:20b
# Update config.json to use gpt-oss:20b
```

### Permission errors
Run `./setup.sh` to check macOS permissions for:
- Notifications
- Accessibility
- Screen Recording

## Project Structure

```
LocalMCP/
├── config.json              # Configuration
├── requirements.txt         # Dependencies
├── setup.sh                 # Setup script
│
├── tools.py                 # Basic tools (7)
├── advanced_tools.py        # Advanced tools (15)
├── advanced_tool_registry.py # Tool definitions
├── smart_helpers.py         # Smart app resolution & YouTube
├── workflow_runner.py       # Workflow executor
├── workflows.json           # Workflow definitions
│
├── mcp_server.py           # MCP server (stdio)
├── ollama_client.py        # Ollama integration + interactive mode
├── test_tools.py           # Testing suite
└── examples.py             # Usage examples
```

## Contributing

Edit `workflows.json` to add your own automation workflows!

## License

MIT

