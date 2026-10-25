"""
TencentDB Agent Memory Integration Module

Integrates TencentDB Agent Memory v2 API for:
- Layered memory architecture (L0-L3)
- Symbolic memory with Mermaid canvas
- Short-term context compression (offload)
- Hybrid recall (BM25 + vector + RRF)

Features:
- Token savings up to 61.38% (benchmark: WideSearch)
- Task success rate improvement up to 51.52%
- Persona memory accuracy improvement from 48% to 76%

Usage:
    >>> from cursor_framework import TDAMIntegration
    >>> tdam = TDAMIntegration()
    >>> tdam.capture_conversation("session-1", messages)
    >>> memories = tdam.recall("user preferences")
    >>> canvas = tdam.get_mermaid_canvas("session-1")
"""

from __future__ import annotations

import os
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class MemoryLayer(Enum):
    """
    TDAM Memory Layer levels (from abstract to concrete).

    Maps to TDAM's L0-L3 architecture:
    - L3_Persona: User profile, preferences, communication style
    - L2_Scenario: Scene blocks, workflow patterns
    - L1_Atom: Atomic facts, specific details
    - L0_Conversation: Raw conversation history
    """

    L3_PERSONA = "l3_persona"  # User profile/preferences
    L2_SCENARIO = "l2_scenario"  # Scene/workflow blocks
    L1_ATOM = "l1_atom"  # Atomic facts
    L0_CONVERSATION = "l0_conversation"  # Raw messages


class OffloadStrategy(Enum):
    """Context offload strategies for short-term memory."""

    MILD = "mild"  # Trigger at 50% context window
    AGGRESSIVE = "aggressive"  # Trigger at 85% context window
    ADAPTIVE = "adaptive"  # Auto-adjust based on task type


@dataclass
class TDAMConfig:
    """Configuration for TencentDB Agent Memory integration."""

    # Connection
    endpoint: str = "http://127.0.0.1:8420"
    api_key: Optional[str] = None
    service_id: Optional[str] = None

    # Recall settings
    recall_strategy: str = "hybrid"  # keyword | embedding | hybrid
    max_results: int = 5
    max_chars_per_memory: int = 0  # 0 = no limit
    max_total_recall_chars: int = 0  # 0 = no limit
    recall_timeout_ms: int = 5000

    # Pipeline settings
    l1_every_n_conversations: int = 5
    max_memories_per_session: int = 20
    l1_idle_timeout_seconds: int = 600
    l2_min_interval_seconds: int = 900
    persona_trigger_every_n: int = 50

    # Offload settings
    offload_enabled: bool = False
    mild_offload_ratio: float = 0.5
    aggressive_compress_ratio: float = 0.85
    mmd_max_token_ratio: float = 0.2  # Mermaid canvas token budget

    # Storage backend
    store_backend: str = "sqlite"  # sqlite | memory
    data_dir: Optional[Path] = None

    # Embedding (optional, for vector search)
    embedding_enabled: bool = False
    embedding_base_url: Optional[str] = None
    embedding_api_key: Optional[str] = None
    embedding_model: Optional[str] = None

    def from_env(self) -> "TDAMConfig":
        """Load configuration from environment variables."""
        self.endpoint = os.getenv("TDAM_ENDPOINT", self.endpoint)
        self.api_key = os.getenv("TDAM_API_KEY", self.api_key)
        self.service_id = os.getenv("TDAM_SERVICE_ID", self.service_id)
        self.offload_enabled = os.getenv("TDAM_OFFLOAD_ENABLED", str(self.offload_enabled)).lower() == "true"
        return self


@dataclass
class MemoryItem:
    """A single memory item from recall."""

    id: str
    content: str
    layer: MemoryLayer
    score: float
    session_id: Optional[str] = None
    created_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationTurn:
    """A single turn in a conversation."""

    role: str  # user | assistant | system | tool
    content: str
    tool_name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_params: Optional[dict] = None
    tool_result: Optional[str] = None
    timestamp: Optional[datetime] = None


@dataclass
class OffloadResult:
    """Result from context offload/compression."""

    messages: list[dict]
    mermaid_canvas: str
    report: dict[str, Any]
    tokens_before: int
    tokens_after: int
    compression_ratio: float


class TDAMClient:
    """
    Client for TencentDB Agent Memory Gateway API.

    Wraps the Python SDK's MemoryClient with framework-specific
    convenience methods and error handling.
    """

    def __init__(self, config: Optional[TDAMConfig] = None):
        self.config = config or TDAMConfig()
        self._client = None
        self._async_client = None
        self._connected = False

    def _ensure_client(self):
        """Lazy initialization of HTTP client."""
        if self._client is not None:
            return

        try:
            import httpx
            self._client = httpx.Client(
                base_url=self.config.endpoint,
                timeout=30.0,
                headers=self._build_headers(),
            )
            self._connected = True
            logger.info("TDAM client connected to %s", self.config.endpoint)
        except ImportError:
            logger.warning("httpx not installed, TDAM remote features disabled")
            self._connected = False

    def _build_headers(self) -> dict[str, str]:
        """Build request headers."""
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def is_connected(self) -> bool:
        """Check if TDAM Gateway is reachable."""
        try:
            self._ensure_client()
            if self._client is None:
                return False
            resp = self._client.get("/health")
            return resp.status_code == 200
        except Exception:
            return False

    # === L0: Conversation Management ===

    def add_conversation(self, session_id: str, messages: list[ConversationTurn]) -> dict:
        """
        Add a conversation turn to L0 layer.

        Args:
            session_id: Unique session identifier
            messages: List of conversation turns

        Returns:
            Dict with accepted_ids
        """
        self._ensure_client()
        if self._client is None:
            return {"accepted_ids": [], "error": "client not available"}

        payload = {
            "session_key": session_id,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "tool_name": m.tool_name,
                    "tool_call_id": m.tool_call_id,
                    "tool_params": m.tool_params,
                    "tool_result": m.tool_result,
                    "timestamp": (m.timestamp or datetime.now()).isoformat(),
                }
                for m in messages
            ],
        }

        try:
            resp = self._client.post("/v2/conversation/add", json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error("Failed to add conversation: %s", e)
            return {"accepted_ids": [], "error": str(e)}

    def search_conversations(
        self, query: str, session_id: Optional[str] = None, limit: int = 5
    ) -> list[MemoryItem]:
        """Search L0 conversation history."""
        self._ensure_client()
        if self._client is None:
            return []

        payload = {"query": query, "limit": limit}
        if session_id:
            payload["session_key"] = session_id

        try:
            resp = self._client.post("/v2/conversation/search", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return [
                MemoryItem(
                    id=item.get("id", ""),
                    content=item.get("content", ""),
                    layer=MemoryLayer.L0_CONVERSATION,
                    score=item.get("score", 0.0),
                    session_id=item.get("session_key"),
                )
                for item in data.get("items", [])
            ]
        except Exception as e:
            logger.error("Failed to search conversations: %s", e)
            return []

    # === L1: Atomic Memory Management ===

    def search_atomic(self, query: str, limit: int = 5) -> list[MemoryItem]:
        """
        Search L1 atomic memories (facts).

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching memory items
        """
        self._ensure_client()
        if self._client is None:
            return []

        payload = {"query": query, "limit": limit}
        if self.config.max_chars_per_memory > 0:
            payload["max_chars"] = self.config.max_chars_per_memory

        try:
            resp = self._client.post("/v2/atomic/search", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return [
                MemoryItem(
                    id=item.get("id", ""),
                    content=item.get("content", ""),
                    layer=MemoryLayer.L1_ATOM,
                    score=item.get("score", 0.0),
                    metadata=item.get("metadata", {}),
                )
                for item in data.get("items", [])
            ]
        except Exception as e:
            logger.error("Failed to search atomic memories: %s", e)
            return []

    def update_atomic(
        self, memory_id: str, content: str, background: Optional[str] = None
    ) -> bool:
        """Update an existing L1 atomic memory."""
        self._ensure_client()
        if self._client is None:
            return False

        payload = {"id": memory_id, "content": content}
        if background:
            payload["background"] = background

        try:
            resp = self._client.post("/v2/atomic/update", json=payload)
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error("Failed to update atomic memory: %s", e)
            return False

    # === L2: Scenario Management ===

    def list_scenarios(self, path_prefix: str = "") -> list[str]:
        """List L2 scenario files."""
        self._ensure_client()
        if self._client is None:
            return []

        try:
            resp = self._client.post("/v2/scenario/ls", json={"path_prefix": path_prefix})
            resp.raise_for_status()
            data = resp.json()
            return [entry.get("name", "") for entry in data.get("entries", [])]
        except Exception as e:
            logger.error("Failed to list scenarios: %s", e)
            return []

    def read_scenario(self, path: str) -> Optional[str]:
        """Read a L2 scenario file."""
        self._ensure_client()
        if self._client is None:
            return None

        try:
            resp = self._client.post("/v2/scenario/read", json={"path": path})
            resp.raise_for_status()
            return resp.json().get("content")
        except Exception as e:
            logger.error("Failed to read scenario: %s", e)
            return None

    def write_scenario(
        self, path: str, content: str, summary: Optional[str] = None
    ) -> bool:
        """Write a L2 scenario file."""
        self._ensure_client()
        if self._client is None:
            return False

        payload = {"path": path, "content": content}
        if summary:
            payload["summary"] = summary

        try:
            resp = self._client.post("/v2/scenario/write", json=payload)
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error("Failed to write scenario: %s", e)
            return False

    # === L3: Core Memory (Persona) ===

    def read_persona(self) -> Optional[str]:
        """Read L3 persona (user profile)."""
        self._ensure_client()
        if self._client is None:
            return None

        try:
            resp = self._client.post("/v2/core/read", json={})
            resp.raise_for_status()
            return resp.json().get("content")
        except Exception as e:
            logger.error("Failed to read persona: %s", e)
            return None

    def write_persona(self, content: str) -> bool:
        """Write L3 persona (user profile)."""
        self._ensure_client()
        if self._client is None:
            return False

        try:
            resp = self._client.post("/v2/core/write", json={"content": content})
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error("Failed to write persona: %s", e)
            return False

    # === Offload: Short-term Context Compression ===

    def offload_ingest(
        self,
        session_id: str,
        tool_pairs: list[dict],
    ) -> bool:
        """
        Fire-and-forget ingest of tool calls for async L1 processing.

        Args:
            session_id: Session identifier
            tool_pairs: List of {tool_name, tool_call_id, params, result, timestamp}

        Returns:
            True if accepted
        """
        self._ensure_client()
        if self._client is None:
            return False

        payload = {"session_id": session_id, "tool_pairs": tool_pairs}

        try:
            resp = self._client.post("/v2/offload/ingest", json=payload)
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error("Failed to ingest offload: %s", e)
            return False

    def offload_compact(
        self,
        session_id: str,
        messages: list[ConversationTurn],
        ratio: float = 0.7,
        context_window: int = 128000,
    ) -> Optional[OffloadResult]:
        """
        Compact context into Mermaid canvas.

        Args:
            session_id: Session identifier
            messages: Conversation messages to compact
            ratio: Target compression ratio (0.0-1.0)
            context_window: Context window size

        Returns:
            OffloadResult with compressed messages and canvas
        """
        self._ensure_client()
        if self._client is None:
            return None

        payload = {
            "session_id": session_id,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": (m.timestamp or datetime.now()).isoformat(),
                }
                for m in messages
            ],
            "ratio": ratio,
            "context_window": context_window,
        }

        try:
            resp = self._client.post("/v2/offload/compact", json=payload)
            resp.raise_for_status()
            data = resp.json()

            tokens_before = sum(len(m.get("content", "").split()) // 4 for m in messages)
            tokens_after = int(tokens_before * ratio)

            return OffloadResult(
                messages=data.get("messages", []),
                mermaid_canvas=data.get("mmd", ""),
                report=data.get("report", {}),
                tokens_before=tokens_before,
                tokens_after=tokens_after,
                compression_ratio=ratio,
            )
        except Exception as e:
            logger.error("Failed to compact context: %s", e)
            return None

    def query_mmd(self, session_id: str, node_ids: list[str]) -> list[dict]:
        """
        Query raw content from offloaded Mermaid canvas nodes.

        Args:
            session_id: Session identifier
            node_ids: List of node IDs to retrieve

        Returns:
            List of {node_id, content} dicts
        """
        self._ensure_client()
        if self._client is None:
            return []

        payload = {"session_id": session_id, "node_ids": node_ids}

        try:
            resp = self._client.post("/v2/offload/query-mmd", json=payload)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except Exception as e:
            logger.error("Failed to query MMD: %s", e)
            return []

    def close(self):
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None


class TDAMIntegration:
    """
    High-level integration for TencentDB Agent Memory.

    Provides a unified interface combining:
    - TDAM layered memory (L0-L3)
    - Symbolic memory (Mermaid canvas)
    - Short-term context compression
    - Hybrid recall

    Usage:
        >>> tdam = TDAMIntegration()
        >>> tdam.capture_conversation("session-1", messages)
        >>> memories = tdam.recall("user preferences")
        >>> context = tdam.build_context("session-1", "design landing page")
    """

    def __init__(self, config: Optional[TDAMConfig] = None):
        self.config = config or TDAMConfig()
        self.client = TDAMClient(self.config)
        self._local_cache: dict[str, list[MemoryItem]] = {}
        self._persona_cache: Optional[str] = None
        self._last_recall_time: Optional[datetime] = None

    @classmethod
    def from_env(cls) -> "TDAMIntegration":
        """Create integration from environment variables."""
        config = TDAMConfig().from_env()
        return cls(config)

    def is_available(self) -> bool:
        """Check if TDAM Gateway is available."""
        return self.client.is_connected()

    # === High-level Operations ===

    def capture_conversation(
        self, session_id: str, messages: list[ConversationTurn]
    ) -> dict:
        """
        Capture conversation into L0 layer and trigger L1 extraction.

        Args:
            session_id: Session identifier
            messages: Conversation turns

        Returns:
            Capture result with IDs
        """
        result = self.client.add_conversation(session_id, messages)

        # Auto-cache for local access
        if session_id not in self._local_cache:
            self._local_cache[session_id] = []

        return result

    def capture_tool_call(
        self,
        session_id: str,
        tool_name: str,
        params: dict,
        result: str,
        call_id: Optional[str] = None,
    ) -> bool:
        """
        Capture a single tool call for async L1 processing.

        This is fire-and-forget - use for logging tool executions
        without blocking the main flow.

        Args:
            session_id: Session identifier
            tool_name: Name of the tool
            params: Tool parameters
            result: Tool execution result
            call_id: Optional call ID

        Returns:
            True if accepted for processing
        """
        tool_pair = {
            "tool_name": tool_name,
            "tool_call_id": call_id or f"call_{datetime.now().timestamp()}",
            "params": params,
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }
        return self.client.offload_ingest(session_id, [tool_pair])

    def recall(
        self,
        query: str,
        layers: Optional[list[MemoryLayer]] = None,
        limit: int = 5,
    ) -> list[MemoryItem]:
        """
        Recall memories across layers using hybrid search.

        Args:
            query: Search query
            layers: Specific layers to search (default: all)
            limit: Maximum results per layer

        Returns:
            List of matching memory items, sorted by relevance
        """
        layers = layers or [
            MemoryLayer.L3_PERSONA,
            MemoryLayer.L2_SCENARIO,
            MemoryLayer.L1_ATOM,
        ]

        results: list[MemoryItem] = []
        seen_ids: set[str] = set()

        for layer in layers:
            items: list[MemoryItem] = []

            if layer == MemoryLayer.L1_ATOM:
                items = self.client.search_atomic(query, limit)
            elif layer == MemoryLayer.L0_CONVERSATION:
                items = self.client.search_conversations(query, limit=limit)
            # L2 and L3 require path-based access, not search
            # For L2, use list_scenarios + read_scenario
            # For L3, use read_persona directly

            for item in items:
                if item.id not in seen_ids:
                    results.append(item)
                    seen_ids.add(item.id)

        self._last_recall_time = datetime.now()
        return results[: limit * len(layers)]

    def get_persona(self) -> Optional[str]:
        """
        Get user persona from L3 layer.

        Returns cached version if available.
        """
        if self._persona_cache:
            return self._persona_cache

        self._persona_cache = self.client.read_persona()
        return self._persona_cache

    def update_persona(self, content: str) -> bool:
        """
        Update user persona in L3 layer.

        Args:
            content: New persona content (Markdown)

        Returns:
            True if updated successfully
        """
        success = self.client.write_persona(content)
        if success:
            self._persona_cache = content
        return success

    def get_scenario(self, path: str) -> Optional[str]:
        """
        Read a scenario from L2 layer.

        Args:
            path: Scenario file path (e.g., "工作.md", "project-alpha.md")

        Returns:
            Scenario content or None
        """
        return self.client.read_scenario(path)

    def list_scenarios(self, prefix: str = "") -> list[str]:
        """List available scenarios from L2 layer."""
        return self.client.list_scenarios(prefix)

    def compact_context(
        self,
        session_id: str,
        messages: list[ConversationTurn],
        ratio: float = 0.7,
        context_window: int = 128000,
    ) -> Optional[OffloadResult]:
        """
        Compact conversation into Mermaid canvas.

        This is the core short-term memory compression:
        - Offloads verbose tool logs to external storage
        - Converts state to lightweight Mermaid symbols
        - Preserves traceability via node_id references

        Args:
            session_id: Session identifier
            messages: Conversation to compact
            ratio: Target compression (0.7 = keep 70% meaning in 70% tokens)
            context_window: Context window size

        Returns:
            OffloadResult with compressed content and canvas
        """
        return self.client.offload_compact(session_id, messages, ratio, context_window)

    def get_mermaid_canvas(self, session_id: str) -> str:
        """
        Get Mermaid canvas for a session.

        The canvas shows task state as a graph with node_id references.
        Use with query_mmd() to retrieve full content for specific nodes.

        Args:
            session_id: Session identifier

        Returns:
            Mermaid diagram string
        """
        # For now, return empty - would need session-specific endpoint
        # This will be enhanced when we have session canvas API
        return ""

    def build_context(
        self,
        session_id: str,
        current_task: str,
        max_tokens: int = 4000,
    ) -> dict[str, Any]:
        """
        Build a complete context from all memory layers.

        This is the main entry point for context-aware task execution:
        1. Recall relevant memories (L1, L2, L3)
        2. Load persona (L3) for user preferences
        3. Load relevant scenarios (L2) for workflow patterns
        4. Compress into token budget

        Args:
            session_id: Current session
            current_task: Current task description
            max_tokens: Maximum tokens for context

        Returns:
            Dict with {persona, scenarios, memories, canvas, total_tokens}
        """
        context: dict[str, Any] = {
            "session_id": session_id,
            "task": current_task,
            "persona": None,
            "scenarios": [],
            "memories": [],
            "canvas": "",
            "total_tokens": 0,
        }

        # 1. Load persona (L3) - typically small, always include
        persona = self.get_persona()
        if persona:
            context["persona"] = persona

        # 2. Recall relevant memories (L1)
        memories = self.recall(current_task, layers=[MemoryLayer.L1_ATOM], limit=5)
        context["memories"] = [
            {"id": m.id, "content": m.content, "score": m.score}
            for m in memories
        ]

        # 3. Estimate tokens
        persona_tokens = len(persona.split()) // 4 if persona else 0
        memory_tokens = sum(len(m["content"].split()) // 4 for m in context["memories"])
        context["total_tokens"] = persona_tokens + memory_tokens

        # 4. If over budget, compress memories
        if context["total_tokens"] > max_tokens:
            # Keep high-score memories, drop others
            budget = max_tokens - persona_tokens - 200  # Reserve for overhead
            kept = []
            for m in sorted(context["memories"], key=lambda x: x["score"], reverse=True):
                if budget <= 0:
                    break
                m_tokens = len(m["content"].split()) // 4
                if m_tokens <= budget:
                    kept.append(m)
                    budget -= m_tokens
            context["memories"] = kept
            context["total_tokens"] = persona_tokens + sum(
                len(m["content"].split()) // 4 for m in kept
            )

        return context

    def close(self):
        """Clean up resources."""
        self.client.close()


# === Factory Functions ===

def create_tdam_integration(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    service_id: Optional[str] = None,
) -> TDAMIntegration:
    """
    Create a configured TDAMIntegration instance.

    Args:
        endpoint: TDAM Gateway URL
        api_key: API key for authentication
        service_id: Service/team identifier

    Returns:
        Configured TDAMIntegration instance
    """
    config = TDAMConfig(
        endpoint=endpoint or "http://127.0.0.1:8420",
        api_key=api_key,
        service_id=service_id,
    )
    return TDAMIntegration(config)


def create_tdam_integration_from_env() -> TDAMIntegration:
    """Create TDAMIntegration from environment variables."""
    return TDAMIntegration.from_env()
