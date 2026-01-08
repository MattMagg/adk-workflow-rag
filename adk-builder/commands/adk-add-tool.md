---
name: adk-add-tool
description: Add a tool to an ADK agent with intelligent tool type selection
argument-hint: Optional tool description
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Add Tool to Agent

Invoke the `adk-planner` agent to:
1. Find existing agent in project
2. Recommend tool type (FunctionTool, Built-in, OpenAPI, MCP, etc.)
3. Plan the integration with proper configuration

After plan approval, `adk-executor` implements the tool.

Reference `@adk-tools` skill for tool patterns.
