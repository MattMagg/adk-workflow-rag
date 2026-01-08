---
name: adk-streaming
description: Enable streaming responses for an ADK agent
argument-hint: Optional streaming type
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Enable Streaming

Invoke the `adk-planner` agent to:
1. Find existing agent in project
2. Recommend streaming type (SSE, Bidirectional, Live API)
3. Plan the streaming implementation

After plan approval, `adk-executor` implements streaming.

Reference `@adk-streaming` skill for streaming patterns.
