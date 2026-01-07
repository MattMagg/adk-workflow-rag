# ADK Builder Plugin Design

> **For Claude:** Use superpowers:writing-plans to create the implementation plan from this design.

**Plugin Name:** `adk-builder`
**Tagline:** *End-to-end agentic systems development with Google ADK*
**Date:** 2026-01-07
**Status:** Design Complete - Ready for Implementation

---

## Overview

A Claude Code plugin that provides comprehensive guidance for building production-ready agentic systems with Google's Agent Development Kit (ADK). The plugin makes ADK knowledge directly accessible through auto-activated skills and explicit commands with intelligent decision logic.

### Goals

1. Auto-activate relevant ADK knowledge based on development context
2. Provide explicit commands for common ADK development actions
3. Include intelligent decision logic to recommend optimal approaches
4. Cover the full ADK development lifecycle end-to-end

### Non-Goals (v1)

- Autonomous agents (deferred to v2)
- MCP server integrations
- Hooks for automated validation

---

## Source Material

**43 workflow files** in `.agent/workflows/` totaling ~13,400 lines of ADK guidance:
- Already grounded and validated against official ADK documentation
- Uses Gemini 3 models as standard
- Organized in 12 categories

**These source files remain unchanged** - the plugin copies/adapts content into Claude Code plugin structure.

---

## Architecture

### Plugin Location

```
/Users/mac-main/rag_qdrant_voyage/adk-builder/
```

### Distribution

1. **Direct:** `claude --plugin-dir ./adk-builder`
2. **Marketplace:** Separate marketplace repo pointing to this plugin (future)

---

## Components

### Skills (11)

Auto-activated based on development context:

| Skill | Source Workflows | Trigger Context |
|-------|------------------|-----------------|
| `adk-getting-started` | adk-init, adk-init-create-project, adk-init-yaml-config | "new project", "setup", "initialize", "scaffold" |
| `adk-agents` | adk-agents-create, adk-agents-custom, adk-agents-multi-model | "create agent", "LlmAgent", "BaseAgent", "litellm" |
| `adk-tools` | 7 tool workflows | "add tool", "FunctionTool", "MCP", "OpenAPI" |
| `adk-behavior` | 6 behavior workflows | "callback", "state", "artifacts", "human-in-loop" |
| `adk-multi-agent` | 4 multi-agent workflows | "sub-agent", "delegation", "orchestration", "A2A" |
| `adk-memory` | adk-memory-service, adk-memory-grounding | "memory", "MemoryService", "RAG", "grounding" |
| `adk-security` | 3 security workflows | "guardrail", "auth", "safety", "security" |
| `adk-streaming` | 3 streaming workflows | "streaming", "SSE", "websocket", "Live API", "voice" |
| `adk-deployment` | 3 deploy workflows | "deploy", "production", "Agent Engine", "Cloud Run" |
| `adk-quality` | 5 quality workflows | "test", "eval", "tracing", "logging", "observability" |
| `adk-advanced` | 2 advanced workflows | "visual builder", "thinking", "ThinkingConfig" |

**Skill Structure:**
```
skills/adk-tools/
├── SKILL.md           # Core knowledge, trigger description
├── references/        # Detailed workflow content
│   ├── function-tools.md
│   ├── long-running-tools.md
│   └── ...
└── examples/          # Code examples (optional)
```

### Commands (10)

Explicit actions with intelligent decision logic (Pattern C: Contextual Inference + Confirmation):

| Command | Purpose | Decision Logic |
|---------|---------|----------------|
| `/adk-init` | Initialize new ADK project | Detects GCP setup → recommends API key vs Vertex AI auth |
| `/adk-create-agent` | Create new agent | Asks: LLM reasoning needed? → LlmAgent (default) or BaseAgent |
| `/adk-add-tool` | Add tool to agent | Asks: What's your source? → Function / OpenAPI / MCP / Builtin |
| `/adk-add-behavior` | Add callbacks, state, events | Asks: What behavior? → Multiple may apply |
| `/adk-multi-agent` | Set up multi-agent system | Recommends delegation (simplest), offers orchestration/A2A |
| `/adk-add-memory` | Add memory capabilities | Asks: Session memory or knowledge grounding? |
| `/adk-secure` | Add security features | Recommends guardrails first, asks about auth needs |
| `/adk-streaming` | Enable streaming responses | Recommends SSE, asks if voice/video needed for Live API |
| `/adk-deploy` | Deploy to production | **Recommends Agent Engine** (managed + integrated services) |
| `/adk-test` | Create tests/evals | Recommends evals, offers tracing/logging/user-sim |

**Command Decision Pattern:**
```
1. Analyze context (existing config, project structure)
2. Present recommendation with reasoning
3. Offer alternatives
4. Load appropriate workflow based on selection
5. Execute step-by-step with verification
```

### Agents (v2 - Future)

Deferred to v2 after core plugin is proven:

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `adk-architect` | Design agent systems, recommend patterns | "design an agent for X" |
| `adk-reviewer` | Review ADK code for best practices | After writing code, `/adk-review` |
| `adk-debugger` | Diagnose ADK-specific issues | Error encounters |

---

## File Structure

```
adk-builder/
├── .claude-plugin/
│   └── plugin.json              # Manifest
├── skills/
│   ├── adk-getting-started/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── init.md
│   │       ├── create-project.md
│   │       └── yaml-config.md
│   ├── adk-agents/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── llm-agent.md
│   │       ├── custom-agent.md
│   │       └── multi-model.md
│   ├── adk-tools/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── function-tools.md
│   │       ├── long-running-tools.md
│   │       ├── builtin-tools.md
│   │       ├── openapi-tools.md
│   │       ├── mcp-tools.md
│   │       ├── third-party-tools.md
│   │       └── computer-use.md
│   ├── adk-behavior/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── callbacks.md
│   │       ├── plugins.md
│   │       ├── state.md
│   │       ├── artifacts.md
│   │       ├── events.md
│   │       └── confirmation.md
│   ├── adk-multi-agent/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── delegation.md
│   │       ├── orchestration.md
│   │       ├── advanced.md
│   │       └── a2a.md
│   ├── adk-memory/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── memory-service.md
│   │       └── grounding.md
│   ├── adk-security/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── guardrails.md
│   │       ├── auth.md
│   │       └── security-plugins.md
│   ├── adk-streaming/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── sse.md
│   │       ├── bidirectional.md
│   │       └── multimodal.md
│   ├── adk-deployment/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── agent-engine.md
│   │       ├── cloudrun.md
│   │       └── gke.md
│   ├── adk-quality/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── tracing.md
│   │       ├── logging.md
│   │       ├── observability.md
│   │       ├── evals.md
│   │       └── user-sim.md
│   └── adk-advanced/
│       ├── SKILL.md
│       └── references/
│           ├── visual-builder.md
│           └── thinking.md
├── commands/
│   ├── adk-init.md
│   ├── adk-create-agent.md
│   ├── adk-add-tool.md
│   ├── adk-add-behavior.md
│   ├── adk-multi-agent.md
│   ├── adk-add-memory.md
│   ├── adk-secure.md
│   ├── adk-streaming.md
│   ├── adk-deploy.md
│   └── adk-test.md
└── README.md
```

---

## Implementation Notes

### Skill SKILL.md Format

```markdown
---
name: ADK Tools
description: This skill should be used when the user asks about "adding tools", "FunctionTool", "MCP integration", "OpenAPI tools", or needs guidance on extending agent capabilities with custom tools, built-in tools, or third-party integrations.
version: 1.0.0
---

# ADK Tools

[Core knowledge - 1,500-2,000 words in imperative form]

## References

For detailed implementation guides, see:
- `references/function-tools.md` - Custom Python function tools
- `references/openapi-tools.md` - Generate tools from OpenAPI specs
- ...
```

### Command Format

```markdown
---
name: adk-deploy
description: Deploy ADK agent to production with intelligent platform selection
argument-hint: Optional deployment target (agent-engine, cloudrun, gke)
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "AskUserQuestion"]
---

# Deploy ADK Agent

[Decision logic and workflow execution instructions FOR Claude]
```

### Content Adaptation

When copying workflow content to plugin:
1. Remove Antigravity-specific frontmatter (triggers, dependencies, etc.)
2. Keep all code examples, tables, and step-by-step instructions
3. Add Claude Code plugin-appropriate frontmatter
4. Ensure code blocks have language specifiers
5. Update any gemini-2.x model references to gemini-3

---

## Validation Criteria

### Skills
- [ ] Each SKILL.md has proper frontmatter with trigger-rich description
- [ ] References contain complete workflow content
- [ ] Trigger phrases are specific and differentiated

### Commands
- [ ] Each command has decision logic implemented
- [ ] Commands reference appropriate skills
- [ ] AskUserQuestion used for decision points
- [ ] Recommendations include reasoning

### Plugin
- [ ] plugin.json is valid
- [ ] All files follow naming conventions
- [ ] README documents installation and usage
- [ ] Plugin loads without errors in Claude Code

---

## Distribution (Future)

**Marketplace repo** (separate): `github.com/yourname/claude-plugins-marketplace`

```json
{
  "name": "yourname-marketplace",
  "plugins": [{
    "name": "adk-builder",
    "source": {
      "source": "url",
      "url": "https://github.com/yourname/rag_qdrant_voyage.git",
      "path": "adk-builder"
    },
    "description": "End-to-end agentic systems development with Google ADK"
  }]
}
```

---

## v2 Roadmap

1. **Agents**: Add adk-architect, adk-reviewer, adk-debugger
2. **Hooks**: Auto-validate ADK code on save
3. **MCP**: Integration with ADK dev server
4. **Marketplace**: Publish to community marketplace
