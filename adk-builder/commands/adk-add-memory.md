---
name: adk-add-memory
description: Add memory capabilities to an ADK agent
argument-hint: Optional memory type
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Add Memory to Agent

Invoke the `adk-planner` agent to:
1. Find existing agent in project
2. Recommend memory type (MemoryService or Grounding/RAG)
3. Plan the integration with proper configuration

After plan approval, `adk-executor` implements memory.

Reference `@adk-memory` skill for memory patterns.
