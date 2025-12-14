"""
MCP Server Implementation
Handles tool registration and execution following MCP protocol
"""

import json
import sys
from typing import Dict, Any, List, Optional, Tuple
from difflib import SequenceMatcher
from core.tools import TOOLS, get_enabled_tools


def fuzzy_match_tool(tool_name: str, available_tools: List[str], threshold: float = 0.6) -> Optional[Tuple[str, float]]:
    """
    Find the best fuzzy match for a tool name.
    
    Args:
        tool_name: The tool name to match
        available_tools: List of available tool names
        threshold: Minimum similarity ratio (0-1) to consider a match
        
    Returns:
        Tuple of (matched_tool_name, similarity_score) or None if no match
    """
    best_match = None
    best_score = 0
    
    tool_lower = tool_name.lower().replace("_", "").replace("-", "")
    
    for tool in available_tools:
        tool_normalized = tool.lower().replace("_", "").replace("-", "")
        
        # Direct sequence matching
        score = SequenceMatcher(None, tool_lower, tool_normalized).ratio()
        
        # Bonus for substring matches
        if tool_lower in tool_normalized or tool_normalized in tool_lower:
            score = max(score, 0.75)
        
        # Bonus for matching prefix
        if tool_normalized.startswith(tool_lower[:4]) or tool_lower.startswith(tool_normalized[:4]):
            score += 0.1
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = tool
    
    return (best_match, best_score) if best_match else None


# Tool name aliases - maps common LLM variations to actual tool names
TOOL_ALIASES = {
    # Spotify variations
    "spotify_current_track": "spotify_get_current_track",
    "spotify_now_playing": "spotify_get_current_track",
    "get_current_track": "spotify_get_current_track",
    "spotify_play": "spotify_resume",
    "spotify_stop": "spotify_pause",
    "spotify_skip": "spotify_next_track",
    "spotify_next_song": "spotify_next_track",
    "spotify_back": "spotify_previous_track",
    "spotify_prev": "spotify_previous_track",
    "spotify_volume": "spotify_set_volume",
    "spotify_get_vol": "spotify_get_volume",
    "spotify_shuffle": "spotify_toggle_shuffle",
    "spotify_repeat": "spotify_toggle_repeat",
    "get_spotify_status": "spotify_get_status",
    
    # Browser variations - Generic
    "open_tab": "browser_new_tab",
    "new_browser_tab": "browser_new_tab",
    "close_tab": "browser_close_tab",
    "browser_close": "browser_close_tab",
    "get_url": "browser_get_current_url",
    "current_url": "browser_get_current_url",
    "get_page_url": "browser_get_current_url",
    "browser_url": "browser_get_current_url",
    "browser_title": "browser_get_current_title",
    "get_title": "browser_get_current_title",
    "page_title": "browser_get_current_title",
    "browser_back": "browser_go_back",
    "go_back": "browser_go_back",
    "browser_forward": "browser_go_forward",
    "go_forward": "browser_go_forward",
    "browser_reload": "browser_refresh",
    "reload_page": "browser_refresh",
    "tab_count": "browser_get_tab_count",
    "count_tabs": "browser_get_tab_count",
    "list_tabs": "browser_get_all_tabs",
    "get_tabs": "browser_get_all_tabs",
    "browser_tabs": "browser_get_all_tabs",
    "browser_incognito": "browser_open_incognito",
    "private_window": "browser_open_incognito",
    "incognito": "browser_open_incognito",
    "browser_devtools": "browser_open_devtools",
    "devtools": "browser_open_devtools",
    "developer_tools": "browser_open_devtools",
    
    # Chrome-specific (map to generic browser tools)
    "chrome_get_current_url": "browser_get_current_url",
    "chrome_new_tab": "browser_new_tab",
    "chrome_close_tab": "browser_close_tab",
    "chrome_refresh": "browser_refresh",
    "chrome_go_back": "browser_go_back",
    "chrome_go_forward": "browser_go_forward",
    "chrome_duplicate_tab": "browser_duplicate_tab",
    "chrome_open_url": "browser_new_tab",
    
    # Safari-specific (map to generic browser tools)
    "safari_get_current_url": "browser_get_current_url",
    "safari_new_tab": "browser_new_tab",
    "safari_close_tab": "browser_close_tab",
    "safari_refresh": "browser_refresh",
    
    # Brave-specific (map to generic browser tools)
    "brave_get_current_url": "browser_get_current_url",
    "brave_new_tab": "browser_new_tab",
    "brave_close_tab": "browser_close_tab",
    
    # App variations  
    "launch_app": "open_application",
    "start_app": "open_application",
    "run_app": "open_application",
    "open_app": "open_application",
    "quit_app": "close_application",
    "kill_app": "close_application",
    "close_app": "close_application",
    
    # File variations
    "find_file": "quick_find_file",
    "search_file": "quick_find_file",
    "locate_file": "quick_find_file",
    "search_files": "quick_find_file",
    "find_files": "quick_find_file",
    "create_folder": "create_directory",
    "make_folder": "create_directory",
    "mkdir": "create_directory",
    "make_directory": "create_directory",
    "new_folder": "create_directory",
    
    # System variations
    "volume": "set_volume",
    "change_volume": "set_volume",
    "adjust_volume": "set_volume",
    "brightness": "set_brightness",
    "change_brightness": "set_brightness",
    "adjust_brightness": "set_brightness",
    "dark_mode": "toggle_dark_mode",
    "toggle_darkmode": "toggle_dark_mode",
    "wifi": "toggle_wifi",
    "bluetooth": "toggle_bluetooth",
    "lock": "lock_screen",
    "sleep": "sleep_computer",
    "battery": "get_battery_status",
    "battery_status": "get_battery_status",
    
    # Clipboard variations
    "clipboard": "clipboard_read",
    "get_clipboard": "clipboard_read",
    "read_clipboard": "clipboard_read",
    "whats_on_clipboard": "clipboard_read",
    "clipboard_content": "clipboard_read",
    "paste_history": "clipboard_get_history",
    "clipboard_history": "clipboard_get_history",
    "clear_clipboard": "clipboard_clear",
    
    # Notes/Reminders
    "new_note": "create_note",
    "add_note": "create_note",
    "new_reminder": "create_reminder",
    "add_reminder": "create_reminder",
    "remind_me": "create_reminder",
    
    # Terminal
    "terminal": "open_terminal_command",
    "run_command": "run_shell_command",
    "shell": "run_shell_command",
    "exec": "run_shell_command",
    "execute": "run_shell_command",
    "execute_command": "run_shell_command",
    
    # Spotlight / File Search
    "find_large_files": "find_large_files",
    "large_files": "find_large_files",
    "big_files": "find_large_files",
    "disk_usage": "find_apps_using_disk_space",
    "app_size": "find_apps_using_disk_space",
    "largest_apps": "find_apps_using_disk_space",
    "recent_files": "find_files_by_date",
    "files_by_date": "find_files_by_date",
    "modified_today": "find_files_by_date",
    "search_content": "find_by_content",
    "content_search": "find_by_content",
    "files_containing": "find_by_content",
    "unused_apps": "find_unused_apps",
    "old_apps": "find_unused_apps",
    
    # Network
    "check_network": "get_network_info",
    "network_status": "get_network_info",
    "speed_test": "test_download_speed",
    "internet_speed": "test_download_speed",
    "public_ip": "get_ip_info",
    "my_ip": "get_ip_info",
    "ip_info": "get_ip_info",
}

# Parameter aliases - maps common LLM variations to expected parameter names
PARAMETER_ALIASES = {
    # Application tools
    "application": "app_name",
    "app": "app_name",
    "application_name": "app_name",
    "name": "app_name",  # Common for apps
    
    # File tools
    "file": "file_path",
    "filepath": "file_path",
    "path": "file_path",
    "filename": "file_path",
    "source": "source_path",
    "destination": "dest_path",
    "dest": "dest_path",
    "target": "dest_path",
    
    # URL tools
    "url": "webpage_url",
    "link": "webpage_url",
    "website": "webpage_url",
    "address": "webpage_url",
    
    # Browser tools
    "tab": "tab_index",
    "tab_number": "tab_index",
    "browser": "browser_name",
    
    # Directory tools
    "folder": "directory",
    "dir": "directory",
    "folder_path": "directory",
    
    # Search tools
    "search": "query",
    "search_term": "query",
    "search_query": "query",
    "term": "query",
    "keywords": "query",
    "query": "filename",  # For quick_find_file
    "name": "filename",   # For quick_find_file
    
    # Volume/audio
    "vol": "volume",
    "level": "volume",
    "volume_level": "volume",
    
    # Text/content
    "message": "text",
    "content": "text",
    "body": "text",
    
    # Music/Spotify
    "song": "track",
    "track_name": "track",
    "artist": "artist_name",
    "album": "album_name",
    "playlist": "playlist_name",
    
    # Command/Shell
    "cmd": "command",
    "shell_command": "command",
    "script": "command",
    
    # Network
    "ip": "ip_address",
    "address": "ip_address",
    "host": "ip_address",
}


class MCPServer:
    """MCP Server for macOS integration tools"""
    
    def __init__(self, config: dict):
        self.config = config
        self.tools = get_enabled_tools(config)
        self.server_info = config.get('server', {})
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Return list of available tools in MCP format
        
        Returns:
            List of tool definitions
        """
        tools_list = []
        for name, tool in self.tools.items():
            tools_list.append({
                "name": name,
                "description": tool["description"],
                "inputSchema": tool["parameters"]
            })
        return tools_list
    
    def _normalize_parameters(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize parameter names using aliases and tool schema
        
        Args:
            tool_name: Name of the tool
            parameters: Raw parameters from LLM
            
        Returns:
            Normalized parameters matching function signature
        """
        if not parameters:
            return {}
        
        # Get expected parameters from tool schema
        tool = self.tools.get(tool_name, {})
        schema = tool.get("parameters", {})
        expected_params = set(schema.get("properties", {}).keys())
        
        normalized = {}
        
        for key, value in parameters.items():
            # If the key is already correct, use it
            if key in expected_params:
                normalized[key] = value
            # Check if it's an alias
            elif key in PARAMETER_ALIASES:
                alias_target = PARAMETER_ALIASES[key]
                # Only use alias if target is in expected params
                if alias_target in expected_params:
                    normalized[alias_target] = value
                else:
                    # Try to find any matching expected param
                    normalized[key] = value
            else:
                # Pass through unknown params (let function handle errors)
                normalized[key] = value
        
        return normalized
    
    def _sanitize_tool_name(self, tool_name: str) -> str:
        """
        Sanitize tool name by removing common LLM hallucination prefixes/suffixes.
        
        Args:
            tool_name: Raw tool name from LLM
            
        Returns:
            Cleaned tool name
        """
        import re
        
        if not tool_name:
            return tool_name
            
        original = tool_name
        
        # Remove EVERYTHING after <|channel|> or similar artifacts (common LLM hallucination)
        # Pattern: tool_name<|anything|>garbage or tool_name<|garbage
        tool_name = re.sub(r'<\|.*$', '', tool_name)
        
        # Remove common hallucinated prefixes (loop to handle nested prefixes)
        prefixes_to_strip = [
            "assistant<|channel|>",
            "namespace.functions.",
            "namespace.",
            "functions.",
            "function.",
            "tools.",
            "tool.",
            "mcp.",
            "macgpt.",
            "spotify.",
            "browser.",
            "<|",
        ]
        
        changed = True
        while changed:
            changed = False
            for prefix in prefixes_to_strip:
                if tool_name.lower().startswith(prefix.lower()):
                    tool_name = tool_name[len(prefix):]
                    changed = True
        
        # Remove common hallucinated suffixes
        suffixes_to_strip = [
            "<|channel|>commentary",
            "<|channel|>",
            "|>",
            "<|",
        ]
        
        for suffix in suffixes_to_strip:
            if tool_name.lower().endswith(suffix.lower()):
                tool_name = tool_name[:-len(suffix)]
        
        # Remove any remaining special characters at start/end
        tool_name = tool_name.strip("<|>./")
        
        # Handle cases like "analysis" which is garbage
        garbage_names = ["analysis", "channel", "assistant", "function", "tool", "commentary", "namespace"]
        if tool_name.lower() in garbage_names:
            return ""  # Return empty to trigger "tool not found"
        
        # Final cleanup - only allow valid tool name characters
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tool_name):
            # Try to extract a valid tool name from the mess
            match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)', tool_name)
            if match:
                tool_name = match.group(1)
        
        if tool_name != original:
            print(f"  → Sanitized '{original}' to '{tool_name}'", file=sys.stderr)
        
        return tool_name
    
    def _resolve_tool_name(self, tool_name: str) -> str:
        """
        Resolve tool name aliases to actual tool names
        
        Args:
            tool_name: Tool name (possibly an alias)
            
        Returns:
            Resolved tool name
        """
        # First sanitize the tool name
        tool_name = self._sanitize_tool_name(tool_name)
        
        if not tool_name:
            return ""
        
        # Check if it's an alias
        if tool_name in TOOL_ALIASES:
            resolved = TOOL_ALIASES[tool_name]
            print(f"  → Resolved '{tool_name}' to '{resolved}'", file=sys.stderr)
            return resolved
        return tool_name
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with given parameters
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters
        
        Returns:
            Tool execution result
        """
        # Resolve tool name aliases
        resolved_name = self._resolve_tool_name(tool_name)
        
        # Handle garbage/empty tool names
        if not resolved_name:
            return {
                "success": False,
                "error": f"Invalid tool name '{tool_name}'. Use 'tools' command to see available tools."
            }
        
        if resolved_name not in self.tools:
            # Try fuzzy matching as last resort
            fuzzy_result = fuzzy_match_tool(tool_name, list(self.tools.keys()))
            
            if fuzzy_result:
                matched_tool, score = fuzzy_result
                # Auto-use if very high confidence (>85%)
                if score > 0.85:
                    print(f"  → Auto-corrected '{tool_name}' to '{matched_tool}' (confidence: {score:.0%})", file=sys.stderr)
                    resolved_name = matched_tool
                else:
                    # Suggest but don't auto-execute for lower confidence
                    return {
                        "success": False,
                        "error": f"Tool '{tool_name}' not found. Did you mean '{matched_tool}'? (confidence: {score:.0%})"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found. Use 'tools' command to see available tools."
                }
        
        try:
            tool = self.tools[resolved_name]
            function = tool["function"]
            
            # Normalize parameters to handle LLM variations
            normalized_params = self._normalize_parameters(resolved_name, parameters)
            
            # Execute the tool function
            result = function(**normalized_params)
            return result
        except TypeError as e:
            return {
                "success": False,
                "error": f"Invalid parameters: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}"
            }
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming MCP request
        
        Args:
            request: MCP request dictionary
        
        Returns:
            MCP response dictionary
        """
        method = request.get('method')
        
        if method == 'initialize':
            return {
                "protocolVersion": "0.1.0",
                "serverInfo": {
                    "name": self.server_info.get('name', 'macos-integration'),
                    "version": self.server_info.get('version', '0.1.0')
                },
                "capabilities": {
                    "tools": {}
                }
            }
        
        elif method == 'tools/list':
            return {
                "tools": self.list_tools()
            }
        
        elif method == 'tools/call':
            params = request.get('params', {})
            tool_name = params.get('name')
            tool_params = params.get('arguments', {})
            
            result = self.execute_tool(tool_name, tool_params)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }
        
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    def run_stdio(self):
        """
        Run server in stdio mode (standard MCP transport)
        Reads JSON-RPC requests from stdin and writes responses to stdout
        """
        print(f"MCP Server '{self.server_info.get('name')}' starting in stdio mode...", file=sys.stderr)
        print(f"Loaded {len(self.tools)} tools", file=sys.stderr)
        
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                
                # Write response as JSON-RPC
                json_response = json.dumps({
                    "jsonrpc": "2.0",
                    "id": request.get('id'),
                    "result": response
                })
                print(json_response)
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                error_response = json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                })
                print(error_response)
                sys.stdout.flush()
            except Exception as e:
                error_response = json.dumps({
                    "jsonrpc": "2.0",
                    "id": request.get('id') if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                })
                print(error_response)
                sys.stdout.flush()


def load_config(config_path: str = 'config.json') -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Config file '{config_path}' not found. Using defaults.", file=sys.stderr)
        return {
            "server": {"name": "macos-integration", "version": "0.1.0"},
            "tools": {"enabled": []}
        }


if __name__ == '__main__':
    config = load_config()
    server = MCPServer(config)
    server.run_stdio()

