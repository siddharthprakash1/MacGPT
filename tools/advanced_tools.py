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


def get_network_info(**kwargs) -> dict:
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


def spotify_play_library(item: str = "liked") -> dict:
    """
    Play Spotify library items like Liked Songs, playlists, or albums
    
    Args:
        item: What to play - "liked", "discover", "release radar", or a playlist name
    
    Returns:
        dict: Result with success status
    """
    try:
        import time
        
        # Open Spotify first
        subprocess.run(['open', '-a', 'Spotify'], check=False)
        time.sleep(1.5)
        
        item_lower = item.lower().strip()
        
        # Map common requests to Spotify URIs
        uri_map = {
            "liked": "spotify:collection:tracks",
            "liked songs": "spotify:collection:tracks",
            "my liked songs": "spotify:collection:tracks",
            "favorites": "spotify:collection:tracks",
            "saved songs": "spotify:collection:tracks",
            "discover": "spotify:playlist:37i9dQZEVXcQ9COmYvLnAL",
            "discover weekly": "spotify:playlist:37i9dQZEVXcQ9COmYvLnAL",
            "release radar": "spotify:playlist:37i9dQZEVXdNxfTNOg82rb",
            "daily mix": "spotify:playlist:37i9dQZF1E35F7gvkWxrjr",
        }
        
        # Get URI or use search
        uri = uri_map.get(item_lower)
        
        if uri:
            # Play specific URI
            script = f'''
            tell application "Spotify"
                activate
                play track "{uri}"
            end tell
            '''
        else:
            # Search and play playlist
            escaped = item.replace('"', '\\"')
            script = f'''
            tell application "Spotify"
                activate
                play track "spotify:search:{escaped}"
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        
        return {
            "success": True,
            "item": item,
            "message": f"Playing {item} on Spotify app"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Make sure Spotify desktop app is installed"
        }


def spotify_get_current_track() -> dict:
    """
    Get information about the currently playing track on Spotify
    
    Returns:
        dict: Track name, artist, album, duration, position
    """
    try:
        script = '''
        tell application "Spotify"
            if player state is playing or player state is paused then
                set trackName to name of current track
                set trackArtist to artist of current track
                set trackAlbum to album of current track
                set trackDuration to duration of current track
                set trackPosition to player position
                set isPlaying to (player state is playing)
                return trackName & "|" & trackArtist & "|" & trackAlbum & "|" & trackDuration & "|" & trackPosition & "|" & isPlaying
            else
                return "NOT_PLAYING"
            end if
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        
        if output == "NOT_PLAYING":
            return {"success": True, "playing": False, "message": "Spotify is not playing anything"}
        
        parts = output.split("|")
        if len(parts) >= 6:
            duration_ms = int(float(parts[3]))
            position_ms = int(float(parts[4]) * 1000)
            return {
                "success": True,
                "playing": parts[5] == "true",
                "track": parts[0],
                "artist": parts[1],
                "album": parts[2],
                "duration": f"{duration_ms // 60000}:{(duration_ms // 1000) % 60:02d}",
                "position": f"{position_ms // 60000}:{(position_ms // 1000) % 60:02d}",
                "progress_percent": round((position_ms / duration_ms) * 100, 1) if duration_ms > 0 else 0
            }
        return {"success": True, "raw": output}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_next_track() -> dict:
    """Skip to the next track on Spotify"""
    try:
        script = '''
        tell application "Spotify"
            next track
            delay 0.5
            return name of current track & " by " & artist of current track
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        return {"success": True, "now_playing": result.stdout.strip(), "message": "Skipped to next track"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_previous_track() -> dict:
    """Go back to the previous track on Spotify"""
    try:
        script = '''
        tell application "Spotify"
            previous track
            delay 0.5
            return name of current track & " by " & artist of current track
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        return {"success": True, "now_playing": result.stdout.strip(), "message": "Went to previous track"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_pause() -> dict:
    """Pause Spotify playback"""
    try:
        script = 'tell application "Spotify" to pause'
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "message": "Spotify paused"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_resume() -> dict:
    """Resume Spotify playback"""
    try:
        script = 'tell application "Spotify" to play'
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "message": "Spotify resumed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_toggle_playback() -> dict:
    """Toggle play/pause on Spotify"""
    try:
        script = 'tell application "Spotify" to playpause'
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "message": "Toggled Spotify playback"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_set_volume(volume: int) -> dict:
    """
    Set Spotify volume (0-100)
    
    Args:
        volume: Volume level 0-100
    """
    try:
        volume = max(0, min(100, volume))
        script = f'tell application "Spotify" to set sound volume to {volume}'
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "volume": volume, "message": f"Spotify volume set to {volume}%"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_get_volume() -> dict:
    """Get current Spotify volume"""
    try:
        script = 'tell application "Spotify" to return sound volume'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        volume = int(result.stdout.strip())
        return {"success": True, "volume": volume, "message": f"Spotify volume is {volume}%"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_toggle_shuffle() -> dict:
    """Toggle shuffle mode on Spotify"""
    try:
        script = '''
        tell application "Spotify"
            set shuffling to not shuffling
            return shuffling
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        is_shuffling = result.stdout.strip() == "true"
        return {"success": True, "shuffle": is_shuffling, "message": f"Shuffle {'enabled' if is_shuffling else 'disabled'}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_toggle_repeat() -> dict:
    """Toggle repeat mode on Spotify"""
    try:
        script = '''
        tell application "Spotify"
            set repeating to not repeating
            return repeating
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        is_repeating = result.stdout.strip() == "true"
        return {"success": True, "repeat": is_repeating, "message": f"Repeat {'enabled' if is_repeating else 'disabled'}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_play_artist(artist_name: str) -> dict:
    """
    Play music by a specific artist on Spotify
    
    Args:
        artist_name: Name of the artist
    """
    try:
        import time
        subprocess.run(['open', '-a', 'Spotify'], check=False)
        time.sleep(1)
        
        escaped = artist_name.replace('"', '\\"')
        script = f'''
        tell application "Spotify"
            activate
            play track "spotify:search:artist:{escaped}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "artist": artist_name, "message": f"Playing music by {artist_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_play_album(album_name: str, artist: str = "") -> dict:
    """
    Play a specific album on Spotify
    
    Args:
        album_name: Name of the album
        artist: Optional artist name for better matching
    """
    try:
        import time
        subprocess.run(['open', '-a', 'Spotify'], check=False)
        time.sleep(1)
        
        query = f"{album_name} {artist}".strip().replace('"', '\\"')
        script = f'''
        tell application "Spotify"
            activate
            play track "spotify:search:album:{query}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "album": album_name, "artist": artist, "message": f"Playing album {album_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_play_playlist(playlist_name: str) -> dict:
    """
    Play a playlist by name on Spotify
    
    Args:
        playlist_name: Name of the playlist to play
    """
    try:
        import time
        subprocess.run(['open', '-a', 'Spotify'], check=False)
        time.sleep(1)
        
        escaped = playlist_name.replace('"', '\\"')
        script = f'''
        tell application "Spotify"
            activate
            play track "spotify:search:playlist:{escaped}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "playlist": playlist_name, "message": f"Playing playlist {playlist_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_seek(position_seconds: int) -> dict:
    """
    Seek to a position in the current track
    
    Args:
        position_seconds: Position in seconds to seek to
    """
    try:
        script = f'tell application "Spotify" to set player position to {position_seconds}'
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        mins = position_seconds // 60
        secs = position_seconds % 60
        return {"success": True, "position": f"{mins}:{secs:02d}", "message": f"Seeked to {mins}:{secs:02d}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_get_status() -> dict:
    """Get full Spotify playback status including shuffle, repeat, volume"""
    try:
        script = '''
        tell application "Spotify"
            set playerState to player state as string
            set vol to sound volume
            set shuf to shuffling
            set rep to repeating
            if playerState is "playing" or playerState is "paused" then
                set trackName to name of current track
                set trackArtist to artist of current track
                return playerState & "|" & trackName & "|" & trackArtist & "|" & vol & "|" & shuf & "|" & rep
            else
                return playerState & "||||" & vol & "|" & shuf & "|" & rep
            end if
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        parts = result.stdout.strip().split("|")
        
        return {
            "success": True,
            "state": parts[0] if len(parts) > 0 else "unknown",
            "track": parts[1] if len(parts) > 1 and parts[1] else None,
            "artist": parts[2] if len(parts) > 2 and parts[2] else None,
            "volume": int(parts[3]) if len(parts) > 3 and parts[3] else 0,
            "shuffle": parts[4] == "true" if len(parts) > 4 else False,
            "repeat": parts[5] == "true" if len(parts) > 5 else False
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_play_genre(genre: str) -> dict:
    """
    Play music from a specific genre on Spotify
    
    Args:
        genre: Genre name (pop, rock, jazz, classical, hip-hop, etc.)
    """
    try:
        import time
        subprocess.run(['open', '-a', 'Spotify'], check=False)
        time.sleep(1)
        
        escaped = genre.replace('"', '\\"')
        script = f'''
        tell application "Spotify"
            activate
            play track "spotify:search:genre:{escaped}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "genre": genre, "message": f"Playing {genre} music"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotify_play_mood(mood: str) -> dict:
    """
    Play music matching a mood on Spotify
    
    Args:
        mood: Mood/vibe (chill, happy, sad, energetic, focus, sleep, workout, party)
    """
    try:
        import time
        subprocess.run(['open', '-a', 'Spotify'], check=False)
        time.sleep(1)
        
        # Map moods to search terms
        mood_map = {
            "chill": "chill vibes",
            "happy": "happy hits",
            "sad": "sad songs",
            "energetic": "energy boost",
            "focus": "deep focus",
            "sleep": "sleep sounds",
            "workout": "workout motivation",
            "party": "party hits",
            "relax": "relaxing music",
            "study": "study music",
            "morning": "morning motivation",
            "night": "late night vibes"
        }
        
        search_term = mood_map.get(mood.lower(), mood)
        escaped = search_term.replace('"', '\\"')
        
        script = f'''
        tell application "Spotify"
            activate
            play track "spotify:search:{escaped}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "mood": mood, "message": f"Playing {mood} music"}
    except Exception as e:
        return {"success": False, "error": str(e)}


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


# ==================== BROWSER TOOLS ====================

def browser_get_current_url(browser: str = "chrome") -> dict:
    """
    Get the URL of the current tab
    
    Args:
        browser: chrome, brave, safari, firefox, arc
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "firefox": "Firefox",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = 'tell application "Safari" to return URL of front document'
        else:
            script = f'tell application "{app_name}" to return URL of active tab of front window'
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        return {"success": True, "browser": app_name, "url": result.stdout.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_get_current_title(browser: str = "chrome") -> dict:
    """
    Get the title of the current tab
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = 'tell application "Safari" to return name of front document'
        else:
            script = f'tell application "{app_name}" to return title of active tab of front window'
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        return {"success": True, "browser": app_name, "title": result.stdout.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_get_all_tabs(browser: str = "chrome") -> dict:
    """
    Get list of all open tabs with their URLs and titles
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = '''
            tell application "Safari"
                set tabList to {}
                repeat with w in windows
                    repeat with t in tabs of w
                        set end of tabList to (name of t & "|" & URL of t)
                    end repeat
                end repeat
                return tabList
            end tell
            '''
        else:
            script = f'''
            tell application "{app_name}"
                set tabList to {{}}
                repeat with w in windows
                    repeat with t in tabs of w
                        set end of tabList to (title of t & "|" & URL of t)
                    end repeat
                end repeat
                return tabList
            end tell
            '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
        raw = result.stdout.strip()
        
        tabs = []
        if raw:
            for item in raw.split(", "):
                if "|" in item:
                    parts = item.split("|")
                    tabs.append({"title": parts[0], "url": parts[1] if len(parts) > 1 else ""})
        
        return {"success": True, "browser": app_name, "tab_count": len(tabs), "tabs": tabs}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_new_tab(url: str = "", browser: str = "chrome") -> dict:
    """
    Open a new tab, optionally with a URL
    
    Args:
        url: URL to open (empty for blank tab)
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if url:
            if app_name == "Safari":
                script = f'''
                tell application "Safari"
                    activate
                    tell front window to set current tab to (make new tab with properties {{URL:"{url}"}})
                end tell
                '''
            else:
                script = f'''
                tell application "{app_name}"
                    activate
                    tell front window to make new tab with properties {{URL:"{url}"}}
                end tell
                '''
        else:
            if app_name == "Safari":
                script = f'''
                tell application "Safari"
                    activate
                    tell front window to set current tab to (make new tab)
                end tell
                '''
            else:
                script = f'''
                tell application "{app_name}"
                    activate
                    tell front window to make new tab
                end tell
                '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "url": url or "blank", "message": f"New tab opened in {app_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_close_tab(browser: str = "chrome") -> dict:
    """
    Close the current tab
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = 'tell application "Safari" to close current tab of front window'
        else:
            script = f'tell application "{app_name}" to close active tab of front window'
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Tab closed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_close_all_tabs(browser: str = "chrome") -> dict:
    """
    Close all tabs in the browser
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = '''
            tell application "Safari"
                repeat with w in windows
                    close tabs of w
                end repeat
            end tell
            '''
        else:
            script = f'''
            tell application "{app_name}"
                repeat with w in windows
                    close tabs of w
                end repeat
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "All tabs closed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_refresh(browser: str = "chrome") -> dict:
    """
    Refresh the current tab
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        # Use keyboard shortcut Cmd+R
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "r" using command down
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Page refreshed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_go_back(browser: str = "chrome") -> dict:
    """
    Go back to previous page
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "[" using command down
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Went back"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_go_forward(browser: str = "chrome") -> dict:
    """
    Go forward to next page
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "]" using command down
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Went forward"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_switch_tab(tab_index: int, browser: str = "chrome") -> dict:
    """
    Switch to a specific tab by index (1-based)
    
    Args:
        tab_index: Tab number (1 for first tab)
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = f'''
            tell application "Safari"
                activate
                set current tab of front window to tab {tab_index} of front window
            end tell
            '''
        else:
            script = f'''
            tell application "{app_name}"
                activate
                set active tab index of front window to {tab_index}
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "tab": tab_index, "message": f"Switched to tab {tab_index}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_open_incognito(url: str = "", browser: str = "chrome") -> dict:
    """
    Open incognito/private window
    
    Args:
        url: Optional URL to open
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = '''
            tell application "Safari"
                activate
                tell application "System Events" to keystroke "n" using {command down, shift down}
            end tell
            '''
        else:
            # Chrome/Brave incognito
            script = f'''
            tell application "{app_name}"
                activate
                tell application "System Events" to keystroke "n" using {{command down, shift down}}
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        
        if url:
            import time
            time.sleep(0.5)
            script2 = f'''
            tell application "{app_name}"
                set URL of active tab of front window to "{url}"
            end tell
            '''
            subprocess.run(['osascript', '-e', script2], timeout=5)
        
        return {"success": True, "browser": app_name, "mode": "incognito/private", "url": url or "blank"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_search(query: str, browser: str = "chrome", engine: str = "google") -> dict:
    """
    Search using browser's search
    
    Args:
        query: Search query
        browser: chrome, brave, safari
        engine: google, bing, duckduckgo, youtube
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        # Search engine URLs
        engines = {
            "google": f"https://www.google.com/search?q={query.replace(' ', '+')}",
            "bing": f"https://www.bing.com/search?q={query.replace(' ', '+')}",
            "duckduckgo": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
            "ddg": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
            "youtube": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
            "yt": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
            "amazon": f"https://www.amazon.com/s?k={query.replace(' ', '+')}",
            "github": f"https://github.com/search?q={query.replace(' ', '+')}",
        }
        
        url = engines.get(engine.lower(), engines["google"])
        
        if app_name == "Safari":
            script = f'tell application "Safari" to open location "{url}"'
        else:
            script = f'tell application "{app_name}" to open location "{url}"'
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "engine": engine, "query": query, "url": url}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_zoom(direction: str, browser: str = "chrome") -> dict:
    """
    Zoom in or out on the page
    
    Args:
        direction: in, out, or reset
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if direction.lower() == "in":
            key = "+"
        elif direction.lower() == "out":
            key = "-"
        else:  # reset
            key = "0"
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "{key}" using command down
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "zoom": direction}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_find_on_page(text: str, browser: str = "chrome") -> dict:
    """
    Open find dialog and search for text on page
    
    Args:
        text: Text to find
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        escaped = text.replace('"', '\\"')
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events"
            keystroke "f" using command down
            delay 0.3
            keystroke "{escaped}"
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "searching_for": text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_bookmark_page(browser: str = "chrome") -> dict:
    """
    Bookmark the current page
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "d" using command down
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Bookmark dialog opened"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_open_devtools(browser: str = "chrome") -> dict:
    """
    Open developer tools
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            # Safari uses Cmd+Option+I
            script = '''
            tell application "Safari" to activate
            tell application "System Events" to keystroke "i" using {command down, option down}
            '''
        else:
            # Chrome/Brave use Cmd+Option+I or F12
            script = f'''
            tell application "{app_name}" to activate
            tell application "System Events" to keystroke "i" using {{command down, option down}}
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Developer tools opened"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_screenshot_page(filepath: str = "~/Desktop/screenshot.png", browser: str = "chrome") -> dict:
    """
    Take a screenshot of the current browser window
    
    Args:
        filepath: Where to save the screenshot
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        expanded_path = os.path.expanduser(filepath)
        
        # Get window ID and capture
        script = f'''
        tell application "{app_name}"
            activate
            set windowID to id of front window
        end tell
        return windowID
        '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        window_id = result.stdout.strip()
        
        # Use screencapture
        subprocess.run(['screencapture', '-l', window_id, expanded_path], check=True, timeout=10)
        
        return {"success": True, "browser": app_name, "filepath": expanded_path, "message": "Screenshot saved"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_open_multiple_urls(urls: list, browser: str = "chrome") -> dict:
    """
    Open multiple URLs in new tabs
    
    Args:
        urls: List of URLs to open
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari",
            "arc": "Arc"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        opened = []
        for url in urls:
            if app_name == "Safari":
                script = f'''
                tell application "Safari"
                    activate
                    tell front window to make new tab with properties {{URL:"{url}"}}
                end tell
                '''
            else:
                script = f'''
                tell application "{app_name}"
                    activate
                    tell front window to make new tab with properties {{URL:"{url}"}}
                end tell
                '''
            subprocess.run(['osascript', '-e', script], timeout=5)
            opened.append(url)
        
        return {"success": True, "browser": app_name, "urls_opened": len(opened), "urls": opened}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_duplicate_tab(browser: str = "chrome") -> dict:
    """
    Duplicate the current tab
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        # Get current URL and open in new tab
        if app_name == "Safari":
            script = '''
            tell application "Safari"
                set currentURL to URL of front document
                tell front window to make new tab with properties {URL:currentURL}
            end tell
            '''
        else:
            script = f'''
            tell application "{app_name}"
                set currentURL to URL of active tab of front window
                tell front window to make new tab with properties {{URL:currentURL}}
            end tell
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Tab duplicated"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_mute_tab(browser: str = "chrome") -> dict:
    """
    Mute the current tab
    
    Args:
        browser: chrome, brave
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        # Right-click tab and mute (using keyboard shortcut for Chrome)
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "m" using {{control down, shift down}}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Tab mute toggled"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_pin_tab(browser: str = "chrome") -> dict:
    """
    Pin the current tab
    
    Args:
        browser: chrome, brave
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        # Use menu to pin tab
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events"
            click menu item "Pin Tab" of menu "Tab" of menu bar 1 of process "{app_name}"
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Tab pinned"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_clear_history(browser: str = "chrome") -> dict:
    """
    Open clear browsing data dialog
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = '''
            tell application "Safari" to activate
            tell application "System Events"
                click menu item "Clear History…" of menu "History" of menu bar 1 of process "Safari"
            end tell
            '''
        else:
            # Chrome/Brave: Cmd+Shift+Delete
            script = f'''
            tell application "{app_name}" to activate
            tell application "System Events" to keystroke (ASCII character 8) using {{command down, shift down}}
            '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Clear history dialog opened"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_view_source(browser: str = "chrome") -> dict:
    """
    View page source code
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "u" using {{command down, option down}}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Viewing page source"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_print_page(browser: str = "chrome") -> dict:
    """
    Open print dialog for current page
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "p" using command down
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Print dialog opened"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_fullscreen(browser: str = "chrome") -> dict:
    """
    Toggle fullscreen mode
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "f" using {{command down, control down}}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Fullscreen toggled"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_next_tab(browser: str = "chrome") -> dict:
    """
    Switch to next tab
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke tab using {{control down}}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Switched to next tab"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_previous_tab(browser: str = "chrome") -> dict:
    """
    Switch to previous tab
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke tab using {{control down, shift down}}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Switched to previous tab"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_reopen_closed_tab(browser: str = "chrome") -> dict:
    """
    Reopen the last closed tab
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "t" using {{command down, shift down}}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Reopened last closed tab"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_reading_mode(browser: str = "safari") -> dict:
    """
    Toggle reading mode (Safari Reader)
    
    Args:
        browser: safari (only Safari supports this natively)
    """
    try:
        script = '''
        tell application "Safari" to activate
        tell application "System Events" to keystroke "r" using {command down, shift down}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": "Safari", "message": "Reading mode toggled"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_save_page(filepath: str = "~/Desktop/page.html", browser: str = "chrome") -> dict:
    """
    Save the current page
    
    Args:
        filepath: Where to save
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to keystroke "s" using command down
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "message": "Save dialog opened"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_get_tab_count(browser: str = "chrome") -> dict:
    """
    Get the number of open tabs
    
    Args:
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        if app_name == "Safari":
            script = '''
            tell application "Safari"
                set tabCount to 0
                repeat with w in windows
                    set tabCount to tabCount + (count of tabs of w)
                end repeat
                return tabCount
            end tell
            '''
        else:
            script = f'''
            tell application "{app_name}"
                set tabCount to 0
                repeat with w in windows
                    set tabCount to tabCount + (count of tabs of w)
                end repeat
                return tabCount
            end tell
            '''
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        count = int(result.stdout.strip())
        return {"success": True, "browser": app_name, "tab_count": count}
    except Exception as e:
        return {"success": False, "error": str(e)}


def browser_scroll(direction: str, amount: str = "page", browser: str = "chrome") -> dict:
    """
    Scroll the page
    
    Args:
        direction: up, down, top, bottom
        amount: page, half, or pixels
        browser: chrome, brave, safari
    """
    try:
        browser_apps = {
            "chrome": "Google Chrome",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        app_name = browser_apps.get(browser.lower(), browser)
        
        direction = direction.lower()
        
        if direction == "top":
            key_script = 'keystroke (ASCII character 1) using command down'  # Cmd+Home
        elif direction == "bottom":
            key_script = 'keystroke (ASCII character 4) using command down'  # Cmd+End
        elif direction == "down":
            if amount == "page":
                key_script = 'key code 121'  # Page Down
            else:
                key_script = 'key code 125'  # Down Arrow
        else:  # up
            if amount == "page":
                key_script = 'key code 116'  # Page Up
            else:
                key_script = 'key code 126'  # Up Arrow
        
        script = f'''
        tell application "{app_name}" to activate
        tell application "System Events" to {key_script}
        '''
        
        subprocess.run(['osascript', '-e', script], check=True, timeout=5)
        return {"success": True, "browser": app_name, "scrolled": direction}
    except Exception as e:
        return {"success": False, "error": str(e)}


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

