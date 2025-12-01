"""
State-of-the-Art Agent Memory System for MacGPT
================================================================================
A sophisticated, fully local memory system with:
- Importance scoring & decay
- Semantic similarity matching (TF-IDF based, no external APIs)
- Episodic memory (conversation summaries)
- Procedural memory (learned workflows)
- Associative memory (linked concepts)
- Automatic consolidation
================================================================================
"""

import json
import os
import re
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from pathlib import Path
from collections import Counter, defaultdict
import hashlib


class SemanticIndex:
    """
    Local TF-IDF based semantic similarity engine.
    No external APIs - runs entirely on device.
    """
    
    def __init__(self):
        self.documents: Dict[str, str] = {}  # id -> text
        self.idf: Dict[str, float] = {}
        self.tfidf: Dict[str, Dict[str, float]] = {}  # id -> {term: score}
        self._dirty = True
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize and normalize text"""
        text = text.lower()
        # Remove punctuation and split
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        # Remove common stopwords
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                     'can', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
                     'from', 'as', 'into', 'through', 'during', 'before', 'after',
                     'above', 'below', 'between', 'under', 'again', 'further',
                     'then', 'once', 'here', 'there', 'when', 'where', 'why',
                     'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some',
                     'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                     'than', 'too', 'very', 'just', 'and', 'but', 'if', 'or',
                     'because', 'until', 'while', 'about', 'against', 'this',
                     'that', 'these', 'those', 'am', 'i', 'me', 'my', 'myself',
                     'we', 'our', 'you', 'your', 'he', 'him', 'his', 'she', 'her',
                     'it', 'its', 'they', 'them', 'their', 'what', 'which', 'who'}
        return [t for t in tokens if t not in stopwords and len(t) > 1]
    
    def add_document(self, doc_id: str, text: str):
        """Add a document to the index"""
        self.documents[doc_id] = text
        self._dirty = True
    
    def remove_document(self, doc_id: str):
        """Remove a document from the index"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            self._dirty = True
    
    def _rebuild_index(self):
        """Rebuild TF-IDF index"""
        if not self._dirty:
            return
        
        # Calculate document frequencies
        doc_freq: Dict[str, int] = Counter()
        doc_terms: Dict[str, Counter] = {}
        
        for doc_id, text in self.documents.items():
            tokens = self._tokenize(text)
            term_counts = Counter(tokens)
            doc_terms[doc_id] = term_counts
            for term in set(tokens):
                doc_freq[term] += 1
        
        # Calculate IDF
        num_docs = len(self.documents)
        self.idf = {}
        for term, freq in doc_freq.items():
            self.idf[term] = math.log((num_docs + 1) / (freq + 1)) + 1
        
        # Calculate TF-IDF for each document
        self.tfidf = {}
        for doc_id, term_counts in doc_terms.items():
            total_terms = sum(term_counts.values())
            self.tfidf[doc_id] = {}
            for term, count in term_counts.items():
                tf = count / total_terms if total_terms > 0 else 0
                self.tfidf[doc_id][term] = tf * self.idf.get(term, 1)
        
        self._dirty = False
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Search for similar documents.
        Returns list of (doc_id, similarity_score) tuples.
        """
        self._rebuild_index()
        
        if not self.documents:
            return []
        
        # Tokenize query
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        
        # Calculate query TF-IDF
        query_counts = Counter(query_tokens)
        total = sum(query_counts.values())
        query_tfidf = {}
        for term, count in query_counts.items():
            tf = count / total
            query_tfidf[term] = tf * self.idf.get(term, 1)
        
        # Calculate cosine similarity with each document
        scores = []
        query_norm = math.sqrt(sum(v**2 for v in query_tfidf.values()))
        
        for doc_id, doc_tfidf in self.tfidf.items():
            # Dot product
            dot = sum(query_tfidf.get(term, 0) * score 
                     for term, score in doc_tfidf.items())
            
            # Document norm
            doc_norm = math.sqrt(sum(v**2 for v in doc_tfidf.values()))
            
            # Cosine similarity
            if query_norm > 0 and doc_norm > 0:
                similarity = dot / (query_norm * doc_norm)
                if similarity > 0.05:  # Threshold for relevance
                    scores.append((doc_id, similarity))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class MemoryItem:
    """A single memory item with metadata"""
    
    def __init__(self, content: str, memory_type: str, category: str = "general",
                 importance: float = 0.5, associations: List[str] = None,
                 metadata: Dict[str, Any] = None):
        self.id = hashlib.md5(f"{content}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        self.content = content
        self.type = memory_type  # fact, preference, shortcut, episode, procedure
        self.category = category
        self.importance = importance  # 0.0 to 1.0
        self.associations = associations or []  # IDs of related memories
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()
        self.last_accessed = datetime.now().isoformat()
        self.access_count = 0
        self.reinforcement_count = 0  # Times this was confirmed/used
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type,
            "category": self.category,
            "importance": self.importance,
            "associations": self.associations,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
            "reinforcement_count": self.reinforcement_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryItem':
        item = cls(
            content=data["content"],
            memory_type=data["type"],
            category=data.get("category", "general"),
            importance=data.get("importance", 0.5),
            associations=data.get("associations", []),
            metadata=data.get("metadata", {})
        )
        item.id = data["id"]
        item.created_at = data.get("created_at", datetime.now().isoformat())
        item.last_accessed = data.get("last_accessed", datetime.now().isoformat())
        item.access_count = data.get("access_count", 0)
        item.reinforcement_count = data.get("reinforcement_count", 0)
        return item
    
    def access(self):
        """Record an access to this memory"""
        self.last_accessed = datetime.now().isoformat()
        self.access_count += 1
    
    def reinforce(self):
        """Reinforce this memory (confirmed correct)"""
        self.reinforcement_count += 1
        # Boost importance when reinforced
        self.importance = min(1.0, self.importance + 0.1)
    
    def get_relevance_score(self) -> float:
        """
        Calculate current relevance score based on:
        - Base importance
        - Recency (decay over time)
        - Access frequency
        - Reinforcement
        """
        # Time decay factor (half-life of 30 days)
        try:
            created = datetime.fromisoformat(self.created_at)
            days_old = (datetime.now() - created).days
            recency_factor = math.exp(-days_old / 30)
        except:
            recency_factor = 0.5
        
        # Access frequency bonus
        access_factor = min(1.0, 0.5 + (self.access_count * 0.05))
        
        # Reinforcement bonus
        reinforcement_factor = min(1.0, 0.5 + (self.reinforcement_count * 0.1))
        
        # Combined score
        score = (
            self.importance * 0.4 +
            recency_factor * 0.2 +
            access_factor * 0.2 +
            reinforcement_factor * 0.2
        )
        
        return min(1.0, score)


class AgentMemory:
    """
    State-of-the-art Agent Memory System
    
    Features:
    - Semantic search (local TF-IDF)
    - Importance scoring with decay
    - Episodic memory (conversation summaries)
    - Procedural memory (learned workflows)
    - Associative linking
    - Automatic consolidation
    """
    
    MEMORY_DIR = os.path.expanduser("~/.macgpt")
    MEMORY_FILE = os.path.expanduser("~/.macgpt/memory.json")
    
    def __init__(self):
        self.memories: Dict[str, MemoryItem] = {}
        self.semantic_index = SemanticIndex()
        self.procedures: Dict[str, Dict[str, Any]] = {}  # Learned workflows
        self.episodes: List[Dict[str, Any]] = []  # Conversation summaries
        self.command_history: List[Dict[str, Any]] = []
        self.metadata = {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "version": "2.0",
            "total_interactions": 0
        }
        self._load()
    
    def _ensure_dir(self):
        """Ensure memory directory exists"""
        Path(self.MEMORY_DIR).mkdir(parents=True, exist_ok=True)
    
    def _load(self):
        """Load memories from disk"""
        try:
            if os.path.exists(self.MEMORY_FILE):
                with open(self.MEMORY_FILE, 'r') as f:
                    data = json.load(f)
                
                # Load memories
                for mem_data in data.get("memories", []):
                    mem = MemoryItem.from_dict(mem_data)
                    self.memories[mem.id] = mem
                    self.semantic_index.add_document(mem.id, mem.content)
                
                # Load procedures
                self.procedures = data.get("procedures", {})
                
                # Load episodes
                self.episodes = data.get("episodes", [])
                
                # Load command history
                self.command_history = data.get("command_history", [])
                
                # Load metadata
                if "metadata" in data:
                    self.metadata.update(data["metadata"])
                    
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load memories: {e}")
    
    def _save(self):
        """Save memories to disk"""
        try:
            self._ensure_dir()
            self.metadata["last_updated"] = datetime.now().isoformat()
            
            data = {
                "memories": [m.to_dict() for m in self.memories.values()],
                "procedures": self.procedures,
                "episodes": self.episodes[-50:],  # Keep last 50 episodes
                "command_history": self.command_history[-200:],  # Keep last 200 commands
                "metadata": self.metadata
            }
            
            with open(self.MEMORY_FILE, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except IOError as e:
            print(f"Warning: Could not save memories: {e}")
    
    # ==================== CORE MEMORY OPERATIONS ====================
    
    def remember(self, content: str, memory_type: str = "fact", 
                 category: str = "general", importance: float = 0.5,
                 metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Store a new memory with intelligent processing.
        
        Args:
            content: The memory content
            memory_type: fact, preference, shortcut, episode, procedure
            category: Category for organization
            importance: Initial importance score (0-1)
            metadata: Additional metadata
        """
        # Check for similar existing memories
        similar = self.semantic_index.search(content, top_k=3)
        
        for mem_id, similarity in similar:
            if similarity > 0.85:  # Very similar - reinforce instead
                existing = self.memories.get(mem_id)
                if existing:
                    existing.reinforce()
                    self._save()
                    return {
                        "success": True,
                        "action": "reinforced",
                        "message": f"Reinforced existing memory: {existing.content[:50]}...",
                        "memory_id": mem_id
                    }
        
        # Create new memory
        mem = MemoryItem(
            content=content,
            memory_type=memory_type,
            category=category,
            importance=importance,
            metadata=metadata or {}
        )
        
        # Find associations
        associations = []
        for mem_id, similarity in similar:
            if similarity > 0.3:
                associations.append(mem_id)
                # Add reverse association
                if mem_id in self.memories:
                    self.memories[mem_id].associations.append(mem.id)
        mem.associations = associations
        
        # Store
        self.memories[mem.id] = mem
        self.semantic_index.add_document(mem.id, content)
        self._save()
        
        return {
            "success": True,
            "action": "created",
            "message": f"Remembered: {content[:50]}...",
            "memory_id": mem.id,
            "associations": len(associations)
        }
    
    def recall(self, query: str = "", category: str = None, 
               memory_type: str = None, top_k: int = 10,
               min_relevance: float = 0.1) -> Dict[str, Any]:
        """
        Intelligently recall memories.
        
        Uses semantic search + relevance scoring for best results.
        """
        results = []
        
        if query:
            # Semantic search
            search_results = self.semantic_index.search(query, top_k=top_k * 2)
            
            for mem_id, similarity in search_results:
                mem = self.memories.get(mem_id)
                if not mem:
                    continue
                
                # Apply filters
                if category and mem.category != category:
                    continue
                if memory_type and mem.type != memory_type:
                    continue
                
                # Calculate combined score
                relevance = mem.get_relevance_score()
                combined_score = (similarity * 0.6) + (relevance * 0.4)
                
                if combined_score >= min_relevance:
                    mem.access()  # Record access
                    results.append({
                        "id": mem.id,
                        "content": mem.content,
                        "type": mem.type,
                        "category": mem.category,
                        "score": round(combined_score, 3),
                        "importance": mem.importance,
                        "associations": len(mem.associations)
                    })
        else:
            # No query - return top memories by relevance
            all_mems = []
            for mem in self.memories.values():
                if category and mem.category != category:
                    continue
                if memory_type and mem.type != memory_type:
                    continue
                
                relevance = mem.get_relevance_score()
                if relevance >= min_relevance:
                    mem.access()
                    all_mems.append({
                        "id": mem.id,
                        "content": mem.content,
                        "type": mem.type,
                        "category": mem.category,
                        "score": round(relevance, 3),
                        "importance": mem.importance,
                        "associations": len(mem.associations)
                    })
            
            all_mems.sort(key=lambda x: x["score"], reverse=True)
            results = all_mems[:top_k]
        
        self._save()
        
        return {
            "success": True,
            "count": len(results),
            "memories": results
        }
    
    def forget(self, query: str = None, memory_id: str = None) -> Dict[str, Any]:
        """Forget memories by query or ID"""
        removed = 0
        
        if memory_id and memory_id in self.memories:
            # Remove by ID
            mem = self.memories.pop(memory_id)
            self.semantic_index.remove_document(memory_id)
            removed = 1
        elif query:
            # Find and remove by semantic search
            search_results = self.semantic_index.search(query, top_k=5)
            for mem_id, similarity in search_results:
                if similarity > 0.5:  # Only remove good matches
                    if mem_id in self.memories:
                        self.memories.pop(mem_id)
                        self.semantic_index.remove_document(mem_id)
                        removed += 1
        
        if removed > 0:
            self._save()
            return {"success": True, "message": f"Forgot {removed} memory(s)"}
        return {"success": False, "message": "No matching memories found"}
    
    # ==================== PREFERENCES ====================
    
    def set_preference(self, key: str, value: str) -> Dict[str, Any]:
        """Set a user preference"""
        content = f"User preference: {key} = {value}"
        return self.remember(
            content=content,
            memory_type="preference",
            category="preferences",
            importance=0.7,
            metadata={"key": key, "value": value}
        )
    
    def get_preference(self, key: str) -> Optional[str]:
        """Get a preference by key"""
        results = self.recall(query=f"preference {key}", memory_type="preference", top_k=5)
        
        for mem in results.get("memories", []):
            mem_obj = self.memories.get(mem["id"])
            if mem_obj and mem_obj.metadata.get("key") == key:
                return mem_obj.metadata.get("value")
        return None
    
    def list_preferences(self) -> Dict[str, str]:
        """List all preferences"""
        results = self.recall(memory_type="preference", top_k=50)
        prefs = {}
        for mem in results.get("memories", []):
            mem_obj = self.memories.get(mem["id"])
            if mem_obj and "key" in mem_obj.metadata:
                prefs[mem_obj.metadata["key"]] = mem_obj.metadata.get("value", "")
        return prefs
    
    # ==================== SHORTCUTS / PROCEDURES ====================
    
    def create_shortcut(self, name: str, command: str, description: str = "") -> Dict[str, Any]:
        """Create a command shortcut"""
        self.procedures[name] = {
            "command": command,
            "description": description,
            "created": datetime.now().isoformat(),
            "use_count": 0
        }
        
        # Also store as memory for semantic search
        self.remember(
            content=f"Shortcut '{name}': {command}. {description}",
            memory_type="shortcut",
            category="shortcuts",
            importance=0.6,
            metadata={"name": name, "command": command}
        )
        
        self._save()
        return {"success": True, "message": f"Created shortcut '{name}'"}
    
    def get_shortcut(self, name: str) -> Optional[str]:
        """Get a shortcut command"""
        if name in self.procedures:
            self.procedures[name]["use_count"] = self.procedures[name].get("use_count", 0) + 1
            self._save()
            return self.procedures[name]["command"]
        return None
    
    def list_shortcuts(self) -> Dict[str, str]:
        """List all shortcuts"""
        return {name: data["command"] for name, data in self.procedures.items()}
    
    def delete_shortcut(self, name: str) -> Dict[str, Any]:
        """Delete a shortcut"""
        if name in self.procedures:
            del self.procedures[name]
            self._save()
            return {"success": True, "message": f"Deleted shortcut '{name}'"}
        return {"success": False, "message": f"Shortcut '{name}' not found"}
    
    def learn_procedure(self, name: str, steps: List[str], trigger: str = "") -> Dict[str, Any]:
        """
        Learn a multi-step procedure/workflow.
        
        Args:
            name: Procedure name
            steps: List of steps to execute
            trigger: Natural language trigger phrase
        """
        self.procedures[name] = {
            "type": "procedure",
            "steps": steps,
            "trigger": trigger,
            "created": datetime.now().isoformat(),
            "use_count": 0
        }
        
        # Store as searchable memory
        steps_text = " -> ".join(steps)
        self.remember(
            content=f"Procedure '{name}': {trigger}. Steps: {steps_text}",
            memory_type="procedure",
            category="procedures",
            importance=0.7,
            metadata={"name": name, "steps": steps}
        )
        
        self._save()
        return {"success": True, "message": f"Learned procedure '{name}' with {len(steps)} steps"}
    
    # ==================== EPISODIC MEMORY ====================
    
    def save_episode(self, summary: str, key_points: List[str] = None,
                     tools_used: List[str] = None) -> Dict[str, Any]:
        """
        Save a conversation episode summary.
        
        Args:
            summary: Brief summary of what happened
            key_points: Key takeaways from the conversation
            tools_used: Tools that were used
        """
        episode = {
            "id": hashlib.md5(f"{summary}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
            "summary": summary,
            "key_points": key_points or [],
            "tools_used": tools_used or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self.episodes.append(episode)
        
        # Also store as searchable memory
        self.remember(
            content=f"Conversation: {summary}. Key points: {', '.join(key_points or [])}",
            memory_type="episode",
            category="episodes",
            importance=0.4,  # Episodes decay faster
            metadata=episode
        )
        
        self._save()
        return {"success": True, "episode_id": episode["id"]}
    
    def get_recent_episodes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation episodes"""
        return self.episodes[-limit:]
    
    # ==================== COMMAND HISTORY ====================
    
    def log_command(self, command: str, tool_used: str = None, 
                    success: bool = True) -> None:
        """Log a command for pattern learning"""
        self.command_history.append({
            "command": command,
            "tool": tool_used,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
        self.metadata["total_interactions"] = self.metadata.get("total_interactions", 0) + 1
        
        # Don't save on every command - batch saves
        if len(self.command_history) % 10 == 0:
            self._save()
    
    def get_frequent_commands(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most frequently used commands"""
        command_counts = Counter(h["command"] for h in self.command_history if h.get("command"))
        return [
            {"command": cmd, "count": count}
            for cmd, count in command_counts.most_common(limit)
        ]
    
    def get_frequent_tools(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most frequently used tools"""
        tool_counts = Counter(h["tool"] for h in self.command_history if h.get("tool"))
        return [
            {"tool": tool, "count": count}
            for tool, count in tool_counts.most_common(limit)
        ]
    
    # ==================== CONTEXT ====================
    
    def set_context(self, key: str, value: str) -> Dict[str, Any]:
        """Set current working context"""
        return self.remember(
            content=f"Current context: {key} = {value}",
            memory_type="context",
            category="context",
            importance=0.8,  # Context is important
            metadata={"key": key, "value": value, "is_current": True}
        )
    
    def get_context(self) -> Dict[str, str]:
        """Get all current context"""
        results = self.recall(memory_type="context", top_k=20)
        context = {}
        for mem in results.get("memories", []):
            mem_obj = self.memories.get(mem["id"])
            if mem_obj and mem_obj.metadata.get("is_current"):
                key = mem_obj.metadata.get("key")
                if key:
                    context[key] = mem_obj.metadata.get("value", "")
        return context
    
    def clear_context(self) -> Dict[str, Any]:
        """Clear all current context"""
        removed = 0
        for mem_id, mem in list(self.memories.items()):
            if mem.type == "context" and mem.metadata.get("is_current"):
                self.memories.pop(mem_id)
                self.semantic_index.remove_document(mem_id)
                removed += 1
        
        self._save()
        return {"success": True, "message": f"Cleared {removed} context items"}
    
    # ==================== CONSOLIDATION ====================
    
    def consolidate(self) -> Dict[str, Any]:
        """
        Consolidate and optimize memories:
        - Merge similar memories
        - Remove low-relevance memories
        - Update associations
        """
        merged = 0
        removed = 0
        
        # Find and merge very similar memories
        mem_list = list(self.memories.values())
        merged_ids = set()
        
        for i, mem1 in enumerate(mem_list):
            if mem1.id in merged_ids:
                continue
                
            similar = self.semantic_index.search(mem1.content, top_k=5)
            
            for mem_id, similarity in similar:
                if mem_id == mem1.id or mem_id in merged_ids:
                    continue
                
                if similarity > 0.9:  # Very similar
                    mem2 = self.memories.get(mem_id)
                    if mem2:
                        # Merge into mem1 (keep the more important one)
                        if mem2.importance > mem1.importance:
                            mem1, mem2 = mem2, mem1
                        
                        mem1.reinforcement_count += mem2.reinforcement_count
                        mem1.access_count += mem2.access_count
                        mem1.associations.extend(mem2.associations)
                        
                        # Remove mem2
                        self.memories.pop(mem2.id)
                        self.semantic_index.remove_document(mem2.id)
                        merged_ids.add(mem2.id)
                        merged += 1
        
        # Remove very low relevance memories (but keep recent ones)
        for mem_id, mem in list(self.memories.items()):
            relevance = mem.get_relevance_score()
            try:
                age_days = (datetime.now() - datetime.fromisoformat(mem.created_at)).days
            except:
                age_days = 0
            
            # Only remove old, low-relevance, unused memories
            if relevance < 0.1 and age_days > 30 and mem.access_count < 2:
                self.memories.pop(mem_id)
                self.semantic_index.remove_document(mem_id)
                removed += 1
        
        self._save()
        
        return {
            "success": True,
            "merged": merged,
            "removed": removed,
            "remaining": len(self.memories)
        }
    
    # ==================== SUMMARY FOR PROMPT ====================
    
    def get_memory_summary(self, max_items: int = 10) -> str:
        """
        Get a concise summary of relevant memories for the system prompt.
        Intelligently selects the most relevant memories.
        """
        summary_parts = []
        
        # Get preferences
        prefs = self.list_preferences()
        if prefs:
            pref_items = list(prefs.items())[:5]
            pref_str = ", ".join(f"{k}={v}" for k, v in pref_items)
            summary_parts.append(f"Preferences: {pref_str}")
        
        # Get current context
        context = self.get_context()
        if context:
            ctx_items = list(context.items())[:3]
            ctx_str = ", ".join(f"{k}={v}" for k, v in ctx_items)
            summary_parts.append(f"Context: {ctx_str}")
        
        # Get top relevant facts
        facts = self.recall(memory_type="fact", top_k=5)
        fact_contents = [m["content"][:100] for m in facts.get("memories", [])]
        if fact_contents:
            summary_parts.append(f"Known facts: {'; '.join(fact_contents)}")
        
        # Get shortcuts
        shortcuts = self.list_shortcuts()
        if shortcuts:
            shortcut_names = list(shortcuts.keys())[:5]
            summary_parts.append(f"User shortcuts: {', '.join(shortcut_names)}")
        
        # Get recent episode
        recent = self.get_recent_episodes(1)
        if recent:
            summary_parts.append(f"Recent: {recent[0]['summary'][:100]}")
        
        return "\n".join(summary_parts) if summary_parts else ""
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        type_counts = Counter(m.type for m in self.memories.values())
        return {
            "total_memories": len(self.memories),
            "by_type": dict(type_counts),
            "shortcuts": len(self.procedures),
            "episodes": len(self.episodes),
            "commands_logged": len(self.command_history),
            "total_interactions": self.metadata.get("total_interactions", 0)
        }
    
    # ==================== RESET ====================
    
    def reset_all(self) -> Dict[str, Any]:
        """Reset all memories"""
        self.memories = {}
        self.semantic_index = SemanticIndex()
        self.procedures = {}
        self.episodes = []
        self.command_history = []
        self.metadata = {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "version": "2.0",
            "total_interactions": 0
        }
        self._save()
        return {"success": True, "message": "All memories reset"}


# Global instance
_memory_instance = None

def get_memory() -> AgentMemory:
    """Get or create the global memory instance"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = AgentMemory()
    return _memory_instance
