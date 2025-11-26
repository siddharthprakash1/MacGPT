"""
Window Management Tools
Snap, resize, move windows like a pro
"""

import subprocess
from typing import Optional, Tuple


def get_screen_dimensions(display: int = 0) -> Tuple[int, int, int, int]:
    """
    Get screen dimensions for specified display
    
    Returns:
        Tuple of (x_offset, y_offset, width, height)
    """
    try:
        # Get display info using system_profiler
        script = '''
        tell application "Finder"
            set desktopBounds to bounds of window of desktop
            return desktopBounds
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=3)
        
        # Parse bounds: {x1, y1, x2, y2}
        bounds = result.stdout.strip().split(', ')
        if len(bounds) >= 4:
            x1 = int(bounds[0])
            y1 = int(bounds[1])
            x2 = int(bounds[2])
            y2 = int(bounds[3])
            
            # For multi-display, estimate based on display index
            # Most common setup: MacBook (1920) + External (1920 or more)
            if display == 0:
                # Main display
                return (0, 25, x2, y2 - 25)
            else:
                # External display - assume same width as main, positioned to the right
                width = x2
                return (width * display, 25, width, y2 - 25)
        
        # Fallback to common resolutions
        if display == 0:
            return (0, 25, 1920, 1055)  # MacBook Pro 16"
        else:
            return (1920 * display, 25, 1920, 1080)  # Standard external
            
    except Exception:
        # Fallback dimensions
        if display == 0:
            return (0, 25, 1920, 1055)
        else:
            return (1920 * display, 25, 1920, 1080)


def snap_window_left(app_name: str, bring_front: bool = False, display: int = 0) -> dict:
    """Snap window to left half of screen (50% width)"""
    try:
        x_offset, y_offset, screen_width, screen_height = get_screen_dimensions(display)
        
        # Left half: 0% to 50% of screen width
        x = x_offset
        y = y_offset
        width = int(screen_width * 0.5)
        height = screen_height
        
        frontmost_line = "set frontmost to true" if bring_front else ""
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                {frontmost_line}
                tell window 1
                    set position to {{{x}, {y}}}
                    set size to {{{width}, {height}}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} snapped to left (50%)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def snap_window_right(app_name: str, bring_front: bool = False, display: int = 0) -> dict:
    """Snap window to right half of screen (50% width)"""
    try:
        x_offset, y_offset, screen_width, screen_height = get_screen_dimensions(display)
        
        # Right half: 50% to 100% of screen width
        x = x_offset + int(screen_width * 0.5)
        y = y_offset
        width = int(screen_width * 0.5)
        height = screen_height
        
        frontmost_line = "set frontmost to true" if bring_front else ""
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                {frontmost_line}
                tell window 1
                    set position to {{{x}, {y}}}
                    set size to {{{width}, {height}}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} snapped to right (50%)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_display_bounds() -> dict:
    """Get bounds of all displays (screens)"""
    try:
        script = '''
        tell application "Finder"
            set screenCount to count of windows of application "System Events"
        end tell
        
        tell application "System Events"
            tell application process "Finder"
                set mainScreen to get bounds of window of desktop
                return mainScreen as list
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=3)
        
        # Get screen info using system_profiler for better multi-monitor detection
        result2 = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                capture_output=True, text=True, timeout=5)
        
        return {
            "success": True,
            "info": result2.stdout,
            "message": "Use display index 0 for main screen, 1 for second screen, etc."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def snap_side_by_side(left_app: str, right_app: str, display: int = 0) -> dict:
    """Snap two apps side by side - left app on left 50%, right app on right 50%
    
    Args:
        left_app: App to place on left
        right_app: App to place on right  
        display: Display index (0=main, 1=second monitor, etc.)
    """
    try:
        x_offset, y_offset, screen_width, screen_height = get_screen_dimensions(display)
        
        # Left app: 0% to 50%
        left_x = x_offset
        left_y = y_offset
        left_width = int(screen_width * 0.5)
        left_height = screen_height
        
        # Right app: 50% to 100%
        right_x = x_offset + int(screen_width * 0.5)
        right_y = y_offset
        right_width = int(screen_width * 0.5)
        right_height = screen_height
        
        script = f'''
        tell application "System Events"
            -- Snap left app
            tell process "{left_app}"
                tell window 1
                    set position to {{{left_x}, {left_y}}}
                    set size to {{{left_width}, {left_height}}}
                end tell
            end tell
            
            -- Small delay
            delay 0.1
            
            -- Snap right app
            tell process "{right_app}"
                tell window 1
                    set position to {{{right_x}, {right_y}}}
                    set size to {{{right_width}, {right_height}}}
                end tell
            end tell
            
            -- Make both visible by raising them
            set visible of process "{left_app}" to true
            set visible of process "{right_app}" to true
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        
        display_name = "main screen" if display == 0 else f"external monitor {display}"
        return {
            "success": True, 
            "message": f"{left_app} (left 50%) and {right_app} (right 50%) arranged on {display_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def snap_to_display(app_name: str, display: int = 1, position: str = "left") -> dict:
    """Snap window to specific display (monitor) with percentage-based sizing
    
    Args:
        app_name: Application name
        display: Display index (0=main MacBook screen, 1=external monitor)
        position: 'left' (50%), 'right' (50%), or 'full' (100%) for that display
    """
    try:
        x_offset, y_offset, screen_width, screen_height = get_screen_dimensions(display)
        
        # Calculate based on position
        if position == "left":
            # Left 50%
            x = x_offset
            width = int(screen_width * 0.5)
        elif position == "right":
            # Right 50%
            x = x_offset + int(screen_width * 0.5)
            width = int(screen_width * 0.5)
        else:  # full
            # Full 100%
            x = x_offset
            width = screen_width
        
        y = y_offset
        height = screen_height
        
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set position to {{{x}, {y}}}
                    set size to {{{width}, {height}}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        
        display_name = "main screen" if display == 0 else f"external monitor {display}"
        percentage = "50%" if position in ["left", "right"] else "100%"
        return {
            "success": True,
            "message": f"{app_name} snapped to {position} ({percentage}) on {display_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def maximize_window(app_name: str, display: int = 0) -> dict:
    """Maximize window to 100% of screen (not native fullscreen)"""
    try:
        x_offset, y_offset, screen_width, screen_height = get_screen_dimensions(display)
        
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set position to {{{x_offset}, {y_offset}}}
                    set size to {{{screen_width}, {screen_height}}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        
        display_name = "main screen" if display == 0 else f"display {display}"
        return {"success": True, "message": f"{app_name} maximized on {display_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def center_window(app_name: str, display: int = 0, width_percent: float = 0.5, height_percent: float = 0.6) -> dict:
    """Center window on screen with custom size (default: 50% width, 60% height)"""
    try:
        x_offset, y_offset, screen_width, screen_height = get_screen_dimensions(display)
        
        # Calculate centered window size
        window_width = int(screen_width * width_percent)
        window_height = int(screen_height * height_percent)
        
        # Calculate centered position
        x = x_offset + int((screen_width - window_width) / 2)
        y = y_offset + int((screen_height - window_height) / 2)
        
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                set frontmost to true
                tell window 1
                    set position to {{{x}, {y}}}
                    set size to {{{window_width}, {window_height}}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": f"{app_name} centered ({int(width_percent*100)}% x {int(height_percent*100)}%)"}
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

