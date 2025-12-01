#!/usr/bin/env python3
"""
Test Suite for New Spotify & Browser Tools
Tests 49 new tools thoroughly
"""

import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:7889"

# ============================================================
# SPOTIFY TOOLS TESTS (20 tools)
# ============================================================
SPOTIFY_TESTS = [
    # Playback Control
    ("Spotify: Play Liked Songs", "play my liked songs on spotify", ["spotify_play_library"]),
    ("Spotify: Pause", "pause spotify", ["spotify_pause", "control_music"]),
    ("Spotify: Resume", "resume spotify", ["spotify_resume", "control_music"]),
    ("Spotify: Toggle Playback", "play pause spotify", ["spotify_toggle_playback", "control_music"]),
    ("Spotify: Next Track", "skip to next song on spotify", ["spotify_next_track", "control_music"]),
    ("Spotify: Previous Track", "go back to previous song", ["spotify_previous_track", "control_music"]),
    
    # Track Info
    ("Spotify: Get Current Track", "what song is playing on spotify", ["spotify_get_current_track", "get_current_song"]),
    ("Spotify: Get Status", "whats the spotify status", ["spotify_get_status"]),
    
    # Volume
    ("Spotify: Set Volume", "set spotify volume to 60", ["spotify_set_volume"]),
    ("Spotify: Get Volume", "what is spotify volume", ["spotify_get_volume"]),
    
    # Modes
    ("Spotify: Toggle Shuffle", "turn on shuffle on spotify", ["spotify_toggle_shuffle"]),
    ("Spotify: Toggle Repeat", "enable repeat on spotify", ["spotify_toggle_repeat"]),
    
    # Content Playback
    ("Spotify: Play Artist", "play taylor swift on spotify", ["spotify_play_artist", "play_spotify_track"]),
    ("Spotify: Play Album", "play the album thriller on spotify", ["spotify_play_album", "play_spotify_track"]),
    ("Spotify: Play Playlist", "play my workout playlist on spotify", ["spotify_play_playlist", "spotify_play_library"]),
    ("Spotify: Play Genre", "play jazz music on spotify", ["spotify_play_genre", "play_spotify_track"]),
    ("Spotify: Play Mood", "play some chill music", ["spotify_play_mood", "play_spotify_track"]),
    ("Spotify: Search Track", "play shape of you on spotify", ["play_spotify_track"]),
    
    # Library
    ("Spotify: Discover Weekly", "play discover weekly", ["spotify_play_library"]),
    ("Spotify: Release Radar", "play release radar on spotify", ["spotify_play_library"]),
]

# ============================================================
# BROWSER TOOLS TESTS (32 tools)
# ============================================================
BROWSER_TESTS = [
    # Tab Management
    ("Browser: New Tab", "open a new tab in chrome", ["browser_new_tab"]),
    ("Browser: New Tab with URL", "open github.com in a new tab", ["browser_new_tab", "open_url"]),
    ("Browser: Close Tab", "close the current tab in chrome", ["browser_close_tab"]),
    ("Browser: Close All Tabs", "close all tabs in chrome", ["browser_close_all_tabs"]),
    ("Browser: Get Tab Count", "how many tabs do i have open in chrome", ["browser_get_tab_count"]),
    ("Browser: Get All Tabs", "list all my open tabs in chrome", ["browser_get_all_tabs"]),
    ("Browser: Switch Tab", "switch to tab 2 in chrome", ["browser_switch_tab"]),
    ("Browser: Next Tab", "go to next tab", ["browser_next_tab"]),
    ("Browser: Previous Tab", "go to previous tab", ["browser_previous_tab"]),
    ("Browser: Duplicate Tab", "duplicate this tab in chrome", ["browser_duplicate_tab"]),
    ("Browser: Reopen Closed Tab", "reopen my last closed tab", ["browser_reopen_closed_tab"]),
    ("Browser: Pin Tab", "pin this tab", ["browser_pin_tab"]),
    ("Browser: Mute Tab", "mute this tab", ["browser_mute_tab"]),
    
    # Navigation
    ("Browser: Refresh", "refresh the page", ["browser_refresh"]),
    ("Browser: Go Back", "go back in chrome", ["browser_go_back"]),
    ("Browser: Go Forward", "go forward in chrome", ["browser_go_forward"]),
    ("Browser: Scroll Down", "scroll down the page", ["browser_scroll"]),
    ("Browser: Scroll Top", "scroll to top of page", ["browser_scroll"]),
    
    # Page Info
    ("Browser: Get URL", "what is the current url in chrome", ["browser_get_current_url"]),
    ("Browser: Get Title", "what is the title of this page", ["browser_get_current_title"]),
    
    # Search
    ("Browser: Google Search", "search google for python tutorials", ["browser_search"]),
    ("Browser: YouTube Search", "search youtube for coding videos", ["browser_search"]),
    ("Browser: DuckDuckGo Search", "search duckduckgo for privacy tools", ["browser_search"]),
    ("Browser: GitHub Search", "search github for react projects", ["browser_search"]),
    
    # Page Actions
    ("Browser: Zoom In", "zoom in on chrome", ["browser_zoom"]),
    ("Browser: Zoom Out", "zoom out", ["browser_zoom"]),
    ("Browser: Zoom Reset", "reset zoom", ["browser_zoom"]),
    ("Browser: Find on Page", "find the word login on this page", ["browser_find_on_page"]),
    ("Browser: Bookmark", "bookmark this page", ["browser_bookmark_page"]),
    ("Browser: Print", "print this page", ["browser_print_page"]),
    ("Browser: Save Page", "save this page", ["browser_save_page"]),
    ("Browser: Fullscreen", "make chrome fullscreen", ["browser_fullscreen"]),
    
    # Privacy & Dev
    ("Browser: Incognito", "open incognito window", ["browser_open_incognito"]),
    ("Browser: Dev Tools", "open developer tools", ["browser_open_devtools"]),
    ("Browser: View Source", "view page source", ["browser_view_source"]),
    ("Browser: Clear History", "clear browsing history", ["browser_clear_history"]),
    ("Browser: Screenshot", "take a screenshot of the browser", ["browser_screenshot_page"]),
    
    # Multi-URL
    ("Browser: Multiple URLs", "open github.com and stackoverflow.com in new tabs", ["browser_open_multiple_urls", "browser_new_tab"]),
    
    # Safari Specific
    ("Browser: Safari Reading Mode", "enable reading mode in safari", ["browser_reading_mode"]),
]

# ============================================================
# MULTI-BROWSER TESTS
# ============================================================
MULTI_BROWSER_TESTS = [
    ("Chrome: Get URL", "what url is open in chrome", ["browser_get_current_url"]),
    ("Brave: Get URL", "what url is open in brave", ["browser_get_current_url"]),
    ("Safari: Get URL", "what url is open in safari", ["browser_get_current_url"]),
    ("Chrome: New Tab", "open new tab in google chrome", ["browser_new_tab"]),
    ("Brave: New Tab", "open new tab in brave browser", ["browser_new_tab"]),
    ("Safari: New Tab", "open new tab in safari", ["browser_new_tab"]),
]

def reset_conversation():
    try:
        requests.post(f"{BASE_URL}/api/reset", timeout=5)
        return True
    except:
        return False

def run_test(name, question, expected_tools, timeout=60):
    """Run a single test"""
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": question},
            timeout=timeout
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            return {
                "name": name,
                "passed": False,
                "time": elapsed,
                "error": f"HTTP {response.status_code}",
                "tools_called": []
            }
        
        data = response.json()
        
        if not data.get('success'):
            return {
                "name": name,
                "passed": False,
                "time": elapsed,
                "error": data.get('error', 'Unknown'),
                "tools_called": []
            }
        
        tools_called = [t['tool'] for t in data.get('tool_executions', [])]
        tool_results = [t['result'].get('success', False) for t in data.get('tool_executions', [])]
        
        # Check if any expected tool was called
        tool_matched = any(t in tools_called for t in expected_tools) if expected_tools else True
        
        # Check if tools executed successfully
        tools_succeeded = any(tool_results) if tool_results else True
        
        return {
            "name": name,
            "passed": tool_matched and tools_succeeded,
            "time": elapsed,
            "tools_called": tools_called,
            "tool_results": tool_results,
            "response": data.get('response', '')[:200],
            "expected": expected_tools
        }
        
    except requests.exceptions.Timeout:
        return {
            "name": name,
            "passed": False,
            "time": timeout,
            "error": "Timeout",
            "tools_called": []
        }
    except Exception as e:
        return {
            "name": name,
            "passed": False,
            "time": time.time() - start_time,
            "error": str(e),
            "tools_called": []
        }

def run_test_suite(suite_name, tests):
    """Run a test suite and return results"""
    print(f"\n{'='*70}")
    print(f"🧪 {suite_name}")
    print(f"{'='*70}")
    
    results = []
    passed = 0
    failed = 0
    
    for name, question, expected_tools in tests:
        print(f"\n📋 {name}")
        print(f"   Q: {question[:50]}{'...' if len(question) > 50 else ''}")
        
        result = run_test(name, question, expected_tools)
        results.append(result)
        
        if result['passed']:
            passed += 1
            print(f"   ✅ PASS ({result['time']:.1f}s)")
            print(f"   Tools: {result['tools_called']}")
        else:
            failed += 1
            print(f"   ❌ FAIL ({result['time']:.1f}s)")
            if 'error' in result:
                print(f"   Error: {result['error']}")
            else:
                print(f"   Expected: {result.get('expected', [])}")
                print(f"   Got: {result['tools_called']}")
        
        # Show response preview
        if result.get('response'):
            preview = result['response'][:80].replace('\n', ' ')
            print(f"   💬 {preview}...")
        
        time.sleep(0.5)  # Brief pause between tests
    
    print(f"\n{'─'*70}")
    print(f"📊 {suite_name} Results: {passed}/{len(tests)} passed ({passed/len(tests)*100:.0f}%)")
    
    return results, passed, failed

def main():
    print("=" * 70)
    print("🧪 MacGPT NEW TOOLS TEST SUITE")
    print("   Testing 49 new Spotify & Browser tools")
    print("=" * 70)
    print(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check server
    try:
        requests.get(BASE_URL, timeout=5)
        print(f"   ✅ Server running at {BASE_URL}")
    except:
        print(f"   ❌ Server not running!")
        print(f"   Start with: python start_web.py")
        return
    
    all_results = []
    total_passed = 0
    total_failed = 0
    
    # Reset conversation
    print("\n🔄 Resetting conversation...")
    reset_conversation()
    
    # Run Spotify tests
    results, passed, failed = run_test_suite("SPOTIFY TOOLS (20 tests)", SPOTIFY_TESTS)
    all_results.extend(results)
    total_passed += passed
    total_failed += failed
    
    # Reset and run Browser tests
    reset_conversation()
    results, passed, failed = run_test_suite("BROWSER TOOLS (32 tests)", BROWSER_TESTS)
    all_results.extend(results)
    total_passed += passed
    total_failed += failed
    
    # Run multi-browser tests
    reset_conversation()
    results, passed, failed = run_test_suite("MULTI-BROWSER TESTS (6 tests)", MULTI_BROWSER_TESTS)
    all_results.extend(results)
    total_passed += passed
    total_failed += failed
    
    # Final Summary
    total_tests = total_passed + total_failed
    
    print("\n" + "=" * 70)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 70)
    
    print(f"\n🎯 Overall Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   ✅ Passed: {total_passed}")
    print(f"   ❌ Failed: {total_failed}")
    print(f"   📈 Pass Rate: {total_passed/total_tests*100:.1f}%")
    
    # Calculate average time
    total_time = sum(r['time'] for r in all_results)
    print(f"   ⏱️  Total Time: {total_time:.1f}s")
    print(f"   📊 Avg Time: {total_time/total_tests:.1f}s per test")
    
    # Show failed tests
    failed_tests = [r for r in all_results if not r['passed']]
    if failed_tests:
        print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
        for r in failed_tests:
            print(f"   - {r['name']}: {r.get('error', 'Tool mismatch')}")
    
    # Show slow tests
    slow_tests = [r for r in all_results if r['time'] > 20]
    if slow_tests:
        print(f"\n🐢 SLOW TESTS (>20s):")
        for r in sorted(slow_tests, key=lambda x: -x['time']):
            print(f"   - {r['name']}: {r['time']:.1f}s")
    
    # Save results
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed": total_passed,
        "failed": total_failed,
        "pass_rate": total_passed/total_tests*100,
        "total_time": total_time,
        "results": all_results
    }
    
    with open("tests/new_tools_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Report saved to: tests/new_tools_report.json")
    print("\n" + "=" * 70)
    print("🏁 Testing Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()

