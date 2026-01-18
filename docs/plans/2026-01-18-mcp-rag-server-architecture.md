# MCP RAG Server Architecture Specification

> **For Claude:** This is an architectural specification document. Implementation should follow the patterns defined here.

**Goal:** Design an MCP server that exposes the RAG platform as agent-consumable tools with first-pass retrieval quality, scalable ingestion, and agent-driven diagnostics.

**Architecture:** FastMCP-based Python server with stdio transport, exposing retrieval, ingestion, and diagnostic tools through a hierarchical namespace. Configuration-driven behavior via presets and flags.

**Tech Stack:** FastMCP, Qdrant, Voyage AI, FastEmbed SPLADE, Pydantic

---

## Deliverable 1: MCP Best Practices Research Summary

### Key Findings

**Protocol Patterns (2025 Spec)**
- **Stdio transport** is the baseline and preferred for development and local integration
- **Streamable HTTP** with OAuth 2.1 is mandatory for remote/networked production deployments
- **outputSchema** and **structuredContent** fields enable typed, validated outputs (June 2025 spec)
- Tool results must be both LLM-parsable and human-readable

**Tool Design Principles**
- Use `@mcp.tool()` decorators with explicit name, title, and description
- Docstrings define tool descriptions; type hints generate input schemas
- `ToolAnnotations` classify tools as `readOnlyHint=True` or `destructiveHint=True`
- Async handlers (`async def`) are preferred for I/O-bound operations
- Context parameter enables progress reporting for long operations

**Production Requirements**
- Emit structured logs with correlation IDs and tool invocation IDs
- Record latency, success/failure, and token-cost hints
- Surface soft limits and rate limits explicitly so agents can budget calls
- Implement request cancellation and timeouts to prevent resource stranding
- Never echo secrets in tool results or elicitation messages

**Security Best Practices**
- Never pass unvalidated input to command execution
- Implement input sanitization for all tool parameters
- Use parameterized queries for database operations
- Follow least-privilege principles for tool permissions
- Maintain internal registries of vetted operations

**Packaging Patterns**
- PyPI distribution with `pip install` for stdio-based local servers
- Docker containerization for remote deployments
- CLI entrypoint via `[project.scripts]` in pyproject.toml
- Configuration via environment variables and YAML files

---

## Deliverable 2: Repository Structure Analysis

### Directory Organization

```
/Users/mac-main/rag_qdrant_voyage/
├── src/grounding/                    # Core RAG pipeline
│   ├── config.py                     # Configuration loader (Settings, env substitution)
│   ├── clients/                      # Service wrappers
│   │   ├── qdrant_client.py          # QdrantClientWrapper (singleton)
│   │   ├── voyage_client.py          # VoyageClientWrapper (embed, rerank)
│   │   └── fastembed_client.py       # FastEmbedClient (SPLADE sparse)
│   ├── contracts/                    # Data models
│   │   ├── chunk.py                  # Chunk Pydantic model
│   │   ├── document.py               # Document model
│   │   └── ids.py                    # Deterministic ID generation
│   ├── chunkers/                     # Content processors
│   │   ├── markdown.py               # Heading-aware MD chunking
│   │   └── python_code.py            # AST-based Python chunking
│   ├── query/                        # Retrieval pipeline
│   │   └── query.py                  # search() function - 6-stage pipeline
│   ├── scripts/                      # Lifecycle scripts
│   │   ├── 00_smoke_test_connections.py
│   │   ├── 01_print_effective_config.py
│   │   ├── 02_ensure_collection_schema.py
│   │   ├── 03_ingest_corpus.py       # Main ingestion orchestrator
│   │   └── 04_query_demo.py
│   └── util/                         # Utilities
│       ├── hashing.py                # SHA-1/SHA-256
│       ├── fs_walk.py                # File discovery with globs
│       └── time.py                   # ISO8601 timestamps
├── config/
│   └── settings.yaml                 # Main configuration
├── corpora/                          # Source repositories (Git submodules)
├── tests/                            # Test suite
└── pyproject.toml                    # Package configuration
```

### Key Conventions

**Configuration Pattern**
- `get_settings()` returns LRU-cached singleton loading `.env` + `config/settings.yaml`
- Environment variable substitution via `${VAR}` syntax in YAML
- Pydantic models for type-safe configuration access

**Client Pattern**
- Singleton via `@lru_cache(maxsize=1)` decorators on `get_*_client()` functions
- Lazy initialization on first use
- Wrappers encapsulate API-specific details

**ID Generation**
- `parent_doc_id = SHA-1(corpus:commit:path)` - stable document identifier
- `chunk_id = SHA-1(parent_doc_id:chunk_index:text_hash)` - stable chunk identifier
- IDs change when content changes, enabling idempotent upserts

**Corpus Groups**
```python
CORPUS_GROUPS = {
    "adk": ["adk_docs", "adk_python"],
    "openai": ["openai_agents_docs", "openai_agents_python"],
    "langchain": ["langgraph_python", "langchain_python", "deepagents_python", "deepagents_docs"],
    "langgraph": ["langgraph_python", "deepagents_python", "deepagents_docs"],
    "anthropic": ["claude_sdk_docs", "claude_sdk_python"],
    "crewai": ["crewai_docs", "crewai_python"],
    "general": ["agent_dev_docs"],
}
```

**Retrieval Pipeline (6 Stages)**
1. Query Expansion (optional) - generates code/docs query variations
2. Hybrid Search - dense (Voyage) + sparse (SPLADE) with DBSF/RRF fusion
3. Candidate Balancing - ensures docs/code mix before reranking
4. VoyageAI Reranking - cross-encoder refinement with intent-aware prompts
5. Context Expansion - fetches adjacent chunks around top-K results
6. Coverage Gates - enforces minimum docs/code representation

**Ingestion Pipeline**
1. File Discovery - glob-based filtering per corpus config
2. Chunking - markdown (heading-aware) or Python (AST-based)
3. Embedding - dense (Voyage) + sparse (SPLADE)
4. Upsert - batch processing with idempotency via text_hash

---

## Deliverable 3: MCP Tool Contract Proposal

### Entry Point Router: Policy-Based (Not a Separate Tool)

The router is implemented as **tool description guidance** rather than a separate routing tool. Each tool's description includes explicit usage conditions, and agents follow the standardized behavior contract through tool descriptions.

**Rationale**: A separate routing tool adds latency and complexity. Policy-based routing through clear tool descriptions enables agents to make correct first-pass decisions without an extra round-trip.

### Namespace Organization

Tools are organized under a single `rag` namespace with functional suffixes:

| Tool Name | Category | Purpose |
|-----------|----------|---------|
| `rag_search` | Retrieval | Primary retrieval with full pipeline |
| `rag_search_quick` | Retrieval | Fast retrieval without reranking |
| `rag_ingest_start` | Ingestion | Start ingestion job for corpus/path |
| `rag_ingest_status` | Ingestion | Check job progress and status |
| `rag_corpus_list` | Discovery | List available corpora and stats |
| `rag_corpus_info` | Discovery | Get corpus details and health |
| `rag_diagnose` | Diagnostics | Run diagnostic checks |
| `rag_config_show` | Configuration | Show current configuration |

### Primary Tools

#### `rag_search` - Full Pipeline Retrieval

**When to Use**: Default choice for all retrieval needs. Use when you need accurate, comprehensive results with proper ranking.

**Parameters**:
```python
query: str                          # Natural language query (required)
sdk: Optional[str] = None           # Filter by SDK: adk|openai|langchain|langgraph|anthropic|crewai
corpus: Optional[List[str]] = None  # Filter by specific corpus names
kind: Optional[str] = None          # Filter by type: doc|code
preset: str = "balanced"            # Retrieval preset (see Configuration)
top_k: int = 12                     # Number of results
mode: str = "build"                 # Intent: build|debug|explain|refactor
expand_context: bool = True         # Fetch adjacent chunks
verbose: bool = False               # Include timing/debug info
```

**Output**: Evidence Pack
```python
{
    "query": str,
    "count": int,
    "evidence": [
        {
            "id": str,              # Chunk ID
            "corpus": str,          # Source corpus
            "kind": str,            # "doc" or "code"
            "path": str,            # File path
            "lines": str,           # Line range (e.g., "42-78")
            "text": str,            # Chunk content
            "score": float,         # Relevance score
            "title": Optional[str], # Section title if available
            "is_expanded": bool     # True if from context expansion
        }
    ],
    "coverage": {
        "doc_count": int,
        "code_count": int,
        "corpora": List[str]
    },
    "timing": Optional[dict],       # If verbose=True
    "warnings": List[str]           # Any issues encountered
}
```

**Error Handling**:
- If no results: Returns empty evidence with warning suggesting broader query
- If corpus not found: Returns error with list of valid corpora
- If API timeout: Returns partial results with warning

**Usage Instructions for Agents**:
1. Always specify `sdk` when you know the target framework
2. Use `mode` to match your task intent (debug for errors, explain for understanding)
3. Check `coverage` to ensure you have both docs and code
4. If `warnings` mentions "low coverage", broaden your query or remove filters
5. Use evidence `path` and `lines` for precise citations

---

#### `rag_search_quick` - Fast Retrieval

**When to Use**: When speed matters more than ranking quality. Use for exploratory searches, existence checks, or when you'll do your own filtering.

**Parameters**:
```python
query: str                          # Natural language query (required)
sdk: Optional[str] = None           # Filter by SDK
corpus: Optional[List[str]] = None  # Filter by corpus
kind: Optional[str] = None          # Filter by type
top_k: int = 20                     # Number of results (higher default)
```

**Output**: Same structure as `rag_search` but without reranking scores.

**Trade-offs**:
- 3-5x faster than `rag_search`
- No reranking (results ordered by hybrid search score only)
- No context expansion
- Higher top_k default to compensate for less precise ranking

---

#### `rag_ingest_start` - Start Ingestion Job

**When to Use**: When evidence indicates missing or outdated content. Part of agent self-healing flow.

**Parameters**:
```python
corpus: str                         # Corpus name to ingest (required)
path_filter: Optional[str] = None   # Glob pattern to limit scope
force: bool = False                 # Re-ingest even if unchanged
dry_run: bool = False               # Validate without upserting
```

**Output**:
```python
{
    "job_id": str,                  # UUID for tracking
    "corpus": str,
    "status": "started",
    "files_discovered": int,
    "estimated_chunks": int,
    "message": str
}
```

**Error Handling**:
- Invalid corpus: Returns error with valid corpus list
- Path not found: Returns error with discovered paths
- Already running: Returns existing job_id with status

**Usage Instructions for Agents**:
1. Only trigger when `rag_diagnose` or search results indicate stale/missing content
2. Use `path_filter` to limit scope for faster ingestion
3. Use `dry_run=True` first to validate before actual ingestion
4. After starting, poll `rag_ingest_status` for completion

---

#### `rag_ingest_status` - Check Job Status

**When to Use**: After starting an ingestion job to monitor progress.

**Parameters**:
```python
job_id: str                         # Job ID from rag_ingest_start (required)
```

**Output**:
```python
{
    "job_id": str,
    "corpus": str,
    "status": str,                  # pending|running|completed|failed
    "progress": {
        "files_processed": int,
        "files_total": int,
        "chunks_created": int,
        "chunks_skipped": int,      # Unchanged (idempotent)
        "percent_complete": float
    },
    "timing": {
        "started_at": str,          # ISO8601
        "elapsed_seconds": float,
        "estimated_remaining": Optional[float]
    },
    "error": Optional[str]          # If status=failed
}
```

**Usage Instructions for Agents**:
1. Poll every 5-10 seconds for running jobs
2. If status=failed, check `error` and consider retry with different parameters
3. Wait for status=completed before retrying retrieval

---

#### `rag_corpus_list` - List Available Corpora

**When to Use**: To discover what's available before querying. Use at session start or when unsure about data scope.

**Parameters**:
```python
include_stats: bool = True          # Include chunk counts
```

**Output**:
```python
{
    "corpora": [
        {
            "name": str,            # Corpus identifier
            "kind": str,            # "doc" or "code"
            "sdk_group": str,       # Parent SDK group
            "repo": str,            # Source repository
            "chunk_count": int,     # Number of indexed chunks
            "last_ingested": str    # ISO8601 timestamp
        }
    ],
    "sdk_groups": {
        "adk": ["adk_docs", "adk_python"],
        ...
    },
    "total_chunks": int
}
```

**Usage Instructions for Agents**:
1. Call once at session start to understand available data
2. Use `sdk_groups` to understand corpus relationships
3. Check `chunk_count` - 0 means corpus needs ingestion

---

#### `rag_corpus_info` - Get Corpus Details

**When to Use**: To get detailed information about a specific corpus before querying or ingesting.

**Parameters**:
```python
corpus: str                         # Corpus name (required)
```

**Output**:
```python
{
    "corpus": str,
    "kind": str,
    "repo": str,
    "ref": str,                     # Git branch/tag
    "current_commit": str,          # Latest indexed commit
    "chunk_count": int,
    "last_ingested": str,
    "config": {
        "include_globs": List[str],
        "exclude_globs": List[str],
        "allowed_exts": List[str]
    },
    "health": {
        "status": str,              # healthy|stale|empty
        "days_since_ingestion": int,
        "commit_drift": int         # Commits behind HEAD
    }
}
```

**Usage Instructions for Agents**:
1. Check `health.status` before relying on corpus data
2. If `status=stale` and content seems outdated, trigger `rag_ingest_start`
3. Use `config` to understand what files are indexed

---

#### `rag_diagnose` - Run Diagnostics

**When to Use**: When retrieval results seem wrong, incomplete, or when self-healing is needed.

**Parameters**:
```python
check: str = "all"                  # Specific check: all|connections|corpora|embeddings
corpus: Optional[str] = None        # Focus on specific corpus
```

**Output**:
```python
{
    "timestamp": str,
    "checks": {
        "qdrant_connection": {
            "status": str,          # ok|error
            "latency_ms": float,
            "message": str
        },
        "voyage_api": {
            "status": str,
            "latency_ms": float,
            "message": str
        },
        "corpora_health": [
            {
                "corpus": str,
                "status": str,      # healthy|stale|empty|error
                "chunk_count": int,
                "recommendation": Optional[str]
            }
        ]
    },
    "recommendations": List[str],   # Actionable suggestions
    "overall_status": str           # healthy|degraded|unhealthy
}
```

**Usage Instructions for Agents**:
1. Run when search returns unexpected results
2. Check `recommendations` for specific actions
3. If `overall_status=unhealthy`, address `checks` with status=error first
4. Use targeted `check` parameter for faster diagnosis

---

#### `rag_config_show` - Show Configuration

**When to Use**: To understand current retrieval behavior or debug configuration issues.

**Parameters**:
```python
section: str = "all"                # Section: all|retrieval|corpora|presets
redact_secrets: bool = True         # Mask API keys
```

**Output**:
```python
{
    "retrieval": {
        "fusion_method": str,
        "top_k": int,
        "first_stage_k": int,
        "rerank_candidates": int,
        "context_expansion": {
            "enabled": bool,
            "expand_top_k": int,
            "window_size": int
        }
    },
    "presets": {
        "balanced": {...},
        "precision": {...},
        "recall": {...}
    },
    "corpora": {...}
}
```

---

### Per-Tool Usage Instructions Summary

| Tool | Use When | Output Action | On Error |
|------|----------|---------------|----------|
| `rag_search` | Need accurate retrieval | Use evidence for citations | Check warnings, broaden query |
| `rag_search_quick` | Need fast exploration | Filter results yourself | Retry with rag_search |
| `rag_ingest_start` | Content missing/stale | Store job_id, poll status | Check corpus name, path |
| `rag_ingest_status` | Monitoring ingestion | Wait for completion | Retry job if failed |
| `rag_corpus_list` | Session start, discovery | Cache corpus info | Check connection |
| `rag_corpus_info` | Before query/ingest | Check health status | Verify corpus exists |
| `rag_diagnose` | Results seem wrong | Follow recommendations | Escalate to human |
| `rag_config_show` | Debug configuration | Understand defaults | N/A |

---

## Deliverable 4: Retrieval Configuration Approach

### Preset-Based Configuration

Retrieval behavior is controlled through **presets** - named configurations that set multiple parameters coherently. Agents select presets based on their task intent.

#### Available Presets

**`balanced`** (Default)
- Best for: General-purpose retrieval, most use cases
- Pipeline: Full 6-stage with moderate parameters
- Parameters:
  ```yaml
  top_k: 12
  first_stage_k: 80
  rerank_candidates: 60
  fusion_method: "dbsf"
  expand_context: true
  expand_top_k: 5
  expand_window: 1
  ```

**`precision`**
- Best for: When you need highly relevant results, low noise tolerance
- Pipeline: Aggressive reranking, strict coverage gates
- Parameters:
  ```yaml
  top_k: 8
  first_stage_k: 100
  rerank_candidates: 80
  fusion_method: "dbsf"
  expand_context: true
  expand_top_k: 3
  expand_window: 1
  score_threshold: 0.3
  ```

**`recall`**
- Best for: When you need comprehensive coverage, can tolerate noise
- Pipeline: Wide net, less aggressive filtering
- Parameters:
  ```yaml
  top_k: 20
  first_stage_k: 120
  rerank_candidates: 100
  fusion_method: "rrf"
  expand_context: true
  expand_top_k: 8
  expand_window: 2
  score_threshold: 0.0
  ```

**`speed`**
- Best for: Quick lookups, existence checks, interactive exploration
- Pipeline: Skip reranking, minimal expansion
- Parameters:
  ```yaml
  top_k: 15
  first_stage_k: 60
  rerank: false
  expand_context: false
  ```

#### Mode-Based Intent

The `mode` parameter affects reranking behavior through intent-aware prompts:

| Mode | Intent | Reranking Bias |
|------|--------|----------------|
| `build` | Implementation | Favors code examples, API usage |
| `debug` | Troubleshooting | Favors error handling, edge cases |
| `explain` | Understanding | Favors conceptual docs, guides |
| `refactor` | Improvement | Favors patterns, best practices |

#### Configuration Discovery

Agents discover available configurations through:
1. `rag_config_show` tool returns all presets with their parameters
2. Tool descriptions include recommended preset for common scenarios
3. Default preset (`balanced`) works well for 80% of cases

#### Override Mechanism

Explicit parameters override preset values:
```python
# Use precision preset but increase results
rag_search(query="...", preset="precision", top_k=15)
```

---

## Deliverable 5: Indexing and Ingestion Lifecycle

### Job-Based Ingestion Pattern

Ingestion operations are exposed as **asynchronous jobs** to handle long-running operations without blocking agent workflows.

#### Job Lifecycle

```
rag_ingest_start(corpus="adk_docs")
        │
        ▼
    ┌─────────┐
    │ pending │ → Job queued, resources allocated
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ running │ → Discovery → Chunking → Embedding → Upsert
    └────┬────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌────────┐
│completed│ │ failed │
└─────────┘ └────────┘
```

#### Job State Persistence

Jobs are tracked in-memory with periodic state dumps to `manifests/jobs.json`:
```json
{
    "jobs": {
        "uuid-1": {
            "corpus": "adk_docs",
            "status": "completed",
            "started_at": "2026-01-18T14:30:00Z",
            "completed_at": "2026-01-18T14:35:42Z",
            "stats": {
                "files": 234,
                "chunks_created": 1847,
                "chunks_skipped": 0
            }
        }
    }
}
```

#### Incremental Updates

Ingestion is **incremental by default** through text_hash comparison:
1. Before upserting, query existing chunks for the corpus
2. Extract `text_hash` from all existing chunks
3. For each new chunk, check if `text_hash` already exists
4. Skip chunks with unchanged content (idempotent)
5. Only embed and upsert changed/new chunks

#### Retry and Error Handling

**Automatic Retry**:
- Embedding API failures: 3 retries with exponential backoff
- Qdrant upsert failures: 3 retries with exponential backoff
- Transient network errors: Automatic retry

**Manual Recovery**:
- `force=True` parameter re-ingests even unchanged chunks
- Failed jobs retain partial progress; restart continues from last batch
- `path_filter` enables targeted re-ingestion of specific files

#### Progress Tracking

Progress is tracked at multiple granularities:
- **File level**: `files_processed / files_total`
- **Chunk level**: `chunks_created + chunks_skipped`
- **Time estimates**: Based on rolling average of batch processing time

#### Maintenance Operations

**Corpus Refresh** (via `rag_ingest_start`):
- Default: Incremental (only changed content)
- `force=True`: Full re-ingestion

**Stale Content Detection** (via `rag_corpus_info`):
- Compare indexed commit with repository HEAD
- Report `commit_drift` (commits behind)
- Health status `stale` when drift > threshold

**Cleanup** (future enhancement):
- Remove orphaned chunks (file deleted from source)
- Compact vector storage
- Optimize payload indexes

#### Agent Self-Healing Flow

When agents detect missing or stale content:

1. **Detection**: `rag_search` returns low-quality results or warnings
2. **Diagnosis**: `rag_diagnose` confirms corpus health issues
3. **Trigger**: `rag_ingest_start` with appropriate scope
4. **Monitor**: Poll `rag_ingest_status` until complete
5. **Retry**: Re-execute original `rag_search`
6. **Limit**: Only one self-heal attempt per query to prevent loops

---

## Deliverable 6: Packaging and Distribution Approach

### Package Structure

```
rag-mcp-server/
├── src/
│   └── rag_mcp_server/
│       ├── __init__.py
│       ├── server.py               # FastMCP server definition
│       ├── tools/
│       │   ├── retrieval.py        # rag_search, rag_search_quick
│       │   ├── ingestion.py        # rag_ingest_start, rag_ingest_status
│       │   ├── discovery.py        # rag_corpus_list, rag_corpus_info
│       │   └── diagnostics.py      # rag_diagnose, rag_config_show
│       ├── jobs/
│       │   ├── manager.py          # Job lifecycle management
│       │   └── worker.py           # Background job execution
│       └── config.py               # Server configuration
├── pyproject.toml
├── README.md
└── Dockerfile
```

### Installation Method

**Primary: pip install (stdio transport)**
```bash
pip install rag-mcp-server
```

**Alternative: Docker (HTTP transport)**
```bash
docker pull ghcr.io/org/rag-mcp-server
docker run -e VOYAGE_API_KEY=... -e QDRANT_URL=... rag-mcp-server
```

### CLI Entrypoint

**pyproject.toml**:
```toml
[project.scripts]
rag-mcp-server = "rag_mcp_server.server:main"
```

**Usage**:
```bash
# Run with stdio transport (default)
rag-mcp-server

# Run with HTTP transport
rag-mcp-server --transport http --port 8080

# Run with custom config
rag-mcp-server --config /path/to/config.yaml
```

### Configuration

**Environment Variables** (required):
```bash
VOYAGE_API_KEY=your-voyage-api-key
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=agentic_grounding_v1
```

**Environment Variables** (optional):
```bash
RAG_MCP_LOG_LEVEL=INFO
RAG_MCP_CONFIG_PATH=/custom/config.yaml
RAG_MCP_TRANSPORT=stdio
RAG_MCP_PORT=8080
```

**Configuration File** (`~/.config/rag-mcp-server/config.yaml` or `./config/settings.yaml`):
```yaml
qdrant:
  url: ${QDRANT_URL}
  api_key: ${QDRANT_API_KEY}
  collection: ${QDRANT_COLLECTION}

voyage:
  api_key: ${VOYAGE_API_KEY}
  docs_model: "voyage-context-3"
  code_model: "voyage-code-3"
  rerank_model: "rerank-2.5"

retrieval_defaults:
  # ... (existing settings.yaml structure)
```

### Agent Integration

**Claude Code Configuration** (`.mcp.json`):
```json
{
    "mcpServers": {
        "rag": {
            "command": "rag-mcp-server",
            "env": {
                "VOYAGE_API_KEY": "${VOYAGE_API_KEY}",
                "QDRANT_URL": "${QDRANT_URL}",
                "QDRANT_API_KEY": "${QDRANT_API_KEY}",
                "QDRANT_COLLECTION": "agentic_grounding_v1"
            }
        }
    }
}
```

**Cursor Configuration** (`~/.cursor/mcp.json`):
```json
{
    "mcpServers": {
        "rag": {
            "command": "rag-mcp-server",
            "env": {
                "VOYAGE_API_KEY": "...",
                "QDRANT_URL": "...",
                "QDRANT_API_KEY": "...",
                "QDRANT_COLLECTION": "agentic_grounding_v1"
            }
        }
    }
}
```

### Discovery Flow

1. Agent loads MCP configuration
2. Launches `rag-mcp-server` process with stdio transport
3. Server initializes, validates credentials, connects to Qdrant
4. Server advertises available tools via MCP `list_tools`
5. Agent caches tool definitions for session

---

## Deliverable 7: Risk Identification and Mitigation

### Performance Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Voyage API latency** | High retrieval latency | Medium | Cache embeddings for repeated queries; batch embedding requests; implement request timeouts |
| **Qdrant query timeout** | Failed searches | Low | Configure appropriate timeouts; implement retry with backoff; use `speed` preset for time-critical queries |
| **Large result sets** | Memory exhaustion | Low | Enforce `top_k` limits; stream results for large responses; implement pagination |
| **Context expansion overhead** | Increased latency | Medium | Make expansion optional; limit `expand_top_k` and `window_size`; disable for `speed` preset |
| **Concurrent ingestion** | Resource contention | Medium | Limit concurrent jobs; queue excess requests; implement job prioritization |

### Cost Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Voyage API costs** | High embedding/rerank costs | High | Cache embeddings; batch requests; skip reranking for `speed` preset; monitor usage |
| **Qdrant storage** | Growing storage costs | Medium | Implement chunk deduplication; prune stale content; monitor collection size |
| **Ingestion frequency** | Excessive re-embedding | Medium | Incremental ingestion by default; text_hash comparison; rate limit ingestion jobs |

**Cost Estimation**:
- Voyage embedding: ~$0.10 per 1M tokens
- Voyage reranking: ~$0.05 per 1K documents
- Qdrant Cloud: ~$25/month for 1M vectors (starter tier)

**Budget Controls**:
- Expose cost hints in tool responses
- Track daily/monthly usage
- Alert when approaching limits

### Correctness Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Stale indexed content** | Incorrect/outdated results | Medium | Health checks via `rag_corpus_info`; commit drift detection; agent self-healing |
| **Chunking errors** | Missing content, broken context | Low | Comprehensive chunker tests; heading-aware boundaries; overlap for context |
| **Reranking bias** | Relevant results demoted | Low | Large candidate pool (60+); coverage gates; mode-based intent tuning |
| **Filter mismatch** | Wrong corpus selected | Medium | Validate corpus/SDK names; suggest corrections; list valid options on error |
| **ID collisions** | Data corruption | Very Low | SHA-1 with structured inputs; deterministic generation; verify uniqueness |

### Operational Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Qdrant unavailable** | Complete retrieval failure | Low | Connection health checks; graceful degradation; clear error messages |
| **Voyage API unavailable** | No embedding/reranking | Low | Health checks; fallback to sparse-only search; cache recent embeddings |
| **Job failures** | Incomplete ingestion | Medium | Retry logic; partial progress preservation; manual recovery tools |
| **Configuration errors** | Silent failures | Medium | Validate config on startup; redacted config display; comprehensive error messages |
| **Memory leaks** | Server degradation | Low | Connection pooling; client singleton pattern; periodic health checks |

### Monitoring Strategy

**Health Endpoints**:
- `rag_diagnose` tool for agent-accessible diagnostics
- Internal `/health` endpoint for orchestration systems

**Metrics to Track**:
- Request latency (p50, p95, p99)
- Error rate by tool
- Voyage API usage (tokens, requests)
- Qdrant query latency
- Active ingestion jobs
- Cache hit rate

**Alerting Thresholds**:
- Latency p95 > 5s
- Error rate > 1%
- Qdrant connection failures > 3
- Ingestion job failures > 2 consecutive

---

## Appendix: Standardized Agent Behavior Contract

The MCP server design supports the following agent workflow:

### 1. Interpret + Plan
- Agent receives user request
- Uses `rag_corpus_list` to understand available data scope
- Determines if retrieval, ingestion, or both are needed

### 2. Clarify (if needed)
- If SDK/corpus is ambiguous, ask user once
- If scope is unclear, ask user once
- Minimize back-and-forth

### 3. Produce Querying Plan
- Select appropriate preset (`balanced`, `precision`, `recall`, `speed`)
- Choose `mode` based on task intent
- Apply corpus/SDK filters

### 4. Execute High-Recall Retrieval
- Call `rag_search` with configured parameters
- Pipeline handles: high recall → rerank → gate → evidence pack
- Check `coverage` and `warnings` in response

### 5. Produce Implementation Plan
- Use evidence `path` and `lines` for precise citations
- Reference chunk `text` for grounding

### 6. Self-Heal (if needed)
- If evidence indicates missing/stale content:
  1. Run `rag_diagnose` to confirm
  2. Trigger `rag_ingest_start` for affected corpus
  3. Wait for `rag_ingest_status` completion
  4. Retry `rag_search` once
- Limit: One self-heal attempt per query
