---
name: adk-create-agent
description: Create a new ADK agent with intelligent type selection
argument-hint: Optional agent name and purpose
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Create ADK Agent

Invoke the `adk-planner` agent to:
1. Understand agent requirements from user description
2. Recommend LlmAgent vs BaseAgent based on use case
3. Plan the implementation with proper configuration

After plan approval, `adk-executor` implements the agent.

Reference `@adk-agents` skill for agent patterns.
