---
name: adk-secure
description: Add security features to an ADK agent
argument-hint: Optional security type
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Secure ADK Agent

Invoke the `adk-planner` agent to:
1. Find existing agent in project
2. Recommend security features (guardrails, auth, plugins)
3. Plan the security implementation

After plan approval, `adk-executor` implements security.

Reference `@adk-security` skill for security patterns.
