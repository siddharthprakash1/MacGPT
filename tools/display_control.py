"""
Display & Monitor Control
Resolution, night shift, screen saver, etc.
"""

import subprocess


def toggle_night_shift() -> dict:
    """Toggle Night Shift on/off"""
    try:
        # Use shortcuts if available, otherwise system preferences
        script = '''
        tell application "System Events"
            tell process "Control Center"
                click menu bar item "Display" of menu bar 1
                delay 0.5
                click button "Night Shift" of window 1
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {
            "success": True,
            "message": "Night Shift toggled"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def start_screen_saver() -> dict:
    """Start screen saver"""
    try:
        subprocess.run(['open', '-a', 'ScreenSaverEngine'], check=True, timeout=2)
        return {
            "success": True,
            "message": "Screen saver started"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_displays() -> dict:
    """List connected displays"""
    try:
        result = subprocess.run(
            ['system_profiler', 'SPDisplaysDataType'],
            capture_output=True, text=True, check=True, timeout=10
        )
        
        # Parse display info
        displays = []
        lines = result.stdout.split('\n')
        current_display = {}
        
        for line in lines:
            line = line.strip()
            if 'Display Type:' in line or 'Resolution:' in line or 'Main Display:' in line:
                displays.append(line)
        
        return {
            "success": True,
            "displays": displays[:10],  # First 10 lines
            "raw": result.stdout[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_display_resolution(width: int, height: int) -> dict:
    """Set display resolution (requires displayplacer: brew install displayplacer)"""
    try:
        # Note: This requires displayplacer to be installed
        subprocess.run(
            ['displayplacer', f'res:{width}x{height}'],
            check=True, timeout=5
        )
        return {
            "success": True,
            "resolution": f"{width}x{height}",
            "message": f"Resolution set to {width}x{height}"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "displayplacer not installed. Run: brew install displayplacer"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mirror_displays() -> dict:
    """Mirror displays"""
    try:
        script = '''
        tell application "System Preferences"
            reveal anchor "displaysDisplayTab" of pane id "com.apple.preference.displays"
            activate
        end tell
        delay 1
        tell application "System Events"
            tell process "System Preferences"
                click checkbox "Mirror Displays" of tab group 1 of window 1
            end tell
        end tell
        quit application "System Preferences"
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=10)
        return {
            "success": True,
            "message": "Display mirroring toggled"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def enable_true_tone(enable: bool = True) -> dict:
    """Enable/disable True Tone"""
    try:
        action = "enable" if enable else "disable"
        # This requires system control
        return {
            "success": False,
            "message": "True Tone control requires manual settings access"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_display_info() -> dict:
    """Get current display information"""
    try:
        # Get screen resolution
        script = '''
        tell application "Finder"
            set screenRes to bounds of window of desktop
            return screenRes
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script],
                              capture_output=True, text=True, check=True, timeout=3)
        
        bounds = result.stdout.strip().split(', ')
        if len(bounds) >= 4:
            width = int(bounds[2])
            height = int(bounds[3])
            
            return {
                "success": True,
                "resolution": f"{width}x{height}",
                "width": width,
                "height": height
            }
        
        return {"success": False, "error": "Could not parse display info"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def toggle_auto_brightness() -> dict:
    """Toggle auto brightness"""
    try:
        # This requires system preferences access
        return {
            "success": False,
            "message": "Auto brightness requires manual settings access"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_refresh_rate(rate: int = 60) -> dict:
    """Set display refresh rate"""
    try:
        # This typically requires third-party tools or system preferences
        return {
            "success": False,
            "message": f"Refresh rate control requires manual settings or displayplacer"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

