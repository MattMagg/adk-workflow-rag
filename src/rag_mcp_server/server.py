"""
FastMCP server definition for the RAG MCP Server.

This module defines the main MCP server that exposes RAG pipeline functionality
as agent-consumable tools. Uses FastMCP framework for Python MCP servers.

Tools exposed:
- rag_search: Full retrieval with reranking and context expansion
- rag_search_quick: Fast retrieval without reranking
- rag_ingest_start: Start background corpus ingestion
- rag_ingest_status: Check ingestion job status
- rag_corpus_list: List available corpora
- rag_corpus_info: Get corpus details and statistics
- rag_diagnose: Run diagnostic checks on RAG platform
- rag_config_show: Display current configuration

Related files:
- src/rag_mcp_server/tools/ - Tool implementations
- src/rag_mcp_server/config.py - Server configuration
- src/grounding/ - Core RAG pipeline
"""

from __future__ import annotations

# TODO: Import FastMCP and define server
# from fastmcp import FastMCP
#
# mcp = FastMCP("rag-server")
#
# # Register tools from tools/ modules
# from src.rag_mcp_server.tools.retrieval import rag_search, rag_search_quick
# from src.rag_mcp_server.tools.ingestion import rag_ingest_start, rag_ingest_status
# from src.rag_mcp_server.tools.discovery import rag_corpus_list, rag_corpus_info
# from src.rag_mcp_server.tools.diagnostics import rag_diagnose, rag_config_show
