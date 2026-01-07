---
name: ADK Tools
description: This skill should be used when the user asks about "adding a tool", "FunctionTool", "creating tools", "MCP integration", "OpenAPI tools", "built-in tools", "google_search tool", "code_execution tool", "long-running tools", "async tools", "third-party tools", "LangChain tools", "computer use", or needs guidance on extending agent capabilities with custom functions, API integrations, or external tool frameworks.
version: 1.0.0
---

# ADK Tools

Guide for adding tools to ADK agents. Tools extend agent capabilities beyond LLM reasoning.

## Tool Types

| Type | Use Case | Complexity |
|------|----------|------------|
| **FunctionTool** | Custom Python functions | Beginner |
| **Built-in** | Google Search, Code Execution | Beginner |
| **OpenAPI** | REST APIs with spec | Intermediate |
| **MCP** | Model Context Protocol servers | Intermediate |
| **Third-Party** | LangChain, CrewAI tools | Intermediate |
| **Long-Running** | Async operations >30s | Intermediate |
| **Computer Use** | Browser/desktop automation | Advanced |

## Quick Start: FunctionTool

```python
def get_weather(city: str) -> dict:
    """Get current weather for a city.

    Args:
        city: City name to get weather for.

    Returns:
        Weather data including temperature and conditions.
    """
    return {"temp": 72, "conditions": "sunny"}

agent = LlmAgent(
    model="gemini-3-flash",
    name="weather_agent",
    tools=[get_weather],  # ADK auto-wraps as FunctionTool
)
```

### Key Requirements

1. **Type hints** - Required for schema generation
2. **Docstring** - LLM uses this to understand the tool
3. **Return type** - Should be JSON-serializable

## Built-in Tools

```python
from google.adk.tools import google_search, code_execution

agent = LlmAgent(
    model="gemini-3-flash",
    name="research_agent",
    tools=[google_search, code_execution],
)
```

## Decision Guide

| If you have... | Use |
|----------------|-----|
| Python function | FunctionTool |
| OpenAPI/Swagger spec | OpenAPIToolset |
| MCP server | MCPToolset |
| LangChain tools | LangchainTool wrapper |
| Need web search | google_search built-in |
| Need code sandbox | code_execution built-in |
| Operation >30s | Long-running pattern |

## References

For detailed guides:
- `references/function-tools.md` - Custom Python functions
- `references/builtin-tools.md` - Google Search, Code Execution
- `references/openapi-tools.md` - REST API integration
- `references/mcp-tools.md` - MCP server integration
- `references/third-party-tools.md` - LangChain, CrewAI
- `references/long-running-tools.md` - Async operations
- `references/computer-use.md` - Browser/desktop automation
