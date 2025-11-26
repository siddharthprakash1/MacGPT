"""
Screen Recording & Media Tools
Record screen, convert images/videos
"""

import subprocess
import os
from datetime import datetime
from PIL import Image


# Track recording PID
_recording_pid = None


def start_screen_recording(output_path: str = None) -> dict:
    """Start screen recording using built-in screencapture"""
    global _recording_pid
    
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.expanduser(f"~/Desktop/recording_{timestamp}.mov")
        
        # Use screencapture for video (requires user approval)
        process = subprocess.Popen(
            ['screencapture', '-v', output_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        _recording_pid = process.pid
        
        return {
            "success": True,
            "output": output_path,
            "pid": process.pid,
            "message": f"Recording started. Use stop_screen_recording to stop."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def stop_screen_recording() -> dict:
    """Stop screen recording"""
    global _recording_pid
    
    try:
        if _recording_pid:
            subprocess.run(['kill', str(_recording_pid)], check=True)
            _recording_pid = None
            return {
                "success": True,
                "message": "Recording stopped"
            }
        else:
            return {"success": False, "error": "No active recording"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def record_audio(duration: int = 10, output_path: str = None) -> dict:
    """Record audio using sox (requires: brew install sox)"""
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.expanduser(f"~/Desktop/audio_{timestamp}.wav")
        
        # Use rec from sox
        subprocess.run(['rec', output_path, 'trim', '0', str(duration)],
                      check=True, timeout=duration + 5)
        
        return {
            "success": True,
            "output": output_path,
            "duration": duration,
            "message": f"Audio recorded: {output_path}"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "sox not installed. Run: brew install sox"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def resize_image(input_path: str, width: int, height: int, output_path: str = None) -> dict:
    """Resize image to specified dimensions"""
    try:
        if not output_path:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_resized{ext}"
        
        with Image.open(input_path) as img:
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            resized.save(output_path)
        
        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "size": f"{width}x{height}",
            "message": f"Image resized to {width}x{height}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def convert_image_format(input_path: str, output_format: str) -> dict:
    """Convert image to different format (png, jpg, webp, etc.)"""
    try:
        name = os.path.splitext(input_path)[0]
        output_path = f"{name}.{output_format}"
        
        with Image.open(input_path) as img:
            # Convert RGBA to RGB for JPEG
            if output_format.lower() in ['jpg', 'jpeg'] and img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                rgb_img.save(output_path, output_format.upper())
            else:
                img.save(output_path, output_format.upper())
        
        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "format": output_format,
            "message": f"Converted to {output_format}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def compress_image(input_path: str, quality: int = 85, output_path: str = None) -> dict:
    """Compress image to reduce file size"""
    try:
        if not output_path:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_compressed{ext}"
        
        with Image.open(input_path) as img:
            img.save(output_path, optimize=True, quality=quality)
        
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "original_size_mb": round(original_size / 1024 / 1024, 2),
            "compressed_size_mb": round(compressed_size / 1024 / 1024, 2),
            "reduction_percent": round(reduction, 1),
            "message": f"Compressed by {reduction:.1f}%"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_image_info(image_path: str) -> dict:
    """Get image metadata"""
    try:
        with Image.open(image_path) as img:
            return {
                "success": True,
                "path": image_path,
                "format": img.format,
                "mode": img.mode,
                "width": img.width,
                "height": img.height,
                "size": f"{img.width}x{img.height}",
                "file_size_mb": round(os.path.getsize(image_path) / 1024 / 1024, 2)
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_thumbnail(input_path: str, max_size: int = 256) -> dict:
    """Create thumbnail of image"""
    try:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_thumb{ext}"
        
        with Image.open(input_path) as img:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            img.save(output_path)
        
        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "max_size": max_size,
            "message": f"Thumbnail created: {output_path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def convert_video_format(input_path: str, output_format: str = "mp4") -> dict:
    """Convert video format using ffmpeg"""
    try:
        name = os.path.splitext(input_path)[0]
        output_path = f"{name}.{output_format}"
        
        subprocess.run(['ffmpeg', '-i', input_path, output_path, '-y'],
                      check=True, capture_output=True, timeout=300)
        
        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "format": output_format,
            "message": f"Video converted to {output_format}"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "ffmpeg not installed. Already available on your system!"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

