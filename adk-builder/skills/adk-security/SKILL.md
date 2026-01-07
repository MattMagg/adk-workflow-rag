---
name: ADK Security
description: This skill should be used when the user asks about "guardrails", "safety", "content filtering", "input validation", "output validation", "authentication", "OAuth", "API keys", "credentials", "security plugins", or needs guidance on implementing safety measures, access control, or secure authentication in ADK agents.
version: 1.0.0
---

# ADK Security

Guide for implementing security features in ADK agents.

## Security Components

| Component | Purpose |
|-----------|---------|
| **Input Guardrails** | Validate/filter user input |
| **Output Guardrails** | Validate/filter agent responses |
| **Authentication** | Secure API access |
| **Security Plugins** | Reusable security bundles |

## Input Guardrails

Block or modify unsafe input:

```python
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

BLOCKED_TOPICS = ["illegal", "harmful"]

async def input_guardrail(ctx: CallbackContext) -> types.Content | None:
    user_input = ctx.user_content.parts[0].text.lower()

    for topic in BLOCKED_TOPICS:
        if topic in user_input:
            return types.Content(
                role="model",
                parts=[types.Part(text="I cannot help with that topic.")]
            )
    return None  # Allow input

agent = LlmAgent(
    model="gemini-3-flash",
    name="safe_agent",
    before_model_callback=input_guardrail,
)
```

## Output Guardrails

Filter agent responses before returning:

```python
async def output_guardrail(ctx: CallbackContext) -> types.Content | None:
    response = ctx.response.parts[0].text

    # Check for PII, profanity, etc.
    if contains_pii(response):
        return types.Content(
            role="model",
            parts=[types.Part(text="[Response filtered for privacy]")]
        )
    return None  # Allow output
```

## Authentication

For tools requiring auth:

```python
# OAuth credentials in environment
# GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET

from google.adk.auth import OAuthCredentials

credentials = OAuthCredentials(
    scopes=["https://www.googleapis.com/auth/calendar"],
)
```

## References

For detailed guides:
- `references/guardrails.md` - Input/output validation
- `references/auth.md` - Authentication patterns
- `references/security-plugins.md` - Reusable security bundles
