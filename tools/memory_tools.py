"""
State-of-the-Art Memory Tools for MacGPT
==========================================
Expose agent memory capabilities as tools the LLM can use.
All processing is local - no external APIs.
"""

from core.memory import get_memory
from typing import Dict, Any, List, Optional


# ==================== REMEMBER / RECALL ====================

def memory_remember(fact: str, category: str = "general", 
                    importance: str = "medium") -> Dict[str, Any]:
    """
    Remember a fact with intelligent storage and association.
    
    Args:
        fact: The fact to remember (natural language)
        category: Category (general, personal, work, project, technical)
        importance: low, medium, or high
    
    Returns:
        Success message with memory ID
    
    Examples:
        - "Remember that my name is John" 
        - "Remember I prefer dark mode"
        - "Remember the API key is stored in ~/.env"
    """
    memory = get_memory()
    
    importance_map = {"low": 0.3, "medium": 0.5, "high": 0.8}
    imp_score = importance_map.get(importance, 0.5)
    
    result = memory.remember(
        content=fact,
        memory_type="fact",
        category=category,
        importance=imp_score
    )
    return result


def memory_recall(query: str = "", category: str = "", 
                  top_k: int = 10) -> Dict[str, Any]:
    """
    Intelligently recall memories using semantic search.
    
    Args:
        query: Search query (uses semantic matching, not exact match)
        category: Filter by category (optional)
        top_k: Maximum results to return
    
    Returns:
        List of relevant memories ranked by relevance
    
    Examples:
        - "What do you remember about me?"
        - "What do you know about my projects?"
        - "Recall facts about API keys"
    """
    memory = get_memory()
    
    result = memory.recall(
        query=query if query else "",
        category=category if category else None,
        top_k=top_k
    )
    
    # Format for display
    if result.get("memories"):
        formatted = []
        for mem in result["memories"]:
            formatted.append({
                "content": mem["content"],
                "relevance": f"{mem['score']*100:.0f}%",
                "category": mem["category"],
                "type": mem["type"]
            })
        result["memories"] = formatted
    
    return result


def memory_forget(query: str) -> Dict[str, Any]:
    """
    Forget memories matching a query.
    
    Args:
        query: Search term - matching memories will be forgotten
    
    Examples:
        - "Forget my old API key"
        - "Forget everything about the old project"
    """
    memory = get_memory()
    return memory.forget(query=query)


# ==================== PREFERENCES ====================

def memory_set_preference(key: str, value: str) -> Dict[str, Any]:
    """
    Save a user preference that persists across sessions.
    
    Args:
        key: Preference name (browser, editor, theme, projects_dir, etc.)
        value: Preference value
    
    Examples:
        - "I prefer Chrome" -> memory_set_preference("browser", "chrome")
        - "My editor is VS Code" -> memory_set_preference("editor", "vscode")
        - "I like dark mode" -> memory_set_preference("theme", "dark")
    """
    memory = get_memory()
    return memory.set_preference(key, value)


def memory_get_preference(key: str) -> Dict[str, Any]:
    """
    Get a saved preference.
    
    Args:
        key: Preference name to retrieve
    """
    memory = get_memory()
    value = memory.get_preference(key)
    if value is not None:
        return {"success": True, "key": key, "value": value}
    return {"success": False, "message": f"No preference '{key}' found"}


def memory_list_preferences() -> Dict[str, Any]:
    """
    List all saved user preferences.
    """
    memory = get_memory()
    prefs = memory.list_preferences()
    return {
        "success": True,
        "preferences": prefs,
        "count": len(prefs)
    }


# ==================== SHORTCUTS & PROCEDURES ====================

def memory_create_shortcut(name: str, command: str, 
                           description: str = "") -> Dict[str, Any]:
    """
    Create a custom command shortcut.
    
    Args:
        name: Short name (e.g., 'dev', 'music', 'standup')
        command: Full command in natural language
        description: What this shortcut does
    
    Examples:
        - "Create shortcut 'dev' for VS Code and Chrome side by side"
        - "Save 'music' as play Spotify at volume 30"
    """
    memory = get_memory()
    return memory.create_shortcut(name, command, description)


def memory_run_shortcut(name: str) -> Dict[str, Any]:
    """
    Get a saved shortcut command to execute.
    
    Args:
        name: Shortcut name
    
    Returns the command that should be executed.
    """
    memory = get_memory()
    command = memory.get_shortcut(name)
    if command:
        return {
            "success": True,
            "shortcut": name,
            "command": command,
            "instruction": f"Execute this command: {command}"
        }
    return {"success": False, "message": f"Shortcut '{name}' not found"}


def memory_list_shortcuts() -> Dict[str, Any]:
    """
    List all saved shortcuts.
    """
    memory = get_memory()
    shortcuts = memory.list_shortcuts()
    return {
        "success": True,
        "shortcuts": shortcuts,
        "count": len(shortcuts)
    }


def memory_delete_shortcut(name: str) -> Dict[str, Any]:
    """
    Delete a saved shortcut.
    """
    memory = get_memory()
    return memory.delete_shortcut(name)


def memory_learn_procedure(name: str, steps: str, 
                           trigger: str = "") -> Dict[str, Any]:
    """
    Learn a multi-step workflow/procedure.
    
    Args:
        name: Procedure name
        steps: Steps separated by ' -> ' or '. '
        trigger: Natural language trigger phrase
    
    Example:
        memory_learn_procedure(
            name="morning_routine",
            steps="Open Chrome -> Check email -> Open Slack -> Start Spotify",
            trigger="start my morning routine"
        )
    """
    memory = get_memory()
    
    # Parse steps
    if ' -> ' in steps:
        step_list = [s.strip() for s in steps.split(' -> ')]
    else:
        step_list = [s.strip() for s in steps.split('. ') if s.strip()]
    
    return memory.learn_procedure(name, step_list, trigger)


# ==================== CONTEXT ====================

def memory_set_context(key: str, value: str) -> Dict[str, Any]:
    """
    Set current working context.
    
    Args:
        key: Context type (project, task, directory, goal)
        value: Context value
    
    Examples:
        - "I'm working on MacGPT" -> memory_set_context("project", "MacGPT")
        - "My task is implementing memory" -> memory_set_context("task", "memory")
    """
    memory = get_memory()
    return memory.set_context(key, value)


def memory_get_context() -> Dict[str, Any]:
    """
    Get current working context.
    """
    memory = get_memory()
    context = memory.get_context()
    return {"success": True, "context": context}


def memory_clear_context() -> Dict[str, Any]:
    """
    Clear all current context (fresh start).
    """
    memory = get_memory()
    return memory.clear_context()


# ==================== EPISODES ====================

def memory_save_episode(summary: str, key_points: str = "") -> Dict[str, Any]:
    """
    Save a conversation episode summary.
    
    Args:
        summary: Brief summary of what happened
        key_points: Comma-separated key takeaways
    
    Example:
        memory_save_episode(
            summary="Helped user set up development environment",
            key_points="installed node, created project, configured VS Code"
        )
    """
    memory = get_memory()
    
    points = [p.strip() for p in key_points.split(',') if p.strip()] if key_points else []
    
    return memory.save_episode(summary, points)


def memory_get_recent_episodes(limit: int = 5) -> Dict[str, Any]:
    """
    Get recent conversation episode summaries.
    """
    memory = get_memory()
    episodes = memory.get_recent_episodes(limit)
    return {
        "success": True,
        "episodes": episodes,
        "count": len(episodes)
    }


# ==================== ANALYTICS ====================

def memory_get_frequent_commands(limit: int = 10) -> Dict[str, Any]:
    """
    Get most frequently used commands.
    """
    memory = get_memory()
    return {
        "success": True,
        "frequent_commands": memory.get_frequent_commands(limit)
    }


def memory_get_frequent_tools(limit: int = 10) -> Dict[str, Any]:
    """
    Get most frequently used tools.
    """
    memory = get_memory()
    return {
        "success": True,
        "frequent_tools": memory.get_frequent_tools(limit)
    }


def memory_stats() -> Dict[str, Any]:
    """
    Get memory system statistics.
    """
    memory = get_memory()
    stats = memory.get_stats()
    summary = memory.get_memory_summary()
    
    return {
        "success": True,
        "stats": stats,
        "summary": summary
    }


# ==================== MAINTENANCE ====================

def memory_consolidate() -> Dict[str, Any]:
    """
    Consolidate and optimize memories.
    Merges similar memories, removes outdated ones.
    """
    memory = get_memory()
    return memory.consolidate()


def memory_reset() -> Dict[str, Any]:
    """
    Reset ALL memories permanently. USE WITH CAUTION!
    """
    memory = get_memory()
    return memory.reset_all()


# ==================== SEARCH ====================

def memory_search(query: str, memory_type: str = "") -> Dict[str, Any]:
    """
    Semantic search across all memories.
    
    Args:
        query: Natural language search query
        memory_type: Optional filter (fact, preference, shortcut, episode, procedure)
    
    Uses TF-IDF based semantic matching - finds relevant memories
    even if exact words don't match.
    """
    memory = get_memory()
    
    result = memory.recall(
        query=query,
        memory_type=memory_type if memory_type else None,
        top_k=15
    )
    
    return result


def memory_associate(memory_query: str, related_to: str) -> Dict[str, Any]:
    """
    Manually associate two memories/concepts.
    
    Args:
        memory_query: Query to find first memory
        related_to: Query to find related memory
    
    Creates bidirectional association between memories.
    """
    memory = get_memory()
    
    # Find both memories
    result1 = memory.recall(query=memory_query, top_k=1)
    result2 = memory.recall(query=related_to, top_k=1)
    
    if not result1.get("memories") or not result2.get("memories"):
        return {"success": False, "message": "Could not find memories to associate"}
    
    mem1_id = result1["memories"][0]["id"]
    mem2_id = result2["memories"][0]["id"]
    
    # Create associations
    if mem1_id in memory.memories and mem2_id in memory.memories:
        if mem2_id not in memory.memories[mem1_id].associations:
            memory.memories[mem1_id].associations.append(mem2_id)
        if mem1_id not in memory.memories[mem2_id].associations:
            memory.memories[mem2_id].associations.append(mem1_id)
        memory._save()
        
        return {
            "success": True,
            "message": "Memories associated",
            "memory1": result1["memories"][0]["content"][:50],
            "memory2": result2["memories"][0]["content"][:50]
        }
    
    return {"success": False, "message": "Could not associate memories"}
