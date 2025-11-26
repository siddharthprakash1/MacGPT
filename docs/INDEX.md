# Documentation Index

Welcome to the macOS AI Commander documentation! Find everything you need to understand, use, and contribute to this project.

## 📖 Documentation Structure

### 🚀 For Users

#### [Getting Started](GETTING_STARTED.md)
**Perfect for**: First-time users, installation help

**Contents**:
- Prerequisites and system requirements
- Step-by-step installation guide
- First commands to try
- Voice control setup
- Configuration options
- Troubleshooting common issues
- Privacy and security information

**Time to read**: ~15 minutes

---

#### [Examples & Workflows](EXAMPLES.md)
**Perfect for**: Learning what's possible, finding inspiration

**Contents**:
- Quick start examples
- Productivity workflows (morning routine, end-of-day cleanup)
- Development workflows (project setup, deployment)
- Creative workflows (video editing, design work)
- Web & research workflows
- Data & database operations
- System maintenance routines
- Real-world use cases
- Pro tips and best practices

**Time to read**: ~20 minutes

---

#### [Main README](README.md)
**Perfect for**: Quick overview of all features

**Contents**:
- Complete tool list (189 tools)
- Categories and capabilities
- Basic usage examples
- Configuration guide
- Project structure

**Time to read**: ~10 minutes

---

### 🔧 For Developers

#### [Architecture Guide](ARCHITECTURE.md)
**Perfect for**: Understanding how it works, contributing code

**Contents**:
- High-level architecture diagram
- Component breakdown
  - Ollama Client
  - MCP Server
  - Tool Registry
  - Tool Implementations
- Complete request flow (user input → execution → output)
- AI integration details
- Model Context Protocol (MCP) explained
- Web UI architecture
- Voice integration (input/output)
- Tool development guide
- Security considerations
- Performance optimization
- Future enhancements

**Time to read**: ~30 minutes

---

#### [Contributing Guide](CONTRIBUTING.md)
**Perfect for**: Contributing new features, fixing bugs

**Contents**:
- Ways to contribute
- Development environment setup
- Code style guidelines
- Tool development tutorial
- Testing requirements
- Commit message conventions
- Pull request process
- Code review expectations
- Bug reporting template
- Feature request template

**Time to read**: ~25 minutes

---

#### [Code Architecture](CODE_ARCHITECTURE.md)
**Perfect for**: Deep technical understanding

**Contents**:
- Detailed code structure
- Module responsibilities
- Data flow diagrams
- API specifications
- Design patterns used
- Extension points

**Time to read**: ~20 minutes

---

## 🗺️ Documentation Map

### By Experience Level

#### 🌱 **Beginner**
1. Start with [Getting Started](GETTING_STARTED.md)
2. Try examples from [Examples](EXAMPLES.md)
3. Browse [Main README](README.md) for capabilities

#### 🌿 **Intermediate**
1. Read [Architecture Guide](ARCHITECTURE.md) to understand internals
2. Explore [Examples](EXAMPLES.md) for complex workflows
3. Review [Main README](README.md) for all available tools

#### 🌳 **Advanced**
1. Study [Architecture Guide](ARCHITECTURE.md) for system design
2. Read [Contributing Guide](CONTRIBUTING.md) to add features
3. Review [Code Architecture](CODE_ARCHITECTURE.md) for implementation details

---

### By Use Case

#### 📝 **I want to install and use it**
→ [Getting Started](GETTING_STARTED.md)

#### 💡 **I want to see what it can do**
→ [Examples](EXAMPLES.md)

#### 🔍 **I want to understand how it works**
→ [Architecture Guide](ARCHITECTURE.md)

#### 🛠️ **I want to add a new tool**
→ [Contributing Guide](CONTRIBUTING.md) → Tool Development section

#### 🐛 **I found a bug**
→ [Contributing Guide](CONTRIBUTING.md) → Bug Reporting section

#### ✨ **I have a feature idea**
→ [Contributing Guide](CONTRIBUTING.md) → Feature Request section

#### ⚙️ **I want to customize it**
→ [Getting Started](GETTING_STARTED.md) → Configuration section

#### 🎤 **I want to use voice control**
→ [Getting Started](GETTING_STARTED.md) → Voice Control section

#### 🌐 **I prefer the web interface**
→ [Getting Started](GETTING_STARTED.md) → Running the System → Option 2

#### 🧠 **I want to understand the AI integration**
→ [Architecture Guide](ARCHITECTURE.md) → AI Integration section

---

## 📊 Quick Reference

### Tool Categories (189 Total)

| Category | Count | Examples |
|----------|-------|----------|
| Window Management | 9 | snap, resize, maximize |
| File Operations | 10 | compress, move, copy |
| Advanced Clipboard | 7 | history, append, images |
| Screen & Media | 8 | record, convert, resize |
| Display Control | 6 | night shift, resolution |
| Package Management | 16 | brew, npm, pip |
| Keyboard & Mouse | 9 | type, click, move |
| Time Machine | 8 | backup, restore, status |
| AirDrop & Handoff | 6 | send, receive, share |
| Database Tools | 11 | query Postgres, MySQL, etc. |
| Web Tools | 14 | scrape, download, speed test |
| App Integrations | 32 | Safari, Chrome, VS Code, etc. |
| Quick Tools | 10 | volume, brightness, lock |
| Advanced Tools | 32 | notes, reminders, music |
| Basic Tools | 7 | notifications, clipboard |

### Key Concepts

**MCP (Model Context Protocol)**: Standard way to describe tools to AI models

**Ollama**: Local AI server that runs models on your Mac

**Tool**: A function the AI can execute (e.g., snap window, compress file)

**Voice Control**: Speech-to-text input and text-to-speech output (CLI only)

**Web UI**: Browser-based interface with animations (port 7889)

**CLI**: Command-line interface with voice support

---

## 🔗 External Resources

### Ollama Documentation
- [Official Ollama Site](https://ollama.ai)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Available Models](https://ollama.ai/library)

### Model Context Protocol
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Examples](https://github.com/modelcontextprotocol)

### macOS Automation
- [AppleScript Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [PyObjC Documentation](https://pyobjc.readthedocs.io/)

### Python Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Requests Library](https://requests.readthedocs.io/)

---

## 📝 Documentation Standards

This documentation follows these principles:

1. **User-First**: Start with what users need to know
2. **Example-Driven**: Show, don't just tell
3. **Progressive Disclosure**: Basic → Advanced
4. **Searchable**: Clear headings and structure
5. **Maintainable**: Update as code changes
6. **Accessible**: Clear language, no jargon

---

## 🆘 Can't Find What You Need?

1. **Search**: Use Cmd+F to search across docs
2. **Issues**: Check [GitHub Issues](github.com/yourrepo/issues)
3. **Discussions**: Ask in [GitHub Discussions](github.com/yourrepo/discussions)
4. **Contact**: Open an issue for missing docs

---

## 📅 Documentation Updates

| File | Last Updated | Version |
|------|--------------|---------|
| GETTING_STARTED.md | 2025-11-26 | 1.0 |
| EXAMPLES.md | 2025-11-26 | 1.0 |
| ARCHITECTURE.md | 2025-11-26 | 1.0 |
| CONTRIBUTING.md | 2025-11-26 | 1.0 |
| README.md | 2025-11-26 | 1.0 |

---

## 🎯 Next Steps

### New User?
1. Read [Getting Started](GETTING_STARTED.md)
2. Install and run your first command
3. Browse [Examples](EXAMPLES.md) for ideas
4. Customize your configuration

### Want to Contribute?
1. Read [Architecture Guide](ARCHITECTURE.md)
2. Review [Contributing Guide](CONTRIBUTING.md)
3. Pick an issue or feature
4. Submit a PR!

### Looking for Inspiration?
1. Browse [Examples](EXAMPLES.md)
2. Try complex workflows
3. Share your own workflows
4. Help improve documentation

---

**Happy Automating!** 🚀

*Last updated: November 26, 2025*

