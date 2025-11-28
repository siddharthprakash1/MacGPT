# macOS AI Commander 🚀

> **AI-Powered macOS Automation System** | Control your entire Mac through natural language using local AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-Required-green.svg)](https://ollama.ai)
[![Tools: 189](https://img.shields.io/badge/Tools-189-purple.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Transform your Mac into an AI-powered automation machine. Use natural language to control windows, manage files, scrape websites, query databases, and execute 189+ system operations - all running locally with complete privacy.

![Demo](docs/assets/demo.gif) <!-- Add a demo GIF if you have one -->

## ✨ Key Features

- 🎤 **Voice Control** - Speak commands naturally (CLI mode)
- 🌐 **Beautiful Web UI** - Glassmorphism design with smooth animations
- 🧠 **Local AI** - Powered by Ollama, no cloud required
- 🔒 **Complete Privacy** - All processing happens on your Mac
- ⚡ **189 Tools** - Comprehensive automation across 15 categories
- 🎯 **Smart Context** - AI understands multi-step workflows
- 📱 **Modern UX** - Intuitive interface for both CLI and web

## 🎬 Quick Demo

```bash
# Install and run in 3 commands
pip install -r requirements.txt
ollama pull gpt-oss:20b
python start_web.py

# Then try:
"Snap Chrome to left and Safari to right"
"Test my internet speed"
"Compress all PDFs in Downloads"
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

### ⌨️ Keyboard & Mouse (9 tools)
Automate typing, clicks, hotkeys, mouse movements
```
"Type 'Hello World' and press cmd+s" → Types and saves
"Move mouse to center of screen" → Moves cursor
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

### Prerequisites
```bash
# macOS 10.15+, Python 3.8+
brew install ollama portaudio
```

### Quick Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/macos-ai-commander.git
cd macos-ai-commander

# 2. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Download AI model
ollama pull gpt-oss:20b

# 4. Run!
python start_cli.py   # CLI with voice
# OR
python start_web.py   # Web UI
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

