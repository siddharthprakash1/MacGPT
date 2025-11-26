# Getting Started with MacOS AI Commander

This guide will walk you through setting up and using your AI-powered macOS automation system.

## 📋 Prerequisites

### System Requirements
- **macOS**: 10.15 (Catalina) or later
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 10GB free space (for models)

### Required Software
1. **Ollama** - Local AI model server
   ```bash
   # Install via Homebrew
   brew install ollama
   
   # Or download from https://ollama.ai
   ```

2. **Python 3** - Usually pre-installed on macOS
   ```bash
   # Check version
   python3 --version
   ```

3. **Xcode Command Line Tools** (for pyobjc)
   ```bash
   xcode-select --install
   ```

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Step 2: Create Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv)
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If you encounter issues with `pyaudio`, install PortAudio first:
```bash
brew install portaudio
pip install pyaudio
```

### Step 4: Download AI Model
```bash
# Start Ollama service (in a separate terminal)
ollama serve

# Pull the recommended model (in your project terminal)
ollama pull gpt-oss:20b

# Alternative faster model (3B params):
ollama pull qwen2.5:3b
```

**Model Comparison:**
| Model | Size | Speed | Intelligence | Recommended For |
|-------|------|-------|--------------|-----------------|
| `gpt-oss:20b` | 11GB | Slower | Higher | Complex tasks |
| `qwen2.5:3b` | 1.9GB | Faster | Good | Quick operations |
| `mistral:latest` | 4.1GB | Medium | Good | Balanced |

### Step 5: Configure (Optional)
Edit `config.json` to customize:
```json
{
  "ollama": {
    "model": "gpt-oss:20b",
    "endpoint": "http://localhost:11434",
    "temperature": 0.7
  }
}
```

## 🎮 Running the System

### Option 1: CLI Mode (with Voice Control)
```bash
python start_cli.py
```

**Features:**
- ✅ Voice input (press Enter, then speak)
- ✅ Voice responses (toggle with "voice on/off")
- ✅ Full tool access
- ✅ Conversation history

**Example Session:**
```
🤖 macOS Assistant Ready!

You: open chrome and spotify
🎯 Opening applications...
✅ Done!

You: [press Enter]
🎤 Listening...
You: (speak) "snap chrome to the left and spotify to the right"
✅ Windows arranged!
```

### Option 2: Web UI Mode
```bash
python start_web.py
```

Then open: `http://localhost:7889`

**Features:**
- ✅ Beautiful animated interface
- ✅ Real-time tool execution display
- ✅ Conversation history
- ✅ Tool list browser
- ✅ Mobile responsive

## 🛠️ First Commands to Try

### Easy Commands
```
"Send a notification that says Hello World"
"What's my battery status?"
"Get system information"
"Take a screenshot"
```

### Window Management
```
"Snap Chrome to the left half"
"Maximize Safari"
"Center the current window"
"Show me all open windows"
```

### File Operations
```
"List files in my Downloads folder"
"Compress all PDFs in Desktop"
"Find all Python files in Documents"
"Create a folder called Projects in Desktop"
```

### Web & Network
```
"Test my internet speed"
"Scrape news from TechCrunch homepage"
"Check if google.com is up"
"Download https://example.com/file.pdf"
```

### System Control
```
"Set volume to 50%"
"Set brightness to 70%"
"Toggle dark mode"
"Lock my screen"
```

## 🎤 Voice Control Guide

### CLI Voice Setup
1. Start CLI: `python start_cli.py`
2. Press **Enter** to activate microphone
3. Speak your command
4. Wait for transcription
5. AI executes and responds

**Enable Voice Responses:**
```
You: voice on
🔊 Voice responses enabled!

You: what time is it?
🔊 (AI speaks the time)
```

**Disable Voice Responses:**
```
You: voice off
🔇 Voice responses disabled.
```

### Microphone Permissions
On first run, macOS will ask for microphone permission:
1. Click "OK" when prompted
2. Or go to: **System Settings → Privacy & Security → Microphone**
3. Enable for Terminal/Python

## 🔧 Configuration Deep Dive

### Model Selection
Edit `config.json`:
```json
"ollama": {
  "model": "gpt-oss:20b"  // Change to your preferred model
}
```

### Enable/Disable Tools
Only enable tools you need for faster loading:
```json
"tools": {
  "enabled": [
    "send_notification",
    "clipboard_read",
    "open_application",
    // Add only the tools you want
  ]
}
```

**To enable all tools**, use:
```json
"tools": {
  "enabled": ["*"]  // All 189 tools
}
```

### Temperature Setting
Controls AI creativity:
```json
"temperature": 0.7  // Range: 0.0 (deterministic) to 1.0 (creative)
```

- **0.0-0.3**: Precise, consistent responses
- **0.4-0.7**: Balanced (recommended)
- **0.8-1.0**: Creative, varied responses

### Custom Port (Web UI)
Edit `start_web.py`:
```python
app.run(host='0.0.0.0', port=7889, debug=False)  # Change port here
```

## 🐛 Troubleshooting

### Ollama Not Running
**Error**: `Connection refused to localhost:11434`

**Fix**:
```bash
# Start Ollama in separate terminal
ollama serve

# Or check if already running
ps aux | grep ollama
```

### Model Not Found
**Error**: `model 'gpt-oss:20b' not found`

**Fix**:
```bash
# Pull the model
ollama pull gpt-oss:20b

# List available models
ollama list
```

### Microphone Not Working (CLI)
**Error**: `Microphone permission denied`

**Fix**:
1. Go to **System Settings → Privacy & Security → Microphone**
2. Enable for Terminal or iTerm
3. Restart the CLI

### PyAudio Installation Error
**Error**: `portaudio.h not found`

**Fix**:
```bash
# Install PortAudio first
brew install portaudio

# Then install pyaudio
pip install pyaudio
```

### Tool Execution Fails
**Error**: Various AppleScript/system errors

**Fix**:
1. Grant **Accessibility** permissions
2. Go to: **System Settings → Privacy & Security → Accessibility**
3. Add Terminal/iTerm/Python
4. Restart the app

### Slow Response Time
**Solutions**:
1. Use a smaller model: `ollama pull qwen2.5:3b`
2. Update config.json: `"model": "qwen2.5:3b"`
3. Ensure no other heavy apps are running
4. Close unused tools in config.json

## 📊 System Monitoring

### Check Ollama Status
```bash
curl http://localhost:11434/api/tags
```

### Monitor Resource Usage
```bash
# CPU/Memory usage
top -pid $(pgrep ollama)

# Model loading status
ollama list
```

### View Logs
```bash
# CLI logs (stdout)
python start_cli.py 2>&1 | tee logs/cli.log

# Web UI logs
python start_web.py 2>&1 | tee logs/web.log
```

## 🔐 Privacy & Security

### Local-Only Processing
- ✅ All AI processing happens locally via Ollama
- ✅ No data sent to cloud services
- ✅ No external API keys required
- ✅ Complete privacy

### Permissions Required
The system needs these macOS permissions:
- **Accessibility**: For window management and system control
- **Automation**: For controlling applications
- **Microphone**: For voice input (CLI only)
- **Files & Folders**: For file operations

Grant only what you need - the system works with partial permissions.

## 🎯 Next Steps

1. ✅ **Try Basic Commands** - Get familiar with capabilities
2. ✅ **Explore Tools** - Run `show all tools` to see what's available
3. ✅ **Customize Config** - Enable only tools you need
4. ✅ **Create Shortcuts** - Add alias to `.zshrc` for quick launch
5. ✅ **Read Advanced Docs** - Check `ADVANCED_USAGE.md`

## 🆘 Getting Help

- 📖 **Documentation**: Check other files in `/docs`
- 🐛 **Issues**: Open a GitHub issue
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Contact**: (Add your contact info)

---

**Ready to automate?** Start with: `python start_cli.py` 🚀

