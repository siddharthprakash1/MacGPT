"""
Database Tools
Query Postgres, MySQL, MongoDB, Redis
"""

import subprocess
import json


def postgres_query(query: str, database: str = "postgres", user: str = "postgres", host: str = "localhost") -> dict:
    """
    Execute PostgreSQL query
    
    Args:
        query: SQL query to execute
        database: Database name
        user: Username
        host: Host address
    """
    try:
        result = subprocess.run(
            ['psql', '-U', user, '-h', host, '-d', database, '-t', '-c', query],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        return {
            "success": True,
            "database": database,
            "result": result.stdout.strip(),
            "rows": len([r for r in result.stdout.strip().split('\n') if r.strip()])
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "PostgreSQL not installed. Run: brew install postgresql"
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr.strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mysql_query(query: str, database: str = "mysql", user: str = "root", password: str = "", host: str = "localhost") -> dict:
    """
    Execute MySQL query
    
    Args:
        query: SQL query to execute
        database: Database name
        user: Username
        password: Password
        host: Host address
    """
    try:
        cmd = ['mysql', '-u', user, '-h', host, '-D', database, '-e', query]
        if password:
            cmd.insert(2, f'-p{password}')
        
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, check=True, timeout=30
        )
        
        return {
            "success": True,
            "database": database,
            "result": result.stdout.strip(),
            "rows": len([r for r in result.stdout.strip().split('\n') if r.strip()]) - 1  # Subtract header
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "MySQL not installed. Run: brew install mysql"
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr.strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mongodb_find(collection: str, query: str = "{}", database: str = "test", host: str = "localhost", port: int = 27017) -> dict:
    """
    Find documents in MongoDB
    
    Args:
        collection: Collection name
        query: Query in JSON format
        database: Database name
        host: Host address
        port: Port number
    """
    try:
        # Use mongosh (new) or mongo (old)
        cmd = f'db.{collection}.find({query}).limit(10)'
        
        result = subprocess.run(
            ['mongosh', f'mongodb://{host}:{port}/{database}', '--quiet', '--eval', cmd],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        return {
            "success": True,
            "database": database,
            "collection": collection,
            "result": result.stdout.strip()
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "MongoDB not installed. Run: brew install mongodb-community"
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr.strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mongodb_insert(collection: str, document: str, database: str = "test", host: str = "localhost", port: int = 27017) -> dict:
    """
    Insert document into MongoDB
    
    Args:
        collection: Collection name
        document: Document in JSON format
        database: Database name
        host: Host address
        port: Port number
    """
    try:
        cmd = f'db.{collection}.insertOne({document})'
        
        result = subprocess.run(
            ['mongosh', f'mongodb://{host}:{port}/{database}', '--quiet', '--eval', cmd],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        return {
            "success": True,
            "database": database,
            "collection": collection,
            "result": result.stdout.strip(),
            "message": "Document inserted"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def redis_get(key: str, host: str = "localhost", port: int = 6379) -> dict:
    """
    Get value from Redis
    
    Args:
        key: Key name
        host: Host address
        port: Port number
    """
    try:
        result = subprocess.run(
            ['redis-cli', '-h', host, '-p', str(port), 'GET', key],
            capture_output=True, text=True, check=True, timeout=10
        )
        
        value = result.stdout.strip()
        
        return {
            "success": True,
            "key": key,
            "value": value if value != "(nil)" else None
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Redis not installed. Run: brew install redis"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def redis_set(key: str, value: str, host: str = "localhost", port: int = 6379, expire: int = None) -> dict:
    """
    Set value in Redis
    
    Args:
        key: Key name
        value: Value to set
        host: Host address
        port: Port number
        expire: Expiration in seconds (optional)
    """
    try:
        cmd = ['redis-cli', '-h', host, '-p', str(port), 'SET', key, value]
        
        if expire:
            cmd.extend(['EX', str(expire)])
        
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, check=True, timeout=10
        )
        
        return {
            "success": True,
            "key": key,
            "value": value,
            "expire": expire,
            "message": "Key set successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def redis_delete(key: str, host: str = "localhost", port: int = 6379) -> dict:
    """Delete key from Redis"""
    try:
        result = subprocess.run(
            ['redis-cli', '-h', host, '-p', str(port), 'DEL', key],
            capture_output=True, text=True, check=True, timeout=10
        )
        
        deleted = int(result.stdout.strip())
        
        return {
            "success": True,
            "key": key,
            "deleted": deleted > 0,
            "message": f"Key {'deleted' if deleted else 'not found'}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def redis_keys(pattern: str = "*", host: str = "localhost", port: int = 6379) -> dict:
    """List Redis keys matching pattern"""
    try:
        result = subprocess.run(
            ['redis-cli', '-h', host, '-p', str(port), 'KEYS', pattern],
            capture_output=True, text=True, check=True, timeout=10
        )
        
        keys = [k.strip() for k in result.stdout.split('\n') if k.strip()]
        
        return {
            "success": True,
            "pattern": pattern,
            "count": len(keys),
            "keys": keys[:50]  # Show first 50
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def postgres_list_databases(user: str = "postgres", host: str = "localhost") -> dict:
    """List all PostgreSQL databases"""
    try:
        result = subprocess.run(
            ['psql', '-U', user, '-h', host, '-l', '-t'],
            capture_output=True, text=True, check=True, timeout=10
        )
        
        databases = []
        for line in result.stdout.split('\n'):
            if line.strip():
                parts = line.split('|')
                if len(parts) > 0:
                    databases.append(parts[0].strip())
        
        return {
            "success": True,
            "count": len(databases),
            "databases": databases
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mysql_list_databases(user: str = "root", password: str = "", host: str = "localhost") -> dict:
    """List all MySQL databases"""
    try:
        cmd = ['mysql', '-u', user, '-h', host, '-e', 'SHOW DATABASES;']
        if password:
            cmd.insert(2, f'-p{password}')
        
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, check=True, timeout=10
        )
        
        databases = [db.strip() for db in result.stdout.split('\n')[1:] if db.strip()]
        
        return {
            "success": True,
            "count": len(databases),
            "databases": databases
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def mongodb_list_collections(database: str = "test", host: str = "localhost", port: int = 27017) -> dict:
    """List all collections in MongoDB database"""
    try:
        cmd = 'db.getCollectionNames()'
        
        result = subprocess.run(
            ['mongosh', f'mongodb://{host}:{port}/{database}', '--quiet', '--eval', cmd],
            capture_output=True, text=True, check=True, timeout=10
        )
        
        return {
            "success": True,
            "database": database,
            "collections": result.stdout.strip()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

