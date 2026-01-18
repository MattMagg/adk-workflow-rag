"""
MCP tools package for the RAG MCP Server.

Provides tool implementations organized by function:
- retrieval: rag_search, rag_search_quick
- ingestion: rag_ingest_start, rag_ingest_status
- discovery: rag_corpus_list, rag_corpus_info
- diagnostics: rag_diagnose, rag_config_show

Related files:
- src/rag_mcp_server/server.py - Registers these tools with FastMCP
- src/grounding/query/query.py - search() wrapped by retrieval tools
- src/grounding/scripts/03_ingest_corpus.py - ingestion logic
"""

from __future__ import annotations

# TODO: Export tool functions once implemented
#
# from src.rag_mcp_server.tools.retrieval import rag_search, rag_search_quick
# from src.rag_mcp_server.tools.ingestion import rag_ingest_start, rag_ingest_status
# from src.rag_mcp_server.tools.discovery import rag_corpus_list, rag_corpus_info
# from src.rag_mcp_server.tools.diagnostics import rag_diagnose, rag_config_show
#
# __all__ = [
#     "rag_search",
#     "rag_search_quick",
#     "rag_ingest_start",
#     "rag_ingest_status",
#     "rag_corpus_list",
#     "rag_corpus_info",
#     "rag_diagnose",
#     "rag_config_show",
# ]
