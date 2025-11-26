# macOS MCP Automation System 🚀

**The Ultimate macOS Automation System** - Control your Mac with AI using 189 powerful tools!

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Pull AI model
ollama pull gpt-oss:20b

# 3. Start!
python start_cli.py   # CLI with voice control
# OR
python start_web.py   # Web UI at http://localhost:7889
```

## 🛠️ What Can It Do?

**189 Tools Across 11 Categories:**
- 🪟 **Window Management** - Snap, resize, move windows
- 📁 **File Operations** - Zip, move, copy, rename files
- 📋 **Advanced Clipboard** - History, images, append text
- 🎬 **Screen & Media** - Record, resize images, convert videos
- 🖥️ **Display Control** - Night Shift, resolution, mirroring
- 📦 **Package Management** - Brew, npm, pip installs
- ⌨️ **Keyboard & Mouse** - Type text, click, move mouse
- 💾 **Time Machine Backups** - Manage backups
- ✈️ **AirDrop & Handoff** - Send files between devices
- 🗄️ **Databases** - Query Postgres, MySQL, MongoDB, Redis
- 🌐 **Web Tools** - Download, scrape, speed test, QR codes

## 📚 Documentation

See full documentation in [`docs/README.md`](docs/README.md)

## 🎤 Voice Control (CLI Mode)

```
You: [press Enter]
🎤 Listening... (speak now)
[You: "Snap Chrome to left half and Safari to right"]
✅ Done!
```

Enable voice responses:
```
You: voice on
🔊 AI will speak responses!
```

## 🌐 Web Interface

Beautiful dark-themed UI with:
- ✅ Real-time tool execution
- ✅ Animated loading states
- ✅ Structured output formatting
- ✅ 189 tools available

## 📂 Clean Architecture

```
core/     - System core (MCP, Ollama)
tools/    - All 189 tool implementations
ui/       - Web interface
docs/     - Full documentation
```

## 🚀 Example Commands

```
"Snap Chrome to left and Safari to right"
"Compress all PDFs in Downloads"
"Test my internet speed"
"Start Time Machine backup"
"Install node via brew"
"Generate QR code for my website"
"Type 'Hello World' and press cmd+s"
"Send this file via AirDrop"
```

## ⚡ Requirements

- macOS 10.15+
- Python 3.8+ 
- [Ollama](https://ollama.ai) with gpt-oss:20b model

---

**Total**: 189 Tools | **Model**: gpt-oss:20b | **Organized**: Clean folder structure

