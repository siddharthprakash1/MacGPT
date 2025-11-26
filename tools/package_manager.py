"""
Package Manager Tools
Brew, npm, pip management
"""

import subprocess


def brew_install(package: str) -> dict:
    """Install package via Homebrew"""
    try:
        result = subprocess.run(['brew', 'install', package],
                              capture_output=True, text=True, check=True, timeout=300)
        return {
            "success": True,
            "package": package,
            "message": f"Installed {package}",
            "output": result.stdout[:500]
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def brew_uninstall(package: str) -> dict:
    """Uninstall package via Homebrew"""
    try:
        result = subprocess.run(['brew', 'uninstall', package],
                              capture_output=True, text=True, check=True, timeout=60)
        return {
            "success": True,
            "package": package,
            "message": f"Uninstalled {package}",
            "output": result.stdout[:500]
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def brew_update() -> dict:
    """Update Homebrew"""
    try:
        result = subprocess.run(['brew', 'update'],
                              capture_output=True, text=True, check=True, timeout=180)
        return {
            "success": True,
            "message": "Homebrew updated",
            "output": result.stdout[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def brew_upgrade(package: str = None) -> dict:
    """Upgrade package(s) via Homebrew"""
    try:
        cmd = ['brew', 'upgrade']
        if package:
            cmd.append(package)
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
        return {
            "success": True,
            "message": f"Upgraded {package if package else 'all packages'}",
            "output": result.stdout[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def brew_list() -> dict:
    """List installed Homebrew packages"""
    try:
        result = subprocess.run(['brew', 'list'],
                              capture_output=True, text=True, check=True, timeout=10)
        packages = result.stdout.strip().split('\n')
        return {
            "success": True,
            "count": len(packages),
            "packages": packages[:50]  # Show first 50
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def brew_search(query: str) -> dict:
    """Search for Homebrew packages"""
    try:
        result = subprocess.run(['brew', 'search', query],
                              capture_output=True, text=True, check=True, timeout=30)
        return {
            "success": True,
            "query": query,
            "results": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def brew_info(package: str) -> dict:
    """Get info about a Homebrew package"""
    try:
        result = subprocess.run(['brew', 'info', package],
                              capture_output=True, text=True, check=True, timeout=10)
        return {
            "success": True,
            "package": package,
            "info": result.stdout[:1000]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def npm_install_global(package: str) -> dict:
    """Install npm package globally"""
    try:
        result = subprocess.run(['npm', 'install', '-g', package],
                              capture_output=True, text=True, check=True, timeout=180)
        return {
            "success": True,
            "package": package,
            "message": f"Installed {package} globally",
            "output": result.stdout[:500]
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def npm_uninstall_global(package: str) -> dict:
    """Uninstall npm package globally"""
    try:
        result = subprocess.run(['npm', 'uninstall', '-g', package],
                              capture_output=True, text=True, check=True, timeout=60)
        return {
            "success": True,
            "package": package,
            "message": f"Uninstalled {package}",
            "output": result.stdout[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def npm_list_global() -> dict:
    """List globally installed npm packages"""
    try:
        result = subprocess.run(['npm', 'list', '-g', '--depth=0'],
                              capture_output=True, text=True, check=True, timeout=10)
        return {
            "success": True,
            "packages": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def npm_update_global() -> dict:
    """Update all global npm packages"""
    try:
        result = subprocess.run(['npm', 'update', '-g'],
                              capture_output=True, text=True, check=True, timeout=180)
        return {
            "success": True,
            "message": "Global npm packages updated",
            "output": result.stdout[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def pip_install(package: str) -> dict:
    """Install Python package via pip"""
    try:
        result = subprocess.run(['pip', 'install', package],
                              capture_output=True, text=True, check=True, timeout=180)
        return {
            "success": True,
            "package": package,
            "message": f"Installed {package}",
            "output": result.stdout[:500]
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def pip_uninstall(package: str) -> dict:
    """Uninstall Python package via pip"""
    try:
        result = subprocess.run(['pip', 'uninstall', '-y', package],
                              capture_output=True, text=True, check=True, timeout=60)
        return {
            "success": True,
            "package": package,
            "message": f"Uninstalled {package}",
            "output": result.stdout[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def pip_list() -> dict:
    """List installed Python packages"""
    try:
        result = subprocess.run(['pip', 'list'],
                              capture_output=True, text=True, check=True, timeout=10)
        return {
            "success": True,
            "packages": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def pip_outdated() -> dict:
    """List outdated Python packages"""
    try:
        result = subprocess.run(['pip', 'list', '--outdated'],
                              capture_output=True, text=True, check=True, timeout=30)
        return {
            "success": True,
            "outdated": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

