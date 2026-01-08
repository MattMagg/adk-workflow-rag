---
name: adk-multi-agent
description: Set up a multi-agent system with intelligent pattern selection
argument-hint: Optional pattern type
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Set Up Multi-Agent System

Invoke the `adk-planner` agent to:
1. Understand the multi-agent requirements
2. Recommend pattern (Delegation, Sequential, Parallel, A2A)
3. Plan the agent hierarchy and routing

After plan approval, `adk-executor` implements the multi-agent system.

Reference `@adk-multi-agent` skill for orchestration patterns.
