---
name: ADK Multi-Agent
description: This skill should be used when the user asks about "multi-agent systems", "sub-agents", "delegation", "agent routing", "orchestration", "SequentialAgent", "ParallelAgent", "LoopAgent", "agent-to-agent", "A2A protocol", "agent hierarchy", or needs guidance on building systems with multiple specialized agents working together.
version: 1.0.0
---

# ADK Multi-Agent Systems

Guide for building multi-agent systems with delegation, orchestration, and inter-agent communication.

## Multi-Agent Patterns

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| **Delegation** | Route to specialized sub-agents | Intermediate |
| **Sequential** | Pipeline of agents in order | Intermediate |
| **Parallel** | Concurrent agent execution | Intermediate |
| **Loop** | Iterative agent execution | Intermediate |
| **Hierarchy** | Nested agent teams | Advanced |
| **A2A** | Cross-system communication | Advanced |

## Quick Start: Delegation

```python
from google.adk.agents import LlmAgent

# Specialized sub-agents
billing_agent = LlmAgent(
    model="gemini-3-flash",
    name="billing",
    description="Handles billing inquiries and payment issues",
    instruction="You handle billing questions...",
)

support_agent = LlmAgent(
    model="gemini-3-flash",
    name="support",
    description="Handles technical support and troubleshooting",
    instruction="You handle technical issues...",
)

# Parent agent routes based on descriptions
root_agent = LlmAgent(
    model="gemini-3-flash",
    name="router",
    instruction="Route user requests to the appropriate specialist.",
    sub_agents=[billing_agent, support_agent],
)
```

## Workflow Agents

For deterministic execution patterns:

```python
from google.adk.agents import SequentialAgent, ParallelAgent

# Sequential: A → B → C
pipeline = SequentialAgent(
    name="pipeline",
    sub_agents=[research_agent, write_agent, review_agent],
)

# Parallel: A, B, C run concurrently
parallel = ParallelAgent(
    name="parallel",
    sub_agents=[search_agent, analyze_agent],
)
```

## Decision Guide

| If you need... | Use |
|----------------|-----|
| Dynamic routing based on query | Delegation (sub_agents) |
| Fixed execution order | SequentialAgent |
| Concurrent execution | ParallelAgent |
| Retry/iteration | LoopAgent |
| Cross-system agents | A2A protocol |

## References

For detailed guides:
- `references/delegation.md` - Sub-agent routing patterns
- `references/orchestration.md` - Sequential, Parallel, Loop agents
- `references/advanced.md` - Hierarchical and complex patterns
- `references/a2a.md` - Agent-to-Agent protocol
