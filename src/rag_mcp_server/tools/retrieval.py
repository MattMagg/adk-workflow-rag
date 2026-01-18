"""
Retrieval tools for the RAG MCP Server.

Provides search tools that wrap the grounding pipeline's search() function:
- rag_search: Full retrieval with reranking and context expansion
- rag_search_quick: Fast retrieval without reranking for latency-sensitive use

Both tools return structured results with:
- Chunk text and metadata
- Relevance scores
- Source file information
- SDK/corpus provenance

Related files:
- src/grounding/query/query.py - search() function being wrapped
- src/rag_mcp_server/config.py - Default search parameters
"""

from __future__ import annotations

# TODO: Implement retrieval tools
#
# @mcp.tool()
# async def rag_search(
#     query: str,
#     top_k: int = 10,
#     sdk: str | None = None,
#     expand_context: bool = True,
# ) -> list[dict]:
#     """
#     Search the RAG knowledge base with full retrieval pipeline.
#
#     Uses hybrid search (dense + sparse), reranking, and context expansion
#     for high-quality results. Suitable for thorough research queries.
#
#     Args:
#         query: Natural language search query
#         top_k: Number of results to return (default 10)
#         sdk: Filter by SDK group (adk, openai, langchain, langgraph, anthropic, crewai)
#         expand_context: Whether to include adjacent chunks (default True)
#
#     Returns:
#         List of search results with text, metadata, and scores
#     """
#     pass
#
#
# @mcp.tool()
# async def rag_search_quick(
#     query: str,
#     top_k: int = 5,
#     sdk: str | None = None,
# ) -> list[dict]:
#     """
#     Fast search without reranking for latency-sensitive queries.
#
#     Uses hybrid search but skips reranking and context expansion.
#     Suitable for quick lookups where speed matters more than precision.
#
#     Args:
#         query: Natural language search query
#         top_k: Number of results to return (default 5)
#         sdk: Filter by SDK group (adk, openai, langchain, langgraph, anthropic, crewai)
#
#     Returns:
#         List of search results with text, metadata, and scores
#     """
#     pass
