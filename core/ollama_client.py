"""
Ollama Integration Client
Handles communication between Ollama and MCP tools
OPTIMIZED for faster responses
"""

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import subprocess
import sys
import os
from typing import List, Dict, Any, Optional
from core.mcp_server import MCPServer, load_config


class OllamaClient:
    """Client for integrating Ollama with MCP tools - OPTIMIZED"""
    
    # Class-level cache for tools (shared across instances)
    _tools_cache = None
    _tools_cache_hash = None
    
    def __init__(self, config: dict):
        self.config = config
        self.ollama_config = config.get('ollama', {})
        self.endpoint = self.ollama_config.get('endpoint', 'http://localhost:11434')
        self.model = self.ollama_config.get('model', 'gemma2:27b')
        self.temperature = self.ollama_config.get('temperature', 0.7)
        
        self.mcp_server = MCPServer(config)
        self.conversation_history = []
        
        # Max conversation history to prevent slowdown (keep last N exchanges)
        self.max_history = 20  # 10 user + 10 assistant messages
        
        # Setup connection pooling for faster requests
        self.session = requests.Session()
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(
            pool_connections=5,
            pool_maxsize=10,
            max_retries=retry_strategy
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Cache tools on init
        self._cache_tools()
    
    def _cache_tools(self):
        """Cache tools list - only rebuild if tools change"""
        tools_hash = hash(frozenset(self.mcp_server.tools.keys()))
        
        if OllamaClient._tools_cache_hash != tools_hash:
            OllamaClient._tools_cache = []
            for name, tool in self.mcp_server.tools.items():
                OllamaClient._tools_cache.append({
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                })
            OllamaClient._tools_cache_hash = tools_hash
    
    def get_tools_for_ollama(self) -> List[Dict[str, Any]]:
        """Return cached tools list"""
        return OllamaClient._tools_cache or []
    
    def _trim_history(self):
        """Keep conversation history manageable for faster responses"""
        if len(self.conversation_history) > self.max_history:
            # Keep system prompt if present
            system_prompt = None
            if self.conversation_history and self.conversation_history[0].get('role') == 'system':
                system_prompt = self.conversation_history[0]
            
            # Keep only recent messages
            self.conversation_history = self.conversation_history[-self.max_history:]
            
            # Re-add system prompt at start
            if system_prompt and (not self.conversation_history or 
                                   self.conversation_history[0].get('role') != 'system'):
                self.conversation_history.insert(0, system_prompt)
    
    def chat(self, message: str, stream: bool = False) -> Dict[str, Any]:
        """
        Send a chat message to Ollama with tool support
        OPTIMIZED for speed
        """
        # Add user message to history (skip empty messages from tool follow-up)
        if message:
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
        
        # Trim history to prevent slowdown
        self._trim_history()
        
        # Use cached tools
        tools = self.get_tools_for_ollama()
        
        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "stream": stream,
            "options": {
                "temperature": self.temperature,
                "num_ctx": 4096,  # Reasonable context window
            },
            # Keep model loaded in memory for faster subsequent requests
            "keep_alive": "10m"
        }
        
        # Only add tools if available
        if tools:
            payload["tools"] = tools
        
        try:
            # Use session for connection pooling
            response = self.session.post(
                f"{self.endpoint}/api/chat",
                json=payload,
                timeout=120
            )
            
            # Check for tool support error
            if response.status_code == 400:
                error_data = response.json()
                if 'does not support tools' in str(error_data.get('error', '')):
                    print(f"\n⚠️  Note: {self.model} doesn't support native tool calling", file=sys.stderr)
                    payload.pop('tools', None)
                    response = self.session.post(
                        f"{self.endpoint}/api/chat",
                        json=payload,
                        timeout=120
                    )
            
            response.raise_for_status()
            result = response.json()
            
            # Check if model wants to call a tool
            message_response = result.get('message', {})
            tool_calls = message_response.get('tool_calls', [])
            
            if tool_calls:
                # Execute tool calls
                tool_results = []
                for tool_call in tool_calls:
                    function = tool_call.get('function', {})
                    tool_name = function.get('name')
                    tool_args = function.get('arguments', {})
                    
                    print(f"\n🔧 Executing: {tool_name}")
                    
                    # Execute the tool
                    tool_result = self.mcp_server.execute_tool(tool_name, tool_args)
                    tool_results.append(tool_result)
                
                # Add assistant's tool call to history
                self.conversation_history.append(message_response)
                
                # Add tool results to history
                self.conversation_history.append({
                    "role": "tool",
                    "content": json.dumps(tool_results)
                })
                
                # Get final response from model (recursive call)
                return self.chat("", stream=stream)
            
            else:
                # Regular response without tool calls
                self.conversation_history.append(message_response)
                return result
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to communicate with Ollama: {str(e)}"
            }
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def set_system_prompt(self, prompt: str):
        """Set a system prompt for the conversation"""
        self.conversation_history = [{
            "role": "system",
            "content": prompt
        }]


# Optimized system prompt - shorter but effective
SYSTEM_PROMPT = """You are MacGPT, a macOS assistant with system tools.

RULES:
- Use tools to execute tasks, don't just describe them
- quick_find_file for file search (fast)
- play_spotify_track for Spotify music
- open_application to launch apps
- Keep responses brief and formatted with markdown

Execute actions directly when asked."""


def speak_text(text: str):
    """Use macOS say command for text-to-speech"""
    try:
        subprocess.Popen(['say', text])
    except:
        pass


# Initialize Vosk model (lazy loading)
_vosk_model = None

def get_vosk_model():
    """Get or initialize Vosk model"""
    global _vosk_model
    if _vosk_model is None:
        from vosk import Model
        model_path = os.path.expanduser("~/.vosk/vosk-model-small-en-us-0.15")
        
        if not os.path.exists(model_path):
            print("⏳ Downloading Vosk model (first time only, ~40MB)...", flush=True)
            import urllib.request
            import zipfile
            
            url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
            zip_path = os.path.expanduser("~/.vosk/model.zip")
            os.makedirs(os.path.expanduser("~/.vosk"), exist_ok=True)
            
            urllib.request.urlretrieve(url, zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.expanduser("~/.vosk"))
            
            os.remove(zip_path)
            print("✅ Model downloaded!", flush=True)
        
        _vosk_model = Model(model_path)
    
    return _vosk_model


def listen_for_voice() -> Optional[str]:
    """Listen for voice input and transcribe using Vosk"""
    try:
        import pyaudio
        from vosk import KaldiRecognizer
        
        model = get_vosk_model()
        
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        stream.start_stream()
        
        rec = KaldiRecognizer(model, 16000)
        rec.SetMaxAlternatives(0)
        rec.SetWords(False)
        
        print("🎤 Listening... (speak now)", flush=True)
        
        for _ in range(0, 40):  # 5 seconds
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                break
        
        result_json = rec.FinalResult()
        result_dict = json.loads(result_json)
        text = result_dict.get("text", "").strip()
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        if text:
            return text
        else:
            print("❌ No speech detected")
            return None
            
    except OSError as e:
        print(f"❌ Microphone error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def interactive_mode():
    """Run interactive chat mode with Ollama"""
    config = load_config()
    client = OllamaClient(config)
    
    voice_mode = False
    
    print("=" * 60)
    print("🤖 MacGPT Interactive Mode")
    print("=" * 60)
    print(f"Model: {client.model}")
    print(f"Available tools: {len(client.mcp_server.tools)}")
    print("\nCommands: quit, reset, tools, voice on/off, listen")
    print("=" * 60)
    print()
    
    # Set optimized system prompt
    client.set_system_prompt(SYSTEM_PROMPT)
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input or user_input.lower() == 'listen':
                voice_input = listen_for_voice()
                if voice_input:
                    print(f"📝 You said: {voice_input}\n")
                    user_input = voice_input
                else:
                    continue
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                if voice_mode:
                    speak_text("Goodbye!")
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                client.reset_conversation()
                client.set_system_prompt(SYSTEM_PROMPT)
                print("🔄 Conversation reset\n")
                continue
            
            if user_input.lower() == 'tools':
                print("\n📋 Available tools:")
                for tool_name in list(client.mcp_server.tools.keys())[:20]:
                    print(f"  - {tool_name}")
                print(f"  ... and {len(client.mcp_server.tools) - 20} more")
                print()
                continue
            
            if user_input.lower() in ['voice on', 'voice']:
                voice_mode = True
                print("🔊 Voice mode enabled\n")
                speak_text("Voice mode enabled")
                continue
            
            if user_input.lower() == 'voice off':
                voice_mode = False
                print("🔇 Voice mode disabled\n")
                continue
            
            print("\n🤖 Assistant: ", end="", flush=True)
            response = client.chat(user_input)
            
            if 'error' in response:
                print(f"❌ Error: {response['error']}")
            else:
                content = response.get('message', {}).get('content', '')
                print(content)
                
                if voice_mode and content:
                    speak_text(content)
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == '__main__':
    interactive_mode()
