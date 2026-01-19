"""
Entry point for running the RAG MCP server as a module.

Usage:
    python -m rag_mcp_server
    python -m rag_mcp_server --transport http --port 8080
"""

from rag_mcp_server.server import main

if __name__ == "__main__":
    main()
