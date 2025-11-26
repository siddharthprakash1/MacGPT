"""
Keyboard & Mouse Automation
Type text, press keys, click, move mouse
"""

import subprocess
from typing import Tuple


def get_screen_size() -> Tuple[int, int]:
    """Get current screen dimensions"""
    try:
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
            width = int(bounds[2])
            height = int(bounds[3])
            return (width, height)
        
        # Fallback to common resolution
        return (1920, 1080)
            
    except Exception:
        # Fallback dimensions
        return (1920, 1080)


def type_text(text: str, delay: float = 0.1) -> dict:
    """Type text (simulate keyboard input)"""
    try:
        # Escape quotes and backslashes
        escaped = text.replace('\\', '\\\\').replace('"', '\\"')
        
        script = f'''
        tell application "System Events"
            keystroke "{escaped}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=10)
        return {
            "success": True,
            "text": text[:50],
            "message": f"Typed {len(text)} characters"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def press_key(key: str, modifiers: list = None) -> dict:
    """
    Press key with optional modifiers
    
    Args:
        key: Key to press (e.g., 'a', 'return', 'tab', 'space')
        modifiers: List of modifiers (e.g., ['command'], ['command', 'shift'])
    """
    try:
        if modifiers:
            modifier_str = ' '.join([f'{mod} down' for mod in modifiers])
            script = f'''
            tell application "System Events"
                keystroke "{key}" using {{{modifier_str}}}
            end tell
            '''
        else:
            script = f'''
            tell application "System Events"
                keystroke "{key}"
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        
        mod_text = f" with {', '.join(modifiers)}" if modifiers else ""
        return {
            "success": True,
            "key": key,
            "modifiers": modifiers or [],
            "message": f"Pressed {key}{mod_text}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def press_hotkey(combo: str) -> dict:
    """
    Press hotkey combination (e.g., 'cmd+c', 'ctrl+alt+del')
    
    Args:
        combo: Key combination (e.g., 'cmd+c', 'cmd+shift+4')
    """
    try:
        # Parse combination
        parts = combo.lower().split('+')
        key = parts[-1]
        
        # Map common shortcuts
        modifier_map = {
            'cmd': 'command',
            'ctrl': 'control',
            'alt': 'option',
            'shift': 'shift'
        }
        
        modifiers = [modifier_map.get(m, m) for m in parts[:-1]]
        
        return press_key(key, modifiers)
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def key_down(key: str) -> dict:
    """Press and hold key down"""
    try:
        script = f'''
        tell application "System Events"
            key down {key}
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "key": key,
            "message": f"Key {key} held down"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def key_up(key: str) -> dict:
    """Release held key"""
    try:
        script = f'''
        tell application "System Events"
            key up {key}
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "key": key,
            "message": f"Key {key} released"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mouse_click(x: int = None, y: int = None, clicks: int = 1, position: str = None) -> dict:
    """
    Click mouse at position or current location
    
    Args:
        x: X coordinate (None for current position)
        y: Y coordinate (None for current position)
        clicks: Number of clicks (1 for single, 2 for double)
        position: Named position like 'center' (overrides x/y)
    """
    try:
        # Handle named positions
        if position:
            screen_width, screen_height = get_screen_size()
            position_map = {
                'center': (screen_width // 2, screen_height // 2),
                'top-left': (0, 0),
                'top-right': (screen_width, 0),
                'bottom-left': (0, screen_height),
                'bottom-right': (screen_width, screen_height),
            }
            
            if position.lower() in position_map:
                x, y = position_map[position.lower()]
        
        if x is not None and y is not None:
            # Move and click
            script = f'''
            tell application "System Events"
                set mouseLoc to {{{x}, {y}}}
                click at mouseLoc
            end tell
            '''
        else:
            # Click at current position
            click_type = "double click" if clicks == 2 else "click"
            script = f'''
            tell application "System Events"
                {click_type}
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        
        location = f" at ({x}, {y})" if x and y else " at current position"
        return {
            "success": True,
            "x": x,
            "y": y,
            "clicks": clicks,
            "message": f"Clicked{location}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mouse_move(x: int = None, y: int = None, position: str = None) -> dict:
    """
    Move mouse to position (resolution-independent)
    
    Args:
        x: X coordinate (or None if using position)
        y: Y coordinate (or None if using position)
        position: Named position like 'center', 'top-left', 'bottom-right'
    """
    try:
        screen_width, screen_height = get_screen_size()
        
        # Handle named positions
        if position:
            position_map = {
                'center': (screen_width // 2, screen_height // 2),
                'top-left': (0, 0),
                'top-right': (screen_width, 0),
                'bottom-left': (0, screen_height),
                'bottom-right': (screen_width, screen_height),
                'top-center': (screen_width // 2, 0),
                'bottom-center': (screen_width // 2, screen_height),
                'left-center': (0, screen_height // 2),
                'right-center': (screen_width, screen_height // 2),
            }
            
            if position.lower() in position_map:
                x, y = position_map[position.lower()]
            else:
                return {
                    "success": False,
                    "error": f"Unknown position: {position}. Use: center, top-left, etc."
                }
        
        # If x or y are not provided, calculate center
        if x is None or y is None:
            x = screen_width // 2
            y = screen_height // 2
        
        # Use cliclick if available (brew install cliclick)
        subprocess.run(['cliclick', f'm:{x},{y}'], check=True, timeout=2)
        return {
            "success": True,
            "x": x,
            "y": y,
            "screen_width": screen_width,
            "screen_height": screen_height,
            "message": f"Mouse moved to ({x}, {y}) - center of {screen_width}x{screen_height} screen"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "cliclick not installed. Run: brew install cliclick"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mouse_right_click(x: int = None, y: int = None, position: str = None) -> dict:
    """Right-click mouse at position or current location"""
    try:
        # Handle named positions
        if position:
            screen_width, screen_height = get_screen_size()
            position_map = {
                'center': (screen_width // 2, screen_height // 2),
                'top-left': (0, 0),
                'top-right': (screen_width, 0),
                'bottom-left': (0, screen_height),
                'bottom-right': (screen_width, screen_height),
            }
            
            if position.lower() in position_map:
                x, y = position_map[position.lower()]
        
        if x is not None and y is not None:
            subprocess.run(['cliclick', f'rc:{x},{y}'], check=True, timeout=2)
        else:
            subprocess.run(['cliclick', 'rc:.'], check=True, timeout=2)
        
        location = f" at ({x}, {y})" if x and y else ""
        return {
            "success": True,
            "x": x,
            "y": y,
            "message": f"Right-clicked{location}"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "cliclick not installed. Run: brew install cliclick"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_mouse_position() -> dict:
    """Get current mouse position"""
    try:
        script = '''
        tell application "System Events"
            return (position of (get mouse))
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script],
                              capture_output=True, text=True, check=True, timeout=2)
        
        coords = result.stdout.strip().split(', ')
        if len(coords) == 2:
            return {
                "success": True,
                "x": int(coords[0]),
                "y": int(coords[1])
            }
        
        return {"success": False, "error": "Could not parse position"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def scroll(direction: str = "down", amount: int = 5) -> dict:
    """
    Scroll mouse wheel
    
    Args:
        direction: 'up' or 'down'
        amount: Scroll amount
    """
    try:
        if direction == "down":
            subprocess.run(['cliclick', f'w:-{amount}'], check=True, timeout=2)
        else:
            subprocess.run(['cliclick', f'w:{amount}'], check=True, timeout=2)
        
        return {
            "success": True,
            "direction": direction,
            "amount": amount,
            "message": f"Scrolled {direction} by {amount}"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "cliclick not installed. Run: brew install cliclick"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def drag_mouse(from_x: int, from_y: int, to_x: int, to_y: int) -> dict:
    """Drag mouse from one position to another"""
    try:
        subprocess.run(['cliclick', f'm:{from_x},{from_y}', 'dd:.', f'm:{to_x},{to_y}', 'du:.'],
                      check=True, timeout=5)
        return {
            "success": True,
            "from": f"({from_x}, {from_y})",
            "to": f"({to_x}, {to_y})",
            "message": f"Dragged from ({from_x}, {from_y}) to ({to_x}, {to_y})"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "cliclick not installed. Run: brew install cliclick"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

