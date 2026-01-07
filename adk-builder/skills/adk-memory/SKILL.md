---
name: ADK Memory
description: This skill should be used when the user asks about "memory", "MemoryService", "long-term memory", "remember across sessions", "RAG", "retrieval augmented generation", "grounding", "knowledge base", "vector search", or needs guidance on implementing persistent memory or grounding agent responses in external knowledge.
version: 1.0.0
---

# ADK Memory

Guide for implementing memory and grounding in ADK agents.

## Memory Types

| Type | Purpose | Persistence |
|------|---------|-------------|
| **Session State** | Within-conversation data | Session only |
| **MemoryService** | Long-term memories | Cross-session |
| **Grounding** | External knowledge (RAG) | External store |

## MemoryService

Store and recall information across sessions:

```python
from google.adk.memory import MemoryService

memory_service = MemoryService()

agent = LlmAgent(
    model="gemini-3-flash",
    name="agent",
    memory_service=memory_service,
)
```

The agent can now:
- Remember facts across conversations
- Recall user preferences
- Build context over time

## Grounding (RAG)

Ground responses in external knowledge:

```python
from google.adk.tools import VertexAISearchTool

# Connect to Vertex AI Search datastore
search_tool = VertexAISearchTool(
    project_id="my-project",
    location="us-central1",
    datastore_id="my-datastore",
)

agent = LlmAgent(
    model="gemini-3-flash",
    name="grounded_agent",
    tools=[search_tool],
    instruction="Always search for relevant information before answering.",
)
```

## Decision Guide

| If you need... | Use |
|----------------|-----|
| Remember facts across sessions | MemoryService |
| Search documents/knowledge base | Grounding (RAG) |
| Store data within session | Session State |
| Cite sources | Grounding with attribution |

## References

For detailed guides:
- `references/memory-service.md` - Long-term memory patterns
- `references/grounding.md` - RAG and knowledge grounding
