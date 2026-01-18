"""
Discovery tools for the RAG MCP Server.

Provides tools for exploring available knowledge:
- rag_corpus_list: List all configured corpora
- rag_corpus_info: Get detailed info about a specific corpus

These help agents understand what knowledge is available for searching.

Related files:
- config/settings.yaml - Corpus configuration in ingestion.corpora
- src/grounding/config.py - Configuration loading
"""

from __future__ import annotations

# TODO: Implement discovery tools
#
# @mcp.tool()
# async def rag_corpus_list() -> list[dict]:
#     """
#     List all available corpora in the RAG knowledge base.
#
#     Returns:
#         List of corpus summaries with name, kind (doc/code), and SDK group
#     """
#     pass
#
#
# @mcp.tool()
# async def rag_corpus_info(
#     corpus: str,
# ) -> dict:
#     """
#     Get detailed information about a specific corpus.
#
#     Args:
#         corpus: Corpus name (e.g., "adk_docs", "openai_agents_python")
#
#     Returns:
#         Dict with:
#         - name: Corpus identifier
#         - kind: "doc" or "code"
#         - sdk_group: Parent SDK (adk, openai, langchain, etc.)
#         - chunk_count: Number of indexed chunks
#         - source_path: Local path to source files
#         - file_patterns: Include/exclude globs
#     """
#     pass
