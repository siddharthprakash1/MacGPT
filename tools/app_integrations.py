"""
Deep App Integrations
Control specific apps with detailed functionality
"""

import subprocess
from typing import Optional


# ==================== SAFARI ====================

def safari_open_url(url: str, new_tab: bool = True) -> dict:
    """
    Open URL in Safari (new tab or window)
    
    Args:
        url: URL to open
        new_tab: Open in new tab (True) or new window (False)
    
    Returns:
        dict: Result
    """
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        script = f'''
        tell application "Safari"
            activate
            {'make new document' if not new_tab else 'tell window 1 to set current tab to (make new tab)'}
            set URL of document 1 to "{url}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "url": url,
            "message": f"Opened {url} in Safari"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def safari_close_tabs() -> dict:
    """Close all Safari tabs"""
    try:
        script = '''
        tell application "Safari"
            close every tab of every window
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {"success": True, "message": "Closed all Safari tabs"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def safari_get_current_url() -> dict:
    """Get current Safari URL"""
    try:
        script = '''
        tell application "Safari"
            return URL of current tab of window 1
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, check=True, timeout=2)
        return {
            "success": True,
            "url": result.stdout.strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== MESSAGES ====================

def send_imessage(recipient: str, message: str) -> dict:
    """
    Send iMessage
    
    Args:
        recipient: Phone number or email
        message: Message text
    
    Returns:
        dict: Result
    """
    try:
        escaped_msg = message.replace('"', '\\"').replace('\\', '\\\\')
        script = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{recipient}" of targetService
            send "{escaped_msg}" to targetBuddy
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {
            "success": True,
            "recipient": recipient,
            "message": "Message sent"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== MAIL ====================

def send_email(to: str, subject: str, body: str) -> dict:
    """
    Send email via Mail app
    
    Args:
        to: Recipient email
        subject: Email subject
        body: Email body
    
    Returns:
        dict: Result
    """
    try:
        script = f'''
        tell application "Mail"
            set theMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}", visible:true}}
            tell theMessage
                make new to recipient with properties {{address:"{to}"}}
            end tell
            activate
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {
            "success": True,
            "to": to,
            "subject": subject,
            "message": "Email draft created (click Send in Mail)"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== CALENDAR ====================

def create_calendar_event(title: str, start_date: str, duration: int = 60) -> dict:
    """
    Create calendar event
    
    Args:
        title: Event title
        start_date: Start date/time "YYYY-MM-DD HH:MM"
        duration: Duration in minutes
    
    Returns:
        dict: Result
    """
    try:
        script = f'''
        tell application "Calendar"
            tell calendar "Calendar"
                make new event with properties {{summary:"{title}", start date:date "{start_date}", end date:(date "{start_date}") + {duration} * minutes}}
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "title": title,
            "start": start_date,
            "message": f"Created calendar event '{title}'"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== FINDER ====================

def finder_search(query: str) -> dict:
    """
    Open Finder search
    
    Args:
        query: Search query
    
    Returns:
        dict: Result
    """
    try:
        script = f'''
        tell application "Finder"
            activate
            open search window
            set search window's target to home
            set search window's search query to "{query}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "query": query,
            "message": f"Opened Finder search for '{query}'"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_selected_files() -> dict:
    """Get currently selected files in Finder"""
    try:
        script = '''
        tell application "Finder"
            set selectedItems to selection
            set fileList to {}
            repeat with anItem in selectedItems
                set end of fileList to POSIX path of (anItem as text)
            end repeat
            return fileList
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, check=True, timeout=2)
        
        files = [f.strip() for f in result.stdout.split(',') if f.strip()]
        return {
            "success": True,
            "count": len(files),
            "files": files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== SYSTEM SETTINGS ====================

def toggle_bluetooth() -> dict:
    """Toggle Bluetooth on/off"""
    try:
        # Use blueutil if installed, otherwise fallback
        subprocess.run(['blueutil', '-p', 'toggle'], check=False, timeout=2)
        return {"success": True, "message": "Bluetooth toggled"}
    except:
        return {
            "success": False,
            "error": "Install blueutil: brew install blueutil"
        }


def set_wallpaper(image_path: str) -> dict:
    """
    Set desktop wallpaper
    
    Args:
        image_path: Path to image file
    
    Returns:
        dict: Result
    """
    try:
        script = f'''
        tell application "System Events"
            tell every desktop
                set picture to "{image_path}"
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "wallpaper": image_path,
            "message": f"Wallpaper set to {image_path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== FOCUS/PRODUCTIVITY ====================

def enable_focus_mode(mode: str = "Do Not Disturb") -> dict:
    """
    Enable Focus mode
    
    Args:
        mode: Focus mode name
    
    Returns:
        dict: Result
    """
    try:
        # This works on macOS 12+ (Monterey and later)
        script = f'''
        tell application "System Events"
            tell process "Control Center"
                click menu bar item "Focus" of menu bar 1
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=False, timeout=3)
        return {
            "success": True,
            "mode": mode,
            "message": f"Toggled Focus mode"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== QUICK ACTIONS ====================

def get_clipboard_history() -> dict:
    """Get recent clipboard (last 5 items)"""
    # This would require a clipboard manager - return current for now
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        return {
            "success": True,
            "current": result.stdout,
            "note": "Install a clipboard manager for history"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def quick_timer(seconds: int, message: str = "Timer done!") -> dict:
    """
    Set a quick timer with notification
    
    Args:
        seconds: Seconds to wait
        message: Notification message
    
    Returns:
        dict: Result
    """
    try:
        script = f'''
        delay {seconds}
        display notification "{message}" with title "Timer"
        '''
        # Run in background
        subprocess.Popen(['osascript', '-e', script])
        
        return {
            "success": True,
            "seconds": seconds,
            "message": f"Timer set for {seconds} seconds"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def show_notification_with_sound(title: str, message: str, sound: str = "default") -> dict:
    """
    Show notification with sound
    
    Args:
        title: Title
        message: Message
        sound: Sound name (default, Glass, Ping, etc.)
    
    Returns:
        dict: Result
    """
    try:
        sound_cmd = f'sound name "{sound}"' if sound != "default" else ""
        script = f'display notification "{message}" with title "{title}" {sound_cmd}'
        subprocess.run(['osascript', '-e', script], check=True, timeout=2)
        return {
            "success": True,
            "message": "Notification sent with sound"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

