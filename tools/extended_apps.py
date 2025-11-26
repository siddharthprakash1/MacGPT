"""
Extended App Support
Chrome, Brave, VS Code, Zoom, Slack, etc.
"""

import subprocess
import os
from typing import Optional


# ==================== CHROME/BRAVE ====================

def chrome_open_url(url: str, browser: str = "Google Chrome") -> dict:
    """
    Open URL in Chrome or Brave
    
    Args:
        url: URL to open
        browser: "Google Chrome" or "Brave Browser"
    
    Returns:
        dict: Result
    """
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        script = f'''
        tell application "{browser}"
            activate
            tell window 1
                set current tab to (make new tab with properties {{URL:"{url}"}})
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "url": url,
            "browser": browser,
            "message": f"Opened {url} in {browser}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def chrome_get_current_url(browser: str = "Google Chrome") -> dict:
    """Get current URL from Chrome/Brave"""
    try:
        script = f'''
        tell application "{browser}"
            return URL of active tab of window 1
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, check=True, timeout=2)
        return {
            "success": True,
            "url": result.stdout.strip(),
            "browser": browser
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def chrome_close_tabs(browser: str = "Google Chrome") -> dict:
    """Close all Chrome/Brave tabs"""
    try:
        script = f'''
        tell application "{browser}"
            close every tab of every window
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "browser": browser,
            "message": f"Closed all tabs in {browser}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== VS CODE ====================

def vscode_open_file(file_path: str) -> dict:
    """
    Open file in VS Code
    
    Args:
        file_path: Path to file or directory
    
    Returns:
        dict: Result
    """
    try:
        subprocess.run(['code', file_path], check=True, timeout=3)
        return {
            "success": True,
            "file": file_path,
            "message": f"Opened {file_path} in VS Code"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def vscode_open_workspace(workspace_path: str) -> dict:
    """Open workspace in VS Code"""
    try:
        subprocess.run(['code', workspace_path], check=True, timeout=3)
        return {
            "success": True,
            "workspace": workspace_path,
            "message": f"Opened workspace in VS Code"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== SLACK ====================

def open_slack_channel(channel_name: str) -> dict:
    """
    Open Slack channel
    
    Args:
        channel_name: Channel name (e.g., "general")
    
    Returns:
        dict: Result
    """
    try:
        # Slack deep link
        url = f"slack://channel?team=T1234567&id={channel_name}"
        subprocess.run(['open', url], check=True, timeout=2)
        return {
            "success": True,
            "channel": channel_name,
            "message": f"Opening Slack channel: {channel_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_slack_dm(user_name: str) -> dict:
    """Open Slack DM with user"""
    try:
        script = f'''
        tell application "Slack"
            activate
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=2)
        return {
            "success": True,
            "user": user_name,
            "message": "Opened Slack (search for user manually)"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== ZOOM ====================

def start_zoom_meeting(meeting_id: Optional[str] = None) -> dict:
    """
    Start or join Zoom meeting
    
    Args:
        meeting_id: Meeting ID (optional)
    
    Returns:
        dict: Result
    """
    try:
        if meeting_id:
            url = f"zoommtg://zoom.us/join?confno={meeting_id}"
            subprocess.run(['open', url], check=True, timeout=2)
            return {
                "success": True,
                "meeting_id": meeting_id,
                "message": f"Joining Zoom meeting: {meeting_id}"
            }
        else:
            subprocess.run(['open', '-a', 'zoom.us'], check=True, timeout=2)
            return {
                "success": True,
                "message": "Opened Zoom"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== TERMINAL ====================

def open_terminal_command(command: str, new_window: bool = True) -> dict:
    """
    Open Terminal and run command
    
    Args:
        command: Command to run
        new_window: Open in new window
    
    Returns:
        dict: Result
    """
    try:
        script = f'''
        tell application "Terminal"
            activate
            {'do script "' + command + '"' if new_window else 'do script "' + command + '" in front window'}
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True, timeout=3)
        return {
            "success": True,
            "command": command,
            "message": f"Opened Terminal and ran: {command}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== DOCKER ====================

def docker_ps() -> dict:
    """List running Docker containers"""
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'],
                              capture_output=True, text=True, check=True, timeout=5)
        return {
            "success": True,
            "containers": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def docker_start_container(container_name: str) -> dict:
    """Start Docker container"""
    try:
        subprocess.run(['docker', 'start', container_name], check=True, timeout=5)
        return {
            "success": True,
            "container": container_name,
            "message": f"Started container: {container_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def docker_stop_container(container_name: str) -> dict:
    """Stop Docker container"""
    try:
        subprocess.run(['docker', 'stop', container_name], check=True, timeout=10)
        return {
            "success": True,
            "container": container_name,
            "message": f"Stopped container: {container_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== GIT ====================

def git_status(repo_path: str = ".") -> dict:
    """Get git status of repository"""
    try:
        result = subprocess.run(['git', '-C', repo_path, 'status', '--short'],
                              capture_output=True, text=True, check=True, timeout=3)
        return {
            "success": True,
            "repo": repo_path,
            "status": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def git_pull(repo_path: str = ".") -> dict:
    """Git pull in repository"""
    try:
        result = subprocess.run(['git', '-C', repo_path, 'pull'],
                              capture_output=True, text=True, check=True, timeout=10)
        return {
            "success": True,
            "repo": repo_path,
            "output": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def git_commit(repo_path: str, message: str) -> dict:
    """Git commit all changes"""
    try:
        subprocess.run(['git', '-C', repo_path, 'add', '.'], check=True, timeout=3)
        subprocess.run(['git', '-C', repo_path, 'commit', '-m', message], 
                      check=True, timeout=3)
        return {
            "success": True,
            "repo": repo_path,
            "message": f"Committed: {message}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== PRODUCTIVITY ====================

def pomodoro_timer(work_minutes: int = 25, break_minutes: int = 5) -> dict:
    """
    Start Pomodoro timer
    
    Args:
        work_minutes: Work duration
        break_minutes: Break duration
    
    Returns:
        dict: Result
    """
    try:
        work_seconds = work_minutes * 60
        break_seconds = break_minutes * 60
        
        script = f'''
        delay {work_seconds}
        display notification "Time for a {break_minutes} minute break!" with title "Pomodoro" sound name "Glass"
        delay {break_seconds}
        display notification "Break over! Back to work." with title "Pomodoro" sound name "Glass"
        '''
        subprocess.Popen(['osascript', '-e', script])
        
        return {
            "success": True,
            "work_minutes": work_minutes,
            "break_minutes": break_minutes,
            "message": f"Pomodoro timer started: {work_minutes}min work, {break_minutes}min break"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def take_break_reminder(minutes: int = 60) -> dict:
    """Set break reminder"""
    try:
        seconds = minutes * 60
        script = f'''
        delay {seconds}
        display notification "Time to take a break and stretch!" with title "Health Reminder" sound name "Glass"
        '''
        subprocess.Popen(['osascript', '-e', script])
        
        return {
            "success": True,
            "minutes": minutes,
            "message": f"Break reminder set for {minutes} minutes"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== DOWNLOAD/FILE MANAGEMENT ====================

def open_downloads_folder() -> dict:
    """Open Downloads folder in Finder"""
    try:
        downloads_path = os.path.expanduser("~/Downloads")
        subprocess.run(['open', downloads_path], check=True, timeout=2)
        return {
            "success": True,
            "path": downloads_path,
            "message": "Opened Downloads folder"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_desktop() -> dict:
    """Open Desktop in Finder"""
    try:
        desktop_path = os.path.expanduser("~/Desktop")
        subprocess.run(['open', desktop_path], check=True, timeout=2)
        return {
            "success": True,
            "path": desktop_path,
            "message": "Opened Desktop"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_disk_usage() -> dict:
    """Get disk usage information"""
    try:
        result = subprocess.run(['df', '-h', '/'],
                              capture_output=True, text=True, check=True, timeout=2)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            return {
                "success": True,
                "total": parts[1],
                "used": parts[2],
                "available": parts[3],
                "percent": parts[4]
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

