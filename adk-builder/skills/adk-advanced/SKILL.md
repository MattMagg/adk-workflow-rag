---
name: ADK Advanced
description: This skill should be used when the user asks about "visual builder", "no-code agent builder", "drag and drop", "ThinkingConfig", "extended thinking", "chain of thought", "reasoning", or needs guidance on using ADK's visual development tools or configuring advanced reasoning capabilities.
version: 1.0.0
---

# ADK Advanced Features

Guide for advanced ADK features including visual building and extended thinking.

## Advanced Features

| Feature | Purpose |
|---------|---------|
| **Visual Builder** | No-code agent design |
| **ThinkingConfig** | Extended reasoning |

## Visual Builder

Build agents with drag-and-drop:

```bash
# Launch visual builder
adk web --builder

# Access at http://localhost:8000/builder
```

Features:
- Drag-and-drop agent design
- Visual tool configuration
- Export to Python code

## Extended Thinking

Enable chain-of-thought reasoning:

```python
from google.adk.agents import LlmAgent
from google.genai.types import ThinkingConfig

agent = LlmAgent(
    model="gemini-3-flash",
    name="thinking_agent",
    thinking_config=ThinkingConfig(
        thinking_budget=1024,  # Token budget for thinking
    ),
    instruction="Think step by step before answering.",
)
```

### When to Use

- Complex reasoning tasks
- Multi-step problems
- Tasks requiring planning

## References

For detailed guides:
- `references/visual-builder.md` - Visual development tools
- `references/thinking.md` - Extended thinking configuration
