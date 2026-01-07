---
name: ADK Behavior
description: This skill should be used when the user asks about "callbacks", "lifecycle hooks", "before_model_call", "after_tool_call", "plugins", "session state", "state management", "artifacts", "file uploads", "events", "EventActions", "human-in-the-loop", "confirmation", or needs guidance on customizing agent behavior, intercepting execution, managing state across turns, or implementing approval workflows.
version: 1.0.0
---

# ADK Behavior

Guide for customizing agent behavior through callbacks, state, artifacts, and events.

## Behavior Components

| Component | Purpose |
|-----------|---------|
| **Callbacks** | Intercept lifecycle events (before/after) |
| **Plugins** | Reusable callback bundles |
| **State** | Session data persistence |
| **Artifacts** | File/binary handling |
| **Events** | Flow control, custom events |
| **Confirmation** | Human-in-the-loop approval |

## Callbacks

Intercept agent execution at lifecycle points:

```python
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

async def log_model_call(ctx: CallbackContext) -> None:
    print(f"Calling model with: {ctx.request}")

agent = LlmAgent(
    model="gemini-3-flash",
    name="agent",
    before_model_callback=log_model_call,
)
```

### Available Callbacks

| Callback | Trigger Point |
|----------|---------------|
| `before_model_callback` | Before LLM call |
| `after_model_callback` | After LLM response |
| `before_tool_callback` | Before tool execution |
| `after_tool_callback` | After tool returns |

## Session State

Store data across conversation turns:

```python
def my_tool(ctx: ToolContext, query: str) -> str:
    # Read state
    count = ctx.state.get("query_count", 0)

    # Update state
    ctx.state["query_count"] = count + 1

    return f"Query #{count + 1}: {query}"
```

## Human-in-the-Loop

Require user confirmation for sensitive actions:

```python
async def confirm_action(ctx: CallbackContext) -> types.Content | None:
    tool_name = ctx.tool_call.name
    if tool_name in ["delete_file", "send_email"]:
        # Return content to ask for confirmation
        return types.Content(
            role="model",
            parts=[types.Part(text=f"Confirm {tool_name}? (yes/no)")]
        )
    return None  # Allow without confirmation
```

## References

For detailed guides:
- `references/callbacks.md` - Lifecycle callback patterns
- `references/plugins.md` - Reusable callback bundles
- `references/state.md` - Session state management
- `references/artifacts.md` - File/binary handling
- `references/events.md` - EventActions and flow control
- `references/confirmation.md` - Human-in-the-loop patterns
