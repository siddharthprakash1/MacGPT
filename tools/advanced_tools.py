"""
Advanced macOS Integration Tools
More powerful tools for real-world automation
"""

import subprocess
import os
import json
import re
from pathlib import Path
from typing import Optional, List


# ==================== FILE OPERATIONS ====================

def read_file(filepath: str, lines: Optional[int] = None) -> dict:
    """
    Read contents of a file
    
    Args:
        filepath: Path to the file
        lines: Number of lines to read (None for all)
    
    Returns:
        dict: File content
    """
    try:
        path = Path(filepath).expanduser()
        with open(path, 'r', encoding='utf-8') as f:
            if lines:
                content = ''.join(f.readlines()[:lines])
            else:
                content = f.read()
        
        return {
            "success": True,
            "filepath": str(path),
            "content": content,
            "size": path.stat().st_size
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def write_file(filepath: str, content: str, mode: str = "overwrite") -> dict:
    """
    Write content to a file
    
    Args:
        filepath: Path to the file
        content: Content to write
        mode: 'overwrite' or 'append'
    
    Returns:
        dict: Result with success status
    """
    try:
        path = Path(filepath).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        
        write_mode = 'a' if mode == 'append' else 'w'
        with open(path, write_mode, encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "filepath": str(path),
            "bytes_written": len(content.encode('utf-8')),
            "mode": mode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_files(directory: str, pattern: str = "*", recursive: bool = False) -> dict:
    """
    List files in a directory
    
    Args:
        directory: Directory path
        pattern: Glob pattern (e.g., "*.py", "*.txt")
        recursive: Search recursively
    
    Returns:
        dict: List of files
    """
    try:
        path = Path(directory).expanduser()
        
        if recursive:
            files = list(path.rglob(pattern))
        else:
            files = list(path.glob(pattern))
        
        file_list = []
        for f in sorted(files):
            if f.is_file():
                file_list.append({
                    "path": str(f),
                    "name": f.name,
                    "size": f.stat().st_size,
                    "modified": f.stat().st_mtime
                })
        
        return {
            "success": True,
            "directory": str(path),
            "count": len(file_list),
            "files": file_list
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def create_directory(directory: str) -> dict:
    """
    Create a directory (with parents if needed)
    
    Args:
        directory: Directory path to create
    
    Returns:
        dict: Result with success status
    """
    try:
        path = Path(directory).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        
        return {
            "success": True,
            "directory": str(path),
            "message": f"Directory created: {path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== APPLICATION CONTROL ====================

def open_application(app_name: str) -> dict:
    """
    Open a macOS application
    
    Args:
        app_name: Application name (e.g., "Safari", "Notes", "Music")
    
    Returns:
        dict: Result with success status
    """
    try:
        subprocess.run(['open', '-a', app_name], check=True)
        return {
            "success": True,
            "application": app_name,
            "message": f"Opened {app_name}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def close_application(app_name: str, force: bool = False) -> dict:
    """
    Close a macOS application
    
    Args:
        app_name: Application name
        force: Force quit if True
    
    Returns:
        dict: Result with success status
    """
    try:
        if force:
            script = f'tell application "{app_name}" to quit'
            subprocess.run(['killall', app_name], check=False)
        else:
            script = f'tell application "{app_name}" to quit'
            subprocess.run(['osascript', '-e', script], check=True)
        
        return {
            "success": True,
            "application": app_name,
            "message": f"Closed {app_name}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_running_apps() -> dict:
    """
    List all running applications
    
    Returns:
        dict: List of running applications
    """
    try:
        result = subprocess.run(
            ['osascript', '-e', 'tell application "System Events" to get name of every process whose background only is false'],
            capture_output=True,
            text=True,
            check=True
        )
        
        apps = [app.strip() for app in result.stdout.split(',')]
        
        return {
            "success": True,
            "count": len(apps),
            "applications": sorted(apps)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== APPLE NOTES INTEGRATION ====================

def create_note(title: str, content: str, folder: str = "Notes") -> dict:
    """
    Create a new note in Apple Notes
    
    Args:
        title: Note title
        content: Note content
        folder: Folder name (default: Notes)
    
    Returns:
        dict: Result with success status
    """
    try:
        # Escape quotes in content
        title_escaped = title.replace('"', '\\"')
        content_escaped = content.replace('"', '\\"')
        
        script = f'''
        tell application "Notes"
            tell folder "{folder}"
                make new note with properties {{name:"{title_escaped}", body:"{content_escaped}"}}
            end tell
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], check=True)
        
        return {
            "success": True,
            "title": title,
            "folder": folder,
            "message": f"Created note '{title}' in {folder}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def search_notes(query: str, limit: int = 10) -> dict:
    """
    Search Apple Notes
    
    Args:
        query: Search query
        limit: Maximum results
    
    Returns:
        dict: List of matching notes
    """
    try:
        script = f'''
        tell application "Notes"
            set noteList to {{}}
            set allNotes to every note
            repeat with aNote in allNotes
                set noteBody to body of aNote as text
                set noteName to name of aNote as text
                if noteBody contains "{query}" or noteName contains "{query}" then
                    set end of noteList to noteName
                end if
            end repeat
            return noteList
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        
        notes = [n.strip() for n in result.stdout.split(',') if n.strip()][:limit]
        
        return {
            "success": True,
            "query": query,
            "count": len(notes),
            "notes": notes
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== REMINDERS ====================

def create_reminder(title: str, list_name: str = "Reminders", due_date: Optional[str] = None) -> dict:
    """
    Create a reminder in Apple Reminders
    
    Args:
        title: Reminder title
        list_name: List name (default: Reminders)
        due_date: Due date (format: "YYYY-MM-DD HH:MM")
    
    Returns:
        dict: Result with success status
    """
    try:
        title_escaped = title.replace('"', '\\"')
        
        if due_date:
            script = f'''
            tell application "Reminders"
                tell list "{list_name}"
                    make new reminder with properties {{name:"{title_escaped}", due date:date "{due_date}"}}
                end tell
            end tell
            '''
        else:
            script = f'''
            tell application "Reminders"
                tell list "{list_name}"
                    make new reminder with properties {{name:"{title_escaped}"}}
                end tell
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True)
        
        return {
            "success": True,
            "title": title,
            "list": list_name,
            "due_date": due_date,
            "message": f"Created reminder '{title}'"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== PROCESS MANAGEMENT ====================

def list_processes(filter_name: Optional[str] = None) -> dict:
    """
    List running processes
    
    Args:
        filter_name: Filter by process name (optional)
    
    Returns:
        dict: List of processes
    """
    try:
        if filter_name:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )
            lines = [line for line in result.stdout.split('\n') if filter_name.lower() in line.lower()]
        else:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')[:20]  # Limit to 20
        
        processes = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    processes.append({
                        "user": parts[0],
                        "pid": parts[1],
                        "cpu": parts[2],
                        "mem": parts[3],
                        "command": parts[10]
                    })
        
        return {
            "success": True,
            "count": len(processes),
            "processes": processes
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def kill_process(pid: int, force: bool = False) -> dict:
    """
    Kill a process by PID
    
    Args:
        pid: Process ID
        force: Use SIGKILL if True, SIGTERM if False
    
    Returns:
        dict: Result with success status
    """
    try:
        signal = '-9' if force else '-15'
        subprocess.run(['kill', signal, str(pid)], check=True)
        
        return {
            "success": True,
            "pid": pid,
            "message": f"Killed process {pid}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== WEB & URL OPERATIONS ====================

def open_url(url: str, browser: str = "default") -> dict:
    """
    Open a URL in browser
    
    Args:
        url: URL to open
        browser: Browser name (default, Safari, Chrome, Firefox)
    
    Returns:
        dict: Result with success status
    """
    try:
        if browser == "default":
            subprocess.run(['open', url], check=True)
        else:
            subprocess.run(['open', '-a', browser, url], check=True)
        
        return {
            "success": True,
            "url": url,
            "browser": browser,
            "message": f"Opened {url}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_network_info() -> dict:
    """
    Get network information
    
    Returns:
        dict: Network information
    """
    try:
        # Get WiFi network name (try multiple interfaces)
        wifi_name = "Not connected"
        for interface in ['en0', 'en1']:
            try:
                wifi_result = subprocess.run(
                    ['networksetup', '-getairportnetwork', interface],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if 'Current Wi-Fi Network:' in wifi_result.stdout:
                    wifi_name = wifi_result.stdout.split('Current Wi-Fi Network:')[1].strip()
                    break
            except:
                continue
        
        # Get IP address
        ip_address = "Unknown"
        try:
            ip_result = subprocess.run(
                ['ifconfig'],
                capture_output=True,
                text=True,
                check=False
            )
            
            for line in ip_result.stdout.split('\n'):
                if 'inet ' in line and '127.0.0.1' not in line and '::1' not in line:
                    parts = line.strip().split()
                    if len(parts) >= 2 and parts[0] == 'inet':
                        # Skip link-local addresses
                        if not parts[1].startswith('169.254'):
                            ip_address = parts[1]
                            break
        except:
            pass
        
        return {
            "success": True,
            "wifi_network": wifi_name,
            "ip_address": ip_address
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== MUSIC CONTROL ====================

def control_music(action: str) -> dict:
    """
    Control Apple Music/Spotify
    
    Args:
        action: 'play', 'pause', 'next', 'previous', 'stop'
    
    Returns:
        dict: Result with success status
    """
    # Map actions to correct AppleScript commands
    action_map = {
        'play': 'play',
        'pause': 'pause',
        'next': 'next track',
        'previous': 'previous track',
        'stop': 'stop'
    }
    
    applescript_action = action_map.get(action, action)
    
    try:
        script = f'tell application "Music" to {applescript_action}'
        subprocess.run(['osascript', '-e', script], check=True)
        
        return {
            "success": True,
            "action": action,
            "message": f"Music {action}"
        }
    except Exception as e:
        # Try Spotify if Music fails
        try:
            script = f'tell application "Spotify" to {applescript_action}'
            subprocess.run(['osascript', '-e', script], check=True)
            return {
                "success": True,
                "action": action,
                "application": "Spotify",
                "message": f"Spotify {action}"
            }
        except:
            return {
                "success": False,
                "error": str(e)
            }


def play_spotify_track(query: str) -> dict:
    """
    Search and play a track on Spotify
    
    Args:
        query: Song name or "artist - song"
    
    Returns:
        dict: Result with success status
    """
    try:
        # Open Spotify first
        subprocess.run(['open', '-a', 'Spotify'], check=False)
        
        # Wait a moment for Spotify to open
        import time
        time.sleep(1)
        
        # Use AppleScript to search and play
        escaped_query = query.replace('"', '\\"')
        script = f'''
        tell application "Spotify"
            activate
            play track "spotify:search:{escaped_query}"
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], check=True)
        
        return {
            "success": True,
            "query": query,
            "message": f"Playing '{query}' on Spotify"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Make sure Spotify is installed and try opening it manually first"
        }


def get_current_song() -> dict:
    """
    Get currently playing song info
    
    Returns:
        dict: Song information
    """
    try:
        script = '''
        tell application "Music"
            if player state is playing then
                set trackName to name of current track
                set trackArtist to artist of current track
                set trackAlbum to album of current track
                return trackName & " by " & trackArtist & " from " & trackAlbum
            else
                return "Not playing"
            end if
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            "success": True,
            "song_info": result.stdout.strip()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== SMART HELPERS ====================

def run_shell_command(command: str, timeout: int = 30) -> dict:
    """
    Run a shell command (use with caution!)
    
    Args:
        command: Shell command to run
        timeout: Timeout in seconds
    
    Returns:
        dict: Command output
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

