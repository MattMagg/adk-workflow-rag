---
name: adk-test
description: Create tests and evaluations for an ADK agent
argument-hint: Optional test type
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Test ADK Agent

Invoke the `adk-planner` agent to:
1. Find existing agent in project
2. Recommend testing approach (evals, tracing, logging, user sim)
3. Plan the test implementation

After plan approval, `adk-executor` implements tests.

Reference `@adk-quality` skill for testing patterns.
