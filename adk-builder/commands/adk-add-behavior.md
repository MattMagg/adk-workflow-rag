---
name: adk-add-behavior
description: Add behavior customization (callbacks, state, events) to an ADK agent
argument-hint: Optional behavior type
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Add Behavior to Agent

Invoke the `adk-planner` agent to:
1. Find existing agent in project
2. Recommend behavior type (callbacks, state, artifacts, events, confirmation)
3. Plan the implementation

After plan approval, `adk-executor` implements the behavior.

Reference `@adk-behavior` skill for behavior patterns.
