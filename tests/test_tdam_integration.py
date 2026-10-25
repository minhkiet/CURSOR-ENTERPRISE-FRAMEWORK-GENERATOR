"""
Tests for TencentDB Agent Memory integration.

These tests verify:
- TDAMConfig loading from environment
- TDAMClient connection handling
- TDAMIntegration high-level operations
- MemoryManager TDAM sync methods
- TokenOptimizer Mermaid compression
- ContextBuilder with TDAM recall
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime


class TestTDAMConfig:
    """Tests for TDAMConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        from cursor_framework import TDAMConfig

        config = TDAMConfig()
        assert config.endpoint == "http://127.0.0.1:8420"
        assert config.recall_strategy == "hybrid"
        assert config.max_results == 5
        assert config.offload_enabled is False

    def test_config_from_env(self):
        """Test loading config from environment variables."""
        from cursor_framework import TDAMConfig

        with patch.dict(
            "os.environ",
            {
                "TDAM_ENDPOINT": "http://custom:9000",
                "TDAM_API_KEY": "test-key-123",
                "TDAM_SERVICE_ID": "my-service",
                "TDAM_OFFLOAD_ENABLED": "true",
            },
            clear=False,
        ):
            config = TDAMConfig().from_env()
            assert config.endpoint == "http://custom:9000"
            assert config.api_key == "test-key-123"
            assert config.service_id == "my-service"
            assert config.offload_enabled is True


class TestTDAMClient:
    """Tests for TDAMClient."""

    def test_client_init(self):
        """Test client initialization."""
        from cursor_framework import TDAMClient, TDAMConfig

        config = TDAMConfig(endpoint="http://test:8420")
        client = TDAMClient(config)
        assert client.config.endpoint == "http://test:8420"
        assert client._client is None  # Lazy init

    def test_is_connected_false_when_no_client(self):
        """Test connection check returns False when not connected."""
        from cursor_framework import TDAMClient, TDAMConfig

        config = TDAMConfig()
        client = TDAMClient(config)

        # Mock _ensure_client to raise
        with patch.object(client, "_ensure_client", side_effect=Exception("test")):
            assert client.is_connected() is False

    def test_add_conversation_without_client(self):
        """Test add_conversation returns error dict when no client."""
        from cursor_framework import TDAMClient, TDAMConfig, ConversationTurn

        client = TDAMClient(TDAMConfig())
        messages = [
            ConversationTurn(role="user", content="Hello"),
            ConversationTurn(role="assistant", content="Hi!"),
        ]

        result = client.add_conversation("session-1", messages)
        assert "error" in result
        assert result["accepted_ids"] == []


class TestTDAMIntegration:
    """Tests for TDAMIntegration high-level interface."""

    def test_integration_init(self):
        """Test integration initialization."""
        from cursor_framework import TDAMIntegration, TDAMConfig

        config = TDAMConfig(endpoint="http://test:8420")
        tdam = TDAMIntegration(config)

        assert tdam.config.endpoint == "http://test:8420"
        assert tdam.client is not None
        assert tdam._local_cache == {}

    def test_integration_from_env(self):
        """Test creating integration from environment."""
        from cursor_framework import TDAMIntegration

        with patch.dict(
            "os.environ",
            {"TDAM_ENDPOINT": "http://env:8420"},
            clear=False,
        ):
            tdam = TDAMIntegration.from_env()
            assert tdam.config.endpoint == "http://env:8420"

    def test_is_available_returns_false_when_not_connected(self):
        """Test is_available returns False when gateway not reachable."""
        from cursor_framework import TDAMIntegration

        tdam = TDAMIntegration()

        with patch.object(tdam.client, "is_connected", return_value=False):
            assert tdam.is_available() is False

    def test_capture_conversation(self):
        """Test capturing conversation."""
        from cursor_framework import TDAMIntegration, ConversationTurn

        tdam = TDAMIntegration()

        # Mock the client
        mock_result = {"accepted_ids": ["msg-1", "msg-2"]}
        with patch.object(
            tdam.client, "add_conversation", return_value=mock_result
        ):
            messages = [
                ConversationTurn(role="user", content="Test"),
            ]
            result = tdam.capture_conversation("session-1", messages)

            assert result["accepted_ids"] == ["msg-1", "msg-2"]
            assert "session-1" in tdam._local_cache

    def test_capture_tool_call(self):
        """Test capturing tool call (fire-and-forget)."""
        from cursor_framework import TDAMIntegration

        tdam = TDAMIntegration()

        with patch.object(
            tdam.client, "offload_ingest", return_value=True
        ) as mock_ingest:
            result = tdam.capture_tool_call(
                session_id="session-1",
                tool_name="search",
                params={"q": "test"},
                result="Search results here",
            )

            assert result is True
            mock_ingest.assert_called_once()
            call_args = mock_ingest.call_args[0]
            assert call_args[0] == "session-1"
            assert len(call_args[1]) == 1
            assert call_args[1][0]["tool_name"] == "search"

    def test_recall(self):
        """Test recalling memories."""
        from cursor_framework import TDAMIntegration, MemoryLayer, MemoryItem

        tdam = TDAMIntegration()

        mock_items = [
            MemoryItem(
                id="mem-1",
                content="User prefers dark mode",
                layer=MemoryLayer.L1_ATOM,
                score=0.95,
            ),
            MemoryItem(
                id="mem-2",
                content="Project uses TypeScript",
                layer=MemoryLayer.L1_ATOM,
                score=0.88,
            ),
        ]

        with patch.object(
            tdam.client, "search_atomic", return_value=mock_items
        ):
            results = tdam.recall("user preferences", limit=5)
            assert len(results) == 2
            assert results[0].content == "User prefers dark mode"

    def test_get_persona_caching(self):
        """Test persona caching."""
        from cursor_framework import TDAMIntegration

        tdam = TDAMIntegration()
        assert tdam._persona_cache is None

        with patch.object(
            tdam.client, "read_persona", return_value="# User Profile\n..."
        ) as mock_read:
            persona = tdam.get_persona()
            assert persona == "# User Profile\n..."
            assert tdam._persona_cache == "# User Profile\n..."

            # Second call should use cache
            persona2 = tdam.get_persona()
            assert persona2 == "# User Profile\n..."
            mock_read.assert_called_once()  # Only called once

    def test_update_persona(self):
        """Test updating persona."""
        from cursor_framework import TDAMIntegration

        tdam = TDAMIntegration()

        with patch.object(
            tdam.client, "write_persona", return_value=True
        ) as mock_write:
            result = tdam.update_persona("# Updated Profile\n...")
            assert result is True
            mock_write.assert_called_once_with("# Updated Profile\n...")
            assert tdam._persona_cache == "# Updated Profile\n..."

    def test_compact_context(self):
        """Test context compaction."""
        from cursor_framework import TDAMIntegration, ConversationTurn, OffloadResult

        tdam = TDAMIntegration()

        mock_result = OffloadResult(
            messages=[{"role": "user", "content": "Summary"}],
            mermaid_canvas="graph LR\n  A --> B",
            report={"compressed": True},
            tokens_before=10000,
            tokens_after=3000,
            compression_ratio=0.3,
        )

        with patch.object(
            tdam.client, "offload_compact", return_value=mock_result
        ):
            messages = [
                ConversationTurn(role="user", content="Long conversation..."),
                ConversationTurn(role="assistant", content="Response..."),
            ]
            result = tdam.compact_context(
                "session-1", messages, ratio=0.3, context_window=128000
            )

            assert result is not None
            assert result.tokens_before == 10000
            assert result.tokens_after == 3000
            assert result.compression_ratio == 0.3


class TestMemoryManagerTDAM:
    """Tests for MemoryManager TDAM integration methods."""

    def test_set_tdam_integration(self):
        """Test attaching TDAM to MemoryManager."""
        from cursor_framework import MemoryManager, TDAMIntegration

        manager = MemoryManager()
        tdam = TDAMIntegration()

        manager.set_tdam_integration(tdam)
        assert hasattr(manager, "_tdam")
        assert manager._tdam is tdam

    def test_sync_to_tdam(self):
        """Test syncing hot tier to TDAM."""
        from cursor_framework import MemoryManager, TDAMIntegration, MemoryTier

        manager = MemoryManager()
        tdam = TDAMIntegration()

        # Add some entries
        manager.store("key1", "value1", tier=MemoryTier.HOT)
        manager.store("key2", "value2", tier=MemoryTier.HOT)

        with patch.object(
            tdam, "capture_conversation", return_value={"accepted_ids": ["id-1"]}
        ):
            manager.set_tdam_integration(tdam)
            result = manager.sync_to_tdam("session-1")

            assert result["synced"] == 2
            assert "result" in result

    def test_recall_from_tdam(self):
        """Test recalling from TDAM."""
        from cursor_framework import MemoryManager, TDAMIntegration, MemoryLayer, MemoryItem

        manager = MemoryManager()
        tdam = TDAMIntegration()

        mock_items = [
            MemoryItem(
                id="mem-1",
                content="Test memory",
                layer=MemoryLayer.L1_ATOM,
                score=0.9,
            )
        ]

        with patch.object(tdam, "recall", return_value=mock_items):
            manager.set_tdam_integration(tdam)
            results = manager.recall_from_tdam("test query")

            assert len(results) == 1
            assert results[0].content == "Test memory"

    def test_get_persona_from_tdam(self):
        """Test getting persona from TDAM."""
        from cursor_framework import MemoryManager, TDAMIntegration

        manager = MemoryManager()
        tdam = TDAMIntegration()

        with patch.object(tdam, "get_persona", return_value="# Persona"):
            manager.set_tdam_integration(tdam)
            persona = manager.get_persona_from_tdam()

            assert persona == "# Persona"

    def test_compact_context_to_tdam(self):
        """Test compacting context via TDAM."""
        from cursor_framework import (
            MemoryManager,
            TDAMIntegration,
            ConversationTurn,
            OffloadResult,
        )

        manager = MemoryManager()
        tdam = TDAMIntegration()

        mock_result = OffloadResult(
            messages=[],
            mermaid_canvas="graph LR",
            report={},
            tokens_before=5000,
            tokens_after=1500,
            compression_ratio=0.3,
        )

        with patch.object(tdam, "compact_context", return_value=mock_result):
            manager.set_tdam_integration(tdam)
            messages = [ConversationTurn(role="user", content="Test")]
            result = manager.compact_context_to_tdam("session-1", messages)

            assert result is not None
            assert result.tokens_after == 1500

    def test_get_tdam_stats(self):
        """Test getting combined stats."""
        from cursor_framework import MemoryManager, TDAMIntegration

        manager = MemoryManager()
        tdam = TDAMIntegration()

        with patch.object(tdam, "is_available", return_value=True):
            manager.set_tdam_integration(tdam)
            stats = manager.get_tdam_stats()

            assert "local" in stats
            assert "tdam" in stats
            assert stats["tdam"]["tdam_available"] is True


class TestTokenOptimizerTDAM:
    """Tests for TokenOptimizer TDAM integration."""

    def test_set_tdam(self):
        """Test attaching TDAM to TokenOptimizer."""
        from cursor_framework import TokenOptimizer, TDAMIntegration

        optimizer = TokenOptimizer()
        tdam = TDAMIntegration()

        optimizer.set_tdam(tdam)
        assert hasattr(optimizer, "_tdam")
        assert optimizer._tdam is tdam

    def test_compact_with_mermaid(self):
        """Test Mermaid-based compression."""
        from cursor_framework import TokenOptimizer, TDAMIntegration, OffloadResult

        optimizer = TokenOptimizer()
        tdam = TDAMIntegration()

        mock_result = OffloadResult(
            messages=[{"role": "user", "content": "Hi"}],
            mermaid_canvas="graph LR\n  A-->B",
            report={},
            tokens_before=10000,
            tokens_after=3000,
            compression_ratio=0.3,
        )

        with patch.object(tdam, "compact_context", return_value=mock_result):
            optimizer.set_tdam(tdam)
            result = optimizer.compact_with_mermaid(
                "session-1",
                [{"role": "user", "content": "Hello world"}],
                ratio=0.3,
            )

            assert result is not None
            assert result.tokens_after == 3000

    def test_compact_with_mermaid_fallback(self):
        """Test fallback when TDAM not configured."""
        from cursor_framework import TokenOptimizer

        optimizer = TokenOptimizer()
        # Don't set TDAM

        result = optimizer.compact_with_mermaid(
            "session-1",
            [{"role": "user", "content": "Hello"}],
        )

        assert result is None

    def test_build_mermaid_context(self):
        """Test building context with Mermaid."""
        from cursor_framework import TokenOptimizer, TDAMIntegration

        optimizer = TokenOptimizer()
        tdam = TDAMIntegration()

        with patch.object(
            tdam, "build_context", return_value={
                "persona": "# User",
                "memories": [{"id": "1", "content": "Test", "score": 0.9}],
                "canvas": "graph LR\n  A-->B",
                "total_tokens": 500,
            }
        ):
            optimizer.set_tdam(tdam)
            result = optimizer.build_mermaid_context(
                "session-1", "design landing page", max_tokens=4000
            )

            assert "text" in result
            assert result["persona"] == "# User"
            assert result["canvas"] == "graph LR\n  A-->B"

    def test_should_trigger_offload(self):
        """Test offload threshold detection."""
        from cursor_framework import TokenOptimizer

        optimizer = TokenOptimizer(max_tokens=100000, compression_threshold=0.7)

        # Threshold is 70000 (100000 * 0.7)
        assert optimizer.should_trigger_offload(60000) is False
        assert optimizer.should_trigger_offload(75000) is True


class TestContextBuilderTDAM:
    """Tests for ContextBuilder TDAM integration."""

    def test_set_tdam(self):
        """Test attaching TDAM to ContextBuilder."""
        from cursor_framework import ContextBuilder, TDAMIntegration

        cb = ContextBuilder()
        tdam = TDAMIntegration()

        cb.set_tdam(tdam)
        assert hasattr(cb, "_tdam")
        assert cb._tdam is tdam

    def test_build_with_memory(self):
        """Test building context with memory integration."""
        from cursor_framework import ContextBuilder, TDAMIntegration, MemoryItem, MemoryLayer

        cb = ContextBuilder()
        tdam = TDAMIntegration()

        mock_items = [
            MemoryItem(
                id="mem-1",
                content="User prefers TypeScript",
                layer=MemoryLayer.L1_ATOM,
                score=0.95,
            )
        ]

        with patch.object(tdam, "get_persona", return_value="# Profile"):
            with patch.object(tdam, "recall", return_value=mock_items):
                cb.set_tdam(tdam)
                result = cb.build_with_memory(
                    "build a React component",
                    session_id="session-1",
                    include_persona=True,
                    include_memories=True,
                )

                assert result.persona == "# Profile"
                assert len(result.memories) == 1
                assert result.memories[0]["content"] == "User prefers TypeScript"

    def test_recall_memories(self):
        """Test recalling memories without full build."""
        from cursor_framework import ContextBuilder, TDAMIntegration, MemoryItem, MemoryLayer

        cb = ContextBuilder()
        tdam = TDAMIntegration()

        mock_items = [
            MemoryItem(
                id="mem-1",
                content="Test",
                layer=MemoryLayer.L1_ATOM,
                score=0.9,
            )
        ]

        with patch.object(tdam, "recall", return_value=mock_items):
            cb.set_tdam(tdam)
            results = cb.recall_memories("test query")

            assert len(results) == 1
            assert results[0]["id"] == "mem-1"

    def test_recall_memories_without_tdam(self):
        """Test recall returns empty when TDAM not configured."""
        from cursor_framework import ContextBuilder

        cb = ContextBuilder()
        # Don't set TDAM

        results = cb.recall_memories("test")
        assert results == []


class TestIntegrationScenarios:
    """End-to-end integration scenarios."""

    def test_full_memory_flow(self):
        """Test complete memory flow: capture -> extract -> recall."""
        from cursor_framework import TDAMIntegration, MemoryLayer, ConversationTurn, MemoryItem

        tdam = TDAMIntegration()

        # Mock all client methods
        with patch.object(tdam.client, "add_conversation", return_value={"accepted_ids": ["1"]}):
            with patch.object(tdam.client, "search_atomic", return_value=[]):
                # Capture conversation
                messages = [
                    ConversationTurn(
                        role="user",
                        content="I prefer dark mode and TypeScript",
                    ),
                    ConversationTurn(
                        role="assistant",
                        content="I'll remember that preference.",
                    ),
                ]
                result = tdam.capture_conversation("session-1", messages)
                assert result["accepted_ids"] == ["1"]

        # Recall with mock
        mock_memory = [
            MemoryItem(
                id="pref-1",
                content="User prefers dark mode",
                layer=MemoryLayer.L1_ATOM,
                score=0.95,
            )
        ]

        with patch.object(tdam.client, "search_atomic", return_value=mock_memory):
            results = tdam.recall("preferences")
            assert len(results) == 1
            assert "dark mode" in results[0].content

    def test_compact_and_resume(self):
        """Test context compaction and resumption."""
        from cursor_framework import TDAMIntegration, ConversationTurn, OffloadResult

        tdam = TDAMIntegration()

        mock_result = OffloadResult(
            messages=[
                {"role": "user", "content": "Summarized task"},
                {"role": "assistant", "content": "Continuing from summary"},
            ],
            mermaid_canvas="graph LR\n  Start-->Continue",
            report={
                "nodes_extracted": 50,
                "compression_ratio": 0.25,
            },
            tokens_before=50000,
            tokens_after=12500,
            compression_ratio=0.25,
        )

        with patch.object(tdam.client, "offload_compact", return_value=mock_result):
            messages = [
                ConversationTurn(role="user", content=f"Step {i}")
                for i in range(100)
            ]

            result = tdam.compact_context("session-1", messages, ratio=0.25)

            assert result is not None
            assert result.tokens_after < result.tokens_before
            assert "Start" in result.mermaid_canvas

    def test_persona_update_cycle(self):
        """Test persona creation and update."""
        from cursor_framework import TDAMIntegration

        tdam = TDAMIntegration()

        # Initial read (cache miss)
        with patch.object(
            tdam.client, "read_persona", return_value="# Initial Persona"
        ) as mock_read:
            persona = tdam.get_persona()
            assert persona == "# Initial Persona"
            mock_read.assert_called_once()

        # Update persona
        with patch.object(
            tdam.client, "write_persona", return_value=True
        ) as mock_write:
            result = tdam.update_persona("# Updated Persona")
            assert result is True
            mock_write.assert_called_once_with("# Updated Persona")

        # Read again (cache hit)
        persona = tdam.get_persona()
        assert persona == "# Updated Persona"
        # read_persona not called again
        assert mock_read.call_count == 1
