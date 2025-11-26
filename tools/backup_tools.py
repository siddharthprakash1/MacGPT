"""
Time Machine & Backup Tools
Manage backups and restore
"""

import subprocess


def time_machine_status() -> dict:
    """Get Time Machine backup status"""
    try:
        result = subprocess.run(['tmutil', 'status'],
                              capture_output=True, text=True, check=True, timeout=10)
        
        # Parse status
        status_dict = {}
        for line in result.stdout.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip().strip(';')
                value = value.strip().strip(';').strip('"')
                status_dict[key] = value
        
        return {
            "success": True,
            "status": status_dict,
            "raw": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def start_time_machine_backup() -> dict:
    """Start Time Machine backup now"""
    try:
        subprocess.run(['tmutil', 'startbackup'],
                      check=True, timeout=5)
        return {
            "success": True,
            "message": "Time Machine backup started"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def stop_time_machine_backup() -> dict:
    """Stop Time Machine backup"""
    try:
        subprocess.run(['tmutil', 'stopbackup'],
                      check=True, timeout=5)
        return {
            "success": True,
            "message": "Time Machine backup stopped"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_time_machine_backups() -> dict:
    """List available Time Machine backups"""
    try:
        result = subprocess.run(['tmutil', 'listbackups'],
                              capture_output=True, text=True, check=True, timeout=10)
        
        backups = [b.strip() for b in result.stdout.split('\n') if b.strip()]
        
        return {
            "success": True,
            "count": len(backups),
            "backups": backups[-10:]  # Show last 10
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_latest_backup() -> dict:
    """Get latest Time Machine backup info"""
    try:
        result = subprocess.run(['tmutil', 'latestbackup'],
                              capture_output=True, text=True, check=True, timeout=5)
        
        latest = result.stdout.strip()
        
        return {
            "success": True,
            "latest_backup": latest
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_old_backups(keep_count: int = 5) -> dict:
    """Delete old Time Machine backups (keep most recent X)"""
    try:
        # List all backups
        result = subprocess.run(['tmutil', 'listbackups'],
                              capture_output=True, text=True, check=True, timeout=10)
        
        backups = [b.strip() for b in result.stdout.split('\n') if b.strip()]
        
        if len(backups) <= keep_count:
            return {
                "success": True,
                "message": f"Only {len(backups)} backups exist, keeping all"
            }
        
        # Delete old backups
        to_delete = backups[:-keep_count]
        deleted = []
        
        for backup in to_delete:
            try:
                subprocess.run(['tmutil', 'delete', backup],
                             check=True, timeout=60)
                deleted.append(backup)
            except:
                pass
        
        return {
            "success": True,
            "deleted_count": len(deleted),
            "kept_count": keep_count,
            "message": f"Deleted {len(deleted)} old backups"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def enable_time_machine() -> dict:
    """Enable Time Machine automatic backups"""
    try:
        subprocess.run(['tmutil', 'enable'],
                      check=True, timeout=5)
        return {
            "success": True,
            "message": "Time Machine enabled"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def disable_time_machine() -> dict:
    """Disable Time Machine automatic backups"""
    try:
        subprocess.run(['tmutil', 'disable'],
                      check=True, timeout=5)
        return {
            "success": True,
            "message": "Time Machine disabled"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_backup_destination() -> dict:
    """Get Time Machine backup destination"""
    try:
        result = subprocess.run(['tmutil', 'destinationinfo'],
                              capture_output=True, text=True, check=True, timeout=5)
        
        return {
            "success": True,
            "destination": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def compare_backups(backup1: str = None, backup2: str = None) -> dict:
    """Compare two Time Machine backups"""
    try:
        if not backup1 or not backup2:
            # Get last two backups
            result = subprocess.run(['tmutil', 'listbackups'],
                                  capture_output=True, text=True, check=True, timeout=10)
            backups = [b.strip() for b in result.stdout.split('\n') if b.strip()]
            
            if len(backups) < 2:
                return {"success": False, "error": "Not enough backups to compare"}
            
            backup1 = backups[-2]
            backup2 = backups[-1]
        
        result = subprocess.run(['tmutil', 'compare', backup1, backup2],
                              capture_output=True, text=True, check=True, timeout=30)
        
        return {
            "success": True,
            "backup1": backup1,
            "backup2": backup2,
            "differences": result.stdout[:1000]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

