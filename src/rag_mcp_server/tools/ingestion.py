"""
Ingestion tools for the RAG MCP Server.

Provides tools for managing corpus ingestion as background jobs:
- rag_ingest_start: Start ingestion of a corpus (returns job ID)
- rag_ingest_status: Check status of an ingestion job

Ingestion runs asynchronously because it can take minutes for large corpora.
The job manager handles lifecycle and status tracking.

Related files:
- src/grounding/scripts/03_ingest_corpus.py - Core ingestion logic
- src/rag_mcp_server/jobs/manager.py - Job lifecycle management
- src/rag_mcp_server/jobs/worker.py - Background execution
"""

from __future__ import annotations

# TODO: Implement ingestion tools
#
# @mcp.tool()
# async def rag_ingest_start(
#     corpus: str,
#     force: bool = False,
# ) -> dict:
#     """
#     Start background ingestion of a corpus.
#
#     Returns immediately with a job ID. Use rag_ingest_status to poll progress.
#     Ingestion is idempotent by default (skips unchanged files).
#
#     Args:
#         corpus: Corpus name from config (e.g., "adk_docs", "openai_agents_python")
#         force: If True, re-ingest all files even if unchanged
#
#     Returns:
#         Dict with job_id and initial status
#     """
#     pass
#
#
# @mcp.tool()
# async def rag_ingest_status(
#     job_id: str,
# ) -> dict:
#     """
#     Check status of an ingestion job.
#
#     Args:
#         job_id: Job ID returned by rag_ingest_start
#
#     Returns:
#         Dict with status, progress, and any errors
#         Status values: pending, running, completed, failed
#     """
#     pass
