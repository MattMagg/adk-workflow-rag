---
name: adk-deploy
description: Deploy an ADK agent to production with intelligent platform selection
argument-hint: Optional target (agent-engine, cloudrun, gke)
allowed-tools: ["Read", "Write", "Bash", "Glob", "AskUserQuestion", "Task"]
---

# Deploy ADK Agent

Invoke the `adk-planner` agent to:
1. Analyze project requirements and existing configuration
2. Recommend deployment platform (Agent Engine, Cloud Run, GKE)
3. Plan the deployment steps

After plan approval, `adk-executor` executes deployment.

Reference `@adk-deployment` skill for deployment patterns.
