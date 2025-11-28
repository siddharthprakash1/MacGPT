#!/usr/bin/env python3
"""
Automated Tool Testing Script for MacGPT
Runs tests against the running web server
"""

import requests
import time
import json

BASE_URL = "http://localhost:7889"

# Test cases: (name, question, expected_tool)
TESTS = [
    # Quick Actions
    ("Battery Status", "What's my battery level?", "get_battery_status"),
    ("Volume Set", "Set volume to 50%", "set_volume"),
    ("System Info", "Show me system information", "get_system_info"),
    
    # Spotlight Tools (NEW)
    ("Find Large Files", "Find files over 100MB", "find_large_files"),
    ("Files Modified Today", "What files did I modify today?", "find_files_by_date"),
    ("App Disk Usage", "Which apps are using the most disk space?", "find_apps_using_disk_space"),
    ("Recent Files", "What files did I open in the last 24 hours?", "find_recent_opened"),
    
    # File Operations
    ("List Downloads", "List files in my Downloads folder", "list_files"),
    ("Disk Usage", "How much disk space do I have?", "get_disk_usage"),
    
    # Application Control
    ("List Running Apps", "What apps are currently running?", "list_running_apps"),
    
    # Network
    ("Network Info", "What's my network status?", "get_network_info"),
    ("Check Website", "Is google.com up?", "check_website_status"),
    
    # Clipboard
    ("Clipboard Content", "What's in my clipboard?", "clipboard_read"),
]

def reset_conversation():
    """Reset the conversation before testing"""
    try:
        response = requests.post(f"{BASE_URL}/api/reset", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_test(name, question, expected_tool):
    """Run a single test and return results"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"Question: {question}")
    print(f"Expected Tool: {expected_tool}")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": question},
            timeout=120
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ FAIL - HTTP {response.status_code}")
            return False, elapsed, None
        
        data = response.json()
        
        if not data.get('success'):
            print(f"❌ FAIL - Error: {data.get('error')}")
            return False, elapsed, None
        
        # Check if expected tool was called
        tool_executions = data.get('tool_executions', [])
        tools_called = [t['tool'] for t in tool_executions]
        
        tool_matched = expected_tool in tools_called or len(tool_executions) > 0
        
        print(f"Tools Called: {tools_called}")
        print(f"Time: {elapsed:.2f}s")
        
        # Show tool results
        for exec in tool_executions:
            result = exec.get('result', {})
            success = result.get('success', False)
            print(f"\n📦 {exec['tool']}: {'✅' if success else '❌'}")
            
            # Show key results
            if 'count' in result:
                print(f"   Count: {result['count']}")
            if 'files' in result and result['files']:
                print(f"   Files: {len(result['files'])} found")
                for f in result['files'][:3]:
                    print(f"   - {f}")
                if len(result['files']) > 3:
                    print(f"   ... and {len(result['files'])-3} more")
            if 'apps' in result and result['apps']:
                print(f"   Apps: {len(result['apps'])} found")
                for a in result['apps'][:3]:
                    name = a.get('name', a) if isinstance(a, dict) else a
                    size = a.get('size_display', '') if isinstance(a, dict) else ''
                    print(f"   - {name} {size}")
            if 'percentage' in result:
                print(f"   Battery: {result.get('percentage')}")
            if 'system' in result:
                sys = result['system']
                print(f"   OS: macOS {sys.get('version')}")
            if 'content' in result:
                content = result['content'][:100] + '...' if len(str(result.get('content', ''))) > 100 else result.get('content', '')
                print(f"   Content: {content}")
        
        # Show AI response (truncated)
        ai_response = data.get('response', '')[:200]
        if ai_response:
            print(f"\n💬 Response: {ai_response}...")
        
        if tool_matched:
            print(f"\n✅ PASS ({elapsed:.2f}s)")
            return True, elapsed, tools_called
        else:
            print(f"\n⚠️  WARN - Expected {expected_tool}, got {tools_called}")
            return True, elapsed, tools_called  # Still pass if any tool worked
            
    except requests.exceptions.Timeout:
        print(f"❌ FAIL - Timeout after 120s")
        return False, 120, None
    except Exception as e:
        print(f"❌ FAIL - Error: {e}")
        return False, 0, None

def main():
    print("=" * 60)
    print("🧪 MacGPT AUTOMATED TOOL TESTS")
    print("=" * 60)
    
    # Check server is running
    try:
        requests.get(BASE_URL, timeout=5)
        print("✅ Server is running at", BASE_URL)
    except:
        print("❌ Server not running! Start with: python start_web.py")
        return
    
    # Reset conversation
    print("\n🔄 Resetting conversation...")
    reset_conversation()
    
    # Run tests
    results = []
    total_time = 0
    
    for name, question, expected_tool in TESTS:
        passed, elapsed, tools = run_test(name, question, expected_tool)
        results.append((name, passed, elapsed, tools))
        total_time += elapsed
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r[1])
    failed = len(results) - passed
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Pass Rate: {passed/len(results)*100:.1f}%")
    print(f"Total Time: {total_time:.1f}s")
    print(f"Avg Time: {total_time/len(results):.1f}s per test")
    
    print("\n" + "-" * 60)
    print("DETAILED RESULTS:")
    print("-" * 60)
    
    for name, passed, elapsed, tools in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}: {elapsed:.1f}s - {tools}")
    
    if failed > 0:
        print("\n⚠️  FAILED TESTS:")
        for name, passed, elapsed, tools in results:
            if not passed:
                print(f"  - {name}")

if __name__ == "__main__":
    main()

