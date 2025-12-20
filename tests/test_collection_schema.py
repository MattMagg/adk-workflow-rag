"""
Tests for Qdrant collection schema validation per SPEC-02.

These tests verify the collection was created correctly with:
- Named dense vectors (dense_docs, dense_code) at 2048 dimensions with Cosine distance
- Sparse vector (sparse_lexical)
- HNSW config (m=64, ef_construct=512)
- Payload indexes for required fields

Usage:
    pytest tests/test_collection_schema.py -v

Related files:
- docs/spec/qdrant_schema_and_config.md - Spec document
- src/grounding/scripts/02_ensure_collection_schema.py - Schema creation script
"""

import pytest
from qdrant_client.models import Distance

from src.grounding.clients.qdrant_client import get_qdrant_client
from src.grounding.config import get_settings


# ============================================================================
# Expected Configuration (must match 02_ensure_collection_schema.py)
# ============================================================================

EXPECTED_VECTOR_SIZE = 2048
EXPECTED_HNSW_M = 64
EXPECTED_HNSW_EF_CONSTRUCT = 512


@pytest.fixture(scope="module")
def collection_info():
    """Fetch collection info once for all tests."""
    wrapper = get_qdrant_client()
    collection_name = wrapper.collection_name
    
    if not wrapper.client.collection_exists(collection_name):
        pytest.skip(f"Collection '{collection_name}' does not exist. Run 02_ensure_collection_schema.py first.")
    
    return wrapper.client.get_collection(collection_name)


@pytest.fixture(scope="module")
def settings():
    """Get settings for vector space names."""
    return get_settings()


class TestCollectionExists:
    """Tests that the collection exists."""
    
    def test_collection_exists(self):
        """Assert collection exists in Qdrant Cloud."""
        wrapper = get_qdrant_client()
        collection_name = wrapper.collection_name
        
        assert wrapper.client.collection_exists(collection_name), \
            f"Collection '{collection_name}' does not exist"


class TestDenseVectorsConfig:
    """Tests for named dense vector configuration."""
    
    def test_dense_docs_exists(self, collection_info, settings):
        """Assert dense_docs vector exists."""
        vectors = collection_info.config.params.vectors
        assert isinstance(vectors, dict), "Expected named vectors configuration"
        assert settings.vectors.dense_docs in vectors, \
            f"Vector '{settings.vectors.dense_docs}' not found"
    
    def test_dense_docs_size(self, collection_info, settings):
        """Assert dense_docs has correct size (2048)."""
        vectors = collection_info.config.params.vectors
        vec = vectors[settings.vectors.dense_docs]
        assert vec.size == EXPECTED_VECTOR_SIZE, \
            f"Expected size {EXPECTED_VECTOR_SIZE}, got {vec.size}"
    
    def test_dense_docs_distance(self, collection_info, settings):
        """Assert dense_docs uses Cosine distance."""
        vectors = collection_info.config.params.vectors
        vec = vectors[settings.vectors.dense_docs]
        assert vec.distance == Distance.COSINE, \
            f"Expected Cosine distance, got {vec.distance}"
    
    def test_dense_code_exists(self, collection_info, settings):
        """Assert dense_code vector exists."""
        vectors = collection_info.config.params.vectors
        assert isinstance(vectors, dict), "Expected named vectors configuration"
        assert settings.vectors.dense_code in vectors, \
            f"Vector '{settings.vectors.dense_code}' not found"
    
    def test_dense_code_size(self, collection_info, settings):
        """Assert dense_code has correct size (2048)."""
        vectors = collection_info.config.params.vectors
        vec = vectors[settings.vectors.dense_code]
        assert vec.size == EXPECTED_VECTOR_SIZE, \
            f"Expected size {EXPECTED_VECTOR_SIZE}, got {vec.size}"
    
    def test_dense_code_distance(self, collection_info, settings):
        """Assert dense_code uses Cosine distance."""
        vectors = collection_info.config.params.vectors
        vec = vectors[settings.vectors.dense_code]
        assert vec.distance == Distance.COSINE, \
            f"Expected Cosine distance, got {vec.distance}"


class TestSparseVectorConfig:
    """Tests for sparse vector configuration."""
    
    def test_sparse_lexical_exists(self, collection_info, settings):
        """Assert sparse_lexical vector exists."""
        sparse = collection_info.config.params.sparse_vectors
        assert sparse is not None, "No sparse vectors configured"
        assert settings.vectors.sparse_lexical in sparse, \
            f"Sparse vector '{settings.vectors.sparse_lexical}' not found"


class TestHnswConfig:
    """Tests for HNSW configuration (accuracy-first defaults)."""
    
    def test_hnsw_m(self, collection_info):
        """Assert HNSW m = 64."""
        hnsw = collection_info.config.hnsw_config
        assert hnsw.m == EXPECTED_HNSW_M, \
            f"Expected m={EXPECTED_HNSW_M}, got {hnsw.m}"
    
    def test_hnsw_ef_construct(self, collection_info):
        """Assert HNSW ef_construct = 512."""
        hnsw = collection_info.config.hnsw_config
        assert hnsw.ef_construct == EXPECTED_HNSW_EF_CONSTRUCT, \
            f"Expected ef_construct={EXPECTED_HNSW_EF_CONSTRUCT}, got {hnsw.ef_construct}"


class TestPayloadIndexes:
    """Tests for payload index configuration."""
    
    @pytest.fixture(scope="class")
    def payload_schema(self, collection_info):
        """Get payload schema from collection info."""
        return collection_info.payload_schema or {}
    
    @pytest.mark.parametrize("field", [
        "corpus", "repo", "commit", "path", "kind"
    ])
    def test_keyword_indexes_exist(self, payload_schema, field):
        """Assert core keyword indexes exist."""
        assert field in payload_schema, \
            f"Payload index '{field}' not found. Run 02_ensure_collection_schema.py."
    
    def test_chunk_index_exists(self, payload_schema):
        """Assert chunk_index integer index exists."""
        assert "chunk_index" in payload_schema, \
            "Payload index 'chunk_index' not found"
    
    def test_ingested_at_exists(self, payload_schema):
        """Assert ingested_at datetime index exists."""
        assert "ingested_at" in payload_schema, \
            "Payload index 'ingested_at' not found"
