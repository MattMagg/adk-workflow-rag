# Scripts Usage for Agents

This directory contains operational scripts for the RAG pipeline.

## Query Demo
**File**: `04_query_demo.py`

Use this to verify retrieval quality and debug the pipeline.

**Usage**:
```bash
# Run from project root as a module
python -m src.grounding.scripts.04_query_demo "your query here"
```

## Ingestion
**File**: `03_ingest_corpus.py`

Use this to ingest document and code corpora into Qdrant.

**Usage**:
```bash
# Run from project root as a module
python -m src.grounding.scripts.03_ingest_corpus
```
