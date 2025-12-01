"""
Web & URL Tools
Download files, check websites, scrape, QR codes
"""

import subprocess
import requests
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def download_file(url: str, output_path: str = None) -> dict:
    """
    Download file from URL with proper headers
    
    Args:
        url: URL to download
        output_path: Where to save (None = Downloads folder with original name)
    """
    try:
        if not output_path:
            # Extract filename from URL
            filename = os.path.basename(urlparse(url).path) or "download"
            output_path = os.path.expanduser(f"~/Downloads/{filename}")
        
        # Use proper headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Download using requests
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(output_path)
        
        return {
            "success": True,
            "url": url,
            "output": output_path,
            "size_mb": round(file_size / 1024 / 1024, 2),
            "message": f"Downloaded to {output_path}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_website_status(url: str) -> dict:
    """Check if website is up and get status code"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        
        return {
            "success": True,
            "url": url,
            "status_code": response.status_code,
            "status": "UP" if response.status_code < 400 else "DOWN",
            "response_time_ms": int(response.elapsed.total_seconds() * 1000)
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "url": url,
            "status": "DOWN",
            "error": str(e)
        }


def web_scrape(url: str, selector: str = None) -> dict:
    """
    Scrape website content with proper headers
    
    Args:
        url: URL to scrape
        selector: CSS selector (optional, returns specific elements)
    """
    try:
        # Use proper headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        if selector:
            # Get elements matching selector
            elements = soup.select(selector)
            content = [elem.get_text(strip=True) for elem in elements[:20]]  # Limit to 20
        else:
            # Get main content (try to find article or main content area)
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup
            
            # Get all paragraphs for cleaner text
            paragraphs = main_content.find_all('p')
            if paragraphs:
                content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs[:15]])  # First 15 paragraphs
            else:
                content = main_content.get_text(strip=True)[:3000]  # Fallback to first 3000 chars
        
        return {
            "success": True,
            "url": url,
            "title": soup.title.string if soup.title else "No title",
            "content": content,
            "selector": selector,
            "content_length": len(content) if isinstance(content, str) else len(str(content))
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_page_title(url: str) -> dict:
    """Get webpage title with proper headers"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        
        return {
            "success": True,
            "url": url,
            "title": title
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_page_links(url: str) -> dict:
    """Get all links from webpage with proper headers"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for link in soup.find_all('a', href=True)[:50]:  # First 50 links
            links.append({
                "text": link.get_text(strip=True)[:100],
                "href": link['href']
            })
        
        return {
            "success": True,
            "url": url,
            "count": len(links),
            "links": links
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def shorten_url(url: str) -> dict:
    """Shorten URL using is.gd (free, no API key needed)"""
    try:
        response = requests.get(
            'https://is.gd/create.php',
            params={'format': 'simple', 'url': url},
            timeout=10
        )
        response.raise_for_status()
        
        short_url = response.text.strip()
        
        return {
            "success": True,
            "original": url,
            "shortened": short_url,
            "message": f"Shortened: {short_url}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_qr_code(text: str, output_path: str = None) -> dict:
    """Generate QR code for text/URL"""
    try:
        import qrcode
        
        if not output_path:
            output_path = os.path.expanduser("~/Desktop/qrcode.png")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        
        return {
            "success": True,
            "text": text[:100],
            "output": output_path,
            "message": f"QR code saved: {output_path}"
        }
    except ImportError:
        return {
            "success": False,
            "error": "qrcode not installed. Run: pip install qrcode[pil]"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_ip_info(ip_address: str = None) -> dict:
    """
    Get public IP and location info.
    
    Args:
        ip_address: Optional IP to lookup (default: current IP)
    """
    try:
        url = f'https://ipapi.co/{ip_address}/json/' if ip_address else 'https://ipapi.co/json/'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "success": True,
            "ip": data.get('ip'),
            "city": data.get('city'),
            "region": data.get('region'),
            "country": data.get('country_name'),
            "timezone": data.get('timezone'),
            "isp": data.get('org')
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def ping_host(host: str, count: int = 4) -> dict:
    """Ping a host"""
    try:
        result = subprocess.run(
            ['ping', '-c', str(count), host],
            capture_output=True, text=True, timeout=30
        )
        
        # Parse ping results
        lines = result.stdout.split('\n')
        stats_line = [l for l in lines if 'packets transmitted' in l]
        time_line = [l for l in lines if 'min/avg/max' in l]
        
        return {
            "success": True,
            "host": host,
            "stats": stats_line[0] if stats_line else "",
            "times": time_line[0] if time_line else "",
            "raw": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def trace_route(host: str, max_hops: int = 30) -> dict:
    """Trace route to host"""
    try:
        result = subprocess.run(
            ['traceroute', '-m', str(max_hops), host],
            capture_output=True, text=True, timeout=60
        )
        
        return {
            "success": True,
            "host": host,
            "route": result.stdout[:1000]  # First 1000 chars
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def dns_lookup(domain: str) -> dict:
    """DNS lookup for domain"""
    try:
        result = subprocess.run(
            ['dig', '+short', domain],
            capture_output=True, text=True, check=True, timeout=10
        )
        
        ips = [ip.strip() for ip in result.stdout.split('\n') if ip.strip()]
        
        return {
            "success": True,
            "domain": domain,
            "ips": ips
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def whois_lookup(domain: str) -> dict:
    """WHOIS lookup for domain"""
    try:
        result = subprocess.run(
            ['whois', domain],
            capture_output=True, text=True, timeout=30
        )
        
        return {
            "success": True,
            "domain": domain,
            "whois": result.stdout[:1000]  # First 1000 chars
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def test_upload_speed() -> dict:
    """Test internet upload speed"""
    try:
        # Generate random data to upload (5MB)
        import time
        import random
        import string
        
        # Create 5MB of random data
        size_mb = 5
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=size_mb * 1024 * 1024))
        
        # Use httpbin.org for upload test
        test_url = "https://httpbin.org/post"
        
        start = time.time()
        
        # Upload data
        response = requests.post(test_url, data={'data': data}, timeout=30)
        response.raise_for_status()
        
        elapsed = time.time() - start
        
        # Calculate speed
        speed_mbps = (size_mb * 8) / elapsed
        
        return {
            "success": True,
            "size_mb": size_mb,
            "time_seconds": round(elapsed, 2),
            "speed_mbps": round(speed_mbps, 2),
            "message": f"Upload speed: {speed_mbps:.2f} Mbps"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def test_download_speed() -> dict:
    """Test internet download speed"""
    try:
        # Download a larger test file for more accurate measurement
        # Try 50MB first, fallback to 10MB if it takes too long
        test_urls = [
            ("http://speedtest.tele2.net/50MB.zip", 50),
            ("http://speedtest.tele2.net/10MB.zip", 10),
        ]
        
        import time
        
        for test_url, expected_mb in test_urls:
            try:
                start = time.time()
                
                # Stream download with timeout
                response = requests.get(test_url, stream=True, timeout=30)
                response.raise_for_status()
                
                # Download in chunks
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    downloaded += len(chunk)
                    
                    # Stop if taking too long (max 30 seconds)
                    if time.time() - start > 30:
                        break
                
                elapsed = time.time() - start
                
                # If we got a reasonable amount of data, calculate speed
                if downloaded > 1024 * 1024:  # At least 1MB
                    size_mb = downloaded / 1024 / 1024
                    speed_mbps = (size_mb * 8) / elapsed
                    
                    return {
                        "success": True,
                        "size_mb": round(size_mb, 2),
                        "time_seconds": round(elapsed, 2),
                        "speed_mbps": round(speed_mbps, 2),
                        "message": f"Download speed: {speed_mbps:.2f} Mbps"
                    }
                
            except Exception:
                continue
        
        # If all URLs failed
        return {
            "success": False,
            "error": "Could not complete speed test with any test server"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

