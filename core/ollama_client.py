"""
Ollama Integration Client
Handles communication between Ollama and MCP tools
"""

import json
import requests
import subprocess
import sys
import pyaudio
import os
from typing import List, Dict, Any, Optional
from core.mcp_server import MCPServer, load_config
from vosk import Model, KaldiRecognizer


class OllamaClient:
    """Client for integrating Ollama with MCP tools"""
    
    def __init__(self, config: dict):
        self.config = config
        self.ollama_config = config.get('ollama', {})
        self.endpoint = self.ollama_config.get('endpoint', 'http://localhost:11434')
        self.model = self.ollama_config.get('model', 'gemma2:27b')
        self.temperature = self.ollama_config.get('temperature', 0.7)
        
        self.mcp_server = MCPServer(config)
        self.conversation_history = []
    
    def get_tools_for_ollama(self) -> List[Dict[str, Any]]:
        """
        Convert MCP tools to Ollama tool format
        
        Returns:
            List of tools in Ollama format
        """
        tools = []
        for name, tool in self.mcp_server.tools.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })
        return tools
    
    def chat(self, message: str, stream: bool = False) -> Dict[str, Any]:
        """
        Send a chat message to Ollama with tool support
        
        Args:
            message: User message
            stream: Whether to stream the response
        
        Returns:
            Response from Ollama
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Prepare request
        tools = self.get_tools_for_ollama()
        
        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "stream": stream,
            "options": {
                "temperature": self.temperature
            }
        }
        
        # Only add tools if the model supports them
        if tools:
            payload["tools"] = tools
        
        try:
            response = requests.post(
                f"{self.endpoint}/api/chat",
                json=payload,
                timeout=120
            )
            
            # Check for tool support error
            if response.status_code == 400:
                error_data = response.json()
                if 'does not support tools' in str(error_data.get('error', '')):
                    # Retry without tools
                    print(f"\n⚠️  Note: {self.model} doesn't support native tool calling", file=sys.stderr)
                    print(f"   Falling back to basic chat mode\n", file=sys.stderr)
                    payload.pop('tools', None)
                    response = requests.post(
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
                    
                    print(f"\n🔧 Executing tool: {tool_name}")
                    print(f"   Arguments: {json.dumps(tool_args, indent=2)}")
                    
                    # Execute the tool
                    tool_result = self.mcp_server.execute_tool(tool_name, tool_args)
                    tool_results.append(tool_result)
                    
                    print(f"   Result: {json.dumps(tool_result, indent=2)}\n")
                
                # Add assistant's tool call to history
                self.conversation_history.append(message_response)
                
                # Add tool results to history
                self.conversation_history.append({
                    "role": "tool",
                    "content": json.dumps(tool_results)
                })
                
                # Get final response from model
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
        """
        Set a system prompt for the conversation
        
        Args:
            prompt: System prompt text
        """
        self.conversation_history = [{
            "role": "system",
            "content": prompt
        }]


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
        model_path = os.path.expanduser("~/.vosk/vosk-model-small-en-us-0.15")
        
        # Check if model exists
        if not os.path.exists(model_path):
            print("⏳ Downloading Vosk model (first time only, ~40MB)...", flush=True)
            print("   This will take 30-60 seconds...", flush=True)
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
    """
    Listen for voice input and transcribe using Vosk (fast & offline)
    
    Returns:
        str: Transcribed text, or None if failed
    """
    try:
        # Get Vosk model
        model = get_vosk_model()
        
        # Setup audio
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        stream.start_stream()
        
        # Setup recognizer
        rec = KaldiRecognizer(model, 16000)
        rec.SetMaxAlternatives(0)
        rec.SetWords(False)
        
        print("🎤 Listening... (speak now)", flush=True)
        
        # Record for 5 seconds or until silence
        for _ in range(0, 40):  # 40 * 0.125s = 5 seconds
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                break
        
        # Get final result
        result_json = rec.FinalResult()
        result_dict = json.loads(result_json)
        text = result_dict.get("text", "").strip()
        
        # Cleanup
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
        print("💡 Make sure you've granted microphone permissions to Terminal")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def interactive_mode():
    """Run interactive chat mode with Ollama"""
    config = load_config()
    client = OllamaClient(config)
    
    voice_mode = False  # Toggle for voice responses
    
    print("=" * 60)
    print("🤖 Ollama macOS MCP Interactive Mode")
    print("=" * 60)
    print(f"Model: {client.model}")
    print(f"Available tools: {len(client.mcp_server.tools)}")
    print("\nTools:")
    for tool_name in client.mcp_server.tools.keys():
        print(f"  - {tool_name}")
    print("\nCommands:")
    print("  'quit' or 'exit' - End session")
    print("  'reset' - Clear conversation")
    print("  'tools' - List available tools")
    print("  'voice on/off' - Toggle voice responses")
    print("  'listen' or just press Enter - Voice input")
    print("=" * 60)
    print()
    
    # Set helpful system prompt
    client.set_system_prompt(
        "You are a helpful assistant with access to macOS system tools. "
        "When users ask you to perform system tasks, use the available tools to help them. "
        
        "IMPORTANT RULES:\n"
        "- To find files: Use quick_find_file (FAST), NOT run_shell_command with find\n"
        "- To play music on Spotify: Use play_spotify_track tool only\n"
        "- To open apps: Use open_application tool\n"
        "- To search web: Use smart_search or open_url tools\n"
        "- Always use the fastest, most direct tool\n"
        "- Never use slow shell commands when a fast tool exists\n\n"
        
        "FORMATTING RULES:\n"
        "- Keep responses SHORT and well-structured\n"
        "- Use markdown formatting: headings (##), bullet points (-), code blocks (```)\n"
        "- Break information into clear sections\n"
        "- For system info: use bullet points or short paragraphs\n"
        "- For lists: use bullet points, max 5-10 items unless asked for more\n"
        "- For file paths: use code formatting\n"
        "- Don't repeat all the raw data, summarize key points\n\n"
        
        "Always confirm tool execution briefly and format output clearly."
    )
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            # If empty input, trigger voice input
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
                client.set_system_prompt(
                    "You are a helpful assistant with access to macOS system tools."
                )
                print("🔄 Conversation reset\n")
                if voice_mode:
                    speak_text("Conversation reset")
                continue
            
            if user_input.lower() == 'tools':
                print("\n📋 Available tools:")
                for tool_name, tool in client.mcp_server.tools.items():
                    print(f"\n  {tool_name}:")
                    print(f"    {tool['description']}")
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
            
            # Get response from Ollama
            print("\n🤖 Assistant: ", end="", flush=True)
            response = client.chat(user_input)
            
            if 'error' in response:
                error_msg = f"❌ Error: {response['error']}"
                print(error_msg)
                if voice_mode:
                    speak_text(f"Error: {response['error']}")
            else:
                message = response.get('message', {})
                content = message.get('content', '')
                print(content)
                
                # Speak response if voice mode enabled
                if voice_mode and content:
                    speak_text(content)
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            if voice_mode:
                speak_text("Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == '__main__':
    interactive_mode()

