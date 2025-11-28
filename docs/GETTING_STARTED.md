# Getting Started with MacGPT

This guide will walk you through setting up and using your AI-powered macOS automation system.

## ⚡ Quick Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/siddharthprakash1/MacGPT/main/install.sh | bash
```

Then just run:
```bash
macgpt
```

Open **http://localhost:7889** and start chatting! 🎉

---

## 📋 Prerequisites

### System Requirements
- **macOS**: 12.0 (Monterey) or later
- **Python**: 3.9 or higher
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 10GB free space (for AI models)

### Required Software
1. **Ollama** - Local AI model server
   ```bash
   # Install via Homebrew
   brew install ollama
   
   # Or download from https://ollama.ai
   ```

2. **Python 3.9+** - Usually pre-installed on macOS
   ```bash
   # Check version
   python3 --version
   ```

## 🚀 Manual Installation

If you prefer manual setup instead of the one-liner:

### Step 1: Clone the Repository
```bash
git clone https://github.com/siddharthprakash1/MacGPT.git
cd MacGPT
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
# Start Ollama service (runs automatically after brew install)
ollama serve

# Pull the recommended model
ollama pull mistral

# Or for better results:
ollama pull llama3.1
```

**Model Comparison:**
| Model | Size | Speed | Intelligence | Recommended For |
|-------|------|-------|--------------|-----------------|
| `mistral` | 4.1GB | Fast | Good | Quick operations |
| `llama3.1` | 4.7GB | Medium | High | Complex tasks |
| `llama3.1:70b` | 40GB | Slow | Excellent | Best accuracy |

### Step 5: Run MacGPT
```bash
# Web UI (recommended)
python start_web.py

# Or CLI with voice
python start_cli.py
```

## 🎮 Using MacGPT

### Web UI Mode (Recommended)
```bash
python start_web.py
# Or if you used the installer:
macgpt
```

Then open: **http://localhost:7889**

**Features:**
- ✅ Clean dark theme (ChatGPT/Claude style)
- ✅ Real-time tool execution display
- ✅ Conversation history
- ✅ Tool browser (228 tools)
- ✅ Mobile responsive

### CLI Mode (with Voice Control)
```bash
python start_cli.py
```

**Features:**
- ✅ Voice input (press Enter, then speak)
- ✅ Voice responses (toggle with "voice on/off")
- ✅ Full tool access

## 🛠️ Commands to Try

### 🔍 Spotlight Search (NEW!)
```
"Find files over 100MB"
"Which apps are using the most disk space?"
"Find files I modified today"
"Find duplicate files in Downloads"
"Search for documents containing 'invoice'"
```

### 🎵 Spotify Control (20 tools!)
```
"Play my liked songs"
"Play Taylor Swift"
"Play some chill music"
"What song is playing?"
"Skip to next song"
"Set Spotify volume to 50"
"Turn on shuffle"
"Play the album Abbey Road"
"Play workout music"
```

### 🌐 Browser Control (32 tools!)
```
"Open new tab with github.com"
"What tabs do I have open?"
"Close this tab"
"Search YouTube for tutorials"
"Open incognito window"
"Refresh the page"
"Go back"
"Find 'password' on this page"
"Zoom in"
"Bookmark this page"
"Open developer tools"
```

### 🪟 Window Management
```
"Snap Chrome to the left half"
"Open Safari and Notes side by side"
"Maximize Finder"
"Center the current window"
"What windows are open?"
```

### 📁 File Operations
```
"List files in my Downloads folder"
"Compress all PDFs in Desktop"
"Find all Python files in Documents"
"Create a folder called Projects"
```

### ⚡ Quick Actions
```
"What's my battery status?"
"Set volume to 50%"
"Toggle dark mode"
"Lock my screen"
"Show system information"
```

### 📝 Productivity
```
"Create a note called Shopping List"
"Remind me to call mom tomorrow at 5pm"
"Schedule a meeting for Monday at 10am"
```

### 🌐 Web & Network
```
"Is google.com up?"
"What's my IP address?"
"Test my internet speed"
"Open github.com"
```

### 👨‍💻 Developer Tools
```
"Show git status"
"List Docker containers"
"What Homebrew packages do I have?"
"Open this folder in VS Code"
```

## 🎤 Voice Control Guide (CLI)

1. Start CLI: `python start_cli.py`
2. Press **Enter** to activate microphone
3. Speak your command
4. Wait for transcription
5. AI executes and responds

**Enable Voice Responses:**
```
You: voice on
🔊 Voice responses enabled!
```

## 🔧 Configuration

Edit `config.json` to customize:

```json
{
  "ollama": {
    "model": "mistral",
    "endpoint": "http://localhost:11434",
    "temperature": 0.7
  }
}
```

### Change AI Model
```json
"model": "llama3.1"  // Or any Ollama model
```

### Adjust Creativity
```json
"temperature": 0.7  // 0.0 = precise, 1.0 = creative
```

## 🐛 Troubleshooting

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### Model Not Found
```bash
# Pull the model
ollama pull mistral

# List available models
ollama list
```

### Tool Execution Fails
1. Go to **System Settings → Privacy & Security → Accessibility**
2. Add Terminal/iTerm/Python
3. Restart MacGPT

### Slow Responses
1. Use a smaller model: `ollama pull mistral`
2. Close unused applications
3. Check Activity Monitor for resource usage

## 🔐 Privacy & Security

- ✅ **100% Local** - All AI processing via Ollama on your Mac
- ✅ **No Cloud** - Nothing sent to external servers
- ✅ **No API Keys** - No subscriptions needed
- ✅ **Complete Privacy** - Your data stays on your device

### Permissions Required
- **Accessibility**: Window management, system control
- **Automation**: Controlling applications
- **Microphone**: Voice input (CLI only)
- **Files & Folders**: File operations

## 🆘 Getting Help

- 📖 **Docs**: Check other files in `/docs`
- 🐛 **Issues**: [GitHub Issues](https://github.com/siddharthprakash1/MacGPT/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/siddharthprakash1/MacGPT/discussions)
- 👤 **LinkedIn**: [Siddharth Prakash](https://www.linkedin.com/in/siddharth-prakash-771596241/)

---

**Ready to automate your Mac?** 🚀

```bash
macgpt
```
