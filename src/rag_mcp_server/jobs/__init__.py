"""
Jobs package for background task management.

Provides infrastructure for long-running operations:
- manager: Job lifecycle (create, track, complete/fail)
- worker: Background execution with progress reporting

Used by ingestion tools to run corpus ingestion asynchronously.

Related files:
- src/rag_mcp_server/tools/ingestion.py - Creates jobs via rag_ingest_start
- src/grounding/scripts/03_ingest_corpus.py - Ingestion logic run by worker
"""

from __future__ import annotations

# TODO: Export job management components once implemented
#
# from src.rag_mcp_server.jobs.manager import JobManager, JobStatus
# from src.rag_mcp_server.jobs.worker import run_ingestion_job
#
# __all__ = [
#     "JobManager",
#     "JobStatus",
#     "run_ingestion_job",
# ]
