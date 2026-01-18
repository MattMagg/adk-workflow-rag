"""
Server configuration for the RAG MCP Server.

Handles MCP server-specific configuration including:
- Server metadata (name, version, description)
- Tool-specific defaults and limits
- Integration with grounding config via get_settings()

Related files:
- src/grounding/config.py - Core RAG configuration
- config/settings.yaml - Main configuration file
"""

from __future__ import annotations

# TODO: Define server configuration
#
# Server configuration constants:
# - SERVER_NAME: MCP server identifier
# - SERVER_VERSION: Matches package version
# - DEFAULT_TOP_K: Default number of results for retrieval
# - MAX_TOP_K: Maximum allowed top_k value
# - JOB_POLL_INTERVAL: Seconds between job status checks
# - JOB_TIMEOUT: Maximum job duration before timeout
#
# Integration with grounding config:
# - Reuse get_settings() for RAG pipeline configuration
# - Add MCP-specific overrides as needed
