"""
Smart Helper Functions
Handles common app aliases, YouTube searches, and intelligent automation
"""

import subprocess
import urllib.parse
from typing import Optional, Dict


# Common application name aliases
APP_ALIASES = {
    # Browsers
    "brave": "Brave Browser",
    "chrome": "Google Chrome",
    "firefox": "Firefox",
    "safari": "Safari",
    "edge": "Microsoft Edge",
    "opera": "Opera",
    
    # Development
    "vscode": "Visual Studio Code",
    "vs code": "Visual Studio Code",
    "code": "Visual Studio Code",
    "pycharm": "PyCharm",
    "intellij": "IntelliJ IDEA",
    "sublime": "Sublime Text",
    "atom": "Atom",
    "xcode": "Xcode",
    "terminal": "Terminal",
    "iterm": "iTerm",
    
    # Productivity
    "slack": "Slack",
    "discord": "Discord",
    "zoom": "zoom.us",
    "teams": "Microsoft Teams",
    "notes": "Notes",
    "mail": "Mail",
    "calendar": "Calendar",
    "reminders": "Reminders",
    "messages": "Messages",
    
    # Media
    "spotify": "Spotify",
    "music": "Music",
    "itunes": "Music",
    "vlc": "VLC",
    "quicktime": "QuickTime Player",
    
    # Other
    "finder": "Finder",
    "preview": "Preview",
    "photos": "Photos",
    "word": "Microsoft Word",
    "excel": "Microsoft Excel",
    "powerpoint": "Microsoft PowerPoint",
    "keynote": "Keynote",
    "pages": "Pages",
    "numbers": "Numbers"
}


def resolve_app_name(app_name: str) -> str:
    """
    Resolve app name aliases to actual macOS application names
    
    Args:
        app_name: User-provided app name (e.g., "brave", "vscode")
    
    Returns:
        str: Actual macOS application name
    """
    # Try exact match first
    app_lower = app_name.lower().strip()
    if app_lower in APP_ALIASES:
        return APP_ALIASES[app_lower]
    
    # Return original if no alias found
    return app_name


def open_application_smart(app_name: str) -> dict:
    """
    Open application with smart name resolution
    
    Args:
        app_name: Application name (supports aliases)
    
    Returns:
        dict: Result with success status
    """
    resolved_name = resolve_app_name(app_name)
    
    try:
        subprocess.run(['open', '-a', resolved_name], check=True)
        
        message = f"Opened {resolved_name}"
        if resolved_name != app_name:
            message += f" (resolved from '{app_name}')"
        
        return {
            "success": True,
            "application": resolved_name,
            "original_name": app_name,
            "message": message
        }
    except subprocess.CalledProcessError as e:
        # Try to get list of available apps
        return {
            "success": False,
            "error": f"Could not find application '{resolved_name}'",
            "tried_name": resolved_name,
            "original_request": app_name,
            "suggestion": "Try: 'list_running_apps' to see available applications"
        }


def open_youtube_video(query: str, browser: str = "default") -> dict:
    """
    Open a YouTube search or video
    
    Args:
        query: Search query or video title
        browser: Browser to use (default, brave, chrome, safari, etc.)
    
    Returns:
        dict: Result with success status
    """
    try:
        # Create YouTube search URL
        encoded_query = urllib.parse.quote(query)
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        # Resolve browser name
        if browser != "default":
            resolved_browser = resolve_app_name(browser)
            subprocess.run(['open', '-a', resolved_browser, youtube_url], check=True)
            browser_used = resolved_browser
        else:
            subprocess.run(['open', youtube_url], check=True)
            browser_used = "default browser"
        
        return {
            "success": True,
            "query": query,
            "url": youtube_url,
            "browser": browser_used,
            "message": f"Opened YouTube search for '{query}' in {browser_used}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def open_url_smart(url: str, browser: str = "default", search_youtube: bool = False) -> dict:
    """
    Smart URL opening with browser resolution and YouTube support
    
    Args:
        url: URL to open or search query (if search_youtube=True)
        browser: Browser name (supports aliases)
        search_youtube: If True, treats url as YouTube search query
    
    Returns:
        dict: Result with success status
    """
    try:
        # Handle YouTube search
        if search_youtube:
            return open_youtube_video(url, browser)
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://', 'file://')):
            url = 'https://' + url
        
        # Open with specified browser
        if browser != "default":
            resolved_browser = resolve_app_name(browser)
            subprocess.run(['open', '-a', resolved_browser, url], check=True)
            browser_used = resolved_browser
        else:
            subprocess.run(['open', url], check=True)
            browser_used = "default browser"
        
        return {
            "success": True,
            "url": url,
            "browser": browser_used,
            "message": f"Opened {url} in {browser_used}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_available_apps() -> dict:
    """
    Get list of installed applications
    
    Returns:
        dict: List of installed applications
    """
    try:
        # Get apps from /Applications
        result = subprocess.run(
            ['ls', '/Applications'],
            capture_output=True,
            text=True,
            check=True
        )
        
        apps = []
        for line in result.stdout.split('\n'):
            if line.endswith('.app'):
                app_name = line.replace('.app', '')
                apps.append(app_name)
        
        # Also check ~/Applications
        try:
            user_result = subprocess.run(
                ['ls', os.path.expanduser('~/Applications')],
                capture_output=True,
                text=True,
                check=False
            )
            for line in user_result.stdout.split('\n'):
                if line.endswith('.app'):
                    app_name = line.replace('.app', '')
                    if app_name not in apps:
                        apps.append(app_name)
        except:
            pass
        
        return {
            "success": True,
            "count": len(apps),
            "applications": sorted(apps),
            "common_aliases": list(APP_ALIASES.keys())
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def smart_search(query: str, search_type: str = "google") -> dict:
    """
    Smart search across different platforms
    
    Args:
        query: Search query
        search_type: google, youtube, github, stackoverflow, etc.
    
    Returns:
        dict: Result with success status
    """
    try:
        encoded_query = urllib.parse.quote(query)
        
        urls = {
            "google": f"https://www.google.com/search?q={encoded_query}",
            "youtube": f"https://www.youtube.com/results?search_query={encoded_query}",
            "github": f"https://github.com/search?q={encoded_query}",
            "stackoverflow": f"https://stackoverflow.com/search?q={encoded_query}",
            "reddit": f"https://www.reddit.com/search/?q={encoded_query}",
            "twitter": f"https://twitter.com/search?q={encoded_query}",
            "wikipedia": f"https://en.wikipedia.org/wiki/Special:Search?search={encoded_query}",
            "maps": f"https://www.google.com/maps/search/{encoded_query}"
        }
        
        url = urls.get(search_type.lower(), urls["google"])
        subprocess.run(['open', url], check=True)
        
        return {
            "success": True,
            "query": query,
            "search_type": search_type,
            "url": url,
            "message": f"Opened {search_type} search for '{query}'"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


import os  # Need this for expanduser

