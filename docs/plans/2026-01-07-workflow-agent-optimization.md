# ADK Workflow Agent-Optimization Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update all 43 ADK workflows to the agent-optimized format with complete frontmatter, Agent Decision Logic sections, and standardized structure.

**Architecture:** Each workflow file will be enhanced with: (1) complete YAML frontmatter following `_schema.yaml`, (2) Agent Decision Logic section for routing decisions, (3) optional Error Recovery and Next Workflows sections where appropriate. Updates preserve existing content while adding machine-readable metadata.

**Tech Stack:** Markdown, YAML frontmatter, Python validation script

---

## Current State Analysis

From the validation script output:
- **42 workflows** missing `## Agent Decision Logic` section
- **6 workflows** missing `## References` section
- **All 43 workflows** have code blocks without language specifiers
- **42 workflows** have minimal frontmatter (only `description`)
- **1 workflow** (`adk-agents-create.md`) is the fully optimized template

## Target State

Each workflow should have:

### 1. Complete Frontmatter
```yaml
---
description: One-line summary (max 200 chars)
triggers:
  - keyword1
  - keyword2
  - keyword3
category: one-of-12-categories
dependencies:
  - adk-prerequisite-workflow
outputs:
  - path: "{variable}/file.py"
    type: file
context_required:
  - variable_name
completion_criteria:
  - "Checkable condition 1"
  - "Checkable condition 2"
estimated_steps: N
difficulty: beginner|intermediate|advanced
---
```

### 2. Agent Decision Logic Section (after title)
```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - Condition 1
> - Condition 2
>
> **Do NOT use when:**
> - Condition → use `/alternative-workflow`
>
> **Prerequisites:** List of required prior workflows
```

### 3. Standard Sections (in order)
- Agent Decision Logic
- Prerequisites (or Scope for parent workflows)
- Steps 1-N
- Verification
- Troubleshooting
- Error Recovery (optional)
- Next Workflows (optional)
- References

---

## Pre-Execution: RAG Validation

Before updating workflows, validate that the Qdrant vector DB has adequate coverage for each workflow category via RAG queries.

### Validation Queries by Category

Test RAG retrieval for each workflow category to ensure documentation is indexed:

```bash
# Init workflows
python -m src.grounding.query.query_adk "initialize ADK project setup" --top-k 5

# Agents workflows
python -m src.grounding.query.query_adk "create agent LlmAgent" --top-k 5
python -m src.grounding.query.query_adk "custom agent BaseAgent" --top-k 5
python -m src.grounding.query.query_adk "multi-model litellm" --top-k 5

# Tools workflows
python -m src.grounding.query.query_adk "tool function capability" --top-k 5
python -m src.grounding.query.query_adk "long-running async tool" --top-k 5
python -m src.grounding.query.query_adk "openapi rest api spec" --top-k 5
python -m src.grounding.query.query_adk "mcp model context protocol" --top-k 5

# Behavior workflows
python -m src.grounding.query.query_adk "callback lifecycle hook" --top-k 5
python -m src.grounding.query.query_adk "plugin reusable modular" --top-k 5
python -m src.grounding.query.query_adk "state session persistence" --top-k 5
python -m src.grounding.query.query_adk "artifact file upload download" --top-k 5
python -m src.grounding.query.query_adk "event eventactions flow" --top-k 5

# Multi-agent workflows
python -m src.grounding.query.query_adk "multi-agent delegation routing" --top-k 5
python -m src.grounding.query.query_adk "workflow orchestration sequential parallel" --top-k 5

# Memory workflows
python -m src.grounding.query.query_adk "long-term memory service" --top-k 5
python -m src.grounding.query.query_adk "grounding rag knowledge base" --top-k 5

# Security workflows
python -m src.grounding.query.query_adk "guardrail safety filter" --top-k 5
python -m src.grounding.query.query_adk "authentication oauth credential" --top-k 5

# Streaming workflows
python -m src.grounding.query.query_adk "streaming real-time output" --top-k 5
python -m src.grounding.query.query_adk "websocket bidirectional" --top-k 5

# Deploy workflows
python -m src.grounding.query.query_adk "cloud run deployment" --top-k 5
python -m src.grounding.query.query_adk "kubernetes gke cluster" --top-k 5

# Quality workflows
python -m src.grounding.query.query_adk "testing evaluation benchmark" --top-k 5
python -m src.grounding.query.query_adk "logging tracing observability" --top-k 5
```

**Validation Criteria:**
- Each query returns ≥3 results with score ≥0.65
- Results include both documentation and code examples
- Coverage is balanced (docs + code mix)
- Relevant ADK documentation is retrieved

**Test Results (Confirmed):**
✅ Agent creation: 6 results (docs=3, code=3), scores 0.78-0.88
✅ Tool creation: 6 results (docs=2, code=3), scores 0.64-0.79
✅ Multi-agent: 6 results (docs=2, code=3), scores 0.66-0.86
✅ Streaming: 6 results (docs=3, code=3), scores 0.68-0.85

**Next Step:** Run remaining validation queries before executing plan (optional but recommended for confidence)

---

## Workflow List by Category

### init (3 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 1 | `adk-init.md` | none | beginner |
| 2 | `adk-init-create-project.md` | adk-init | beginner |
| 3 | `adk-init-yaml-config.md` | adk-init | beginner |

### agents (3 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 4 | `adk-agents-create.md` | adk-init | beginner |
| 5 | `adk-agents-custom.md` | adk-init, adk-agents-create | intermediate |
| 6 | `adk-agents-multi-model.md` | adk-agents-create | intermediate |

### tools (7 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 7 | `adk-tools-function.md` | adk-agents-create | beginner |
| 8 | `adk-tools-long-running.md` | adk-tools-function | intermediate |
| 9 | `adk-tools-builtin.md` | adk-agents-create | beginner |
| 10 | `adk-tools-openapi.md` | adk-agents-create | intermediate |
| 11 | `adk-tools-mcp.md` | adk-agents-create | intermediate |
| 12 | `adk-tools-third-party.md` | adk-agents-create | intermediate |
| 13 | `adk-tools-computer-use.md` | adk-agents-create | advanced |

### behavior (6 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 14 | `adk-behavior-callbacks.md` | adk-agents-create | intermediate |
| 15 | `adk-behavior-plugins.md` | adk-behavior-callbacks | intermediate |
| 16 | `adk-behavior-state.md` | adk-agents-create | beginner |
| 17 | `adk-behavior-artifacts.md` | adk-agents-create | intermediate |
| 18 | `adk-behavior-events.md` | adk-agents-create | intermediate |
| 19 | `adk-behavior-confirmation.md` | adk-agents-create, adk-tools-function | intermediate |

### multi-agent (4 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 20 | `adk-multi-agent-delegation.md` | adk-agents-create | intermediate |
| 21 | `adk-multi-agent-orchestration.md` | adk-multi-agent-delegation | intermediate |
| 22 | `adk-multi-agent-advanced.md` | adk-multi-agent-delegation | advanced |
| 23 | `adk-multi-agent-a2a.md` | adk-multi-agent-delegation | advanced |

### memory (2 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 24 | `adk-memory-service.md` | adk-agents-create | intermediate |
| 25 | `adk-memory-grounding.md` | adk-agents-create | intermediate |

### security (3 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 26 | `adk-security-guardrails.md` | adk-agents-create, adk-behavior-callbacks | intermediate |
| 27 | `adk-security-auth.md` | adk-agents-create | intermediate |
| 28 | `adk-security-plugins.md` | adk-security-guardrails | advanced |

### streaming (3 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 29 | `adk-streaming-sse.md` | adk-agents-create | intermediate |
| 30 | `adk-streaming-bidi.md` | adk-streaming-sse | intermediate |
| 31 | `adk-streaming-multimodal.md` | adk-streaming-bidi | advanced |

### deploy (3 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 32 | `adk-deploy-agent-engine.md` | adk-agents-create | intermediate |
| 33 | `adk-deploy-cloudrun.md` | adk-agents-create | intermediate |
| 34 | `adk-deploy-gke.md` | adk-agents-create | advanced |

### quality (5 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 35 | `adk-quality-tracing.md` | adk-agents-create | intermediate |
| 36 | `adk-quality-logging.md` | adk-agents-create | beginner |
| 37 | `adk-quality-observability.md` | adk-quality-logging | intermediate |
| 38 | `adk-quality-evals.md` | adk-agents-create | intermediate |
| 39 | `adk-quality-user-sim.md` | adk-quality-evals | advanced |

### advanced (2 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 40 | `adk-advanced-visual-builder.md` | adk-agents-create | intermediate |
| 41 | `adk-advanced-thinking.md` | adk-agents-create | intermediate |

### meta (2 workflows)
| # | Workflow | Dependencies | Difficulty |
|---|----------|--------------|------------|
| 42 | `adk-master.md` | none | beginner |
| 43 | `adk-create-workflow.md` | none | intermediate |

---

## Tasks

### Task 1: Update adk-init.md

**Files:**
- Modify: `.agent/workflows/adk-init.md`

**Step 1: Read current file**

```bash
cat .agent/workflows/adk-init.md
```

**Step 2: Replace frontmatter**

Replace:
```yaml
---
description: Initialize new ADK project with proper structure and dependencies
---
```

With:
```yaml
---
description: Initialize new ADK project with proper structure and dependencies
triggers:
  - init
  - create project
  - new project
  - scaffold
  - start
  - bootstrap
  - setup adk
category: init
dependencies: []
outputs:
  - path: ".venv/"
    type: directory
  - path: ".env"
    type: file
context_required:
  - project_directory
  - auth_method
completion_criteria:
  - "adk --version returns version number"
  - ".env file contains authentication credentials"
  - "Virtual environment is activated"
estimated_steps: 4
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic section**

Insert after `# ADK Workflow: Project Initialization`:

```markdown
---

## Agent Decision Logic

> **Use this workflow when:**
> - User wants to start a new ADK project from scratch
> - User mentions "init", "setup", "create project", or "bootstrap"
> - No existing ADK project structure is detected
>
> **Do NOT use when:**
> - Project already has agent.py with root_agent → use `/adk-agents-create` to modify
> - User wants to add features to existing agent → route to specific workflow
>
> **Prerequisites:** Python 3.10+ installed on system
```

**Step 4: Add language specifiers to code blocks**

Find all ` ``` ` without language and add appropriate specifier:
- Shell commands: `bash`
- Python code: `python`
- Environment files: `env`
- Directory structures: `text`

**Step 5: Verify changes**

```bash
python .agent/scripts/validate_workflows.py --verbose 2>&1 | grep adk-init.md
```

Expected: No errors for adk-init.md

**Step 6: Commit**

```bash
git add .agent/workflows/adk-init.md
git commit -m "feat(workflows): add agent-optimized frontmatter to adk-init"
```

---

### Task 2: Update adk-init-create-project.md

**Files:**
- Modify: `.agent/workflows/adk-init-create-project.md`

**Step 1: Read current file**

```bash
cat .agent/workflows/adk-init-create-project.md
```

**Step 2: Replace frontmatter with complete version**

```yaml
---
description: Scaffold Python ADK project using adk create command
triggers:
  - adk create
  - project structure
  - folder structure
  - scaffold project
category: init
dependencies:
  - adk-init
outputs:
  - path: "{agent_name}/"
    type: directory
  - path: "{agent_name}/agent.py"
    type: file
  - path: "{agent_name}/__init__.py"
    type: file
context_required:
  - agent_name
completion_criteria:
  - "Directory {agent_name}/ exists with agent.py"
  - "adk run {agent_name} shows agent prompt"
estimated_steps: 3
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic section after title**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants to scaffold a new agent project with `adk create`
> - User asks about project structure or folder layout
> - Creating a fresh agent from scratch
>
> **Do NOT use when:**
> - User wants YAML-based no-code agent → use `/adk-init-yaml-config`
> - User already has agent.py and wants to modify it
>
> **Prerequisites:** `/adk-init` completed (ADK installed, venv active)
```

**Step 4: Add language specifiers to all code blocks**

**Step 5: Verify and commit**

```bash
python .agent/scripts/validate_workflows.py --verbose 2>&1 | grep adk-init-create-project.md
git add .agent/workflows/adk-init-create-project.md
git commit -m "feat(workflows): add agent-optimized frontmatter to adk-init-create-project"
```

---

### Task 3: Update adk-init-yaml-config.md

**Files:**
- Modify: `.agent/workflows/adk-init-yaml-config.md`

**Step 1: Read and analyze current content**

**Step 2: Add complete frontmatter**

```yaml
---
description: Configure ADK agents using YAML declarative syntax (no-code)
triggers:
  - yaml
  - config file
  - declarative
  - no-code
  - yaml config
category: init
dependencies:
  - adk-init
outputs:
  - path: "{agent_name}/agent.yaml"
    type: file
context_required:
  - agent_name
  - model_choice
completion_criteria:
  - "agent.yaml exists with valid YAML syntax"
  - "adk run {agent_name} loads agent from YAML"
estimated_steps: 4
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User prefers YAML/declarative configuration over Python code
> - User mentions "no-code", "config file", or "YAML"
> - Simple agent without custom Python logic needed
>
> **Do NOT use when:**
> - User needs custom tools or callbacks → use `/adk-init-create-project` + Python
> - User needs programmatic control over agent behavior
>
> **Prerequisites:** `/adk-init` completed
```

**Step 4: Add language specifiers and verify**

**Step 5: Commit**

```bash
git add .agent/workflows/adk-init-yaml-config.md
git commit -m "feat(workflows): add agent-optimized frontmatter to adk-init-yaml-config"
```

---

### Task 4: Skip adk-agents-create.md (Already Complete)

This workflow was updated in the previous session as the template. Verify it passes validation:

```bash
python .agent/scripts/validate_workflows.py --verbose 2>&1 | grep adk-agents-create.md
```

Expected: Only code block warnings (acceptable)

---

### Task 5: Update adk-agents-custom.md

**Files:**
- Modify: `.agent/workflows/adk-agents-custom.md`

**Step 1: Read current file**

**Step 2: Add complete frontmatter**

```yaml
---
description: Create custom agents by extending BaseAgent for non-LLM logic
triggers:
  - custom agent
  - BaseAgent
  - extend agent
  - non-llm agent
  - programmatic agent
category: agents
dependencies:
  - adk-init
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - agent_name
  - custom_logic_description
completion_criteria:
  - "Custom agent class extends BaseAgent"
  - "run_async method is implemented"
  - "adk run {agent_name} executes custom logic"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs agent with non-LLM logic (API calls, calculations, orchestration)
> - User wants to extend BaseAgent class directly
> - Deterministic behavior required without LLM reasoning
>
> **Do NOT use when:**
> - User wants LLM-powered reasoning → use `/adk-agents-create`
> - User wants to orchestrate multiple LLM agents → use `/adk-multi-agent-orchestration`
>
> **Prerequisites:** `/adk-init` and understanding of `/adk-agents-create` concepts
```

**Step 4: Add language specifiers, verify, commit**

---

### Task 6: Update adk-agents-multi-model.md

**Files:**
- Modify: `.agent/workflows/adk-agents-multi-model.md`

**Step 2: Add complete frontmatter**

```yaml
---
description: Configure agents with different LLM providers via LiteLLM integration
triggers:
  - multi-model
  - litellm
  - claude
  - anthropic
  - openai
  - different model
  - gpt-4
  - model provider
category: agents
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - model_provider
  - model_name
  - api_key_env_var
completion_criteria:
  - "LiteLLM model string used in agent"
  - "API key configured in environment"
  - "Agent responds using specified model"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants to use non-Gemini models (Claude, GPT-4, etc.)
> - User mentions "LiteLLM", "Anthropic", "OpenAI", or specific model names
> - User needs to switch between model providers
>
> **Do NOT use when:**
> - User is fine with Gemini models → use `/adk-agents-create`
> - User wants multiple models in same system → combine with `/adk-multi-agent-delegation`
>
> **Prerequisites:** `/adk-agents-create` completed, target model API key available
```

---

### Task 7: Update adk-tools-function.md

**Files:**
- Modify: `.agent/workflows/adk-tools-function.md`

**Step 2: Add complete frontmatter**

```yaml
---
description: Create custom tools using FunctionTool and ToolContext for agent capabilities
triggers:
  - tool
  - function
  - FunctionTool
  - capability
  - custom tool
  - add tool
category: tools
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/tools.py"
    type: file
context_required:
  - tool_name
  - tool_purpose
  - input_parameters
  - return_type
completion_criteria:
  - "Function with proper type hints and docstring"
  - "Tool registered in agent's tools list"
  - "Agent can invoke tool during conversation"
estimated_steps: 6
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants to add custom functionality to agent
> - User mentions "tool", "function", or "capability"
> - Agent needs to call external APIs or perform calculations
>
> **Do NOT use when:**
> - User needs long-running async tools → use `/adk-tools-long-running`
> - User wants built-in Google tools → use `/adk-tools-builtin`
> - User has OpenAPI spec → use `/adk-tools-openapi`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 8: Update adk-tools-long-running.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Implement async tools with pending status for long-running operations
triggers:
  - long-running
  - async tool
  - background task
  - pending
  - async operation
category: tools
dependencies:
  - adk-tools-function
outputs:
  - path: "{agent_name}/tools.py"
    type: file
context_required:
  - tool_name
  - async_operation_description
completion_criteria:
  - "Tool returns pending FunctionResponse"
  - "Status tracking implemented"
  - "Completion callback or polling works"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - Tool operation takes >30 seconds
> - User needs async/background processing
> - User mentions "long-running", "pending", or "background"
>
> **Do NOT use when:**
> - Tool completes quickly (<30s) → use `/adk-tools-function`
> - User needs simple API calls → use `/adk-tools-function`
>
> **Prerequisites:** `/adk-tools-function` concepts understood
```

---

### Task 9: Update adk-tools-builtin.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Use ADK built-in tools like google_search and code_execution
triggers:
  - builtin
  - google_search
  - code_execution
  - built-in tools
  - prebuilt
category: tools
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - builtin_tool_name
completion_criteria:
  - "Built-in tool imported from google.adk.tools"
  - "Tool added to agent's tools list"
  - "Agent successfully uses tool"
estimated_steps: 3
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs web search capability (google_search)
> - User needs code execution in sandbox (code_execution)
> - User asks about "built-in" or "prebuilt" tools
>
> **Do NOT use when:**
> - User needs custom logic → use `/adk-tools-function`
> - User has existing API spec → use `/adk-tools-openapi`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 10: Update adk-tools-openapi.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Generate tools from OpenAPI/Swagger specifications
triggers:
  - openapi
  - rest api
  - spec
  - swagger
  - api tool
  - openapi spec
category: tools
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/tools.py"
    type: file
context_required:
  - openapi_spec_path_or_url
  - target_operations
completion_criteria:
  - "OpenAPIToolset created from spec"
  - "Tools registered with agent"
  - "Agent can call API endpoints"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User has OpenAPI/Swagger spec for existing API
> - User wants to connect agent to REST API
> - User mentions "OpenAPI", "Swagger", or "spec"
>
> **Do NOT use when:**
> - No spec exists → use `/adk-tools-function` with manual implementation
> - User needs MCP integration → use `/adk-tools-mcp`
>
> **Prerequisites:** `/adk-agents-create` completed, OpenAPI spec available
```

---

### Task 11: Update adk-tools-mcp.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Integrate Model Context Protocol servers for external tool access
triggers:
  - mcp
  - model context protocol
  - mcp server
  - mcp tools
category: tools
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - mcp_server_command_or_url
completion_criteria:
  - "MCPToolset configured with server"
  - "Tools from MCP server available to agent"
  - "Agent can call MCP tools"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User has MCP server to integrate
> - User mentions "MCP", "Model Context Protocol"
> - Connecting to external MCP-compatible services
>
> **Do NOT use when:**
> - User has OpenAPI spec → use `/adk-tools-openapi`
> - User wants custom Python functions → use `/adk-tools-function`
>
> **Prerequisites:** `/adk-agents-create` completed, MCP server available
```

---

### Task 12: Update adk-tools-third-party.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Integrate tools from LangChain, CrewAI, and other frameworks
triggers:
  - langchain
  - crewai
  - third-party
  - external tool
  - framework integration
category: tools
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/tools.py"
    type: file
context_required:
  - source_framework
  - tool_name
completion_criteria:
  - "Third-party tool wrapped for ADK"
  - "Tool works with ADK agent"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User has existing LangChain or CrewAI tools
> - User mentions "LangChain", "CrewAI", or "third-party"
> - Migrating from another framework to ADK
>
> **Do NOT use when:**
> - Building tools from scratch → use `/adk-tools-function`
>
> **Prerequisites:** `/adk-agents-create` completed, third-party package installed
```

---

### Task 13: Update adk-tools-computer-use.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Enable computer use capabilities for browser and desktop automation
triggers:
  - computer use
  - browser
  - desktop
  - automation
  - screen control
category: tools
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - automation_target
completion_criteria:
  - "Computer use tools configured"
  - "Agent can interact with screen/browser"
estimated_steps: 5
difficulty: advanced
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs browser automation
> - User needs desktop/screen interaction
> - User mentions "computer use", "automation", "browser control"
>
> **Do NOT use when:**
> - User just needs API calls → use `/adk-tools-function`
> - User needs web scraping without interaction → use `/adk-tools-function`
>
> **Prerequisites:** `/adk-agents-create` completed, appropriate permissions configured
```

---

### Task 14: Update adk-behavior-callbacks.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Add lifecycle callbacks for logging, validation, and custom behavior
triggers:
  - callback
  - before_
  - after_
  - lifecycle
  - hook
  - intercept
category: behavior
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/callbacks.py"
    type: file
context_required:
  - callback_type
  - callback_purpose
completion_criteria:
  - "Callback function defined with correct signature"
  - "Callback registered with agent"
  - "Callback executes at correct lifecycle point"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs to intercept agent lifecycle events
> - User mentions "callback", "hook", "before", "after", "logging"
> - User wants to add validation or modification at specific points
>
> **Do NOT use when:**
> - User wants reusable callback bundles → use `/adk-behavior-plugins`
> - User just needs state management → use `/adk-behavior-state`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 15: Update adk-behavior-plugins.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Create reusable callback bundles as plugins for modular behavior
triggers:
  - plugin
  - reusable
  - modular
  - extension
  - callback bundle
category: behavior
dependencies:
  - adk-behavior-callbacks
outputs:
  - path: "{agent_name}/plugins/"
    type: directory
context_required:
  - plugin_name
  - plugin_purpose
completion_criteria:
  - "Plugin class created with callbacks"
  - "Plugin registered with agent"
  - "Callbacks execute correctly"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants to bundle callbacks for reuse
> - User mentions "plugin", "modular", "reusable"
> - Building shareable behavior extensions
>
> **Do NOT use when:**
> - User needs single callback → use `/adk-behavior-callbacks`
> - User needs security-specific plugins → use `/adk-security-plugins`
>
> **Prerequisites:** `/adk-behavior-callbacks` concepts understood
```

---

### Task 16: Update adk-behavior-state.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Manage session state, persistence, and cross-turn data
triggers:
  - state
  - session
  - persist
  - storage
  - memory
  - context
category: behavior
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - state_keys
  - persistence_needs
completion_criteria:
  - "State accessed via ToolContext or session"
  - "State persists across turns"
  - "State updates work correctly"
estimated_steps: 4
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs to store data across conversation turns
> - User mentions "state", "session", "persist", "remember"
> - Building stateful agents with context
>
> **Do NOT use when:**
> - User needs long-term memory service → use `/adk-memory-service`
> - User needs file storage → use `/adk-behavior-artifacts`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 17: Update adk-behavior-artifacts.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Handle file uploads, downloads, and binary data with artifacts
triggers:
  - artifact
  - file
  - binary
  - upload
  - download
  - attachment
category: behavior
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - artifact_type
completion_criteria:
  - "Artifact handling implemented"
  - "Files can be uploaded/downloaded"
  - "Binary data processed correctly"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs to handle file uploads/downloads
> - User mentions "artifact", "file", "binary", "attachment"
> - Agent needs to process or return files
>
> **Do NOT use when:**
> - User needs simple state storage → use `/adk-behavior-state`
> - User needs image/audio streaming → use `/adk-streaming-multimodal`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 18: Update adk-behavior-events.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Use EventActions to control agent flow and emit custom events
triggers:
  - event
  - eventactions
  - stream events
  - control flow
  - emit
category: behavior
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - event_types_needed
completion_criteria:
  - "EventActions used correctly"
  - "Custom events emitted"
  - "Event flow controlled"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs to control agent execution flow
> - User mentions "events", "EventActions", "emit"
> - User needs custom event handling
>
> **Do NOT use when:**
> - User needs streaming output → use `/adk-streaming-sse`
> - User needs callbacks → use `/adk-behavior-callbacks`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 19: Update adk-behavior-confirmation.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Implement human-in-the-loop confirmation for sensitive actions
triggers:
  - confirmation
  - approve
  - human-in-loop
  - verify
  - consent
category: behavior
dependencies:
  - adk-agents-create
  - adk-tools-function
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - actions_requiring_confirmation
completion_criteria:
  - "Confirmation flow implemented"
  - "User approval required before action"
  - "Rejection handled gracefully"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs approval before agent takes actions
> - User mentions "confirmation", "approve", "human-in-loop"
> - Sensitive operations require user consent
>
> **Do NOT use when:**
> - User needs input validation → use `/adk-security-guardrails`
> - User needs general callbacks → use `/adk-behavior-callbacks`
>
> **Prerequisites:** `/adk-agents-create` and `/adk-tools-function` completed
```

---

### Task 20: Update adk-multi-agent-delegation.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Create multi-agent systems with sub-agents and delegation
triggers:
  - sub-agent
  - delegation
  - transfer
  - route
  - multi-agent
  - team
category: multi-agent
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - parent_agent_purpose
  - sub_agent_purposes
completion_criteria:
  - "Parent agent with sub_agents list"
  - "Routing based on descriptions works"
  - "Sub-agents execute correctly"
estimated_steps: 6
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs multiple specialized agents
> - User mentions "sub-agent", "delegation", "team", "route"
> - Task requires different agents for different subtasks
>
> **Do NOT use when:**
> - Single agent sufficient → use `/adk-agents-create`
> - User needs workflow orchestration → use `/adk-multi-agent-orchestration`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 21: Update adk-multi-agent-orchestration.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Build workflow agents with sequential, parallel, and loop patterns
triggers:
  - sequential
  - parallel
  - loop
  - workflow agent
  - orchestration
  - pipeline
category: multi-agent
dependencies:
  - adk-multi-agent-delegation
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - orchestration_pattern
  - agent_sequence
completion_criteria:
  - "Workflow agent configured"
  - "Agents execute in correct order/pattern"
  - "Data flows between agents"
estimated_steps: 6
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs deterministic agent execution order
> - User mentions "sequential", "parallel", "pipeline", "workflow"
> - Agents must run in specific patterns
>
> **Do NOT use when:**
> - User needs dynamic routing → use `/adk-multi-agent-delegation`
> - User needs custom orchestration logic → use `/adk-agents-custom`
>
> **Prerequisites:** `/adk-multi-agent-delegation` concepts understood
```

---

### Task 22: Update adk-multi-agent-advanced.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Advanced multi-agent patterns with hierarchy and composition
triggers:
  - hierarchy
  - compose
  - advanced multi
  - team architecture
  - nested agents
category: multi-agent
dependencies:
  - adk-multi-agent-delegation
outputs:
  - path: "{agent_name}/"
    type: directory
context_required:
  - hierarchy_structure
  - agent_responsibilities
completion_criteria:
  - "Hierarchical agent structure implemented"
  - "Agents compose correctly"
  - "Complex routing works"
estimated_steps: 7
difficulty: advanced
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs complex agent hierarchies
> - User mentions "hierarchy", "nested", "advanced multi-agent"
> - Building large-scale agent teams
>
> **Do NOT use when:**
> - Simple delegation sufficient → use `/adk-multi-agent-delegation`
> - Single level of sub-agents enough
>
> **Prerequisites:** `/adk-multi-agent-delegation` mastered
```

---

### Task 23: Update adk-multi-agent-a2a.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Enable agent-to-agent communication using A2A protocol
triggers:
  - a2a
  - interop
  - agent-to-agent
  - protocol
  - cross-system
category: multi-agent
dependencies:
  - adk-multi-agent-delegation
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - a2a_endpoint
  - protocol_version
completion_criteria:
  - "A2A protocol configured"
  - "Agents communicate across systems"
estimated_steps: 6
difficulty: advanced
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs agents to communicate across systems
> - User mentions "A2A", "agent-to-agent", "interop"
> - Building federated agent systems
>
> **Do NOT use when:**
> - Agents in same system → use `/adk-multi-agent-delegation`
> - Single codebase multi-agent
>
> **Prerequisites:** `/adk-multi-agent-delegation` completed
```

---

### Task 24: Update adk-memory-service.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Implement long-term memory using MemoryService
triggers:
  - memory
  - memoryservice
  - long-term
  - remember
  - recall
category: memory
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - memory_scope
completion_criteria:
  - "MemoryService configured"
  - "Agent can store memories"
  - "Agent can recall memories"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs agent to remember across sessions
> - User mentions "memory", "long-term", "remember", "recall"
> - Building agents with persistent knowledge
>
> **Do NOT use when:**
> - User needs session state only → use `/adk-behavior-state`
> - User needs RAG/search → use `/adk-memory-grounding`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 25: Update adk-memory-grounding.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Ground agent responses with external knowledge via RAG
triggers:
  - grounding
  - search
  - rag
  - retrieval
  - knowledge base
category: memory
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - knowledge_source
completion_criteria:
  - "Grounding source configured"
  - "Agent retrieves relevant context"
  - "Responses grounded in knowledge"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs agent grounded in external knowledge
> - User mentions "RAG", "grounding", "knowledge base", "search"
> - Agent should cite sources or use documents
>
> **Do NOT use when:**
> - User needs simple memory → use `/adk-memory-service`
> - User needs web search → use `/adk-tools-builtin`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 26: Update adk-security-guardrails.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Implement input/output guardrails for safety and compliance
triggers:
  - guardrail
  - safety
  - filter
  - block
  - protect
  - validation
category: security
dependencies:
  - adk-agents-create
  - adk-behavior-callbacks
outputs:
  - path: "{agent_name}/guardrails.py"
    type: file
context_required:
  - guardrail_rules
completion_criteria:
  - "Input guardrail callback implemented"
  - "Output guardrail callback implemented"
  - "Blocked content handled gracefully"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs content filtering/validation
> - User mentions "guardrail", "safety", "filter", "block"
> - Building agents with compliance requirements
>
> **Do NOT use when:**
> - User needs auth → use `/adk-security-auth`
> - User needs general callbacks → use `/adk-behavior-callbacks`
>
> **Prerequisites:** `/adk-agents-create` and `/adk-behavior-callbacks` completed
```

---

### Task 27: Update adk-security-auth.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Configure authentication and credential management
triggers:
  - auth
  - oauth
  - credential
  - token
  - authenticate
  - api key
category: security
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/auth.py"
    type: file
context_required:
  - auth_method
  - credentials_location
completion_criteria:
  - "Auth configured correctly"
  - "Credentials securely managed"
  - "Agent authenticates successfully"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs OAuth or API key management
> - User mentions "auth", "credential", "token", "authenticate"
> - Tools require authenticated API calls
>
> **Do NOT use when:**
> - User needs content filtering → use `/adk-security-guardrails`
> - User needs access control policies → use `/adk-security-plugins`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 28: Update adk-security-plugins.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Create security-focused plugins for policy enforcement
triggers:
  - security plugin
  - policy
  - enforcement
  - access control
  - audit
category: security
dependencies:
  - adk-security-guardrails
outputs:
  - path: "{agent_name}/plugins/"
    type: directory
context_required:
  - security_policies
completion_criteria:
  - "Security plugin implemented"
  - "Policies enforced correctly"
  - "Audit logging works"
estimated_steps: 5
difficulty: advanced
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs reusable security policies
> - User mentions "security plugin", "policy", "enforcement", "audit"
> - Building enterprise-grade security
>
> **Do NOT use when:**
> - Simple guardrails sufficient → use `/adk-security-guardrails`
> - Auth only needed → use `/adk-security-auth`
>
> **Prerequisites:** `/adk-security-guardrails` mastered
```

---

### Task 29: Update adk-streaming-sse.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Implement server-sent events streaming for real-time output
triggers:
  - stream
  - sse
  - server-sent
  - realtime output
  - streaming response
category: streaming
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - streaming_use_case
completion_criteria:
  - "SSE streaming configured"
  - "Events stream to client"
  - "Partial responses displayed"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants real-time streaming responses
> - User mentions "stream", "SSE", "real-time", "progressive"
> - Building chat interfaces with streaming
>
> **Do NOT use when:**
> - User needs bidirectional → use `/adk-streaming-bidi`
> - User needs audio/video → use `/adk-streaming-multimodal`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 30: Update adk-streaming-bidi.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Implement bidirectional streaming with WebSocket for live interaction
triggers:
  - bidi
  - websocket
  - live
  - realtime
  - bidirectional
  - two-way
category: streaming
dependencies:
  - adk-streaming-sse
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - interaction_pattern
completion_criteria:
  - "Bidirectional streaming works"
  - "Live interaction functional"
  - "WebSocket connection stable"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs two-way real-time communication
> - User mentions "WebSocket", "bidirectional", "live"
> - Building interactive real-time applications
>
> **Do NOT use when:**
> - One-way streaming sufficient → use `/adk-streaming-sse`
> - User needs audio/video → use `/adk-streaming-multimodal`
>
> **Prerequisites:** `/adk-streaming-sse` concepts understood
```

---

### Task 31: Update adk-streaming-multimodal.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Enable audio/video streaming with Live API for voice agents
triggers:
  - audio
  - video
  - voice
  - multimodal stream
  - live api
  - speech
category: streaming
dependencies:
  - adk-streaming-bidi
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - modality
  - audio_video_requirements
completion_criteria:
  - "Live API configured"
  - "Audio/video streaming works"
  - "Voice interaction functional"
estimated_steps: 6
difficulty: advanced
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs voice/audio interaction
> - User mentions "audio", "video", "voice", "Live API"
> - Building voice assistants or video agents
>
> **Do NOT use when:**
> - Text streaming only → use `/adk-streaming-sse`
> - Text bidirectional → use `/adk-streaming-bidi`
>
> **Prerequisites:** `/adk-streaming-bidi` mastered
```

---

### Task 32: Update adk-deploy-agent-engine.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Deploy agents to Vertex AI Agent Engine for managed hosting
triggers:
  - deploy
  - production
  - vertex
  - agent engine
  - managed
category: deploy
dependencies:
  - adk-agents-create
outputs:
  - path: "deployed_agent_url"
    type: config
context_required:
  - gcp_project
  - gcp_region
completion_criteria:
  - "Agent deployed to Agent Engine"
  - "Endpoint accessible"
  - "Agent responds correctly"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants fully managed deployment
> - User mentions "Agent Engine", "Vertex AI", "managed"
> - Enterprise deployment with auto-scaling needed
>
> **Do NOT use when:**
> - User needs container control → use `/adk-deploy-cloudrun`
> - User needs Kubernetes → use `/adk-deploy-gke`
>
> **Prerequisites:** `/adk-agents-create` completed, GCP project configured
```

---

### Task 33: Update adk-deploy-cloudrun.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Deploy ADK agents to Cloud Run for serverless container hosting
triggers:
  - cloud run
  - cloudrun
  - serverless
  - container
  - docker
category: deploy
dependencies:
  - adk-agents-create
outputs:
  - path: "cloud_run_service_url"
    type: config
context_required:
  - gcp_project
  - gcp_region
  - service_name
completion_criteria:
  - "Container deployed to Cloud Run"
  - "Service URL accessible"
  - "Agent responds correctly"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants serverless container deployment
> - User mentions "Cloud Run", "serverless", "container"
> - Needs more control than Agent Engine
>
> **Do NOT use when:**
> - User wants managed service → use `/adk-deploy-agent-engine`
> - User needs Kubernetes → use `/adk-deploy-gke`
>
> **Prerequisites:** `/adk-agents-create` completed, GCP project configured
```

---

### Task 34: Update adk-deploy-gke.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Deploy ADK agents to GKE for Kubernetes-based hosting
triggers:
  - gke
  - kubernetes
  - k8s
  - cluster
  - helm
category: deploy
dependencies:
  - adk-agents-create
outputs:
  - path: "k8s_deployment.yaml"
    type: file
context_required:
  - gke_cluster
  - namespace
completion_criteria:
  - "Deployment to GKE successful"
  - "Service exposed correctly"
  - "Agent accessible via ingress"
estimated_steps: 6
difficulty: advanced
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User has existing Kubernetes infrastructure
> - User mentions "GKE", "Kubernetes", "K8s", "Helm"
> - Needs enterprise Kubernetes deployment
>
> **Do NOT use when:**
> - User wants simpler deployment → use `/adk-deploy-cloudrun`
> - User wants managed service → use `/adk-deploy-agent-engine`
>
> **Prerequisites:** `/adk-agents-create` completed, GKE cluster available
```

---

### Task 35: Update adk-quality-tracing.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Add distributed tracing with Cloud Trace for debugging
triggers:
  - trace
  - cloud trace
  - tracing
  - span
  - distributed tracing
category: quality
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - gcp_project
completion_criteria:
  - "Tracing configured"
  - "Traces visible in Cloud Trace"
  - "Spans show agent flow"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs distributed tracing
> - User mentions "trace", "Cloud Trace", "span"
> - Debugging agent execution flow
>
> **Do NOT use when:**
> - User needs simple logging → use `/adk-quality-logging`
> - User needs metrics dashboards → use `/adk-quality-observability`
>
> **Prerequisites:** `/adk-agents-create` completed, GCP project configured
```

---

### Task 36: Update adk-quality-logging.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Configure structured logging for debugging and monitoring
triggers:
  - log
  - logging
  - loggingplugin
  - debug
  - print
category: quality
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - log_level
completion_criteria:
  - "Logging configured"
  - "Logs include agent events"
  - "Log level adjustable"
estimated_steps: 3
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs basic logging/debugging
> - User mentions "log", "debug", "print"
> - Starting to troubleshoot agent behavior
>
> **Do NOT use when:**
> - User needs distributed tracing → use `/adk-quality-tracing`
> - User needs full observability → use `/adk-quality-observability`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 37: Update adk-quality-observability.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Integrate third-party observability tools like AgentOps and LangSmith
triggers:
  - observability
  - agentops
  - langsmith
  - monitor
  - dashboard
category: quality
dependencies:
  - adk-quality-logging
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - observability_platform
completion_criteria:
  - "Observability platform integrated"
  - "Metrics visible in dashboard"
  - "Alerts configured"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants third-party observability
> - User mentions "AgentOps", "LangSmith", "dashboard", "monitor"
> - Building production monitoring
>
> **Do NOT use when:**
> - Basic logging sufficient → use `/adk-quality-logging`
> - User has Cloud Trace → use `/adk-quality-tracing`
>
> **Prerequisites:** `/adk-quality-logging` configured
```

---

### Task 38: Update adk-quality-evals.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Create evaluation suites for testing agent behavior
triggers:
  - eval
  - test
  - evaluate
  - benchmark
  - assess
  - quality
category: quality
dependencies:
  - adk-agents-create
outputs:
  - path: "tests/eval/"
    type: directory
context_required:
  - eval_criteria
  - test_cases
completion_criteria:
  - "Eval suite created"
  - "Test cases pass"
  - "Metrics collected"
estimated_steps: 6
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs to test agent quality
> - User mentions "eval", "test", "benchmark", "assess"
> - Building CI/CD quality gates
>
> **Do NOT use when:**
> - User needs synthetic users → use `/adk-quality-user-sim`
> - User needs unit tests → standard pytest
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 39: Update adk-quality-user-sim.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Create synthetic user simulators for automated testing
triggers:
  - user sim
  - simulation
  - synthetic
  - fake user
  - automated testing
category: quality
dependencies:
  - adk-quality-evals
outputs:
  - path: "tests/simulators/"
    type: directory
context_required:
  - user_personas
  - interaction_patterns
completion_criteria:
  - "User simulator created"
  - "Simulated conversations work"
  - "Metrics from simulations"
estimated_steps: 5
difficulty: advanced
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs automated conversation testing
> - User mentions "user sim", "synthetic", "simulator"
> - Stress testing agent at scale
>
> **Do NOT use when:**
> - Manual eval sufficient → use `/adk-quality-evals`
> - Single test cases → use `/adk-quality-evals`
>
> **Prerequisites:** `/adk-quality-evals` completed
```

---

### Task 40: Update adk-advanced-visual-builder.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Use visual builder for drag-and-drop agent creation
triggers:
  - visual builder
  - ui builder
  - drag
  - visual
  - no-code builder
category: advanced
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/"
    type: directory
context_required:
  - builder_platform
completion_criteria:
  - "Agent created via visual builder"
  - "Code exported successfully"
  - "Agent runs locally"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User prefers visual/no-code interfaces
> - User mentions "visual builder", "drag and drop", "UI"
> - Prototyping agents quickly
>
> **Do NOT use when:**
> - User comfortable with code → use `/adk-agents-create`
> - User needs YAML config → use `/adk-init-yaml-config`
>
> **Prerequisites:** Understanding of `/adk-agents-create` concepts
```

---

### Task 41: Update adk-advanced-thinking.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Configure extended thinking and planning capabilities
triggers:
  - thinking
  - planner
  - thinkingconfig
  - reasoning
  - chain of thought
category: advanced
dependencies:
  - adk-agents-create
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - thinking_mode
completion_criteria:
  - "ThinkingConfig configured"
  - "Extended reasoning visible"
  - "Agent shows thinking steps"
estimated_steps: 4
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants visible reasoning/thinking
> - User mentions "thinking", "reasoning", "chain of thought"
> - Building agents that explain their logic
>
> **Do NOT use when:**
> - User wants fast responses → standard agent
> - User needs custom planning → use `/adk-agents-custom`
>
> **Prerequisites:** `/adk-agents-create` completed
```

---

### Task 42: Update adk-master.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Master routing workflow that directs to all ADK workflows
triggers:
  - help
  - adk
  - what workflow
  - which workflow
  - guide me
category: meta
dependencies: []
outputs: []
context_required:
  - user_goal
completion_criteria:
  - "User routed to correct workflow"
  - "Dependency chain identified"
estimated_steps: 2
difficulty: beginner
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User needs help choosing a workflow
> - User asks "which workflow", "what should I use"
> - General ADK questions without specific task
>
> **Do NOT use when:**
> - User has specific task → route to that workflow
> - User explicitly names a workflow
>
> **Prerequisites:** None
```

---

### Task 43: Update adk-create-workflow.md

**Step 2: Add complete frontmatter**

```yaml
---
description: Template and guidelines for creating new ADK workflows
triggers:
  - create workflow
  - new workflow
  - workflow template
  - add workflow
category: meta
dependencies: []
outputs:
  - path: ".agent/workflows/adk-{name}.md"
    type: file
context_required:
  - workflow_name
  - workflow_purpose
completion_criteria:
  - "New workflow file created"
  - "Frontmatter complete"
  - "Validation passes"
estimated_steps: 5
difficulty: intermediate
---
```

**Step 3: Add Agent Decision Logic**

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants to create a new workflow
> - User mentions "workflow template", "add workflow"
> - Extending the workflow library
>
> **Do NOT use when:**
> - User wants to use existing workflow → route there
> - User wants to modify existing workflow
>
> **Prerequisites:** Understanding of workflow structure
```

---

## Final Validation

After all 43 tasks complete:

**Step 1: Run full validation**

```bash
python .agent/scripts/validate_workflows.py --verbose
```

Expected: 0 errors, minimal warnings (only code block language specifiers)

**Step 2: Update manifest**

```bash
# Regenerate manifest if needed based on new frontmatter
python -c "
import json
from pathlib import Path
import yaml

manifest_path = Path('.agent/workflows/_manifest.json')
manifest = json.loads(manifest_path.read_text())

# Update workflow_metadata from actual frontmatter
for wf_file in Path('.agent/workflows').glob('adk-*.md'):
    name = wf_file.stem
    content = wf_file.read_text()
    if content.startswith('---'):
        fm_end = content.index('---', 3)
        fm = yaml.safe_load(content[3:fm_end])
        if name not in manifest['workflow_metadata']:
            manifest['workflow_metadata'][name] = {}
        if 'difficulty' in fm:
            manifest['workflow_metadata'][name]['difficulty'] = fm['difficulty']
        if 'estimated_steps' in fm:
            manifest['workflow_metadata'][name]['estimated_steps'] = fm['estimated_steps']
        if 'outputs' in fm:
            manifest['workflow_metadata'][name]['produces'] = [o.get('path', '') for o in fm['outputs']]

manifest_path.write_text(json.dumps(manifest, indent=2))
print('Manifest updated')
"
```

**Step 3: Commit all changes**

```bash
git add .agent/workflows/
git commit -m "feat(workflows): add agent-optimized frontmatter to all 43 workflows

- Add complete YAML frontmatter with triggers, dependencies, outputs
- Add Agent Decision Logic sections for routing
- Add language specifiers to code blocks
- Update manifest with workflow metadata"
```

**Step 4: Push to remote**

```bash
git push origin main
```

---

## Summary

| Metric | Count |
|--------|-------|
| Total workflows | 43 |
| Already complete | 1 (adk-agents-create.md) |
| To update | 42 |
| Tasks in plan | 43 (including validation) |

Each task follows the same pattern:
1. Read current file
2. Replace/add frontmatter
3. Add Agent Decision Logic section
4. Add language specifiers to code blocks
5. Verify with validation script
6. Commit

Estimated total: ~2-3 hours with subagent execution
