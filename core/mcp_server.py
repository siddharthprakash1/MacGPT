"""
MCP Server Implementation
Handles tool registration and execution following MCP protocol
"""

import json
import sys
from typing import Dict, Any, List
from core.tools import TOOLS, get_enabled_tools


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
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with given parameters
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters
        
        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        try:
            tool = self.tools[tool_name]
            function = tool["function"]
            
            # Execute the tool function
            result = function(**parameters)
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

