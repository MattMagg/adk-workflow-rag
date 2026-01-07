---
name: ADK Streaming
description: This skill should be used when the user asks about "streaming", "real-time responses", "SSE", "server-sent events", "websocket", "bidirectional", "Live API", "voice", "audio", "video", "multimodal streaming", or needs guidance on implementing real-time communication between agents and clients.
version: 1.0.0
---

# ADK Streaming

Guide for implementing streaming and real-time communication in ADK agents.

## Streaming Types

| Type | Use Case | Complexity |
|------|----------|------------|
| **SSE** | Text streaming, progress updates | Intermediate |
| **Bidirectional** | Real-time chat, interrupts | Intermediate |
| **Multimodal** | Voice, video, Live API | Advanced |

## Server-Sent Events (SSE)

Stream responses as they're generated:

```python
from google.adk.runners import Runner

runner = Runner(agent=agent, app_name="app", session_service=sessions)

# Streaming execution
async for event in runner.run_async(
    user_id="user1",
    session_id="session1",
    new_message=content
):
    if event.content:
        print(event.content.parts[0].text, end="", flush=True)
```

## Bidirectional Streaming

Real-time two-way communication:

```python
from google.adk.streaming import BidiStreamingRunner

async with BidiStreamingRunner(agent) as runner:
    # Send messages
    await runner.send(user_message)

    # Receive responses
    async for response in runner.receive():
        process(response)
```

## Live API (Voice/Video)

For voice agents and multimodal:

```python
from google.adk.live import LiveAPIRunner

# Requires Live API compatible model
agent = LlmAgent(
    model="gemini-3-flash-live",  # Live API model
    name="voice_agent",
)

runner = LiveAPIRunner(agent)
# Handle audio/video streams
```

## Decision Guide

| If you need... | Use |
|----------------|-----|
| Text streaming | SSE |
| Real-time chat with interrupts | Bidirectional |
| Voice interaction | Live API |
| Video processing | Live API (multimodal) |

## References

For detailed guides:
- `references/sse.md` - Server-sent events streaming
- `references/bidirectional.md` - WebSocket bidirectional
- `references/multimodal.md` - Live API voice/video
