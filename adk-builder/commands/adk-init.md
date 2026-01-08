---
name: adk-init
description: Initialize a new ADK project with intelligent authentication detection
argument-hint: Optional project name
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Initialize ADK Project

For a new ADK project, invoke the `adk-planner` agent to:
1. Determine project structure (scaffold vs manual)
2. Detect authentication context (API key vs Vertex AI)
3. Create project files with proper configuration

If this is a simple scaffold request with no ambiguity:
- Run `adk create <project_name>` directly
- Set up `.env` with authentication

Reference `@adk-getting-started` skill for initialization patterns.
