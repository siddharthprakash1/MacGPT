"""
Window Management Tools
Snap, resize, move windows like a pro
"""

import subprocess
from typing import Optional


def snap_window_left(app_name: str) -> dict:
    """Snap window to left half of screen"""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set position to {{0, 25}}
                    set size to {{960, 1055}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} snapped to left"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def snap_window_right(app_name: str) -> dict:
    """Snap window to right half of screen"""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set position to {{960, 25}}
                    set size to {{960, 1055}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} snapped to right"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def maximize_window(app_name: str) -> dict:
    """Maximize window (fullscreen)"""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set value of attribute "AXFullScreen" to true
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} maximized"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def center_window(app_name: str) -> dict:
    """Center window on screen"""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set position to {{480, 290}}
                    set size to {{960, 600}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} centered"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def resize_window(app_name: str, width: int, height: int) -> dict:
    """Resize window to specific dimensions"""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set size to {{{width}, {height}}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} resized to {width}x{height}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def move_window(app_name: str, x: int, y: int) -> dict:
    """Move window to specific position"""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set position to {{{x}, {y}}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} moved to ({x}, {y})"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_all_windows() -> dict:
    """List all open windows"""
    try:
        script = '''
        tell application "System Events"
            set windowList to {}
            repeat with proc in (every process whose background only is false)
                set procName to name of proc
                repeat with win in (every window of proc)
                    set end of windowList to procName & " - " & name of win
                end repeat
            end repeat
            return windowList
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, check=True, timeout=3)
        windows = [w.strip() for w in result.stdout.split(',') if w.strip()]
        return {"success": True, "count": len(windows), "windows": windows}
    except Exception as e:
        return {"success": False, "error": str(e)}


def minimize_window(app_name: str) -> dict:
    """Minimize window"""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set value of attribute "AXMinimized" of window 1 to true
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} minimized"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def bring_to_front(app_name: str) -> dict:
    """Bring app window to front"""
    try:
        script = f'''
        tell application "{app_name}"
            activate
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} brought to front"}
    except Exception as e:
        return {"success": False, "error": str(e)}

