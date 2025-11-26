"""
Advanced File Operations
Zip, move, copy, rename, and more
"""

import subprocess
import os
import shutil
import zipfile
import tarfile
from pathlib import Path


def compress_files(files: list, output_name: str, format: str = "zip") -> dict:
    """
    Compress files into archive
    
    Args:
        files: List of file paths
        output_name: Output archive name
        format: 'zip' or 'tar.gz'
    """
    try:
        if format == "zip":
            with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    if os.path.exists(file):
                        zipf.write(file, os.path.basename(file))
        elif format == "tar.gz":
            with tarfile.open(output_name, 'w:gz') as tar:
                for file in files:
                    if os.path.exists(file):
                        tar.add(file, arcname=os.path.basename(file))
        
        return {
            "success": True,
            "archive": output_name,
            "files_compressed": len(files),
            "message": f"Created {output_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_archive(archive_path: str, destination: str = ".") -> dict:
    """Extract zip or tar.gz archive"""
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(destination)
        elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(destination)
        
        return {
            "success": True,
            "archive": archive_path,
            "destination": destination,
            "message": f"Extracted to {destination}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def move_file(source: str, destination: str) -> dict:
    """Move file or directory"""
    try:
        shutil.move(source, destination)
        return {
            "success": True,
            "source": source,
            "destination": destination,
            "message": f"Moved {source} to {destination}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def copy_file(source: str, destination: str) -> dict:
    """Copy file or directory"""
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        
        return {
            "success": True,
            "source": source,
            "destination": destination,
            "message": f"Copied {source} to {destination}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def rename_file(old_path: str, new_name: str) -> dict:
    """Rename file or directory"""
    try:
        directory = os.path.dirname(old_path)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        
        return {
            "success": True,
            "old_path": old_path,
            "new_path": new_path,
            "message": f"Renamed to {new_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def duplicate_file(file_path: str) -> dict:
    """Duplicate file (adds 'copy' to name)"""
    try:
        path = Path(file_path)
        new_name = f"{path.stem}_copy{path.suffix}"
        new_path = path.parent / new_name
        
        shutil.copy2(file_path, new_path)
        
        return {
            "success": True,
            "original": file_path,
            "duplicate": str(new_path),
            "message": f"Created duplicate: {new_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_file_info(file_path: str) -> dict:
    """Get detailed file information"""
    try:
        stat = os.stat(file_path)
        
        return {
            "success": True,
            "path": file_path,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / 1024 / 1024, 2),
            "created": stat.st_birthtime,
            "modified": stat.st_mtime,
            "is_directory": os.path.isdir(file_path),
            "extension": os.path.splitext(file_path)[1]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def bulk_rename(directory: str, pattern: str, replacement: str) -> dict:
    """Bulk rename files in directory"""
    try:
        count = 0
        renamed = []
        
        for filename in os.listdir(directory):
            if pattern in filename:
                old_path = os.path.join(directory, filename)
                new_filename = filename.replace(pattern, replacement)
                new_path = os.path.join(directory, new_filename)
                
                os.rename(old_path, new_path)
                renamed.append({"old": filename, "new": new_filename})
                count += 1
        
        return {
            "success": True,
            "count": count,
            "renamed": renamed,
            "message": f"Renamed {count} files"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_file(file_path: str) -> dict:
    """Delete file or directory"""
    try:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
        
        return {
            "success": True,
            "path": file_path,
            "message": f"Deleted {file_path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_files_by_extension(directory: str, extension: str) -> dict:
    """Find all files with specific extension"""
    try:
        files = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(extension):
                    files.append(os.path.join(root, filename))
        
        return {
            "success": True,
            "extension": extension,
            "count": len(files),
            "files": files[:50]  # Limit to first 50
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

