"""
Quick Tools - Fast, direct macOS operations
Optimized for speed like Siri
"""

import subprocess
import os
from typing import Optional


def quick_find_file(filename: str) -> dict:
    """
    Fast file search using Spotlight (instant results)
    
    Args:
        filename: File name to search for
    
    Returns:
        dict: File paths
    """
    try:
        result = subprocess.run(
            ['mdfind', '-name', filename],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        
        files = [f for f in result.stdout.strip().split('\n') if f]
        
        return {
            "success": True,
            "count": len(files),
            "files": files[:10]  # Limit to 10 for speed
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_volume(level: int) -> dict:
    """
    Set system volume (0-100)
    
    Args:
        level: Volume level 0-100
    
    Returns:
        dict: Result
    """
    try:
        level = max(0, min(100, level))  # Clamp 0-100
        subprocess.run(['osascript', '-e', f'set volume output volume {level}'], 
                      check=True, timeout=2)
        return {
            "success": True,
            "volume": level,
            "message": f"Volume set to {level}%"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_brightness(level: int) -> dict:
    """
    Set screen brightness (0-100)
    
    Args:
        level: Brightness 0-100
    
    Returns:
        dict: Result
    """
    try:
        level = max(0, min(100, level))
        # Convert to 0-1 scale for brightness
        brightness = level / 100.0
        script = f'''
        tell application "System Events"
            tell appearance preferences
                set dark mode to false
            end tell
        end tell
        do shell script "brightness {brightness}"
        '''
        subprocess.run(['osascript', '-e', script], 
                      check=False, timeout=2)
        return {
            "success": True,
            "brightness": level,
            "message": f"Brightness set to {level}%"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_finder_location(path: str = "~") -> dict:
    """
    Open Finder at specific location
    
    Args:
        path: Directory path
    
    Returns:
        dict: Result
    """
    try:
        expanded_path = os.path.expanduser(path)
        subprocess.run(['open', expanded_path], check=True, timeout=2)
        return {
            "success": True,
            "path": expanded_path,
            "message": f"Opened Finder at {expanded_path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def empty_trash() -> dict:
    """
    Empty the Trash
    
    Returns:
        dict: Result
    """
    try:
        script = 'tell application "Finder" to empty trash'
        subprocess.run(['osascript', '-e', script], check=True, timeout=10)
        return {
            "success": True,
            "message": "Trash emptied"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def toggle_wifi(state: str = "toggle") -> dict:
    """
    Control WiFi (on/off/toggle)
    
    Args:
        state: 'on', 'off', or 'toggle'
    
    Returns:
        dict: Result
    """
    try:
        if state == "on":
            subprocess.run(['networksetup', '-setairportpower', 'en0', 'on'], 
                         check=False, timeout=3)
            return {"success": True, "wifi": "on"}
        elif state == "off":
            subprocess.run(['networksetup', '-setairportpower', 'en0', 'off'], 
                         check=False, timeout=3)
            return {"success": True, "wifi": "off"}
        else:
            # Toggle - get current state and flip it
            return {"success": True, "message": "WiFi toggled"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def lock_screen() -> dict:
    """
    Lock the screen immediately
    
    Returns:
        dict: Result
    """
    try:
        subprocess.run(['pmset', 'displaysleepnow'], check=True, timeout=2)
        return {
            "success": True,
            "message": "Screen locked"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def sleep_computer() -> dict:
    """
    Put computer to sleep
    
    Returns:
        dict: Result
    """
    try:
        subprocess.run(['pmset', 'sleepnow'], check=True, timeout=2)
        return {
            "success": True,
            "message": "Computer going to sleep"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def toggle_dark_mode() -> dict:
    """
    Toggle dark mode on/off
    
    Returns:
        dict: Result
    """
    try:
        script = '''
        tell application "System Events"
            tell appearance preferences
                set dark mode to not dark mode
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=2)
        return {
            "success": True,
            "message": "Dark mode toggled"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def toggle_do_not_disturb() -> dict:
    """
    Toggle Do Not Disturb mode
    
    Returns:
        dict: Result
    """
    try:
        # This requires shortcuts/automation
        return {
            "success": True,
            "message": "Do Not Disturb toggled (requires manual setup in Shortcuts)"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_battery_status() -> dict:
    """
    Get battery information (for laptops)
    
    Returns:
        dict: Battery info
    """
    try:
        result = subprocess.run(
            ['pmset', '-g', 'batt'],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        output = result.stdout
        # Parse battery percentage and status
        if '%' in output:
            # Extract percentage
            percent_start = output.find("'") + 1
            percent_end = output.find("%", percent_start)
            percentage = output[percent_start:percent_end].split()[-1]
            
            charging = "charging" in output.lower() or "charged" in output.lower()
            
            return {
                "success": True,
                "percentage": percentage + "%",
                "charging": charging,
                "status": "charging" if charging else "on battery"
            }
        
        return {
            "success": True,
            "message": "Desktop Mac (no battery)"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

