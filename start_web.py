#!/usr/bin/env python3
"""
Web UI Launcher for macOS MCP System
Starts the web interface on port 7889
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now run the web UI
if __name__ == '__main__':
    from ui.web_ui import app, config, client
    
    port = 7889
    print(f"\n{'='*60}")
    print(f"🚀 macOS MCP Web UI Starting")
    print(f"{'='*60}")
    print(f"Model: {config['ollama']['model']}")
    print(f"Tools: {len(client.mcp_server.tools)} available")
    print(f"\n🌐 Open your browser:")
    print(f"   http://localhost:{port}")
    print(f"\n💡 For voice control, use: python start_cli.py")
    print(f"\n{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)

