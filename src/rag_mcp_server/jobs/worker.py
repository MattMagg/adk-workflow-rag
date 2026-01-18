"""
Background job execution for long-running operations.

Runs jobs in separate threads/processes with:
- Progress reporting back to JobManager
- Timeout handling
- Clean error capture

Currently supports ingestion jobs. Extensible for other job types.

Related files:
- src/rag_mcp_server/jobs/manager.py - Job lifecycle management
- src/grounding/scripts/03_ingest_corpus.py - Ingestion logic
"""

from __future__ import annotations

# TODO: Implement job worker
#
# import threading
# from src.rag_mcp_server.jobs.manager import JobManager
#
#
# def run_ingestion_job(
#     job_id: str,
#     corpus: str,
#     force: bool,
#     manager: JobManager,
# ) -> None:
#     """
#     Execute corpus ingestion in background.
#
#     Updates job progress and status via manager.
#     Captures any errors and reports them.
#
#     Args:
#         job_id: Job identifier
#         corpus: Corpus name to ingest
#         force: Whether to force re-ingestion
#         manager: JobManager for status updates
#     """
#     pass
#
#
# def start_background_job(
#     job_id: str,
#     job_type: str,
#     params: dict,
#     manager: JobManager,
# ) -> None:
#     """
#     Start a job in a background thread.
#
#     Args:
#         job_id: Job identifier
#         job_type: Type of job (e.g., "ingestion")
#         params: Job-specific parameters
#         manager: JobManager for status updates
#     """
#     pass
