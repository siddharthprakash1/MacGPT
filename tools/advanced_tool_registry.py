"""
Advanced Tool Registry
Definitions for all advanced macOS tools
"""

from tools.advanced_tools import (
    read_file, write_file, list_files, create_directory,
    close_application, list_running_apps,
    create_note, search_notes,
    create_reminder,
    list_processes, kill_process,
    get_network_info,
    control_music, get_current_song, play_spotify_track,
    run_shell_command
)

from tools.smart_helpers import (
    open_application_smart,
    open_youtube_video,
    open_url_smart,
    get_available_apps,
    smart_search
)

from tools.quick_tools import (
    quick_find_file,
    set_volume,
    set_brightness,
    open_finder_location,
    empty_trash,
    toggle_wifi,
    lock_screen,
    sleep_computer,
    toggle_dark_mode,
    get_battery_status
)

from tools.app_integrations import (
    safari_open_url,
    safari_close_tabs,
    safari_get_current_url,
    send_imessage,
    send_email,
    create_calendar_event,
    finder_search,
    get_selected_files,
    toggle_bluetooth,
    set_wallpaper,
    enable_focus_mode,
    quick_timer,
    show_notification_with_sound
)

from tools.extended_apps import (
    chrome_open_url,
    chrome_get_current_url,
    chrome_close_tabs,
    vscode_open_file,
    vscode_open_workspace,
    open_slack_channel,
    open_slack_dm,
    start_zoom_meeting,
    open_terminal_command,
    docker_ps,
    docker_start_container,
    docker_stop_container,
    git_status,
    git_pull,
    git_commit,
    pomodoro_timer,
    take_break_reminder,
    open_downloads_folder,
    open_desktop,
    get_disk_usage
)

# NEW POWER TOOLS!
from tools.window_management import (
    snap_window_left,
    snap_window_right,
    snap_side_by_side,
    snap_to_display,
    get_display_bounds,
    maximize_window,
    center_window,
    resize_window,
    move_window,
    list_all_windows,
    minimize_window,
    bring_to_front
)

from tools.file_operations import (
    compress_files,
    extract_archive,
    move_file,
    copy_file,
    rename_file,
    duplicate_file,
    get_file_info,
    bulk_rename,
    delete_file,
    find_files_by_extension
)

from tools.clipboard_advanced import (
    clipboard_get_history,
    clipboard_restore_from_history,
    clipboard_save_image,
    clipboard_append,
    clipboard_clear,
    clipboard_get_type,
    clipboard_count_words
)

from tools.screen_media import (
    start_screen_recording,
    stop_screen_recording,
    record_audio,
    resize_image,
    convert_image_format,
    compress_image,
    get_image_info,
    create_thumbnail,
    convert_video_format
)

from tools.display_control import (
    toggle_night_shift,
    start_screen_saver,
    list_displays,
    set_display_resolution,
    mirror_displays,
    get_display_info
)

from tools.package_manager import (
    brew_install,
    brew_uninstall,
    brew_update,
    brew_upgrade,
    brew_list,
    brew_search,
    brew_info,
    npm_install_global,
    npm_uninstall_global,
    npm_list_global,
    npm_update_global,
    pip_install,
    pip_uninstall,
    pip_list,
    pip_outdated
)

# Keyboard/mouse tools removed - they were gimmicky

# NEW SPOTLIGHT POWER TOOLS!
from tools.spotlight_tools import (
    spotlight_advanced_search,
    find_files_by_date,
    find_large_files,
    find_by_content,
    find_by_author,
    find_downloads_from_site,
    find_recent_opened,
    get_file_metadata,
    find_duplicates_by_name,
    spotlight_natural_search,
    find_apps_using_disk_space,
    find_unused_apps
)

from tools.backup_tools import (
    time_machine_status,
    start_time_machine_backup,
    stop_time_machine_backup,
    list_time_machine_backups,
    get_latest_backup,
    enable_time_machine,
    disable_time_machine,
    get_backup_destination
)

from tools.airdrop_handoff import (
    airdrop_send,
    open_airdrop_window,
    get_airdrop_status,
    handoff_url_to_device,
    open_continuity_settings,
    share_text_via_airdrop
)

from tools.database_tools import (
    postgres_query,
    mysql_query,
    mongodb_find,
    mongodb_insert,
    redis_get,
    redis_set,
    redis_delete,
    redis_keys,
    postgres_list_databases,
    mysql_list_databases,
    mongodb_list_collections
)

from tools.web_tools import (
    download_file,
    check_website_status,
    web_scrape,
    get_page_title,
    get_page_links,
    shorten_url,
    generate_qr_code,
    get_ip_info,
    ping_host,
    trace_route,
    dns_lookup,
    whois_lookup,
    test_download_speed,
    test_upload_speed
)

WORKFLOW_TOOLS = {}


ADVANCED_TOOLS = {
    # FILE OPERATIONS
    "read_file": {
        "description": "Read contents of a file from the filesystem",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file to read"
                },
                "lines": {
                    "type": "integer",
                    "description": "Number of lines to read (optional, reads all if not specified)"
                }
            },
            "required": ["filepath"]
        },
        "function": read_file
    },
    
    "write_file": {
        "description": "Write content to a file (creates file if it doesn't exist)",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write"
                },
                "mode": {
                    "type": "string",
                    "enum": ["overwrite", "append"],
                    "description": "Write mode: overwrite or append"
                }
            },
            "required": ["filepath", "content"]
        },
        "function": write_file
    },
    
    "list_files": {
        "description": "List files in a directory with optional pattern matching",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path"
                },
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern (e.g., '*.py', '*.txt')"
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Search recursively in subdirectories"
                }
            },
            "required": ["directory"]
        },
        "function": list_files
    },
    
    "create_directory": {
        "description": "Create a new directory (including parent directories if needed)",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to create"
                }
            },
            "required": ["directory"]
        },
        "function": create_directory
    },
    
    # APPLICATION CONTROL
    "open_application": {
        "description": "Open a macOS application. Supports aliases like 'brave', 'vscode', 'chrome', 'spotify'. Smart name resolution!",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "Application name or alias (e.g., 'Safari', 'brave', 'vscode', 'spotify')"
                }
            },
            "required": ["app_name"]
        },
        "function": open_application_smart
    },
    
    "close_application": {
        "description": "Close a running macOS application",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "Application name"
                },
                "force": {
                    "type": "boolean",
                    "description": "Force quit the application"
                }
            },
            "required": ["app_name"]
        },
        "function": close_application
    },
    
    "list_running_apps": {
        "description": "Get a list of all currently running applications",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": list_running_apps
    },
    
    "get_available_apps": {
        "description": "Get a list of all installed applications on the system",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": get_available_apps
    },
    
    # APPLE NOTES
    "create_note": {
        "description": "Create a new note in Apple Notes app",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Note title"
                },
                "content": {
                    "type": "string",
                    "description": "Note content"
                },
                "folder": {
                    "type": "string",
                    "description": "Folder name (default: Notes)"
                }
            },
            "required": ["title", "content"]
        },
        "function": create_note
    },
    
    "search_notes": {
        "description": "Search for notes in Apple Notes",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results"
                }
            },
            "required": ["query"]
        },
        "function": search_notes
    },
    
    # REMINDERS
    "create_reminder": {
        "description": "Create a reminder in Apple Reminders app",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Reminder title"
                },
                "list_name": {
                    "type": "string",
                    "description": "List name (default: Reminders)"
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date (format: 'YYYY-MM-DD HH:MM')"
                }
            },
            "required": ["title"]
        },
        "function": create_reminder
    },
    
    # PROCESS MANAGEMENT
    "list_processes": {
        "description": "List running system processes with CPU and memory usage",
        "parameters": {
            "type": "object",
            "properties": {
                "filter_name": {
                    "type": "string",
                    "description": "Filter by process name (optional)"
                }
            },
            "required": []
        },
        "function": list_processes
    },
    
    "kill_process": {
        "description": "Terminate a process by PID (use with caution!)",
        "parameters": {
            "type": "object",
            "properties": {
                "pid": {
                    "type": "integer",
                    "description": "Process ID"
                },
                "force": {
                    "type": "boolean",
                    "description": "Force kill (SIGKILL) vs graceful (SIGTERM)"
                }
            },
            "required": ["pid"]
        },
        "function": kill_process
    },
    
    # WEB & NETWORK
    "open_url": {
        "description": "Open a URL in browser. Supports browser aliases like 'brave', 'chrome', 'safari'. Auto-adds https:// if needed.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to open (e.g., 'google.com', 'github.com')"
                },
                "browser": {
                    "type": "string",
                    "description": "Browser name or alias (default, brave, chrome, safari, firefox)"
                }
            },
            "required": ["url"]
        },
        "function": open_url_smart
    },
    
    "open_youtube": {
        "description": "Search and open YouTube videos. Opens YouTube search results for the query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Video title or search query (e.g., 'Nah by Khalid')"
                },
                "browser": {
                    "type": "string",
                    "description": "Browser to use (default, brave, chrome, safari)"
                }
            },
            "required": ["query"]
        },
        "function": open_youtube_video
    },
    
    "smart_search": {
        "description": "Search across different platforms (Google, YouTube, GitHub, StackOverflow, Reddit, Wikipedia, Maps)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "search_type": {
                    "type": "string",
                    "enum": ["google", "youtube", "github", "stackoverflow", "reddit", "twitter", "wikipedia", "maps"],
                    "description": "Platform to search"
                }
            },
            "required": ["query"]
        },
        "function": smart_search
    },
    
    "get_network_info": {
        "description": "Get current network information (WiFi name, IP address)",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": get_network_info
    },
    
    # MUSIC CONTROL
    "control_music": {
        "description": "Control Apple Music or Spotify playback",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["play", "pause", "next", "previous", "stop"],
                    "description": "Playback action"
                }
            },
            "required": ["action"]
        },
        "function": control_music
    },
    
    "get_current_song": {
        "description": "Get information about the currently playing song",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": get_current_song
    },
    
    "play_spotify_track": {
        "description": "Search and play a specific song on Spotify (opens Spotify and plays the track)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Song name or 'artist - song' to search and play"
                }
            },
            "required": ["query"]
        },
        "function": play_spotify_track
    },
    
    # SHELL COMMANDS
    "run_shell_command": {
        "description": "Execute a shell command (use with extreme caution!)",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default: 30)"
                }
            },
            "required": ["command"]
        },
        "function": run_shell_command
    },
    
    # QUICK TOOLS (Fast like Siri)
    "quick_find_file": {
        "description": "FAST file search using Spotlight (instant, better than find command)",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "File name to search for"
                }
            },
            "required": ["filename"]
        },
        "function": quick_find_file
    },
    
    "set_volume": {
        "description": "Set system volume (0-100)",
        "parameters": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "integer",
                    "description": "Volume level 0-100"
                }
            },
            "required": ["level"]
        },
        "function": set_volume
    },
    
    "set_brightness": {
        "description": "Set screen brightness (0-100)",
        "parameters": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "integer",
                    "description": "Brightness level 0-100"
                }
            },
            "required": ["level"]
        },
        "function": set_brightness
    },
    
    "open_finder_location": {
        "description": "Open Finder at a specific folder location",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path (default: home ~)"
                }
            },
            "required": []
        },
        "function": open_finder_location
    },
    
    "empty_trash": {
        "description": "Empty the Trash",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": empty_trash
    },
    
    "toggle_wifi": {
        "description": "Turn WiFi on or off",
        "parameters": {
            "type": "object",
            "properties": {
                "state": {
                    "type": "string",
                    "enum": ["on", "off", "toggle"],
                    "description": "WiFi state"
                }
            },
            "required": ["state"]
        },
        "function": toggle_wifi
    },
    
    "lock_screen": {
        "description": "Lock the screen immediately",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": lock_screen
    },
    
    "sleep_computer": {
        "description": "Put the computer to sleep",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": sleep_computer
    },
    
    "toggle_dark_mode": {
        "description": "Toggle dark mode on/off",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": toggle_dark_mode
    },
    
    "get_battery_status": {
        "description": "Get battery information (percentage, charging status)",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": get_battery_status
    },
    
    # ========== SPOTLIGHT POWER TOOLS (12 tools) ==========
    "spotlight_advanced_search": {
        "description": "Advanced Spotlight search with filters for type, date, size, and folder. Much more powerful than basic find.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query (filename or content)"},
                "kind": {"type": "string", "enum": ["pdf", "image", "video", "audio", "document", "folder", "app", "email", "presentation", "spreadsheet", "code"], "description": "File type filter"},
                "in_folder": {"type": "string", "description": "Limit to folder (e.g., ~/Downloads)"},
                "date_filter": {"type": "string", "description": "today, yesterday, week, month, year, or YYYY-MM-DD"},
                "size_filter": {"type": "string", "enum": ["large", "medium", "small"], "description": "Size filter (large >100MB, medium 10-100MB, small <10MB)"},
                "limit": {"type": "integer", "description": "Max results (default 20)"}
            },
            "required": []
        },
        "function": spotlight_advanced_search
    },
    
    "find_files_by_date": {
        "description": "Find files by creation or modification date - perfect for 'files from last week'",
        "parameters": {
            "type": "object",
            "properties": {
                "date_range": {"type": "string", "description": "today, yesterday, week, month, year"},
                "file_type": {"type": "string", "description": "Optional: pdf, image, video, audio"},
                "in_folder": {"type": "string", "description": "Limit to folder"},
                "limit": {"type": "integer", "description": "Max results"}
            },
            "required": ["date_range"]
        },
        "function": find_files_by_date
    },
    
    "find_large_files": {
        "description": "Find large files for disk cleanup - shows files above a size threshold with total space used. Essential for freeing disk space!",
        "parameters": {
            "type": "object",
            "properties": {
                "min_size_mb": {"type": "integer", "description": "Minimum file size in MB (default 100)"},
                "in_folder": {"type": "string", "description": "Folder to search (default: home)"},
                "file_type": {"type": "string", "enum": ["video", "image", "archive", "disk_image", "audio"], "description": "Limit to file type"},
                "limit": {"type": "integer", "description": "Max results (default 30)"}
            },
            "required": []
        },
        "function": find_large_files
    },
    
    "find_by_content": {
        "description": "Full-text search INSIDE files - find documents containing specific text",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to search for inside files"},
                "file_type": {"type": "string", "description": "pdf, document, email, note"},
                "in_folder": {"type": "string", "description": "Limit to folder"},
                "limit": {"type": "integer", "description": "Max results"}
            },
            "required": ["text"]
        },
        "function": find_by_content
    },
    
    "find_by_author": {
        "description": "Find documents by author name (useful for finding all docs from a specific person)",
        "parameters": {
            "type": "object",
            "properties": {
                "author": {"type": "string", "description": "Author name to search for"},
                "in_folder": {"type": "string", "description": "Limit to folder"},
                "limit": {"type": "integer", "description": "Max results"}
            },
            "required": ["author"]
        },
        "function": find_by_author
    },
    
    "find_downloads_from_site": {
        "description": "Find files downloaded from a specific website - great for finding files from GitHub, Google Drive, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain name (e.g., 'github.com', 'google.com')"},
                "limit": {"type": "integer", "description": "Max results"}
            },
            "required": ["domain"]
        },
        "function": find_downloads_from_site
    },
    
    "find_recent_opened": {
        "description": "Find recently opened files - see what you worked on recently",
        "parameters": {
            "type": "object",
            "properties": {
                "hours": {"type": "integer", "description": "Within last N hours (default 24)"},
                "file_type": {"type": "string", "description": "pdf, image, video, document, code"},
                "limit": {"type": "integer", "description": "Max results"}
            },
            "required": []
        },
        "function": find_recent_opened
    },
    
    "get_file_metadata": {
        "description": "Get ALL Spotlight metadata for a file - dimensions, author, dates, where downloaded from, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to file"}
            },
            "required": ["file_path"]
        },
        "function": get_file_metadata
    },
    
    "find_duplicates_by_name": {
        "description": "Find potential duplicate files by similar names - great for cleanup",
        "parameters": {
            "type": "object",
            "properties": {
                "in_folder": {"type": "string", "description": "Folder to search"},
                "extension": {"type": "string", "description": "File extension (e.g., '.pdf')"},
                "limit": {"type": "integer", "description": "Max files to analyze"}
            },
            "required": []
        },
        "function": find_duplicates_by_name
    },
    
    "spotlight_natural_search": {
        "description": "Natural language file search - understands phrases like 'large video files', 'PDFs from last week', 'images in Downloads'",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural language query (e.g., 'large video files', 'PDFs from last week')"},
                "limit": {"type": "integer", "description": "Max results"}
            },
            "required": ["query"]
        },
        "function": spotlight_natural_search
    },
    
    "find_apps_using_disk_space": {
        "description": "Find which apps are using the most disk space - sorted by size",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max results (default 20)"}
            },
            "required": []
        },
        "function": find_apps_using_disk_space
    },
    
    "find_unused_apps": {
        "description": "Find apps not used in X days - great for cleanup and uninstalling unused apps",
        "parameters": {
            "type": "object",
            "properties": {
                "days_unused": {"type": "integer", "description": "Days since last use (default 90)"},
                "limit": {"type": "integer", "description": "Max results"}
            },
            "required": []
        },
        "function": find_unused_apps
    },
    
    # SAFARI INTEGRATION
    "safari_open_url": {
        "description": "Open URL in Safari (new tab or window)",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to open"},
                "new_tab": {"type": "boolean", "description": "Open in new tab (default: true)"}
            },
            "required": ["url"]
        },
        "function": safari_open_url
    },
    
    "safari_close_tabs": {
        "description": "Close all Safari tabs",
        "parameters": {"type": "object", "properties": {}},
        "function": safari_close_tabs
    },
    
    "safari_get_current_url": {
        "description": "Get the current URL from Safari",
        "parameters": {"type": "object", "properties": {}},
        "function": safari_get_current_url
    },
    
    # MESSAGES
    "send_imessage": {
        "description": "Send an iMessage to someone",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {"type": "string", "description": "Phone number or email"},
                "message": {"type": "string", "description": "Message text"}
            },
            "required": ["recipient", "message"]
        },
        "function": send_imessage
    },
    
    # MAIL
    "send_email": {
        "description": "Create email draft in Mail app (opens for user to send)",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email"},
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body"}
            },
            "required": ["to", "subject", "body"]
        },
        "function": send_email
    },
    
    # CALENDAR
    "create_calendar_event": {
        "description": "Create a calendar event",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Event title"},
                "start_date": {"type": "string", "description": "Start date/time 'YYYY-MM-DD HH:MM'"},
                "duration": {"type": "integer", "description": "Duration in minutes (default: 60)"}
            },
            "required": ["title", "start_date"]
        },
        "function": create_calendar_event
    },
    
    # FINDER
    "finder_search": {
        "description": "Open Finder search window",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        },
        "function": finder_search
    },
    
    "get_selected_files": {
        "description": "Get list of currently selected files in Finder",
        "parameters": {"type": "object", "properties": {}},
        "function": get_selected_files
    },
    
    # SYSTEM CONTROLS
    "toggle_bluetooth": {
        "description": "Toggle Bluetooth on/off (requires: brew install blueutil)",
        "parameters": {"type": "object", "properties": {}},
        "function": toggle_bluetooth
    },
    
    "set_wallpaper": {
        "description": "Set desktop wallpaper image",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Path to image file"}
            },
            "required": ["image_path"]
        },
        "function": set_wallpaper
    },
    
    "enable_focus_mode": {
        "description": "Enable Focus/Do Not Disturb mode",
        "parameters": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "description": "Focus mode name"}
            },
            "required": []
        },
        "function": enable_focus_mode
    },
    
    # QUICK ACTIONS
    "quick_timer": {
        "description": "Set a quick timer with notification (runs in background)",
        "parameters": {
            "type": "object",
            "properties": {
                "seconds": {"type": "integer", "description": "Seconds to wait"},
                "message": {"type": "string", "description": "Notification message"}
            },
            "required": ["seconds"]
        },
        "function": quick_timer
    },
    
    "show_notification_with_sound": {
        "description": "Show notification with sound (Glass, Ping, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title"},
                "message": {"type": "string", "description": "Message"},
                "sound": {"type": "string", "description": "Sound name"}
            },
            "required": ["title", "message"]
        },
        "function": show_notification_with_sound
    },
    
    # CHROME/BRAVE
    "chrome_open_url": {
        "description": "Open URL in Chrome or Brave Browser",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to open"},
                "browser": {"type": "string", "description": "Browser: 'Google Chrome' or 'Brave Browser'"}
            },
            "required": ["url"]
        },
        "function": chrome_open_url
    },
    
    "chrome_get_current_url": {
        "description": "Get current URL from Chrome/Brave",
        "parameters": {
            "type": "object",
            "properties": {
                "browser": {"type": "string", "description": "'Google Chrome' or 'Brave Browser'"}
            },
            "required": []
        },
        "function": chrome_get_current_url
    },
    
    "chrome_close_tabs": {
        "description": "Close all tabs in Chrome/Brave",
        "parameters": {
            "type": "object",
            "properties": {
                "browser": {"type": "string", "description": "'Google Chrome' or 'Brave Browser'"}
            },
            "required": []
        },
        "function": chrome_close_tabs
    },
    
    # VS CODE
    "vscode_open_file": {
        "description": "Open file or directory in VS Code",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to file or directory"}
            },
            "required": ["file_path"]
        },
        "function": vscode_open_file
    },
    
    "vscode_open_workspace": {
        "description": "Open workspace in VS Code",
        "parameters": {
            "type": "object",
            "properties": {
                "workspace_path": {"type": "string", "description": "Path to workspace"}
            },
            "required": ["workspace_path"]
        },
        "function": vscode_open_workspace
    },
    
    # SLACK
    "open_slack_channel": {
        "description": "Open Slack channel",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_name": {"type": "string", "description": "Channel name"}
            },
            "required": ["channel_name"]
        },
        "function": open_slack_channel
    },
    
    "open_slack_dm": {
        "description": "Open Slack DM with user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_name": {"type": "string", "description": "User name"}
            },
            "required": ["user_name"]
        },
        "function": open_slack_dm
    },
    
    # ZOOM
    "start_zoom_meeting": {
        "description": "Start or join Zoom meeting",
        "parameters": {
            "type": "object",
            "properties": {
                "meeting_id": {"type": "string", "description": "Meeting ID (optional)"}
            },
            "required": []
        },
        "function": start_zoom_meeting
    },
    
    # TERMINAL
    "open_terminal_command": {
        "description": "Open Terminal and run a command",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Command to run"},
                "new_window": {"type": "boolean", "description": "Open in new window"}
            },
            "required": ["command"]
        },
        "function": open_terminal_command
    },
    
    # DOCKER
    "docker_ps": {
        "description": "List running Docker containers",
        "parameters": {"type": "object", "properties": {}},
        "function": docker_ps
    },
    
    "docker_start_container": {
        "description": "Start Docker container",
        "parameters": {
            "type": "object",
            "properties": {
                "container_name": {"type": "string", "description": "Container name"}
            },
            "required": ["container_name"]
        },
        "function": docker_start_container
    },
    
    "docker_stop_container": {
        "description": "Stop Docker container",
        "parameters": {
            "type": "object",
            "properties": {
                "container_name": {"type": "string", "description": "Container name"}
            },
            "required": ["container_name"]
        },
        "function": docker_stop_container
    },
    
    # GIT
    "git_status": {
        "description": "Get git status of repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_path": {"type": "string", "description": "Repository path (default: current dir)"}
            },
            "required": []
        },
        "function": git_status
    },
    
    "git_pull": {
        "description": "Git pull in repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_path": {"type": "string", "description": "Repository path"}
            },
            "required": []
        },
        "function": git_pull
    },
    
    "git_commit": {
        "description": "Git commit all changes in repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_path": {"type": "string", "description": "Repository path"},
                "message": {"type": "string", "description": "Commit message"}
            },
            "required": ["message"]
        },
        "function": git_commit
    },
    
    # PRODUCTIVITY
    "pomodoro_timer": {
        "description": "Start Pomodoro timer (work + break cycle)",
        "parameters": {
            "type": "object",
            "properties": {
                "work_minutes": {"type": "integer", "description": "Work duration (default: 25)"},
                "break_minutes": {"type": "integer", "description": "Break duration (default: 5)"}
            },
            "required": []
        },
        "function": pomodoro_timer
    },
    
    "take_break_reminder": {
        "description": "Set break reminder after X minutes",
        "parameters": {
            "type": "object",
            "properties": {
                "minutes": {"type": "integer", "description": "Minutes until reminder"}
            },
            "required": ["minutes"]
        },
        "function": take_break_reminder
    },
    
    # FILE MANAGEMENT
    "open_downloads_folder": {
        "description": "Open Downloads folder in Finder",
        "parameters": {"type": "object", "properties": {}},
        "function": open_downloads_folder
    },
    
    "open_desktop": {
        "description": "Open Desktop in Finder",
        "parameters": {"type": "object", "properties": {}},
        "function": open_desktop
    },
    
    "get_disk_usage": {
        "description": "Get disk space usage information",
        "parameters": {"type": "object", "properties": {}},
        "function": get_disk_usage
    },
    
    # ========== WINDOW MANAGEMENT (9 tools) ==========
    "snap_window_left": {
        "description": "Snap window to left half of screen",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"}
            },
            "required": ["app_name"]
        },
        "function": snap_window_left
    },
    
    "snap_window_right": {
        "description": "Snap window to right half of screen",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"}
            },
            "required": ["app_name"]
        },
        "function": snap_window_right
    },
    
    "snap_side_by_side": {
        "description": "Snap two apps side by side on screen - one on left half, one on right half. Use this when user wants two apps arranged together simultaneously. Supports multiple displays.",
        "parameters": {
            "type": "object",
            "properties": {
                "left_app": {"type": "string", "description": "Application to place on left half"},
                "right_app": {"type": "string", "description": "Application to place on right half"},
                "display": {"type": "integer", "description": "Display index: 0=main screen, 1=second monitor/external display, 2=third display"}
            },
            "required": ["left_app", "right_app"]
        },
        "function": snap_side_by_side
    },
    
    "snap_to_display": {
        "description": "Snap window to specific display/monitor (for multi-monitor setups). Can position left, right, or full screen on chosen display.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"},
                "display": {"type": "integer", "description": "Display index: 0=main MacBook screen, 1=external monitor, 2=second external"},
                "position": {"type": "string", "enum": ["left", "right", "full"], "description": "Position on that display"}
            },
            "required": ["app_name"]
        },
        "function": snap_to_display
    },
    
    "get_display_bounds": {
        "description": "Get information about all connected displays/monitors. Useful for multi-monitor setups.",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "function": get_display_bounds
    },
    
    "maximize_window": {
        "description": "Maximize window (fullscreen)",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"}
            },
            "required": ["app_name"]
        },
        "function": maximize_window
    },
    
    "center_window": {
        "description": "Center window on screen",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"}
            },
            "required": ["app_name"]
        },
        "function": center_window
    },
    
    "resize_window": {
        "description": "Resize window to specific dimensions",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"},
                "width": {"type": "integer", "description": "Width in pixels"},
                "height": {"type": "integer", "description": "Height in pixels"}
            },
            "required": ["app_name", "width", "height"]
        },
        "function": resize_window
    },
    
    "move_window": {
        "description": "Move window to specific position",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"},
                "x": {"type": "integer", "description": "X coordinate"},
                "y": {"type": "integer", "description": "Y coordinate"}
            },
            "required": ["app_name", "x", "y"]
        },
        "function": move_window
    },
    
    "list_all_windows": {
        "description": "List all open windows",
        "parameters": {"type": "object", "properties": {}},
        "function": list_all_windows
    },
    
    "minimize_window": {
        "description": "Minimize window",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"}
            },
            "required": ["app_name"]
        },
        "function": minimize_window
    },
    
    "bring_to_front": {
        "description": "Bring app window to front",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"}
            },
            "required": ["app_name"]
        },
        "function": bring_to_front
    },
    
    # ========== FILE OPERATIONS (10 tools) ==========
    "compress_files": {
        "description": "Compress files into zip or tar.gz archive",
        "parameters": {
            "type": "object",
            "properties": {
                "files": {"type": "array", "items": {"type": "string"}, "description": "List of file paths"},
                "output_name": {"type": "string", "description": "Output archive name"},
                "format": {"type": "string", "description": "'zip' or 'tar.gz'"}
            },
            "required": ["files", "output_name"]
        },
        "function": compress_files
    },
    
    "extract_archive": {
        "description": "Extract zip or tar.gz archive",
        "parameters": {
            "type": "object",
            "properties": {
                "archive_path": {"type": "string", "description": "Path to archive"},
                "destination": {"type": "string", "description": "Destination directory"}
            },
            "required": ["archive_path"]
        },
        "function": extract_archive
    },
    
    "move_file": {
        "description": "Move file or directory",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source path"},
                "destination": {"type": "string", "description": "Destination path"}
            },
            "required": ["source", "destination"]
        },
        "function": move_file
    },
    
    "copy_file": {
        "description": "Copy file or directory",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source path"},
                "destination": {"type": "string", "description": "Destination path"}
            },
            "required": ["source", "destination"]
        },
        "function": copy_file
    },
    
    "rename_file": {
        "description": "Rename file or directory",
        "parameters": {
            "type": "object",
            "properties": {
                "old_path": {"type": "string", "description": "Current file path"},
                "new_name": {"type": "string", "description": "New name"}
            },
            "required": ["old_path", "new_name"]
        },
        "function": rename_file
    },
    
    "duplicate_file": {
        "description": "Duplicate file (adds '_copy' to name)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "File path"}
            },
            "required": ["file_path"]
        },
        "function": duplicate_file
    },
    
    "get_file_info": {
        "description": "Get detailed file information (size, dates, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "File path"}
            },
            "required": ["file_path"]
        },
        "function": get_file_info
    },
    
    "bulk_rename": {
        "description": "Bulk rename files in directory (find & replace pattern)",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Directory path"},
                "pattern": {"type": "string", "description": "Pattern to find"},
                "replacement": {"type": "string", "description": "Replacement text"}
            },
            "required": ["directory", "pattern", "replacement"]
        },
        "function": bulk_rename
    },
    
    "delete_file": {
        "description": "Delete file or directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "File path"}
            },
            "required": ["file_path"]
        },
        "function": delete_file
    },
    
    "find_files_by_extension": {
        "description": "Find all files with specific extension in directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Directory to search"},
                "extension": {"type": "string", "description": "File extension (e.g., '.pdf')"}
            },
            "required": ["directory", "extension"]
        },
        "function": find_files_by_extension
    },
    
    # ========== CLIPBOARD ADVANCED (7 tools) ==========
    "clipboard_get_history": {
        "description": "Get clipboard history (last 10 items)",
        "parameters": {"type": "object", "properties": {}},
        "function": clipboard_get_history
    },
    
    "clipboard_restore_from_history": {
        "description": "Restore clipboard from history by index",
        "parameters": {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "History index (0 = most recent)"}
            },
            "required": ["index"]
        },
        "function": clipboard_restore_from_history
    },
    
    "clipboard_save_image": {
        "description": "Save clipboard image to file",
        "parameters": {
            "type": "object",
            "properties": {
                "output_path": {"type": "string", "description": "Output file path"}
            },
            "required": []
        },
        "function": clipboard_save_image
    },
    
    "clipboard_append": {
        "description": "Append text to clipboard",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to append"}
            },
            "required": ["text"]
        },
        "function": clipboard_append
    },
    
    "clipboard_clear": {
        "description": "Clear clipboard",
        "parameters": {"type": "object", "properties": {}},
        "function": clipboard_clear
    },
    
    "clipboard_get_type": {
        "description": "Get clipboard content type (text, image, file)",
        "parameters": {"type": "object", "properties": {}},
        "function": clipboard_get_type
    },
    
    "clipboard_count_words": {
        "description": "Count words/chars/lines in clipboard",
        "parameters": {"type": "object", "properties": {}},
        "function": clipboard_count_words
    },
    
    # ========== SCREEN & MEDIA (9 tools) ==========
    "start_screen_recording": {
        "description": "Start screen recording",
        "parameters": {
            "type": "object",
            "properties": {
                "output_path": {"type": "string", "description": "Output file path"}
            },
            "required": []
        },
        "function": start_screen_recording
    },
    
    "stop_screen_recording": {
        "description": "Stop screen recording",
        "parameters": {"type": "object", "properties": {}},
        "function": stop_screen_recording
    },
    
    "resize_image": {
        "description": "Resize image to specified dimensions",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "Input image path"},
                "width": {"type": "integer", "description": "Width in pixels"},
                "height": {"type": "integer", "description": "Height in pixels"},
                "output_path": {"type": "string", "description": "Output path"}
            },
            "required": ["input_path", "width", "height"]
        },
        "function": resize_image
    },
    
    "convert_image_format": {
        "description": "Convert image to different format (png, jpg, webp, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "Input image path"},
                "output_format": {"type": "string", "description": "Output format"}
            },
            "required": ["input_path", "output_format"]
        },
        "function": convert_image_format
    },
    
    "compress_image": {
        "description": "Compress image to reduce file size",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "Input image path"},
                "quality": {"type": "integer", "description": "Quality 1-100 (default: 85)"},
                "output_path": {"type": "string", "description": "Output path"}
            },
            "required": ["input_path"]
        },
        "function": compress_image
    },
    
    "get_image_info": {
        "description": "Get image metadata (size, format, dimensions)",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Image path"}
            },
            "required": ["image_path"]
        },
        "function": get_image_info
    },
    
    "create_thumbnail": {
        "description": "Create thumbnail of image",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "Input image path"},
                "max_size": {"type": "integer", "description": "Max dimension (default: 256)"}
            },
            "required": ["input_path"]
        },
        "function": create_thumbnail
    },
    
    "convert_video_format": {
        "description": "Convert video format using ffmpeg",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "Input video path"},
                "output_format": {"type": "string", "description": "Output format (mp4, mov, etc.)"}
            },
            "required": ["input_path"]
        },
        "function": convert_video_format
    },
    
    # ========== DISPLAY CONTROL (6 tools) ==========
    "toggle_night_shift": {
        "description": "Toggle Night Shift on/off",
        "parameters": {"type": "object", "properties": {}},
        "function": toggle_night_shift
    },
    
    "start_screen_saver": {
        "description": "Start screen saver",
        "parameters": {"type": "object", "properties": {}},
        "function": start_screen_saver
    },
    
    "list_displays": {
        "description": "List connected displays",
        "parameters": {"type": "object", "properties": {}},
        "function": list_displays
    },
    
    "set_display_resolution": {
        "description": "Set display resolution (requires displayplacer)",
        "parameters": {
            "type": "object",
            "properties": {
                "width": {"type": "integer", "description": "Width"},
                "height": {"type": "integer", "description": "Height"}
            },
            "required": ["width", "height"]
        },
        "function": set_display_resolution
    },
    
    "mirror_displays": {
        "description": "Toggle display mirroring",
        "parameters": {"type": "object", "properties": {}},
        "function": mirror_displays
    },
    
    "get_display_info": {
        "description": "Get current display information",
        "parameters": {"type": "object", "properties": {}},
        "function": get_display_info
    },
    
    # ========== PACKAGE MANAGEMENT (16 tools) ==========
    "brew_install": {
        "description": "Install package via Homebrew",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name"}
            },
            "required": ["package"]
        },
        "function": brew_install
    },
    
    "brew_uninstall": {
        "description": "Uninstall package via Homebrew",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name"}
            },
            "required": ["package"]
        },
        "function": brew_uninstall
    },
    
    "brew_update": {
        "description": "Update Homebrew",
        "parameters": {"type": "object", "properties": {}},
        "function": brew_update
    },
    
    "brew_upgrade": {
        "description": "Upgrade Homebrew packages",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name (optional)"}
            },
            "required": []
        },
        "function": brew_upgrade
    },
    
    "brew_list": {
        "description": "List installed Homebrew packages",
        "parameters": {"type": "object", "properties": {}},
        "function": brew_list
    },
    
    "brew_search": {
        "description": "Search for Homebrew packages",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        },
        "function": brew_search
    },
    
    "brew_info": {
        "description": "Get info about Homebrew package",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name"}
            },
            "required": ["package"]
        },
        "function": brew_info
    },
    
    "npm_install_global": {
        "description": "Install npm package globally",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name"}
            },
            "required": ["package"]
        },
        "function": npm_install_global
    },
    
    "npm_uninstall_global": {
        "description": "Uninstall npm package globally",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name"}
            },
            "required": ["package"]
        },
        "function": npm_uninstall_global
    },
    
    "npm_list_global": {
        "description": "List globally installed npm packages",
        "parameters": {"type": "object", "properties": {}},
        "function": npm_list_global
    },
    
    "npm_update_global": {
        "description": "Update all global npm packages",
        "parameters": {"type": "object", "properties": {}},
        "function": npm_update_global
    },
    
    "pip_install": {
        "description": "Install Python package via pip",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name"}
            },
            "required": ["package"]
        },
        "function": pip_install
    },
    
    "pip_uninstall": {
        "description": "Uninstall Python package via pip",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {"type": "string", "description": "Package name"}
            },
            "required": ["package"]
        },
        "function": pip_uninstall
    },
    
    "pip_list": {
        "description": "List installed Python packages",
        "parameters": {"type": "object", "properties": {}},
        "function": pip_list
    },
    
    "pip_outdated": {
        "description": "List outdated Python packages",
        "parameters": {"type": "object", "properties": {}},
        "function": pip_outdated
    },
    
    # ========== KEYBOARD & MOUSE - REMOVED (were gimmicky) ==========
    
    # ========== TIME MACHINE & BACKUPS (8 tools) ==========
    "time_machine_status": {
        "description": "Get Time Machine backup status",
        "parameters": {"type": "object", "properties": {}},
        "function": time_machine_status
    },
    
    "start_time_machine_backup": {
        "description": "Start Time Machine backup now",
        "parameters": {"type": "object", "properties": {}},
        "function": start_time_machine_backup
    },
    
    "stop_time_machine_backup": {
        "description": "Stop Time Machine backup",
        "parameters": {"type": "object", "properties": {}},
        "function": stop_time_machine_backup
    },
    
    "list_time_machine_backups": {
        "description": "List available Time Machine backups",
        "parameters": {"type": "object", "properties": {}},
        "function": list_time_machine_backups
    },
    
    "get_latest_backup": {
        "description": "Get latest Time Machine backup info",
        "parameters": {"type": "object", "properties": {}},
        "function": get_latest_backup
    },
    
    "enable_time_machine": {
        "description": "Enable Time Machine automatic backups",
        "parameters": {"type": "object", "properties": {}},
        "function": enable_time_machine
    },
    
    "disable_time_machine": {
        "description": "Disable Time Machine automatic backups",
        "parameters": {"type": "object", "properties": {}},
        "function": disable_time_machine
    },
    
    "get_backup_destination": {
        "description": "Get Time Machine backup destination",
        "parameters": {"type": "object", "properties": {}},
        "function": get_backup_destination
    },
    
    # ========== AIRDROP & HANDOFF (6 tools) ==========
    "airdrop_send": {
        "description": "Open AirDrop to send file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "File path to send"}
            },
            "required": ["file_path"]
        },
        "function": airdrop_send
    },
    
    "open_airdrop_window": {
        "description": "Open AirDrop window",
        "parameters": {"type": "object", "properties": {}},
        "function": open_airdrop_window
    },
    
    "get_airdrop_status": {
        "description": "Check if AirDrop is enabled (WiFi + Bluetooth status)",
        "parameters": {"type": "object", "properties": {}},
        "function": get_airdrop_status
    },
    
    "handoff_url_to_device": {
        "description": "Open URL in Safari for Handoff to other devices",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to hand off"}
            },
            "required": ["url"]
        },
        "function": handoff_url_to_device
    },
    
    "open_continuity_settings": {
        "description": "Open Continuity settings (Handoff, Universal Clipboard)",
        "parameters": {"type": "object", "properties": {}},
        "function": open_continuity_settings
    },
    
    "share_text_via_airdrop": {
        "description": "Share text via AirDrop",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to share"}
            },
            "required": ["text"]
        },
        "function": share_text_via_airdrop
    },
    
    # ========== DATABASE TOOLS (11 tools) ==========
    "postgres_query": {
        "description": "Execute PostgreSQL query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "SQL query"},
                "database": {"type": "string", "description": "Database name"},
                "user": {"type": "string", "description": "Username"},
                "host": {"type": "string", "description": "Host"}
            },
            "required": ["query"]
        },
        "function": postgres_query
    },
    
    "mysql_query": {
        "description": "Execute MySQL query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "SQL query"},
                "database": {"type": "string", "description": "Database name"},
                "user": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "host": {"type": "string", "description": "Host"}
            },
            "required": ["query"]
        },
        "function": mysql_query
    },
    
    "mongodb_find": {
        "description": "Find documents in MongoDB collection",
        "parameters": {
            "type": "object",
            "properties": {
                "collection": {"type": "string", "description": "Collection name"},
                "query": {"type": "string", "description": "Query JSON"},
                "database": {"type": "string", "description": "Database name"},
                "host": {"type": "string", "description": "Host"},
                "port": {"type": "integer", "description": "Port"}
            },
            "required": ["collection"]
        },
        "function": mongodb_find
    },
    
    "mongodb_insert": {
        "description": "Insert document into MongoDB",
        "parameters": {
            "type": "object",
            "properties": {
                "collection": {"type": "string", "description": "Collection name"},
                "document": {"type": "string", "description": "Document JSON"},
                "database": {"type": "string", "description": "Database name"},
                "host": {"type": "string", "description": "Host"},
                "port": {"type": "integer", "description": "Port"}
            },
            "required": ["collection", "document"]
        },
        "function": mongodb_insert
    },
    
    "redis_get": {
        "description": "Get value from Redis",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Key name"},
                "host": {"type": "string", "description": "Host"},
                "port": {"type": "integer", "description": "Port"}
            },
            "required": ["key"]
        },
        "function": redis_get
    },
    
    "redis_set": {
        "description": "Set value in Redis",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Key name"},
                "value": {"type": "string", "description": "Value"},
                "host": {"type": "string", "description": "Host"},
                "port": {"type": "integer", "description": "Port"},
                "expire": {"type": "integer", "description": "Expiration seconds"}
            },
            "required": ["key", "value"]
        },
        "function": redis_set
    },
    
    "redis_delete": {
        "description": "Delete key from Redis",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Key name"},
                "host": {"type": "string", "description": "Host"},
                "port": {"type": "integer", "description": "Port"}
            },
            "required": ["key"]
        },
        "function": redis_delete
    },
    
    "redis_keys": {
        "description": "List Redis keys matching pattern",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Key pattern (e.g., 'user:*')"},
                "host": {"type": "string", "description": "Host"},
                "port": {"type": "integer", "description": "Port"}
            },
            "required": []
        },
        "function": redis_keys
    },
    
    "postgres_list_databases": {
        "description": "List all PostgreSQL databases",
        "parameters": {
            "type": "object",
            "properties": {
                "user": {"type": "string", "description": "Username"},
                "host": {"type": "string", "description": "Host"}
            },
            "required": []
        },
        "function": postgres_list_databases
    },
    
    "mysql_list_databases": {
        "description": "List all MySQL databases",
        "parameters": {
            "type": "object",
            "properties": {
                "user": {"type": "string", "description": "Username"},
                "password": {"type": "string", "description": "Password"},
                "host": {"type": "string", "description": "Host"}
            },
            "required": []
        },
        "function": mysql_list_databases
    },
    
    "mongodb_list_collections": {
        "description": "List all collections in MongoDB database",
        "parameters": {
            "type": "object",
            "properties": {
                "database": {"type": "string", "description": "Database name"},
                "host": {"type": "string", "description": "Host"},
                "port": {"type": "integer", "description": "Port"}
            },
            "required": []
        },
        "function": mongodb_list_collections
    },
    
    # ========== WEB TOOLS (13 tools) ==========
    "download_file": {
        "description": "Download file from URL",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to download"},
                "output_path": {"type": "string", "description": "Output path"}
            },
            "required": ["url"]
        },
        "function": download_file
    },
    
    "check_website_status": {
        "description": "Check if website is up and get status code",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to check"}
            },
            "required": ["url"]
        },
        "function": check_website_status
    },
    
    "web_scrape": {
        "description": "Scrape website content",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to scrape"},
                "selector": {"type": "string", "description": "CSS selector (optional)"}
            },
            "required": ["url"]
        },
        "function": web_scrape
    },
    
    "get_page_title": {
        "description": "Get webpage title",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL"}
            },
            "required": ["url"]
        },
        "function": get_page_title
    },
    
    "get_page_links": {
        "description": "Get all links from webpage",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL"}
            },
            "required": ["url"]
        },
        "function": get_page_links
    },
    
    "shorten_url": {
        "description": "Shorten URL using is.gd service",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to shorten"}
            },
            "required": ["url"]
        },
        "function": shorten_url
    },
    
    "generate_qr_code": {
        "description": "Generate QR code for text/URL",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text or URL"},
                "output_path": {"type": "string", "description": "Output path"}
            },
            "required": ["text"]
        },
        "function": generate_qr_code
    },
    
    "get_ip_info": {
        "description": "Get public IP and location info",
        "parameters": {"type": "object", "properties": {}},
        "function": get_ip_info
    },
    
    "ping_host": {
        "description": "Ping a host",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {"type": "string", "description": "Host to ping"},
                "count": {"type": "integer", "description": "Number of pings"}
            },
            "required": ["host"]
        },
        "function": ping_host
    },
    
    "trace_route": {
        "description": "Trace route to host",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {"type": "string", "description": "Host"},
                "max_hops": {"type": "integer", "description": "Max hops"}
            },
            "required": ["host"]
        },
        "function": trace_route
    },
    
    "dns_lookup": {
        "description": "DNS lookup for domain",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain name"}
            },
            "required": ["domain"]
        },
        "function": dns_lookup
    },
    
    "whois_lookup": {
        "description": "WHOIS lookup for domain",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain name"}
            },
            "required": ["domain"]
        },
        "function": whois_lookup
    },
    
    "test_download_speed": {
        "description": "Test internet download speed",
        "parameters": {"type": "object", "properties": {}},
        "function": test_download_speed
    },
    
    "test_upload_speed": {
        "description": "Test internet upload speed",
        "parameters": {"type": "object", "properties": {}},
        "function": test_upload_speed
    }
}

# Merge workflow tools
ADVANCED_TOOLS.update(WORKFLOW_TOOLS)

