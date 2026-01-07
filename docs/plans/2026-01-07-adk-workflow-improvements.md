# ADK Workflow Improvements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform ADK workflows from human-oriented documentation into agent-optimized execution guides with machine-readable metadata, standardized structure, validation, and clear decision logic.

**Architecture:** Add structured YAML frontmatter with agent-oriented metadata (triggers, dependencies, outputs), create a centralized manifest for workflow discovery, standardize all sections, add agent decision logic, and implement validation tooling.

**Tech Stack:** Markdown, YAML frontmatter, Python (validation scripts), JSON Schema

---

## Current State Analysis

### Inventory
- **Total workflows:** 44 files
- **Total lines:** ~13,391
- **Categories:** init (3), agents (3), tools (7), behavior (6), multi-agent (4), memory (2), security (3), streaming (3), deploy (3), quality (5), advanced (2), meta (2), other (1)

### Strengths Identified
1. Good domain categorization (adk-{category}-{feature})
2. Consistent YAML frontmatter with `description`
3. Most workflows have prerequisites, steps, code examples, troubleshooting
4. Good code examples with syntax highlighting
5. Reference sections linking to documentation

### Issues Identified for Agent Optimization

| Category | Issue | Impact on Agent |
|----------|-------|-----------------|
| Metadata | No triggers/keywords in frontmatter | Agent can't auto-select workflows |
| Metadata | No dependencies declared | Agent doesn't know prerequisite workflows |
| Metadata | No outputs specified | Agent can't verify completion |
| Structure | Inconsistent sections | Agent can't reliably parse workflows |
| Logic | No decision criteria | Agent guesses when to use workflow |
| Validation | No schema/validation | Agent may execute invalid workflows |
| References | Missing workflows (adk-dev-system) | Agent hits dead ends |
| References | Non-ADK file (rag-query.md) | Confuses workflow selection |

---

## Task 1: Define Agent-Optimized Frontmatter Schema

**Files:**
- Create: `.agent/workflows/_schema.yaml`

**Step 1: Write the schema definition**

```yaml
# .agent/workflows/_schema.yaml
# Schema for ADK workflow frontmatter (agent-optimized)

required:
  - description
  - triggers
  - category

optional:
  - dependencies
  - outputs
  - context_required
  - completion_criteria
  - estimated_steps
  - difficulty

field_definitions:
  description:
    type: string
    max_length: 200
    purpose: "One-line summary for agent routing"

  triggers:
    type: array
    items: string
    purpose: "Keywords/phrases that should route to this workflow"
    examples:
      - "create agent"
      - "LlmAgent"
      - "new agent"

  category:
    type: string
    enum: [init, agents, tools, behavior, multi-agent, memory, security, streaming, deploy, quality, advanced, meta]
    purpose: "Primary category for organization"

  dependencies:
    type: array
    items: string
    purpose: "Workflows that must be completed first"
    examples:
      - "adk-init"
      - "adk-agents-create"

  outputs:
    type: array
    items: object
    purpose: "Files/artifacts produced by this workflow"
    item_schema:
      path: string  # e.g., "{agent_name}/agent.py"
      type: enum [file, directory, config, code_block]

  context_required:
    type: array
    items: string
    purpose: "Information agent must gather before starting"
    examples:
      - "agent_name"
      - "model_choice"
      - "project_directory"

  completion_criteria:
    type: array
    items: string
    purpose: "Checkable conditions that indicate successful completion"
    examples:
      - "adk run {agent_name} executes without errors"
      - "root_agent variable is defined"

  estimated_steps:
    type: integer
    purpose: "Number of major steps in workflow"

  difficulty:
    type: string
    enum: [beginner, intermediate, advanced]
    purpose: "Complexity level for agent prioritization"
```

**Step 2: Commit**

```bash
git add .agent/workflows/_schema.yaml
git commit -m "feat(workflows): add agent-optimized frontmatter schema"
```

---

## Task 2: Create Workflow Manifest

**Files:**
- Create: `.agent/workflows/_manifest.json`

**Step 1: Write the manifest structure**

```json
{
  "version": "1.0.0",
  "generated": "2026-01-07",
  "total_workflows": 43,
  "categories": {
    "init": {
      "description": "Project initialization and setup",
      "entry_point": "adk-init",
      "workflows": ["adk-init", "adk-init-create-project", "adk-init-yaml-config"]
    },
    "agents": {
      "description": "Agent creation and configuration",
      "entry_point": "adk-agents-create",
      "workflows": ["adk-agents-create", "adk-agents-custom", "adk-agents-multi-model"]
    },
    "tools": {
      "description": "Tool creation and integration",
      "entry_point": "adk-tools-function",
      "workflows": ["adk-tools-function", "adk-tools-long-running", "adk-tools-builtin", "adk-tools-openapi", "adk-tools-mcp", "adk-tools-third-party", "adk-tools-computer-use"]
    },
    "behavior": {
      "description": "Agent behavior customization",
      "entry_point": "adk-behavior-callbacks",
      "workflows": ["adk-behavior-callbacks", "adk-behavior-plugins", "adk-behavior-state", "adk-behavior-artifacts", "adk-behavior-events", "adk-behavior-confirmation"]
    },
    "multi-agent": {
      "description": "Multi-agent systems and orchestration",
      "entry_point": "adk-multi-agent-delegation",
      "workflows": ["adk-multi-agent-delegation", "adk-multi-agent-orchestration", "adk-multi-agent-advanced", "adk-multi-agent-a2a"]
    },
    "memory": {
      "description": "Memory and grounding services",
      "entry_point": "adk-memory-service",
      "workflows": ["adk-memory-service", "adk-memory-grounding"]
    },
    "security": {
      "description": "Security, authentication, and guardrails",
      "entry_point": "adk-security-guardrails",
      "workflows": ["adk-security-guardrails", "adk-security-auth", "adk-security-plugins"]
    },
    "streaming": {
      "description": "Streaming and real-time communication",
      "entry_point": "adk-streaming-sse",
      "workflows": ["adk-streaming-sse", "adk-streaming-bidi", "adk-streaming-multimodal"]
    },
    "deploy": {
      "description": "Deployment to production environments",
      "entry_point": "adk-deploy-agent-engine",
      "workflows": ["adk-deploy-agent-engine", "adk-deploy-cloudrun", "adk-deploy-gke"]
    },
    "quality": {
      "description": "Testing, evaluation, and observability",
      "entry_point": "adk-quality-evals",
      "workflows": ["adk-quality-tracing", "adk-quality-logging", "adk-quality-observability", "adk-quality-evals", "adk-quality-user-sim"]
    },
    "advanced": {
      "description": "Advanced features and patterns",
      "entry_point": "adk-advanced-thinking",
      "workflows": ["adk-advanced-visual-builder", "adk-advanced-thinking"]
    }
  },
  "dependency_graph": {
    "adk-agents-create": ["adk-init"],
    "adk-agents-custom": ["adk-init", "adk-agents-create"],
    "adk-agents-multi-model": ["adk-agents-create"],
    "adk-tools-function": ["adk-agents-create"],
    "adk-tools-long-running": ["adk-tools-function"],
    "adk-tools-builtin": ["adk-agents-create"],
    "adk-tools-openapi": ["adk-agents-create"],
    "adk-tools-mcp": ["adk-agents-create"],
    "adk-tools-third-party": ["adk-agents-create"],
    "adk-tools-computer-use": ["adk-agents-create"],
    "adk-behavior-callbacks": ["adk-agents-create"],
    "adk-behavior-plugins": ["adk-behavior-callbacks"],
    "adk-behavior-state": ["adk-agents-create"],
    "adk-behavior-artifacts": ["adk-agents-create"],
    "adk-behavior-events": ["adk-agents-create"],
    "adk-behavior-confirmation": ["adk-agents-create", "adk-tools-function"],
    "adk-multi-agent-delegation": ["adk-agents-create"],
    "adk-multi-agent-orchestration": ["adk-multi-agent-delegation"],
    "adk-multi-agent-advanced": ["adk-multi-agent-delegation"],
    "adk-multi-agent-a2a": ["adk-multi-agent-delegation"],
    "adk-memory-service": ["adk-agents-create"],
    "adk-memory-grounding": ["adk-agents-create"],
    "adk-security-guardrails": ["adk-agents-create", "adk-behavior-callbacks"],
    "adk-security-auth": ["adk-agents-create"],
    "adk-security-plugins": ["adk-security-guardrails"],
    "adk-streaming-sse": ["adk-agents-create"],
    "adk-streaming-bidi": ["adk-streaming-sse"],
    "adk-streaming-multimodal": ["adk-streaming-bidi"],
    "adk-deploy-agent-engine": ["adk-agents-create"],
    "adk-deploy-cloudrun": ["adk-agents-create"],
    "adk-deploy-gke": ["adk-agents-create"],
    "adk-quality-tracing": ["adk-agents-create"],
    "adk-quality-logging": ["adk-agents-create"],
    "adk-quality-observability": ["adk-quality-logging"],
    "adk-quality-evals": ["adk-agents-create"],
    "adk-quality-user-sim": ["adk-quality-evals"],
    "adk-advanced-visual-builder": ["adk-agents-create"],
    "adk-advanced-thinking": ["adk-agents-create"]
  },
  "routing_keywords": {
    "init|create|new project|scaffold|start|bootstrap": "adk-init",
    "agent|llmagent|create agent": "adk-agents-create",
    "custom agent|baseagent|extend": "adk-agents-custom",
    "multi-model|litellm|claude|anthropic|openai": "adk-agents-multi-model",
    "tool|function|functiontool": "adk-tools-function",
    "long-running|async tool|background": "adk-tools-long-running",
    "builtin|google_search|code_execution": "adk-tools-builtin",
    "openapi|rest api|spec|swagger": "adk-tools-openapi",
    "mcp|model context protocol": "adk-tools-mcp",
    "langchain|crewai|third-party": "adk-tools-third-party",
    "computer|browser|desktop": "adk-tools-computer-use",
    "callback|before_|after_": "adk-behavior-callbacks",
    "plugin|reusable|modular": "adk-behavior-plugins",
    "state|session|persist": "adk-behavior-state",
    "artifact|file|binary|upload": "adk-behavior-artifacts",
    "event|eventactions|stream": "adk-behavior-events",
    "confirmation|approve|human-in-loop": "adk-behavior-confirmation",
    "sub-agent|delegation|transfer": "adk-multi-agent-delegation",
    "sequential|parallel|loop|workflow": "adk-multi-agent-orchestration",
    "hierarchy|compose|advanced multi": "adk-multi-agent-advanced",
    "a2a|interop|agent-to-agent": "adk-multi-agent-a2a",
    "memory|memoryservice|long-term": "adk-memory-service",
    "grounding|search|rag|retrieval": "adk-memory-grounding",
    "guardrail|safety|filter|block": "adk-security-guardrails",
    "auth|oauth|credential|token": "adk-security-auth",
    "security plugin|policy|enforcement": "adk-security-plugins",
    "stream|sse|server-sent": "adk-streaming-sse",
    "bidi|websocket|live|realtime": "adk-streaming-bidi",
    "audio|video|voice|multimodal stream": "adk-streaming-multimodal",
    "deploy|production|vertex": "adk-deploy-agent-engine",
    "cloud run|cloudrun|serverless": "adk-deploy-cloudrun",
    "gke|kubernetes|k8s": "adk-deploy-gke",
    "trace|cloud trace|tracing": "adk-quality-tracing",
    "log|logging|loggingplugin": "adk-quality-logging",
    "observability|agentops|langsmith": "adk-quality-observability",
    "eval|test|evaluate|benchmark": "adk-quality-evals",
    "user sim|simulation|synthetic": "adk-quality-user-sim",
    "visual builder|ui builder|drag": "adk-advanced-visual-builder",
    "thinking|planner|thinkingconfig": "adk-advanced-thinking"
  }
}
```

**Step 2: Commit**

```bash
git add .agent/workflows/_manifest.json
git commit -m "feat(workflows): add workflow manifest with dependency graph and routing"
```

---

## Task 3: Update Frontmatter for All Workflows (Template)

**Files:**
- Modify: All 43 ADK workflow files

**Step 1: Define the enhanced frontmatter template**

```yaml
---
description: [existing description]
triggers:
  - [keyword1]
  - [keyword2]
category: [category]
dependencies:
  - [workflow-name]  # or empty array []
outputs:
  - path: "{agent_name}/agent.py"
    type: file
context_required:
  - agent_name
  - model_choice
completion_criteria:
  - "adk run {agent_name} executes without errors"
estimated_steps: [N]
difficulty: [beginner|intermediate|advanced]
---
```

**Step 2: Apply to adk-agents-create.md (example)**

Update frontmatter in `.agent/workflows/adk-agents-create.md`:

```yaml
---
description: Create LlmAgent with model, name, instructions, and optional configuration
triggers:
  - create agent
  - new agent
  - LlmAgent
  - agent setup
category: agents
dependencies:
  - adk-init
outputs:
  - path: "{agent_name}/agent.py"
    type: file
  - path: "{agent_name}/__init__.py"
    type: file
context_required:
  - agent_name
  - agent_purpose
  - model_choice
completion_criteria:
  - "agent.py contains root_agent = LlmAgent(...)"
  - "adk run {agent_name} executes without errors"
estimated_steps: 5
difficulty: beginner
---
```

**Step 3: Repeat for remaining 42 workflows**

Each workflow needs frontmatter updated with triggers, dependencies, outputs, context_required, and completion_criteria specific to that workflow.

**Step 4: Commit**

```bash
git add .agent/workflows/*.md
git commit -m "feat(workflows): add agent-optimized frontmatter to all workflows"
```

---

## Task 4: Standardize Section Structure

**Files:**
- Modify: All 43 ADK workflow files

**Step 1: Define standard section order**

Every workflow MUST have these sections in this order:

```markdown
---
[frontmatter]
---

# ADK Workflow: [Title]

[One-paragraph scope/purpose statement]

---

## Agent Decision Logic

> **Use this workflow when:** [conditions]
> **Do NOT use when:** [anti-conditions]
> **Prerequisites:** [list prior workflows]

---

## Prerequisites

- [ ] [Checklist item with checkbox]
- [ ] [Required import or setup]

---

## Step N: [Action Title]

[Explanation]

```python
# Code example
```

---

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|

---

## Integration Points

- **With [X]:** [How it integrates]

---

## Verification

```bash
# Verification command
```

**Expected behavior:**
- [Bullet point]

### Completion Checklist

- [ ] [Verifiable completion criterion]

---

## Error Recovery

| Error | Cause | Recovery Action |
|-------|-------|-----------------|

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|

---

## Next Workflows

After completing this workflow:
- `/adk-next-workflow` — [description]

---

## References

- [Reference title](URL or path)
```

**Step 2: Add "Agent Decision Logic" section to adk-agents-create.md**

Insert after title, before Prerequisites:

```markdown
## Agent Decision Logic

> **Use this workflow when:**
> - User wants to create a new LLM-powered agent
> - User mentions "agent", "LlmAgent", or wants AI reasoning capabilities
> - Building the core "thinking" component of an agentic system
>
> **Do NOT use when:**
> - User needs a custom agent with non-LLM logic → use `/adk-agents-custom`
> - User wants to configure an existing agent's model → use `/adk-agents-multi-model`
> - User needs workflow orchestration without LLM → use `/adk-multi-agent-orchestration`
>
> **Prerequisites:** `/adk-init` must be completed (project structure exists)
```

**Step 3: Add "Error Recovery" section template**

```markdown
## Error Recovery

| Error | Cause | Recovery Action |
|-------|-------|-----------------|
| `ModuleNotFoundError: google.adk` | ADK not installed | Run `pip install google-adk` |
| `ValueError: name 'user' is reserved` | Used reserved agent name | Change `name` parameter |
| `429 RESOURCE_EXHAUSTED` | API quota exceeded | Wait and retry, or request quota increase |
| Agent not appearing in `adk web` | `root_agent` not defined | Ensure agent is assigned to `root_agent` variable |
```

**Step 4: Add "Next Workflows" section**

```markdown
## Next Workflows

After completing this workflow:
- `/adk-tools-function` — Add custom tools to your agent
- `/adk-behavior-state` — Configure session state management
- `/adk-behavior-callbacks` — Add lifecycle callbacks
- `/adk-multi-agent-delegation` — Create sub-agents for delegation
```

**Step 5: Apply standardization to all 43 workflows**

**Step 6: Commit**

```bash
git add .agent/workflows/*.md
git commit -m "feat(workflows): standardize section structure for agent parsing"
```

---

## Task 5: Fix References and Remove Invalid Workflows

**Files:**
- Modify: `.agent/workflows/adk-master.md`
- Delete: `.agent/workflows/rag-query.md` (not an ADK workflow)

**Step 1: Remove reference to non-existent adk-dev-system**

In `adk-master.md`, remove:
```
software dev, e2e            → adk-dev-system
```

And remove from Reference section:
```
| `adk-dev-system` | Multi-agent hierarchical development system |
```

**Step 2: Move rag-query.md out of workflows**

```bash
mkdir -p .agent/tools
mv .agent/workflows/rag-query.md .agent/tools/rag-query.md
```

**Step 3: Update adk-master.md workflow count**

Change "37 Total" to accurate count based on actual files.

**Step 4: Commit**

```bash
git add .agent/workflows/adk-master.md
git add .agent/tools/rag-query.md
git rm .agent/workflows/rag-query.md
git commit -m "fix(workflows): remove invalid references and relocate non-workflow file"
```

---

## Task 6: Create Workflow Validation Script

**Files:**
- Create: `.agent/scripts/validate_workflows.py`

**Step 1: Write the validation script**

```python
#!/usr/bin/env python3
"""
Validate ADK workflow files for schema compliance and consistency.

Usage:
    python .agent/scripts/validate_workflows.py
    python .agent/scripts/validate_workflows.py --fix  # Auto-fix minor issues
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
MANIFEST_PATH = WORKFLOWS_DIR / "_manifest.json"
SCHEMA_PATH = WORKFLOWS_DIR / "_schema.yaml"

REQUIRED_SECTIONS = [
    "Agent Decision Logic",
    "Prerequisites",
    "Verification",
    "Troubleshooting",
    "References",
]

REQUIRED_FRONTMATTER = ["description", "triggers", "category"]


def load_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def validate_frontmatter(path: Path, frontmatter: dict) -> list[str]:
    """Validate frontmatter against schema."""
    errors = []
    for field in REQUIRED_FRONTMATTER:
        if field not in frontmatter:
            errors.append(f"{path.name}: Missing required frontmatter field '{field}'")

    if "category" in frontmatter:
        valid_categories = [
            "init", "agents", "tools", "behavior", "multi-agent",
            "memory", "security", "streaming", "deploy", "quality", "advanced", "meta"
        ]
        if frontmatter["category"] not in valid_categories:
            errors.append(f"{path.name}: Invalid category '{frontmatter['category']}'")

    if "triggers" in frontmatter and not isinstance(frontmatter["triggers"], list):
        errors.append(f"{path.name}: 'triggers' must be a list")

    return errors


def validate_sections(path: Path, content: str) -> list[str]:
    """Validate required sections exist."""
    errors = []
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in content:
            errors.append(f"{path.name}: Missing required section '## {section}'")
    return errors


def validate_code_blocks(path: Path, content: str) -> list[str]:
    """Validate code blocks have language specifiers."""
    errors = []
    code_blocks = re.findall(r'```(\w*)\n', content)
    unnamed_count = sum(1 for lang in code_blocks if not lang)
    if unnamed_count > 0:
        errors.append(f"{path.name}: {unnamed_count} code blocks without language specifier")
    return errors


def validate_manifest_consistency(manifest: dict, workflow_files: list[Path]) -> list[str]:
    """Validate manifest matches actual workflow files."""
    errors = []

    manifest_workflows = set()
    for category in manifest.get("categories", {}).values():
        manifest_workflows.update(category.get("workflows", []))

    actual_workflows = {p.stem for p in workflow_files if not p.name.startswith("_")}

    missing_from_manifest = actual_workflows - manifest_workflows
    missing_files = manifest_workflows - actual_workflows

    for wf in missing_from_manifest:
        errors.append(f"Manifest missing workflow: {wf}")
    for wf in missing_files:
        errors.append(f"Manifest references non-existent workflow: {wf}")

    return errors


def main():
    all_errors = []

    # Get all workflow files
    workflow_files = list(WORKFLOWS_DIR.glob("*.md"))
    workflow_files = [f for f in workflow_files if not f.name.startswith("_")]

    print(f"Validating {len(workflow_files)} workflow files...")

    for path in workflow_files:
        content = path.read_text()
        frontmatter = load_frontmatter(content)

        all_errors.extend(validate_frontmatter(path, frontmatter))
        all_errors.extend(validate_sections(path, content))
        all_errors.extend(validate_code_blocks(path, content))

    # Validate manifest
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text())
        all_errors.extend(validate_manifest_consistency(manifest, workflow_files))
    else:
        all_errors.append("_manifest.json not found")

    # Report results
    if all_errors:
        print(f"\n❌ Found {len(all_errors)} issues:\n")
        for error in sorted(all_errors):
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ All workflows valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
git add .agent/scripts/validate_workflows.py
git commit -m "feat(workflows): add validation script for workflow schema compliance"
```

---

## Task 7: Create Workflow Selection Helper

**Files:**
- Create: `.agent/scripts/select_workflow.py`

**Step 1: Write the selection helper**

```python
#!/usr/bin/env python3
"""
Help agents select the appropriate workflow based on user intent.

Usage:
    python .agent/scripts/select_workflow.py "user query here"
"""

import json
import re
import sys
from pathlib import Path


MANIFEST_PATH = Path(__file__).parent.parent / "workflows" / "_manifest.json"


def load_manifest() -> dict:
    """Load the workflow manifest."""
    return json.loads(MANIFEST_PATH.read_text())


def match_workflow(query: str, manifest: dict) -> list[tuple[str, float]]:
    """Match query to workflows with confidence scores."""
    query_lower = query.lower()
    matches = []

    routing = manifest.get("routing_keywords", {})

    for pattern, workflow in routing.items():
        keywords = pattern.split("|")
        score = 0
        for kw in keywords:
            if kw in query_lower:
                # Exact word match scores higher
                if re.search(rf'\b{re.escape(kw)}\b', query_lower):
                    score += 2
                else:
                    score += 1

        if score > 0:
            matches.append((workflow, score / len(keywords)))

    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:5]  # Top 5


def get_dependencies(workflow: str, manifest: dict) -> list[str]:
    """Get ordered list of dependencies for a workflow."""
    deps = manifest.get("dependency_graph", {}).get(workflow, [])
    all_deps = []

    for dep in deps:
        # Recursively get dependencies
        sub_deps = get_dependencies(dep, manifest)
        for sd in sub_deps:
            if sd not in all_deps:
                all_deps.append(sd)
        if dep not in all_deps:
            all_deps.append(dep)

    return all_deps


def main():
    if len(sys.argv) < 2:
        print("Usage: python select_workflow.py 'user query'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    manifest = load_manifest()

    matches = match_workflow(query, manifest)

    if not matches:
        print("No matching workflows found. Try /adk-master for guidance.")
        sys.exit(0)

    print(f"Query: {query}\n")
    print("Recommended workflows:")

    for workflow, score in matches:
        deps = get_dependencies(workflow, manifest)
        deps_str = " → ".join(deps + [workflow]) if deps else workflow
        print(f"  [{score:.2f}] {deps_str}")

    print(f"\nPrimary recommendation: /adk-{matches[0][0].replace('adk-', '')}")


if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
git add .agent/scripts/select_workflow.py
git commit -m "feat(workflows): add workflow selection helper for agent routing"
```

---

## Task 8: Update adk-master.md with Agent Routing Logic

**Files:**
- Modify: `.agent/workflows/adk-master.md`

**Step 1: Add machine-parseable routing section**

Add after the frontmatter:

```markdown
## Agent Routing Protocol

When selecting a workflow:

1. **Parse user intent** - Extract keywords from the user's request
2. **Check manifest** - Load `_manifest.json` and match against `routing_keywords`
3. **Resolve dependencies** - Use `dependency_graph` to get prerequisite workflows
4. **Execute in order** - Run dependencies first, then target workflow

### Quick Selection Matrix

| User wants to... | Primary workflow | Dependencies |
|------------------|-----------------|--------------|
| Start new project | `adk-init` | None |
| Create an agent | `adk-agents-create` | `adk-init` |
| Add a tool | `adk-tools-function` | `adk-init → adk-agents-create` |
| Deploy to Cloud Run | `adk-deploy-cloudrun` | `adk-init → adk-agents-create` |
| Add guardrails | `adk-security-guardrails` | `adk-init → adk-agents-create → adk-behavior-callbacks` |

### Programmatic Selection

```bash
python .agent/scripts/select_workflow.py "add a function tool to my agent"
```
```

**Step 2: Commit**

```bash
git add .agent/workflows/adk-master.md
git commit -m "feat(workflows): add agent routing protocol to master workflow"
```

---

## Execution Summary

| Task | Files Changed | Purpose |
|------|---------------|---------|
| 1 | `_schema.yaml` | Define frontmatter schema |
| 2 | `_manifest.json` | Create workflow index with dependencies |
| 3 | All 43 workflows | Add agent-optimized frontmatter |
| 4 | All 43 workflows | Standardize sections |
| 5 | `adk-master.md`, `rag-query.md` | Fix invalid references |
| 6 | `validate_workflows.py` | Add validation tooling |
| 7 | `select_workflow.py` | Add selection helper |
| 8 | `adk-master.md` | Add routing protocol |

---

## Verification

After all tasks complete:

```bash
# Run validation
python .agent/scripts/validate_workflows.py

# Test selection
python .agent/scripts/select_workflow.py "create a new agent with tools"

# Verify workflow count
ls -la .agent/workflows/*.md | wc -l  # Should be 43

# Test a workflow
adk run test_agent  # After following adk-init + adk-agents-create
```

**Expected outcomes:**
- Validation passes with 0 errors
- Selection returns correct workflow chains
- All workflows have consistent structure
- Agent can programmatically parse and execute workflows
