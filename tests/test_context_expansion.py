"""
Unit tests for context-aware expansion feature.

Tests the expand_context_around_chunks() function and its integration
into the search pipeline.
"""

import pytest
from unittest.mock import Mock, patch
from qdrant_client import QdrantClient
from qdrant_client.http import models

from src.grounding.query.query import expand_context_around_chunks, search


class TestExpandContextAroundChunks:
    """Unit tests for expand_context_around_chunks function."""

    def test_basic_expansion_both_neighbors(self):
        """Test basic expansion with both N-1 and N+1 neighbors."""
        # Mock candidates
        candidates = [
            {
                "id": "chunk_5",
                "path": "test/file.py",
                "chunk_index": 5,
                "rerank_score": 0.9,
                "text": "chunk 5 content",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": "chunk_5",
                "start_line": 50,
                "end_line": 60,
                "score": 0.9,
                "reranked": True,
            }
        ]

        # Mock Qdrant client
        mock_qdrant = Mock(spec=QdrantClient)

        # Mock scroll response - return chunks 4 and 6
        mock_record_4 = Mock()
        mock_record_4.id = "chunk_4"
        mock_record_4.payload = {
            "path": "test/file.py",
            "chunk_index": 4,
            "text": "chunk 4 content",
            "corpus": "test_corpus",
            "kind": "code",
            "repo": "test/repo",
            "commit": "abc123",
            "chunk_id": "chunk_4",
            "start_line": 40,
            "end_line": 49,
        }

        mock_record_6 = Mock()
        mock_record_6.id = "chunk_6"
        mock_record_6.payload = {
            "path": "test/file.py",
            "chunk_index": 6,
            "text": "chunk 6 content",
            "corpus": "test_corpus",
            "kind": "code",
            "repo": "test/repo",
            "commit": "abc123",
            "chunk_id": "chunk_6",
            "start_line": 61,
            "end_line": 70,
        }

        mock_qdrant.scroll.return_value = ([mock_record_4, mock_record_6], None)

        # Execute expansion
        result, warnings = expand_context_around_chunks(
            candidates=candidates,
            qdrant=mock_qdrant,
            collection_name="test_collection",
            expand_top_k=1,
            window_size=1,
            score_decay_factor=0.85,
            max_expanded_chunks=20,
            verbose=False,
        )

        # Assertions
        assert len(result) == 3  # Original 1 + 2 expanded
        assert len(warnings) == 0

        # Check expanded chunks have correct scores
        expanded_chunks = [r for r in result if r["id"] != "chunk_5"]
        assert len(expanded_chunks) == 2

        # Check score decay (0.9 * 0.85 = 0.765)
        for chunk in expanded_chunks:
            assert chunk["rerank_score"] == pytest.approx(0.765, abs=0.001)
            assert chunk["reranked"] is False
            assert "expanded_from" in chunk
            assert chunk["expanded_from"] == "chunk_5"

    def test_boundary_chunk_no_negative_index(self):
        """Test that chunk_index=0 doesn't try to fetch negative indices."""
        candidates = [
            {
                "id": "chunk_0",
                "path": "test/file.py",
                "chunk_index": 0,
                "rerank_score": 0.9,
                "text": "first chunk",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": "chunk_0",
                "start_line": 1,
                "end_line": 10,
                "score": 0.9,
                "reranked": True,
            }
        ]

        mock_qdrant = Mock(spec=QdrantClient)

        # Mock scroll response - only return chunk 1 (no chunk -1)
        mock_record_1 = Mock()
        mock_record_1.id = "chunk_1"
        mock_record_1.payload = {
            "path": "test/file.py",
            "chunk_index": 1,
            "text": "chunk 1 content",
            "corpus": "test_corpus",
            "kind": "code",
            "repo": "test/repo",
            "commit": "abc123",
            "chunk_id": "chunk_1",
            "start_line": 11,
            "end_line": 20,
        }

        mock_qdrant.scroll.return_value = ([mock_record_1], None)

        result, warnings = expand_context_around_chunks(
            candidates=candidates,
            qdrant=mock_qdrant,
            collection_name="test_collection",
            expand_top_k=1,
            window_size=1,
            score_decay_factor=0.85,
            max_expanded_chunks=20,
            verbose=False,
        )

        # Should have 2 chunks total (original + chunk 1, no negative)
        assert len(result) == 2
        assert len([r for r in result if r["id"] == "chunk_1"]) == 1

    def test_deduplication_against_existing(self):
        """Test that already-existing chunks are not duplicated."""
        candidates = [
            {
                "id": "chunk_5",
                "path": "test/file.py",
                "chunk_index": 5,
                "rerank_score": 0.9,
                "text": "chunk 5 content",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": "chunk_5",
                "start_line": 50,
                "end_line": 60,
                "score": 0.9,
                "reranked": True,
            },
            {
                "id": "chunk_6",  # Already in candidates
                "path": "test/file.py",
                "chunk_index": 6,
                "rerank_score": 0.8,
                "text": "chunk 6 content",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": "chunk_6",
                "start_line": 61,
                "end_line": 70,
                "score": 0.8,
                "reranked": True,
            },
        ]

        mock_qdrant = Mock(spec=QdrantClient)

        # Mock scroll returns chunk 6 (which already exists)
        mock_record_6 = Mock()
        mock_record_6.id = "chunk_6"
        mock_record_6.payload = {
            "path": "test/file.py",
            "chunk_index": 6,
            "text": "chunk 6 content",
            "corpus": "test_corpus",
            "kind": "code",
            "repo": "test/repo",
            "commit": "abc123",
            "chunk_id": "chunk_6",
            "start_line": 61,
            "end_line": 70,
        }

        mock_qdrant.scroll.return_value = ([mock_record_6], None)

        result, warnings = expand_context_around_chunks(
            candidates=candidates,
            qdrant=mock_qdrant,
            collection_name="test_collection",
            expand_top_k=1,
            window_size=1,
            score_decay_factor=0.85,
            max_expanded_chunks=20,
            verbose=False,
        )

        # Should still have 2 chunks (no duplication)
        assert len(result) == 2
        assert len([r for r in result if r["id"] == "chunk_6"]) == 1

    def test_max_expanded_chunks_limit(self):
        """Test that max_expanded_chunks limit is enforced."""
        # Create 10 top candidates
        candidates = [
            {
                "id": f"chunk_{i}",
                "path": "test/file.py",
                "chunk_index": i,
                "rerank_score": 0.9 - (i * 0.01),
                "text": f"chunk {i} content",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": f"chunk_{i}",
                "start_line": i * 10,
                "end_line": (i + 1) * 10,
                "score": 0.9 - (i * 0.01),
                "reranked": True,
            }
            for i in range(10)
        ]

        mock_qdrant = Mock(spec=QdrantClient)

        # Mock scroll returns 20 chunks (2 per candidate)
        mock_records = []
        for i in range(10):
            for offset in [-1, 1]:
                idx = i + offset
                if idx >= 0:
                    mock_record = Mock()
                    mock_record.id = f"chunk_{idx}_expanded"
                    mock_record.payload = {
                        "path": "test/file.py",
                        "chunk_index": idx,
                        "text": f"chunk {idx} content",
                        "corpus": "test_corpus",
                        "kind": "code",
                        "repo": "test/repo",
                        "commit": "abc123",
                        "chunk_id": f"chunk_{idx}_expanded",
                        "start_line": idx * 10,
                        "end_line": (idx + 1) * 10,
                    }
                    mock_records.append(mock_record)

        mock_qdrant.scroll.return_value = (mock_records, None)

        result, warnings = expand_context_around_chunks(
            candidates=candidates,
            qdrant=mock_qdrant,
            collection_name="test_collection",
            expand_top_k=10,
            window_size=1,
            score_decay_factor=0.85,
            max_expanded_chunks=5,  # Limit to 5
            verbose=False,
        )

        # Should have 10 original + 5 expanded (limited)
        assert len(result) == 15
        assert any("truncated to 5" in w for w in warnings)

    def test_window_size_2(self):
        """Test window_size=2 fetches ±2 chunks (5 total per parent)."""
        candidates = [
            {
                "id": "chunk_10",
                "path": "test/file.py",
                "chunk_index": 10,
                "rerank_score": 0.9,
                "text": "chunk 10 content",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": "chunk_10",
                "start_line": 100,
                "end_line": 110,
                "score": 0.9,
                "reranked": True,
            }
        ]

        mock_qdrant = Mock(spec=QdrantClient)

        # Mock scroll returns chunks 8, 9, 11, 12
        mock_records = []
        for idx in [8, 9, 11, 12]:
            mock_record = Mock()
            mock_record.id = f"chunk_{idx}"
            mock_record.payload = {
                "path": "test/file.py",
                "chunk_index": idx,
                "text": f"chunk {idx} content",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": f"chunk_{idx}",
                "start_line": idx * 10,
                "end_line": (idx + 1) * 10,
            }
            mock_records.append(mock_record)

        mock_qdrant.scroll.return_value = (mock_records, None)

        result, warnings = expand_context_around_chunks(
            candidates=candidates,
            qdrant=mock_qdrant,
            collection_name="test_collection",
            expand_top_k=1,
            window_size=2,  # ±2 chunks
            score_decay_factor=0.85,
            max_expanded_chunks=20,
            verbose=False,
        )

        # Should have 5 total (1 original + 4 expanded)
        assert len(result) == 5

        # Check score decay for different distances
        # Distance 1: 0.9 * 0.85^1 = 0.765
        # Distance 2: 0.9 * 0.85^2 = 0.650
        dist_1_chunks = [r for r in result if r["id"] in ["chunk_9", "chunk_11"]]
        dist_2_chunks = [r for r in result if r["id"] in ["chunk_8", "chunk_12"]]

        for chunk in dist_1_chunks:
            assert chunk["rerank_score"] == pytest.approx(0.765, abs=0.001)

        for chunk in dist_2_chunks:
            assert chunk["rerank_score"] == pytest.approx(0.650, abs=0.002)

    def test_score_decay_calculation(self):
        """Test that score decay is calculated correctly."""
        candidates = [
            {
                "id": "chunk_5",
                "path": "test/file.py",
                "chunk_index": 5,
                "rerank_score": 1.0,  # Use 1.0 for easy math
                "text": "chunk 5 content",
                "corpus": "test_corpus",
                "kind": "code",
                "repo": "test/repo",
                "commit": "abc123",
                "chunk_id": "chunk_5",
                "start_line": 50,
                "end_line": 60,
                "score": 1.0,
                "reranked": True,
            }
        ]

        mock_qdrant = Mock(spec=QdrantClient)

        mock_record_4 = Mock()
        mock_record_4.id = "chunk_4"
        mock_record_4.payload = {
            "path": "test/file.py",
            "chunk_index": 4,
            "text": "chunk 4 content",
            "corpus": "test_corpus",
            "kind": "code",
            "repo": "test/repo",
            "commit": "abc123",
            "chunk_id": "chunk_4",
            "start_line": 40,
            "end_line": 49,
        }

        mock_qdrant.scroll.return_value = ([mock_record_4], None)

        result, warnings = expand_context_around_chunks(
            candidates=candidates,
            qdrant=mock_qdrant,
            collection_name="test_collection",
            expand_top_k=1,
            window_size=1,
            score_decay_factor=0.8,  # Different decay factor
            max_expanded_chunks=20,
            verbose=False,
        )

        expanded = [r for r in result if r["id"] == "chunk_4"][0]
        # Score should be 1.0 * 0.8^1 = 0.8
        assert expanded["rerank_score"] == pytest.approx(0.8, abs=0.001)


class TestSearchIntegration:
    """Integration tests for context expansion in search pipeline."""

    @pytest.mark.integration
    @pytest.mark.skipif(
        True, reason="Requires live Qdrant instance - enable for integration testing"
    )
    def test_search_with_expansion_enabled(self):
        """Test that search() with expand_context=True executes expansion."""
        result = search(
            query="LoopAgent",
            top_k=5,
            expand_context=True,
            expand_top_k=3,
            expand_window=1,
            verbose=True,
        )

        # Check that context_expansion timing exists
        assert "context_expansion" in result["timings"]
        assert result["timings"]["context_expansion"] > 0

        # Check that results were returned
        assert result["count"] > 0

    @pytest.mark.integration
    @pytest.mark.skipif(
        True, reason="Requires live Qdrant instance - enable for integration testing"
    )
    def test_search_without_expansion(self):
        """Test that search() without expansion works as before."""
        result = search(query="LoopAgent", top_k=5, expand_context=False, verbose=True)

        # Check that context_expansion timing does NOT exist
        assert "context_expansion" not in result["timings"]

        # Check that results were returned
        assert result["count"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
