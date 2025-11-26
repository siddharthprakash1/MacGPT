"""
AirDrop & Handoff Tools
Share files and continue tasks across devices
"""

import subprocess
import os


def airdrop_send(file_path: str) -> dict:
    """
    Open AirDrop to send file
    
    Args:
        file_path: Path to file to send
    """
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found"}
        
        # Open file with AirDrop
        script = f'''
        tell application "Finder"
            set theFile to POSIX file "{file_path}" as alias
            reveal theFile
            activate
        end tell
        delay 0.5
        tell application "System Events"
            keystroke "i" using {{command down, control down}}
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        
        return {
            "success": True,
            "file": file_path,
            "message": f"AirDrop sharing menu opened for {os.path.basename(file_path)}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_airdrop_window() -> dict:
    """Open AirDrop window in Finder"""
    try:
        subprocess.run(['open', 'x-apple.systempreferences:com.apple.Airdrop-Settings'],
                      check=True, timeout=3)
        return {
            "success": True,
            "message": "AirDrop window opened"
        }
    except Exception as e:
        # Fallback: open Finder AirDrop
        try:
            script = '''
            tell application "Finder"
                activate
                open (path to airdrop)
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True, timeout=3)
            return {
                "success": True,
                "message": "AirDrop opened in Finder"
            }
        except:
            return {"success": False, "error": str(e)}


def enable_airdrop_everyone() -> dict:
    """Enable AirDrop for everyone (not just contacts)"""
    try:
        # This requires system preferences access
        script = '''
        tell application "System Preferences"
            reveal pane id "com.apple.preference.sharing"
            activate
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        
        return {
            "success": True,
            "message": "Opened Sharing preferences (manually enable AirDrop)"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_airdrop_status() -> dict:
    """Check if AirDrop is enabled"""
    try:
        # Check WiFi and Bluetooth status (required for AirDrop)
        wifi_result = subprocess.run(['networksetup', '-getairportpower', 'en0'],
                                    capture_output=True, text=True, timeout=2)
        
        wifi_on = "On" in wifi_result.stdout
        
        # Check Bluetooth
        bt_result = subprocess.run(['defaults', 'read', '/Library/Preferences/com.apple.Bluetooth', 'ControllerPowerState'],
                                  capture_output=True, text=True, timeout=2)
        
        bt_on = bt_result.stdout.strip() == "1"
        
        airdrop_ready = wifi_on and bt_on
        
        return {
            "success": True,
            "wifi_enabled": wifi_on,
            "bluetooth_enabled": bt_on,
            "airdrop_ready": airdrop_ready,
            "message": "AirDrop ready" if airdrop_ready else "AirDrop requires WiFi and Bluetooth"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_to_iphone(file_path: str) -> dict:
    """Send file to iPhone via AirDrop"""
    # This is essentially the same as airdrop_send
    return airdrop_send(file_path)


def send_to_ipad(file_path: str) -> dict:
    """Send file to iPad via AirDrop"""
    # This is essentially the same as airdrop_send
    return airdrop_send(file_path)


def handoff_url_to_device(url: str) -> dict:
    """
    Open URL that can be handed off to another device
    (opens in Safari which supports Handoff)
    """
    try:
        script = f'''
        tell application "Safari"
            activate
            open location "{url}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        
        return {
            "success": True,
            "url": url,
            "message": f"URL opened in Safari (available for Handoff): {url}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_continuity_settings() -> dict:
    """Open Continuity settings (Handoff, Universal Clipboard, etc.)"""
    try:
        subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.general'],
                      check=True, timeout=3)
        return {
            "success": True,
            "message": "Opened General settings (scroll to Handoff section)"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def universal_clipboard_test() -> dict:
    """Test if Universal Clipboard is working"""
    try:
        # Check if user is signed into iCloud
        result = subprocess.run(['defaults', 'read', 'MobileMeAccounts', 'Accounts'],
                              capture_output=True, text=True, timeout=2)
        
        signed_in = "AccountID" in result.stdout
        
        return {
            "success": True,
            "icloud_signed_in": signed_in,
            "message": "Universal Clipboard requires iCloud sign-in and Handoff enabled"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def share_text_via_airdrop(text: str) -> dict:
    """Share text via AirDrop (creates temp file)"""
    try:
        import tempfile
        
        # Create temp text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(text)
            temp_path = f.name
        
        # Send via AirDrop
        result = airdrop_send(temp_path)
        
        return {
            "success": result["success"],
            "text_length": len(text),
            "message": "Text shared via AirDrop"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

