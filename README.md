# MacGPT 🚀

> **AI-Powered macOS Automation** | Control your entire Mac through natural language using local AI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-Required-green.svg)](https://ollama.ai)
[![Tools: 179](https://img.shields.io/badge/Tools-179-purple.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Transform your Mac into an AI-powered automation machine. Use natural language to control windows, manage files, search with Spotlight, play Spotify, and execute 179+ system operations - all running locally with complete privacy.

## ⚡ One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/siddharthprakash1/MacGPT/main/install.sh | bash
```

Then just run:
```bash
macgpt
```

Open **http://localhost:7889** and start chatting! 🎉

## ✨ Key Features

- 🧠 **100% Local AI** - Powered by Ollama, no cloud, complete privacy
- 🌐 **Modern Web UI** - Clean dark theme inspired by ChatGPT/Claude
- 🔍 **Spotlight Search** - Find files, apps, duplicates with natural language
- 🎵 **Spotify Control** - Play liked songs, playlists directly in the app
- 🪟 **Window Management** - Snap, resize, arrange windows by voice
- 📱 **179 Tools** - Comprehensive automation across 15 categories
- 🎤 **Voice Control** - Speak commands naturally (CLI mode)

## 🎬 Quick Demo

```bash
# Examples of what you can say:
"Find files over 100MB"
"Which apps are using the most disk space?"
"Play my liked songs on Spotify"
"Open Chrome and Safari side by side"
"What's my battery level?"
"Create a reminder to call mom tomorrow"
```

## 🛠️ What Can It Do?

### 🪟 Window Management (9 tools)
Snap, resize, maximize, center windows with simple commands
```
"Snap Chrome left and Safari right" → Instant split-screen
"Maximize VS Code" → Fullscreen coding
```

### 📁 File Operations (10 tools)
Compress, extract, move, copy, rename files in bulk
```
"Compress all PDFs in Desktop" → Creates archive.zip
"Find all Python files in Documents" → Lists *.py files
```

### 🌐 Web & Network (14 tools)
Scrape websites, test speeds, download files, generate QR codes
```
"Scrape headlines from TechCrunch" → Returns latest news
"Test my internet speed" → Downloads 50MB, measures speed
```

### 🗄️ Database Tools (11 tools)
Query Postgres, MySQL, MongoDB, Redis directly
```
"Query Postgres: SELECT * FROM users" → Executes and returns results
"Get Redis keys matching 'user:*'" → Lists matching keys
```

### 📦 Package Management (16 tools)
Install, update, manage packages via brew, npm, pip
```
"Install node using brew" → Installs Node.js
"Update all npm packages" → Upgrades global packages
```

### 🔍 Spotlight Search (12 tools)
Powerful file search using macOS Spotlight
```
"Find files over 100MB" → Lists large files with sizes
"Which apps use the most space?" → Shows apps by disk usage
"Find files I modified today" → Recent user files (no system files)
```

### 🎵 Spotify Control (3 tools)
Control Spotify directly from the app
```
"Play my liked songs" → Plays from Spotify app
"Play Discover Weekly" → Starts playlist
"Pause the music" → Controls playback
```

### 🎬 Screen & Media (8 tools)
Record screen, convert images/videos, resize media
```
"Start screen recording" → Captures screen
"Convert image.jpg to PNG" → Converts format
```

**+ 9 more categories**: Clipboard, Display, Time Machine, AirDrop, App Integrations, Quick Tools, System Control

[**→ See all 189 tools**](docs/README.md)

## 📚 Comprehensive Documentation

Perfect for LinkedIn visitors who want to understand the project:

| Guide | Purpose | Time |
|-------|---------|------|
| [🚀 Getting Started](docs/GETTING_STARTED.md) | Installation, setup, first commands | 15 min |
| [💡 Examples & Workflows](docs/EXAMPLES.md) | Real-world use cases, productivity hacks | 20 min |
| [🏗️ Architecture Guide](docs/ARCHITECTURE.md) | How it's built, system design, tech stack | 30 min |
| [🛠️ Contributing Guide](docs/CONTRIBUTING.md) | Add tools, fix bugs, improve code | 25 min |
| [📖 Documentation Index](docs/INDEX.md) | Complete docs navigation | 5 min |

## 🎯 Use Cases

### 💼 Productivity
- **Morning routine**: Check battery, open apps, arrange windows
- **Focus mode**: Close distractions, enable Do Not Disturb, start timer
- **End of day**: Backup files, compress work, clean desktop

### 👨‍💻 Development
- **Project setup**: Create folders, init git, install packages
- **Code review**: Open GitHub, VS Code, arrange windows
- **Deployment**: Pull code, restart containers, verify status

### 📊 Data & Research
- **Web scraping**: Extract data from websites
- **Database queries**: Query multiple databases
- **Speed tests**: Monitor network performance

### 🎨 Creative Work
- **Video editing**: Arrange apps, adjust display settings
- **Design work**: Snap design tools, manage assets
- **Content creation**: Record screen, compress media

[**→ See 50+ workflow examples**](docs/EXAMPLES.md)

## 🎤 Voice Control

Natural speech recognition in CLI mode:

```bash
python start_cli.py

You: [press Enter]
🎤 Listening...

You: "Open Chrome and VS Code, then snap them side by side"
✅ Chrome and VS Code are now arranged!

You: voice on
🔊 Voice responses enabled!
```

**Features:**
- ✅ Offline speech recognition (Vosk)
- ✅ Natural language understanding
- ✅ Optional voice responses
- ✅ Context-aware conversations

## 🌐 Web Interface

Modern, animated UI on `http://localhost:7889`:

**Features:**
- ✨ Glassmorphism design with blur effects
- 🎨 Smooth animations and transitions
- 📱 Mobile-responsive layout
- 🔄 Real-time tool execution display
- 📊 Structured JSON output formatting
- ⚡ Loading indicators for long operations
- 🎯 Tool browser with search

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│          User Interface Layer               │
│   CLI (Voice) │ Web UI (Flask + REST API)   │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────┐
│    Ollama Client Layer      │
│  Conversation Management    │
│  Tool Call Detection        │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│      MCP Server Layer       │
│  Tool Registry & Execution  │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│      189 Tool Modules       │
│  Category-based Organization│
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│    macOS System APIs        │
│  AppleScript │ PyObjC │ CLI │
└─────────────────────────────┘
```

**Tech Stack:**
- **Backend**: Python 3.8+, Flask, Requests
- **AI**: Ollama (local LLM server)
- **Speech**: Vosk (offline recognition)
- **macOS**: PyObjC, AppleScript, shell commands
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Protocol**: Model Context Protocol (MCP)

[**→ Read full architecture guide**](docs/ARCHITECTURE.md)

## 📦 Installation

### Option 1: One-Line Install (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/siddharthprakash1/MacGPT/main/install.sh | bash
```

This will:
- ✅ Check prerequisites (Ollama, Python)
- ✅ Clone the repository to `~/.macgpt`
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create `macgpt` command

Then just run: `macgpt`

### Option 2: Manual Setup
```bash
# Prerequisites: macOS 12+, Python 3.9+, Ollama
brew install ollama

# Clone and setup
git clone https://github.com/siddharthprakash1/MacGPT.git
cd MacGPT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Pull an AI model
ollama pull mistral
# OR for better results:
ollama pull llama3.1

# Run
python start_web.py   # Web UI at http://localhost:7889
python start_cli.py   # CLI with voice control
```

[**→ Detailed installation guide**](docs/GETTING_STARTED.md)

## 🤝 Contributing

We welcome contributions! Whether you want to:
- 🛠️ Add new tools
- 🐛 Fix bugs
- 📖 Improve documentation
- ✨ Enhance UI/UX
- ⚡ Optimize performance

[**→ Contributing guide**](docs/CONTRIBUTING.md)

## 📄 License

MIT License - feel free to use, modify, and distribute.

## 🙏 Acknowledgments

Built with:
- [Ollama](https://ollama.ai) - Local LLM inference
- [Vosk](https://alphacephei.com/vosk/) - Offline speech recognition
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [PyObjC](https://pyobjc.readthedocs.io/) - macOS integration

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 📞 Contact

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Questions and community chat
- **LinkedIn**: https://www.linkedin.com/in/siddharth-prakash-771596241/

---

<div align="center">

**Made with ❤️ for macOS users who want their AI to actually do things**

[Documentation](docs/INDEX.md) · [Examples](docs/EXAMPLES.md) · [Contributing](docs/CONTRIBUTING.md)

</div>

