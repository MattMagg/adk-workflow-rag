#!/usr/bin/env python3
"""
Idempotent Qdrant collection schema creation per SPEC-02.

This script ensures the Qdrant collection exists with the correct schema:
- Named dense vectors: dense_docs (2048, Cosine), dense_code (2048, Cosine)
- Sparse vector: sparse_lexical (on_disk=false)
- HNSW config: m=64, ef_construct=512 (accuracy-first)
- Payload indexes for all required fields

Usage:
    python -m src.grounding.scripts.02_ensure_collection_schema

Related files:
- docs/spec/qdrant_schema_and_config.md - Spec document
- src/grounding/clients/qdrant_client.py - Qdrant client wrapper
- config/settings.yaml - Collection name and vector space names
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel

from qdrant_client.models import (
    Distance,
    VectorParams,
    SparseVectorParams,
    SparseIndexParams,
    HnswConfigDiff,
    PayloadSchemaType,
)

if TYPE_CHECKING:
    from qdrant_client.http.models import CollectionInfo

from grounding.clients.qdrant_client import get_qdrant_client
from grounding.config import get_settings

console = Console()

# ============================================================================
# Schema Configuration (locked per spec §1-3)
# ============================================================================

VECTOR_SIZE = 2048
HNSW_M = 64
HNSW_EF_CONSTRUCT = 512

KEYWORD_INDEXES = [
    "corpus",
    "repo",
    "commit",
    "ref",
    "path",
    "kind",
    "lang",
    "symbol",
    "text_hash",
]

INTEGER_INDEXES = [
    "chunk_index",
    "start_line",
    "end_line",
]

DATETIME_INDEXES = [
    "ingested_at",
]


@dataclass
class SchemaValidationError:
    """Represents a schema mismatch."""
    field: str
    expected: str
    actual: str


def validate_collection_schema(info: "CollectionInfo") -> list[SchemaValidationError]:
    """
    Validate that existing collection matches expected schema.
    
    Args:
        info: Collection info from Qdrant
        
    Returns:
        List of validation errors (empty if schema matches)
    """
    errors: list[SchemaValidationError] = []
    settings = get_settings()
    
    # Get vector config names
    dense_docs_name = settings.vectors.dense_docs
    dense_code_name = settings.vectors.dense_code
    sparse_name = settings.vectors.sparse_lexical
    
    # Check dense vectors
    vectors_config = info.config.params.vectors
    if isinstance(vectors_config, dict):
        # Named vectors
        if dense_docs_name not in vectors_config:
            errors.append(SchemaValidationError(
                field=f"vectors.{dense_docs_name}",
                expected="exists",
                actual="missing"
            ))
        else:
            vec = vectors_config[dense_docs_name]
            if vec.size != VECTOR_SIZE:
                errors.append(SchemaValidationError(
                    field=f"vectors.{dense_docs_name}.size",
                    expected=str(VECTOR_SIZE),
                    actual=str(vec.size)
                ))
            if vec.distance != Distance.COSINE:
                errors.append(SchemaValidationError(
                    field=f"vectors.{dense_docs_name}.distance",
                    expected="Cosine",
                    actual=str(vec.distance)
                ))
        
        if dense_code_name not in vectors_config:
            errors.append(SchemaValidationError(
                field=f"vectors.{dense_code_name}",
                expected="exists",
                actual="missing"
            ))
        else:
            vec = vectors_config[dense_code_name]
            if vec.size != VECTOR_SIZE:
                errors.append(SchemaValidationError(
                    field=f"vectors.{dense_code_name}.size",
                    expected=str(VECTOR_SIZE),
                    actual=str(vec.size)
                ))
            if vec.distance != Distance.COSINE:
                errors.append(SchemaValidationError(
                    field=f"vectors.{dense_code_name}.distance",
                    expected="Cosine",
                    actual=str(vec.distance)
                ))
    else:
        errors.append(SchemaValidationError(
            field="vectors",
            expected="named vectors dict",
            actual="single vector config"
        ))
    
    # Check sparse vectors
    sparse_config = info.config.params.sparse_vectors
    if sparse_config is None or sparse_name not in sparse_config:
        errors.append(SchemaValidationError(
            field=f"sparse_vectors.{sparse_name}",
            expected="exists",
            actual="missing"
        ))
    
    # Check HNSW config
    hnsw = info.config.hnsw_config
    if hnsw.m != HNSW_M:
        errors.append(SchemaValidationError(
            field="hnsw_config.m",
            expected=str(HNSW_M),
            actual=str(hnsw.m)
        ))
    if hnsw.ef_construct != HNSW_EF_CONSTRUCT:
        errors.append(SchemaValidationError(
            field="hnsw_config.ef_construct",
            expected=str(HNSW_EF_CONSTRUCT),
            actual=str(hnsw.ef_construct)
        ))
    
    return errors


def create_collection() -> bool:
    """
    Create the Qdrant collection with required schema.
    
    Returns:
        True if collection was created, False if already existed with matching schema
        
    Raises:
        SystemExit: If collection exists with mismatched schema
    """
    wrapper = get_qdrant_client()
    client = wrapper.client
    collection_name = wrapper.collection_name
    settings = get_settings()
    
    # Get vector space names from config
    dense_docs_name = settings.vectors.dense_docs
    dense_code_name = settings.vectors.dense_code
    sparse_name = settings.vectors.sparse_lexical
    
    console.print(f"\n[bold]Checking collection:[/bold] {collection_name}")
    
    # Check if collection exists
    if client.collection_exists(collection_name):
        console.print("   [yellow]→[/yellow] Collection exists, validating schema...")
        
        info = client.get_collection(collection_name)
        errors = validate_collection_schema(info)
        
        if errors:
            console.print("\n[bold red]Schema mismatch detected![/bold red]")
            for err in errors:
                console.print(f"   [red]✗[/red] {err.field}: expected {err.expected}, got {err.actual}")
            console.print("\n[red]Cannot proceed. Manual intervention required.[/red]")
            console.print("[dim]Options: delete collection manually or create new version.[/dim]")
            sys.exit(1)
        
        console.print("   [green]✓[/green] Schema matches expected configuration")
        return False
    
    # Create collection
    console.print("   [yellow]→[/yellow] Creating collection...")
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            dense_docs_name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            dense_code_name: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        },
        sparse_vectors_config={
            sparse_name: SparseVectorParams(
                index=SparseIndexParams(on_disk=False)
            ),
        },
        hnsw_config=HnswConfigDiff(m=HNSW_M, ef_construct=HNSW_EF_CONSTRUCT),
    )
    
    console.print("   [green]✓[/green] Collection created successfully")
    return True


def create_payload_indexes() -> int:
    """
    Create payload indexes for required fields.
    
    Indexes are created idempotently - if index exists, it's a no-op.
    
    Returns:
        Number of indexes created (0 if all already existed)
    """
    wrapper = get_qdrant_client()
    client = wrapper.client
    collection_name = wrapper.collection_name
    
    console.print("\n[bold]Creating payload indexes...[/bold]")
    
    created_count = 0
    
    # Get existing indexes
    info = client.get_collection(collection_name)
    existing_indexes = set(info.payload_schema.keys()) if info.payload_schema else set()
    
    # Keyword indexes
    for field in KEYWORD_INDEXES:
        if field in existing_indexes:
            console.print(f"   [dim]→ {field} (keyword) - exists[/dim]")
        else:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema=PayloadSchemaType.KEYWORD,
            )
            console.print(f"   [green]✓[/green] {field} (keyword)")
            created_count += 1
    
    # Integer indexes
    for field in INTEGER_INDEXES:
        if field in existing_indexes:
            console.print(f"   [dim]→ {field} (integer) - exists[/dim]")
        else:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema=PayloadSchemaType.INTEGER,
            )
            console.print(f"   [green]✓[/green] {field} (integer)")
            created_count += 1
    
    # Datetime indexes
    for field in DATETIME_INDEXES:
        if field in existing_indexes:
            console.print(f"   [dim]→ {field} (datetime) - exists[/dim]")
        else:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema=PayloadSchemaType.DATETIME,
            )
            console.print(f"   [green]✓[/green] {field} (datetime)")
            created_count += 1
    
    return created_count


def main() -> int:
    """Run the schema creation script."""
    console.print(Panel.fit(
        "[bold blue]SPEC-02 Collection Schema[/bold blue]\n"
        "Ensuring Qdrant collection with accuracy-first config",
        border_style="blue"
    ))
    
    try:
        # Step 1: Create or validate collection
        collection_created = create_collection()
        
        # Step 2: Create payload indexes
        indexes_created = create_payload_indexes()
        
        # Summary
        console.print("\n" + "=" * 50)
        if collection_created:
            console.print(Panel.fit(
                "[bold green]Collection created successfully![/bold green]\n"
                f"Created {indexes_created} payload indexes.\n"
                "Ready for Spec 3 (ingestion).",
                border_style="green"
            ))
        else:
            console.print(Panel.fit(
                "[bold green]Collection already exists with correct schema![/bold green]\n"
                f"Verified/created {indexes_created} payload indexes.\n"
                "Ready for Spec 3 (ingestion).",
                border_style="green"
            ))
        
        return 0
        
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
