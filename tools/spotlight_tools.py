"""
Spotlight Tools - Advanced macOS Spotlight/mdfind Integration
Leverage the full power of Spotlight's indexing for powerful file operations
"""

import subprocess
import os
from datetime import datetime, timedelta
from typing import Optional, List


def spotlight_advanced_search(
    query: str,
    kind: str = None,
    in_folder: str = None,
    date_filter: str = None,
    size_filter: str = None,
    limit: int = 20
) -> dict:
    """
    Advanced Spotlight search with multiple filters
    
    Args:
        query: Search query (filename or content)
        kind: File type - pdf, image, video, audio, document, folder, app, email
        in_folder: Limit search to specific folder
        date_filter: today, yesterday, week, month, year, or YYYY-MM-DD
        size_filter: large (>100MB), medium (10-100MB), small (<10MB)
        limit: Max results (default 20)
    
    Returns:
        dict: Search results with file paths and metadata
    """
    try:
        # Build mdfind command
        cmd = ['mdfind']
        
        # Add folder restriction
        if in_folder:
            expanded = os.path.expanduser(in_folder)
            cmd.extend(['-onlyin', expanded])
        
        # Build query parts
        query_parts = []
        
        # Main query (search filename and content)
        if query:
            query_parts.append(f'(kMDItemDisplayName == "*{query}*"wcd || kMDItemTextContent == "*{query}*"wcd)')
        
        # File type filter
        kind_map = {
            'pdf': 'kMDItemContentType == "com.adobe.pdf"',
            'image': 'kMDItemContentType == "public.image"',
            'video': 'kMDItemContentType == "public.movie"',
            'audio': 'kMDItemContentType == "public.audio"',
            'document': '(kMDItemContentType == "public.text" || kMDItemContentType == "public.data")',
            'folder': 'kMDItemContentType == "public.folder"',
            'app': 'kMDItemContentType == "com.apple.application-bundle"',
            'email': 'kMDItemContentType == "com.apple.mail.emlx"',
            'presentation': 'kMDItemKind == "Keynote Presentation" || kMDItemKind == "Microsoft PowerPoint Document"',
            'spreadsheet': 'kMDItemKind == "Numbers Spreadsheet" || kMDItemKind == "Microsoft Excel Document"',
            'code': '(kMDItemContentType == "public.source-code" || kMDItemDisplayName == "*.py" || kMDItemDisplayName == "*.js")',
        }
        if kind and kind.lower() in kind_map:
            query_parts.append(kind_map[kind.lower()])
        
        # Date filter
        if date_filter:
            today = datetime.now()
            if date_filter == 'today':
                date_str = today.strftime('%Y-%m-%d')
                query_parts.append(f'kMDItemContentModificationDate >= $time.today')
            elif date_filter == 'yesterday':
                query_parts.append(f'kMDItemContentModificationDate >= $time.yesterday')
            elif date_filter == 'week':
                query_parts.append(f'kMDItemContentModificationDate >= $time.this_week')
            elif date_filter == 'month':
                query_parts.append(f'kMDItemContentModificationDate >= $time.this_month')
            elif date_filter == 'year':
                query_parts.append(f'kMDItemContentModificationDate >= $time.this_year')
            else:
                # Custom date YYYY-MM-DD
                query_parts.append(f'kMDItemContentModificationDate >= $time.iso({date_filter})')
        
        # Size filter
        if size_filter:
            if size_filter == 'large':
                query_parts.append('kMDItemFSSize >= 104857600')  # > 100MB
            elif size_filter == 'medium':
                query_parts.append('kMDItemFSSize >= 10485760 && kMDItemFSSize < 104857600')  # 10-100MB
            elif size_filter == 'small':
                query_parts.append('kMDItemFSSize < 10485760')  # < 10MB
        
        # Combine query parts
        full_query = ' && '.join(query_parts) if query_parts else f'kMDItemDisplayName == "*{query}*"wcd'
        cmd.append(full_query)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        files = [f for f in result.stdout.strip().split('\n') if f][:limit]
        
        return {
            "success": True,
            "count": len(files),
            "query": full_query,
            "files": files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_files_by_date(
    date_range: str,
    file_type: str = None,
    in_folder: str = None,
    limit: int = 25,
    include_hidden: bool = False
) -> dict:
    """
    Find USER files by modification date (excludes system/cache files)
    
    Args:
        date_range: today, yesterday, week, month, year
        file_type: Optional filter (pdf, image, video, audio, document, code)
        in_folder: Limit to specific folder (default: searches user folders)
        limit: Max results
        include_hidden: Include Library/cache files (default: False)
    
    Returns:
        dict: Files matching date criteria
    """
    try:
        home = os.path.expanduser("~")
        
        # Folders to EXCLUDE (system/cache files)
        excluded_patterns = [
            '/Library/',
            '/Caches/',
            '/.Trash/',
            '/.cache/',
            '/node_modules/',
            '/.git/',
            '/venv/',
            '/.venv/',
            '/site-packages/',
            '/__pycache__/',
            '/Application Support/',
            '/Containers/',
            '/Saved Application State/',
            '/Logs/',
            '/.npm/',
            '/.cursor/',
            '/HTTPStorages/',
            '-journal',  # SQLite journals
            '.log.',
        ]
        
        # User work folders to search if no folder specified
        user_folders = [
            os.path.join(home, 'Desktop'),
            os.path.join(home, 'Documents'),
            os.path.join(home, 'Downloads'),
            os.path.join(home, 'Projects'),
            os.path.join(home, 'Developer'),
            os.path.join(home, 'Code'),
        ]
        
        all_files = []
        
        # Date queries
        date_queries = {
            'today': 'kMDItemContentModificationDate >= $time.today',
            'yesterday': 'kMDItemContentModificationDate >= $time.yesterday && kMDItemContentModificationDate < $time.today',
            'week': 'kMDItemContentModificationDate >= $time.this_week',
            'month': 'kMDItemContentModificationDate >= $time.this_month',
            'year': 'kMDItemContentModificationDate >= $time.this_year',
        }
        
        base_query = date_queries.get(date_range, f'kMDItemContentModificationDate >= $time.iso({date_range})')
        
        # Add file type filter
        if file_type:
            type_map = {
                'pdf': 'com.adobe.pdf',
                'image': 'public.image',
                'video': 'public.movie',
                'audio': 'public.audio',
                'document': 'public.text',
                'code': 'public.source-code',
            }
            if file_type in type_map:
                base_query += f' && kMDItemContentType == "{type_map[file_type]}"'
        
        # Search specific folder or user folders
        if in_folder:
            search_folders = [os.path.expanduser(in_folder)]
        else:
            # Search common user work folders
            search_folders = [f for f in user_folders if os.path.exists(f)]
            # Also add any folders in Desktop/Personal or similar
            personal_path = os.path.join(home, 'Desktop', 'Personal')
            if os.path.exists(personal_path):
                search_folders.append(personal_path)
        
        for folder in search_folders:
            cmd = ['mdfind', '-onlyin', folder, base_query]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            files = [f for f in result.stdout.strip().split('\n') if f]
            all_files.extend(files)
        
        # Filter out system/cache files unless include_hidden
        if not include_hidden:
            filtered_files = []
            for f in all_files:
                # Skip files matching excluded patterns
                if any(pattern in f for pattern in excluded_patterns):
                    continue
                # Skip hidden files/folders (starting with .)
                parts = f.split('/')
                if any(part.startswith('.') and part != '.' for part in parts[3:]):  # Skip after /Users/name/
                    continue
                filtered_files.append(f)
            all_files = filtered_files
        
        # Remove duplicates and limit
        all_files = list(dict.fromkeys(all_files))[:limit]
        
        return {
            "success": True,
            "date_range": date_range,
            "count": len(all_files),
            "searched_folders": search_folders,
            "files": all_files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_large_files(
    min_size_mb: int = 100,
    in_folder: str = None,
    file_type: str = None,
    limit: int = 30
) -> dict:
    """
    Find large files for disk cleanup - incredibly useful!
    
    Args:
        min_size_mb: Minimum file size in MB (default 100MB)
        in_folder: Limit search to folder (default: home directory)
        file_type: Optional filter (video, image, archive, etc.)
        limit: Max results
    
    Returns:
        dict: Large files with sizes
    """
    try:
        cmd = ['mdfind']
        
        folder = in_folder or '~'
        cmd.extend(['-onlyin', os.path.expanduser(folder)])
        
        # Convert MB to bytes
        size_bytes = min_size_mb * 1024 * 1024
        query = f'kMDItemFSSize >= {size_bytes}'
        
        # Add file type filter
        if file_type:
            type_map = {
                'video': 'public.movie',
                'image': 'public.image',
                'archive': 'public.archive',
                'disk_image': 'public.disk-image',
                'audio': 'public.audio',
            }
            if file_type in type_map:
                query += f' && kMDItemContentType == "{type_map[file_type]}"'
        
        cmd.append(query)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        file_paths = [f for f in result.stdout.strip().split('\n') if f][:limit]
        
        # Get file sizes
        files_with_sizes = []
        for path in file_paths:
            try:
                size = os.path.getsize(path)
                size_mb = size / (1024 * 1024)
                size_gb = size / (1024 * 1024 * 1024)
                files_with_sizes.append({
                    "path": path,
                    "size": f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.1f} MB"
                })
            except:
                files_with_sizes.append({"path": path, "size": "unknown"})
        
        # Sort by size (largest first)
        files_with_sizes.sort(key=lambda x: os.path.getsize(x["path"]) if os.path.exists(x["path"]) else 0, reverse=True)
        
        total_size = sum(os.path.getsize(f["path"]) for f in files_with_sizes if os.path.exists(f["path"]))
        total_gb = total_size / (1024 * 1024 * 1024)
        
        return {
            "success": True,
            "min_size_mb": min_size_mb,
            "count": len(files_with_sizes),
            "total_size": f"{total_gb:.2f} GB",
            "files": files_with_sizes
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_by_content(
    text: str,
    file_type: str = None,
    in_folder: str = None,
    limit: int = 20
) -> dict:
    """
    Full-text content search - search INSIDE files
    
    Args:
        text: Text to search for inside files
        file_type: Limit to specific type (pdf, document, etc.)
        in_folder: Limit to folder
        limit: Max results
    
    Returns:
        dict: Files containing the text
    """
    try:
        cmd = ['mdfind']
        
        if in_folder:
            cmd.extend(['-onlyin', os.path.expanduser(in_folder)])
        
        # Content search query
        query = f'kMDItemTextContent == "*{text}*"wcd'
        
        if file_type:
            type_map = {
                'pdf': 'com.adobe.pdf',
                'document': 'public.text',
                'email': 'com.apple.mail.emlx',
                'note': 'com.apple.notes.note',
            }
            if file_type in type_map:
                query += f' && kMDItemContentType == "{type_map[file_type]}"'
        
        cmd.append(query)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        files = [f for f in result.stdout.strip().split('\n') if f][:limit]
        
        return {
            "success": True,
            "search_text": text,
            "count": len(files),
            "files": files,
            "message": f"Found {len(files)} files containing '{text}'"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_by_author(author: str, in_folder: str = None, limit: int = 20) -> dict:
    """
    Find documents by author name
    
    Args:
        author: Author name to search for
        in_folder: Limit to folder
        limit: Max results
    
    Returns:
        dict: Documents by this author
    """
    try:
        cmd = ['mdfind']
        
        if in_folder:
            cmd.extend(['-onlyin', os.path.expanduser(in_folder)])
        
        query = f'kMDItemAuthors == "*{author}*"wcd'
        cmd.append(query)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        files = [f for f in result.stdout.strip().split('\n') if f][:limit]
        
        return {
            "success": True,
            "author": author,
            "count": len(files),
            "files": files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_downloads_from_site(domain: str, limit: int = 20) -> dict:
    """
    Find files downloaded from a specific website
    
    Args:
        domain: Domain name (e.g., 'github.com', 'google.com')
        limit: Max results
    
    Returns:
        dict: Files downloaded from that site
    """
    try:
        # Search in Downloads folder for files with WhereFroms metadata
        cmd = ['mdfind', '-onlyin', os.path.expanduser('~/Downloads'),
               f'kMDItemWhereFroms == "*{domain}*"wcd']
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        files = [f for f in result.stdout.strip().split('\n') if f][:limit]
        
        return {
            "success": True,
            "domain": domain,
            "count": len(files),
            "files": files,
            "message": f"Found {len(files)} files downloaded from {domain}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_recent_opened(hours: int = 24, file_type: str = None, limit: int = 25) -> dict:
    """
    Find recently opened USER files (excludes system/cache files)
    
    Args:
        hours: Within last N hours (default 24)
        file_type: Optional type filter (pdf, image, video, document, code)
        limit: Max results
    
    Returns:
        dict: Recently opened files
    """
    try:
        home = os.path.expanduser("~")
        
        # Patterns to exclude (system/cache files)
        excluded_patterns = [
            '/Library/',
            '/Caches/',
            '/.Trash/',
            '/.cache/',
            '/node_modules/',
            '/.git/',
            '/Application Support/',
            '/Containers/',
            '/Logs/',
            '/.cursor/',
            '-journal',
            '.log',
            '/HTTPStorages/',
        ]
        
        # Build query
        query = f'kMDItemLastUsedDate >= $time.now(-{hours * 3600})'
        
        if file_type:
            type_map = {
                'pdf': 'com.adobe.pdf',
                'image': 'public.image',
                'video': 'public.movie',
                'document': 'public.text',
                'code': 'public.source-code',
                'audio': 'public.audio',
            }
            if file_type in type_map:
                query += f' && kMDItemContentType == "{type_map[file_type]}"'
        
        # Search in user's home directory
        cmd = ['mdfind', '-onlyin', home, query]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        all_files = [f for f in result.stdout.strip().split('\n') if f]
        
        # Filter out system/cache files
        filtered_files = []
        for f in all_files:
            if any(pattern in f for pattern in excluded_patterns):
                continue
            # Skip hidden files in user directory
            rel_path = f[len(home)+1:] if f.startswith(home) else f
            if rel_path.startswith('.'):
                continue
            filtered_files.append(f)
        
        # Limit results
        filtered_files = filtered_files[:limit]
        
        return {
            "success": True,
            "hours": hours,
            "count": len(filtered_files),
            "files": filtered_files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_file_metadata(file_path: str) -> dict:
    """
    Get all Spotlight metadata for a file
    
    Args:
        file_path: Path to file
    
    Returns:
        dict: All available metadata
    """
    try:
        expanded = os.path.expanduser(file_path)
        
        # Use mdls to get all metadata
        result = subprocess.run(['mdls', expanded], capture_output=True, text=True, timeout=5)
        
        if result.returncode != 0:
            return {"success": False, "error": "Could not read metadata"}
        
        # Parse metadata
        metadata = {}
        for line in result.stdout.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')
                # Clean up key names
                clean_key = key.replace('kMDItem', '').strip()
                if value and value != '(null)':
                    metadata[clean_key] = value
        
        return {
            "success": True,
            "file": expanded,
            "metadata": metadata
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_duplicates_by_name(in_folder: str = None, extension: str = None, limit: int = 50) -> dict:
    """
    Find potential duplicate files by similar names
    
    Args:
        in_folder: Folder to search (default: home)
        extension: File extension to filter (e.g., '.pdf')
        limit: Max files to analyze
    
    Returns:
        dict: Groups of potentially duplicate files
    """
    try:
        cmd = ['mdfind']
        
        folder = in_folder or '~'
        cmd.extend(['-onlyin', os.path.expanduser(folder)])
        
        if extension:
            cmd.append(f'kMDItemDisplayName == "*{extension}"')
        else:
            cmd.append('kMDItemContentType != "public.folder"')
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        all_files = [f for f in result.stdout.strip().split('\n') if f][:limit * 10]
        
        # Group by filename (without path)
        name_groups = {}
        for file_path in all_files:
            name = os.path.basename(file_path)
            # Remove common suffixes like " (1)", " copy", etc.
            import re
            clean_name = re.sub(r'\s*(\(\d+\)|copy|Copy|\-\d+)(\.[^.]+)?$', r'\2', name)
            if clean_name not in name_groups:
                name_groups[clean_name] = []
            name_groups[clean_name].append(file_path)
        
        # Filter to only groups with potential duplicates
        duplicates = {name: paths for name, paths in name_groups.items() if len(paths) > 1}
        
        # Limit and format results
        dup_list = list(duplicates.items())[:limit]
        
        return {
            "success": True,
            "potential_duplicates_groups": len(dup_list),
            "duplicates": dict(dup_list),
            "message": f"Found {len(dup_list)} groups of potential duplicates"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def spotlight_natural_search(query: str, limit: int = 20) -> dict:
    """
    Natural language search - interprets everyday language
    
    Examples:
        - "PDFs from last week"
        - "large video files"
        - "images in Downloads"
        - "documents about project"
        - "music files over 10MB"
    
    Args:
        query: Natural language query
        limit: Max results
    
    Returns:
        dict: Search results
    """
    try:
        query_lower = query.lower()
        
        # Parse natural language
        mdfind_query_parts = []
        folder = None
        
        # Detect file types
        if 'pdf' in query_lower:
            mdfind_query_parts.append('kMDItemContentType == "com.adobe.pdf"')
        elif 'image' in query_lower or 'photo' in query_lower or 'picture' in query_lower:
            mdfind_query_parts.append('kMDItemContentType == "public.image"')
        elif 'video' in query_lower or 'movie' in query_lower:
            mdfind_query_parts.append('kMDItemContentType == "public.movie"')
        elif 'music' in query_lower or 'audio' in query_lower or 'song' in query_lower:
            mdfind_query_parts.append('kMDItemContentType == "public.audio"')
        elif 'document' in query_lower or 'doc' in query_lower:
            mdfind_query_parts.append('(kMDItemContentType == "public.text" || kMDItemKind == "Microsoft Word Document")')
        elif 'spreadsheet' in query_lower or 'excel' in query_lower:
            mdfind_query_parts.append('kMDItemKind == "*Excel*" || kMDItemKind == "*Numbers*"')
        elif 'presentation' in query_lower or 'powerpoint' in query_lower or 'keynote' in query_lower:
            mdfind_query_parts.append('kMDItemKind == "*Keynote*" || kMDItemKind == "*PowerPoint*"')
        
        # Detect time ranges
        if 'today' in query_lower:
            mdfind_query_parts.append('kMDItemContentModificationDate >= $time.today')
        elif 'yesterday' in query_lower:
            mdfind_query_parts.append('kMDItemContentModificationDate >= $time.yesterday')
        elif 'week' in query_lower or 'this week' in query_lower or 'last week' in query_lower:
            mdfind_query_parts.append('kMDItemContentModificationDate >= $time.this_week')
        elif 'month' in query_lower or 'this month' in query_lower:
            mdfind_query_parts.append('kMDItemContentModificationDate >= $time.this_month')
        elif 'year' in query_lower:
            mdfind_query_parts.append('kMDItemContentModificationDate >= $time.this_year')
        
        # Detect size
        if 'large' in query_lower or 'big' in query_lower:
            mdfind_query_parts.append('kMDItemFSSize >= 104857600')  # > 100MB
        elif 'small' in query_lower or 'tiny' in query_lower:
            mdfind_query_parts.append('kMDItemFSSize < 1048576')  # < 1MB
        
        # Size with numbers
        import re
        size_match = re.search(r'(\d+)\s*(?:mb|MB)', query_lower)
        if size_match:
            size_mb = int(size_match.group(1))
            if 'over' in query_lower or 'more than' in query_lower or '>' in query:
                mdfind_query_parts.append(f'kMDItemFSSize >= {size_mb * 1024 * 1024}')
            elif 'under' in query_lower or 'less than' in query_lower or '<' in query:
                mdfind_query_parts.append(f'kMDItemFSSize < {size_mb * 1024 * 1024}')
        
        # Detect folders
        if 'download' in query_lower:
            folder = '~/Downloads'
        elif 'desktop' in query_lower:
            folder = '~/Desktop'
        elif 'document' in query_lower and 'folder' in query_lower:
            folder = '~/Documents'
        
        # Extract keywords for content search
        # Remove common words
        stop_words = {'find', 'search', 'get', 'show', 'list', 'all', 'the', 'in', 'from', 
                     'pdf', 'image', 'video', 'audio', 'large', 'small', 'file', 'files',
                     'today', 'yesterday', 'week', 'month', 'year', 'download', 'desktop',
                     'document', 'folder', 'last', 'this', 'recent', 'big', 'over', 'under',
                     'mb', 'about', 'with', 'and', 'or', 'containing'}
        
        words = re.findall(r'\b\w+\b', query_lower)
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        if keywords:
            keyword = keywords[0]  # Use first meaningful keyword
            mdfind_query_parts.append(f'(kMDItemDisplayName == "*{keyword}*"wcd || kMDItemTextContent == "*{keyword}*"wcd)')
        
        # Build command
        cmd = ['mdfind']
        if folder:
            cmd.extend(['-onlyin', os.path.expanduser(folder)])
        
        final_query = ' && '.join(mdfind_query_parts) if mdfind_query_parts else f'kMDItemDisplayName == "*"'
        cmd.append(final_query)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        files = [f for f in result.stdout.strip().split('\n') if f][:limit]
        
        return {
            "success": True,
            "original_query": query,
            "interpreted_query": final_query,
            "folder_filter": folder,
            "count": len(files),
            "files": files
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_apps_using_disk_space(limit: int = 20) -> dict:
    """
    Find ALL applications sorted by disk usage - scans all app locations
    
    Args:
        limit: Max results
    
    Returns:
        dict: Apps with their sizes, sorted largest first
    """
    try:
        apps = []
        seen_apps = set()  # Avoid duplicates
        
        # All common app locations on macOS
        app_locations = [
            '/Applications',
            os.path.expanduser('~/Applications'),
            '/System/Applications',
            '/System/Applications/Utilities',
            # Homebrew cask locations
            '/opt/homebrew/Caskroom',
            '/usr/local/Caskroom',
        ]
        
        def get_app_size(app_path):
            """Get size of app bundle"""
            try:
                result = subprocess.run(['du', '-sk', app_path], 
                                       capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return int(result.stdout.split()[0])
            except:
                pass
            return 0
        
        # Scan each location
        for location in app_locations:
            if not os.path.exists(location):
                continue
                
            try:
                for item in os.listdir(location):
                    item_path = os.path.join(location, item)
                    
                    # Handle .app bundles directly
                    if item.endswith('.app'):
                        app_name = item
                        if app_name not in seen_apps:
                            seen_apps.add(app_name)
                            size_kb = get_app_size(item_path)
                            if size_kb > 0:
                                size_mb = size_kb / 1024
                                size_gb = size_mb / 1024
                                apps.append({
                                    "name": app_name.replace('.app', ''),
                                    "path": item_path,
                                    "size_mb": round(size_mb, 1),
                                    "size_display": f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.0f} MB",
                                    "location": location
                                })
                    
                    # Handle Homebrew Caskroom structure (app_name/version/App.app)
                    elif os.path.isdir(item_path) and 'Caskroom' in location:
                        try:
                            for version in os.listdir(item_path):
                                version_path = os.path.join(item_path, version)
                                if os.path.isdir(version_path):
                                    for app in os.listdir(version_path):
                                        if app.endswith('.app'):
                                            full_app_path = os.path.join(version_path, app)
                                            if app not in seen_apps:
                                                seen_apps.add(app)
                                                size_kb = get_app_size(full_app_path)
                                                if size_kb > 0:
                                                    size_mb = size_kb / 1024
                                                    size_gb = size_mb / 1024
                                                    apps.append({
                                                        "name": app.replace('.app', ''),
                                                        "path": full_app_path,
                                                        "size_mb": round(size_mb, 1),
                                                        "size_display": f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.0f} MB",
                                                        "location": "Homebrew Cask"
                                                    })
                        except:
                            pass
            except PermissionError:
                continue
        
        # Sort by size (largest first)
        apps.sort(key=lambda x: x['size_mb'], reverse=True)
        top_apps = apps[:limit]
        
        total_mb = sum(a['size_mb'] for a in top_apps)
        total_all = sum(a['size_mb'] for a in apps)
        
        return {
            "success": True,
            "total_apps_found": len(apps),
            "showing": len(top_apps),
            "top_apps_size": f"{total_mb/1024:.2f} GB",
            "all_apps_size": f"{total_all/1024:.2f} GB",
            "apps": top_apps
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_unused_apps(days_unused: int = 90, limit: int = 25) -> dict:
    """
    Find apps that haven't been opened in X days - scans all app locations
    
    Args:
        days_unused: Days since last use (default 90)
        limit: Max results
    
    Returns:
        dict: Unused apps with sizes
    """
    try:
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_unused)
        unused_apps = []
        
        # All app locations
        app_locations = [
            '/Applications',
            os.path.expanduser('~/Applications'),
        ]
        
        def get_last_used(app_path):
            """Get last used date from Spotlight metadata"""
            try:
                result = subprocess.run(['mdls', '-name', 'kMDItemLastUsedDate', app_path],
                                       capture_output=True, text=True, timeout=3)
                output = result.stdout.strip()
                if '(null)' not in output and '=' in output:
                    date_str = output.split('=')[1].strip()
                    # Parse: 2024-01-15 10:30:00 +0000
                    date_part = ' '.join(date_str.split()[:2])
                    return datetime.strptime(date_part, '%Y-%m-%d %H:%M:%S')
            except:
                pass
            return None
        
        def get_app_size(app_path):
            """Get size of app bundle"""
            try:
                result = subprocess.run(['du', '-sk', app_path], 
                                       capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return int(result.stdout.split()[0])
            except:
                pass
            return 0
        
        # Scan app locations
        for location in app_locations:
            if not os.path.exists(location):
                continue
            
            try:
                for item in os.listdir(location):
                    if item.endswith('.app'):
                        app_path = os.path.join(location, item)
                        
                        last_used = get_last_used(app_path)
                        
                        # If never used or used before cutoff
                        if last_used is None or last_used < cutoff_date:
                            size_kb = get_app_size(app_path)
                            size_mb = size_kb / 1024
                            size_gb = size_mb / 1024
                            
                            unused_apps.append({
                                "name": item.replace('.app', ''),
                                "path": app_path,
                                "size_mb": round(size_mb, 1),
                                "size_display": f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.0f} MB",
                                "last_used": last_used.strftime('%Y-%m-%d') if last_used else "Never",
                                "location": location
                            })
            except PermissionError:
                continue
        
        # Sort by size (largest unused apps first - best cleanup candidates)
        unused_apps.sort(key=lambda x: x['size_mb'], reverse=True)
        top_unused = unused_apps[:limit]
        
        total_mb = sum(a['size_mb'] for a in top_unused)
        
        return {
            "success": True,
            "days_unused": days_unused,
            "total_unused_apps": len(unused_apps),
            "showing": len(top_unused),
            "potential_space_savings": f"{total_mb/1024:.2f} GB",
            "apps": top_unused,
            "message": f"Found {len(unused_apps)} apps not used in {days_unused} days. Could free up {total_mb/1024:.2f} GB!"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

