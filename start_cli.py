#!/usr/bin/env python3
"""
CLI Launcher for macOS MCP System
Starts the command-line interface with voice control
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.ollama_client import interactive_mode

if __name__ == '__main__':
    interactive_mode()

