"""
macOS Integration Tools for MCP
Provides various macOS system integration capabilities
"""

import subprocess
import os
import json
import platform
from datetime import datetime


def send_notification(title: str, message: str, subtitle: str = "") -> dict:
    """
    Send a macOS notification
    
    Args:
        title: Notification title
        message: Notification message
        subtitle: Optional subtitle
    
    Returns:
        dict: Result with success status
    """
    try:
        script_parts = [f'display notification "{message}" with title "{title}"']
        if subtitle:
            script_parts[0] = f'display notification "{message}" with title "{title}" subtitle "{subtitle}"'
        
        subprocess.run(['osascript', '-e', script_parts[0]], check=True)
        return {
            "success": True,
            "message": "Notification sent successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def clipboard_read() -> dict:
    """
    Read content from macOS clipboard
    
    Returns:
        dict: Result with clipboard content
    """
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
        return {
            "success": True,
            "content": result.stdout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def clipboard_write(text: str) -> dict:
    """
    Write content to macOS clipboard
    
    Args:
        text: Text to copy to clipboard
    
    Returns:
        dict: Result with success status
    """
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=text)
        return {
            "success": True,
            "message": f"Copied {len(text)} characters to clipboard"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def text_to_speech(text: str, voice: str = "Samantha", rate: int = 200) -> dict:
    """
    Convert text to speech using macOS say command
    
    Args:
        text: Text to speak
        voice: Voice name (default: Samantha)
        rate: Speaking rate in words per minute (default: 200)
    
    Returns:
        dict: Result with success status
    """
    try:
        subprocess.run(['say', '-v', voice, '-r', str(rate), text], check=True)
        return {
            "success": True,
            "message": f"Spoke text using voice '{voice}'"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def take_screenshot(filename: str = None, area: str = "screen") -> dict:
    """
    Take a screenshot on macOS
    
    Args:
        filename: Output filename (default: screenshot_TIMESTAMP.png)
        area: 'screen' for full screen, 'window' for window selection, 'selection' for area selection
    
    Returns:
        dict: Result with filepath
    """
    try:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.png"
        
        filepath = os.path.join(screenshots_dir, filename)
        
        # Build screencapture command
        cmd = ['screencapture']
        if area == 'window':
            cmd.append('-w')  # Window mode
        elif area == 'selection':
            cmd.append('-s')  # Selection mode
        
        cmd.append(filepath)
        
        subprocess.run(cmd, check=True)
        return {
            "success": True,
            "filepath": filepath,
            "message": f"Screenshot saved to {filepath}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def spotlight_search(query: str, limit: int = 10) -> dict:
    """
    Search files using macOS Spotlight
    
    Args:
        query: Search query
        limit: Maximum number of results (default: 10)
    
    Returns:
        dict: Result with list of file paths
    """
    try:
        result = subprocess.run(
            ['mdfind', '-limit', str(limit), query],
            capture_output=True,
            text=True,
            check=True
        )
        
        files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return {
            "success": True,
            "results": files,
            "count": len(files)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_system_info() -> dict:
    """
    Get macOS system information
    
    Returns:
        dict: System information
    """
    try:
        # Get macOS version
        macos_version = platform.mac_ver()[0]
        
        # Get computer name
        computer_name = subprocess.run(
            ['scutil', '--get', 'ComputerName'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Get uptime
        uptime = subprocess.run(
            ['uptime'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        # Get disk usage
        df_output = subprocess.run(
            ['df', '-h', '/'],
            capture_output=True,
            text=True
        ).stdout.strip().split('\n')[1]
        
        disk_parts = df_output.split()
        
        return {
            "success": True,
            "system": {
                "os": "macOS",
                "version": macos_version,
                "computer_name": computer_name,
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "uptime": uptime,
                "disk": {
                    "total": disk_parts[1],
                    "used": disk_parts[2],
                    "available": disk_parts[3],
                    "usage_percent": disk_parts[4]
                }
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Tool registry with metadata for MCP
TOOLS = {
    "send_notification": {
        "description": "Send a macOS notification with title and message",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The notification title"
                },
                "message": {
                    "type": "string",
                    "description": "The notification message"
                },
                "subtitle": {
                    "type": "string",
                    "description": "Optional subtitle"
                }
            },
            "required": ["title", "message"]
        },
        "function": send_notification
    },
    "clipboard_read": {
        "description": "Read the current content from the macOS clipboard",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": clipboard_read
    },
    "clipboard_write": {
        "description": "Write text to the macOS clipboard",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to copy to clipboard"
                }
            },
            "required": ["text"]
        },
        "function": clipboard_write
    },
    "text_to_speech": {
        "description": "Convert text to speech using macOS text-to-speech engine",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to speak"
                },
                "voice": {
                    "type": "string",
                    "description": "Voice name (e.g., Samantha, Alex, Victoria)"
                },
                "rate": {
                    "type": "integer",
                    "description": "Speaking rate in words per minute"
                }
            },
            "required": ["text"]
        },
        "function": text_to_speech
    },
    "take_screenshot": {
        "description": "Take a screenshot on macOS",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Output filename (optional)"
                },
                "area": {
                    "type": "string",
                    "enum": ["screen", "window", "selection"],
                    "description": "Screenshot area type"
                }
            },
            "required": []
        },
        "function": take_screenshot
    },
    "spotlight_search": {
        "description": "Search for files using macOS Spotlight",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results"
                }
            },
            "required": ["query"]
        },
        "function": spotlight_search
    },
    "get_system_info": {
        "description": "Get macOS system information including version, disk usage, and uptime",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": get_system_info
    }
}


def get_enabled_tools(config: dict) -> dict:
    """Filter tools based on configuration"""
    # Merge basic and advanced tools
    try:
        from tools.advanced_tool_registry import ADVANCED_TOOLS
        all_tools = {**TOOLS, **ADVANCED_TOOLS}
    except ImportError:
        all_tools = TOOLS
    
    enabled = config.get('tools', {}).get('enabled', [])
    if not enabled:
        return all_tools
    return {name: tool for name, tool in all_tools.items() if name in enabled}

