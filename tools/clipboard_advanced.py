"""
Advanced Clipboard Operations
History, images, and more
"""

import subprocess
import os
from datetime import datetime


# Simple clipboard history (in-memory for this session)
_clipboard_history = []


def clipboard_save_to_history() -> dict:
    """Save current clipboard to history"""
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        content = result.stdout
        
        if content and (not _clipboard_history or content != _clipboard_history[0]):
            _clipboard_history.insert(0, content)
            if len(_clipboard_history) > 20:  # Keep last 20 items
                _clipboard_history.pop()
        
        return {
            "success": True,
            "message": "Clipboard saved to history"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def clipboard_get_history() -> dict:
    """Get clipboard history"""
    return {
        "success": True,
        "count": len(_clipboard_history),
        "history": _clipboard_history[:10]  # Show last 10
    }


def clipboard_restore_from_history(index: int) -> dict:
    """Restore clipboard from history"""
    try:
        if 0 <= index < len(_clipboard_history):
            content = _clipboard_history[index]
            subprocess.run(['pbcopy'], input=content.encode(), check=True)
            return {
                "success": True,
                "content": content[:100],
                "message": f"Restored item {index} to clipboard"
            }
        else:
            return {"success": False, "error": "Index out of range"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def clipboard_save_image(output_path: str = None) -> dict:
    """Save clipboard image to file"""
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.expanduser(f"~/Desktop/clipboard_{timestamp}.png")
        
        # Use osascript to save clipboard image
        script = f'''
        set theFile to POSIX file "{output_path}"
        set theImage to (the clipboard as «class PNGf»)
        set fileRef to open for access theFile with write permission
        write theImage to fileRef
        close access fileRef
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        
        return {
            "success": True,
            "path": output_path,
            "message": f"Image saved to {output_path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def clipboard_append(text: str) -> dict:
    """Append text to clipboard"""
    try:
        # Get current clipboard
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        current = result.stdout
        
        # Append new text
        new_content = current + text
        subprocess.run(['pbcopy'], input=new_content.encode(), check=True)
        
        return {
            "success": True,
            "appended": text,
            "message": "Text appended to clipboard"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def clipboard_clear() -> dict:
    """Clear clipboard"""
    try:
        subprocess.run(['pbcopy'], input=b'', check=True)
        return {
            "success": True,
            "message": "Clipboard cleared"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def clipboard_get_type() -> dict:
    """Get clipboard content type"""
    try:
        # Check for different types
        script = '''
        set clipboardTypes to {}
        try
            set temp to the clipboard as text
            set end of clipboardTypes to "text"
        end try
        try
            set temp to the clipboard as «class PNGf»
            set end of clipboardTypes to "image"
        end try
        try
            set temp to the clipboard as «class furl»
            set end of clipboardTypes to "file"
        end try
        return clipboardTypes
        '''
        
        result = subprocess.run(['osascript', '-e', script],
                              capture_output=True, text=True, check=True, timeout=2)
        
        types = [t.strip() for t in result.stdout.split(',')]
        
        return {
            "success": True,
            "types": types
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def clipboard_count_words() -> dict:
    """Count words in clipboard"""
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        content = result.stdout
        
        words = len(content.split())
        chars = len(content)
        lines = len(content.splitlines())
        
        return {
            "success": True,
            "words": words,
            "characters": chars,
            "lines": lines
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

