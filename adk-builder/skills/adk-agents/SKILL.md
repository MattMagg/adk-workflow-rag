---
name: ADK Agents
description: This skill should be used when the user asks about "creating an agent", "LlmAgent", "BaseAgent", "custom agent", "agent with different model", "Claude with ADK", "OpenAI with ADK", "LiteLLM", "multi-model agent", or needs guidance on agent configuration, model selection, system instructions, or extending the base agent class for non-LLM logic.
version: 1.0.0
---

# ADK Agents

Guide for creating and configuring agents in Google ADK.

## Agent Types

| Type | Use Case | Class |
|------|----------|-------|
| **LLM Agent** | AI reasoning, tool use, conversation | `LlmAgent` |
| **Custom Agent** | Non-LLM logic, orchestration, API calls | `BaseAgent` |

## Creating an LlmAgent

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    model="gemini-3-flash",
    name="my_agent",
    description="Handles user requests about X",  # For routing
    instruction="""You are a helpful assistant.
    - Be concise
    - Use tools when needed
    """,
)

# Export as root_agent for ADK CLI
root_agent = agent
```

### Required Parameters

| Parameter | Purpose |
|-----------|---------|
| `model` | LLM model string (e.g., `gemini-3-flash`) |
| `name` | Unique identifier (avoid `user`) |

### Recommended Parameters

| Parameter | Purpose |
|-----------|---------|
| `description` | Used by other agents for routing |
| `instruction` | System prompt defining behavior |

## Model Selection

### Gemini Models (Default)
- `gemini-3-flash` - Fast, cost-effective
- `gemini-3-pro` - Most capable

### Other Providers (via LiteLLM)
- `anthropic/claude-sonnet-4` - Claude
- `openai/gpt-4o` - OpenAI

```python
# Using Claude via LiteLLM
agent = LlmAgent(
    model="anthropic/claude-sonnet-4",
    name="claude_agent",
    instruction="...",
)
```

Requires: `pip install litellm` and `ANTHROPIC_API_KEY` env var.

## Custom Agents (BaseAgent)

For non-LLM logic:

```python
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.genai import types

class MyCustomAgent(BaseAgent):
    async def run_async(self, ctx: InvocationContext):
        # Your logic here
        yield types.Content(
            role="model",
            parts=[types.Part(text="Response")]
        )

root_agent = MyCustomAgent(name="custom_agent")
```

## References

For detailed guides:
- `references/llm-agent.md` - Complete LlmAgent configuration
- `references/custom-agent.md` - BaseAgent extension patterns
- `references/multi-model.md` - LiteLLM and model switching
