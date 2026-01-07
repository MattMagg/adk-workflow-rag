# ADK Builder

> End-to-end agentic systems development with Google ADK

A Claude Code plugin providing comprehensive guidance for building production-ready agentic systems with Google's Agent Development Kit (ADK).

## Features

- **11 Auto-Activated Skills**: Domain knowledge surfaces automatically based on context
- **10 Explicit Commands**: Action-oriented workflows with intelligent decision logic
- **Full Lifecycle Coverage**: From project setup to production deployment

## Installation

### Direct (for development)

```bash
claude --plugin-dir /path/to/adk-builder
```

### From This Repo

```bash
git clone https://github.com/yourname/rag_qdrant_voyage.git
claude --plugin-dir ./rag_qdrant_voyage/adk-builder
```

## Skills (Auto-Activated)

| Skill | Triggers When |
|-------|---------------|
| `adk-getting-started` | "new project", "setup", "initialize" |
| `adk-agents` | "create agent", "LlmAgent", "BaseAgent" |
| `adk-tools` | "add tool", "FunctionTool", "MCP" |
| `adk-behavior` | "callback", "state", "artifacts" |
| `adk-multi-agent` | "delegation", "orchestration" |
| `adk-memory` | "memory", "RAG", "grounding" |
| `adk-security` | "guardrail", "auth", "safety" |
| `adk-streaming` | "streaming", "SSE", "Live API" |
| `adk-deployment` | "deploy", "production" |
| `adk-quality` | "test", "eval", "tracing" |
| `adk-advanced` | "visual builder", "thinking" |

## Commands

| Command | Purpose |
|---------|---------|
| `/adk-init` | Initialize new ADK project |
| `/adk-create-agent` | Create new agent |
| `/adk-add-tool` | Add tool to agent |
| `/adk-add-behavior` | Add callbacks, state, events |
| `/adk-multi-agent` | Set up multi-agent system |
| `/adk-add-memory` | Add memory capabilities |
| `/adk-secure` | Add security features |
| `/adk-streaming` | Enable streaming |
| `/adk-deploy` | Deploy to production |
| `/adk-test` | Create tests/evals |

## License

MIT
