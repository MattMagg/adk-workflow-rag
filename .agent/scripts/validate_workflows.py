#!/usr/bin/env python3
"""
Validate ADK workflow files for schema compliance and consistency.

Usage:
    python .agent/scripts/validate_workflows.py
    python .agent/scripts/validate_workflows.py --verbose
    python .agent/scripts/validate_workflows.py --fix  # Future: auto-fix minor issues

Validates:
- Required frontmatter fields (description, triggers, category)
- Required sections (Agent Decision Logic, Prerequisites, etc.)
- Code block language specifiers
- Manifest consistency with actual files
- Dependency graph validity
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
MANIFEST_PATH = WORKFLOWS_DIR / "_manifest.json"
SCHEMA_PATH = WORKFLOWS_DIR / "_schema.yaml"

# Current required fields (will expand as workflows are updated)
REQUIRED_FRONTMATTER = ["description"]

# Future required fields (after migration)
FUTURE_REQUIRED_FRONTMATTER = ["description", "triggers", "category"]

# Required sections for agent-optimized workflows
REQUIRED_SECTIONS = [
    "Prerequisites",
    "Verification",
    "Troubleshooting",
]

# Recommended sections (warnings only)
RECOMMENDED_SECTIONS = [
    "Agent Decision Logic",
    "References",
]

VALID_CATEGORIES = [
    "init", "agents", "tools", "behavior", "multi-agent",
    "memory", "security", "streaming", "deploy", "quality",
    "advanced", "meta"
]


def load_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    if not HAS_YAML:
        # Basic parsing without yaml library
        fm = {}
        for line in match.group(1).strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip()
        return fm

    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def validate_frontmatter(path: Path, frontmatter: dict, strict: bool = False) -> list[str]:
    """Validate frontmatter against schema."""
    errors = []
    warnings = []

    required = FUTURE_REQUIRED_FRONTMATTER if strict else REQUIRED_FRONTMATTER

    for field in required:
        if field not in frontmatter:
            if strict:
                errors.append(f"{path.name}: Missing required frontmatter field '{field}'")
            elif field in FUTURE_REQUIRED_FRONTMATTER:
                warnings.append(f"{path.name}: Missing recommended field '{field}' (will be required)")

    if "category" in frontmatter:
        if frontmatter["category"] not in VALID_CATEGORIES:
            errors.append(f"{path.name}: Invalid category '{frontmatter['category']}'")

    if "triggers" in frontmatter:
        if not isinstance(frontmatter["triggers"], list):
            errors.append(f"{path.name}: 'triggers' must be a list")
        elif len(frontmatter["triggers"]) == 0:
            warnings.append(f"{path.name}: 'triggers' is empty")

    if "dependencies" in frontmatter:
        if not isinstance(frontmatter["dependencies"], list):
            errors.append(f"{path.name}: 'dependencies' must be a list")

    if "estimated_steps" in frontmatter:
        if not isinstance(frontmatter["estimated_steps"], int):
            errors.append(f"{path.name}: 'estimated_steps' must be an integer")

    if "difficulty" in frontmatter:
        valid_difficulties = ["beginner", "intermediate", "advanced"]
        if frontmatter["difficulty"] not in valid_difficulties:
            errors.append(f"{path.name}: Invalid difficulty '{frontmatter['difficulty']}'")

    return errors, warnings


def validate_sections(path: Path, content: str) -> tuple[list[str], list[str]]:
    """Validate required and recommended sections exist."""
    errors = []
    warnings = []

    for section in REQUIRED_SECTIONS:
        # Check for section with ## or different heading levels
        pattern = rf'^##+ {re.escape(section)}'
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            errors.append(f"{path.name}: Missing required section '## {section}'")

    for section in RECOMMENDED_SECTIONS:
        pattern = rf'^##+ {re.escape(section)}'
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"{path.name}: Missing recommended section '## {section}'")

    return errors, warnings


def validate_code_blocks(path: Path, content: str) -> list[str]:
    """Validate code blocks have language specifiers."""
    warnings = []

    # Find all code blocks
    code_blocks = re.findall(r'```(\w*)\n', content)
    unnamed_count = sum(1 for lang in code_blocks if not lang)

    if unnamed_count > 0:
        warnings.append(f"{path.name}: {unnamed_count} code block(s) without language specifier")

    return warnings


def validate_internal_links(path: Path, content: str, all_workflows: set[str]) -> list[str]:
    """Validate internal workflow links point to existing workflows."""
    errors = []

    # Find /adk-* references
    links = re.findall(r'/adk-[\w-]+', content)

    for link in links:
        workflow_name = link[1:]  # Remove leading /
        if workflow_name not in all_workflows and workflow_name != "adk-*":
            # Check if it's a wildcard pattern
            if not workflow_name.endswith('-*'):
                errors.append(f"{path.name}: References non-existent workflow '{link}'")

    return errors


def validate_manifest_consistency(manifest: dict, workflow_files: list[Path]) -> list[str]:
    """Validate manifest matches actual workflow files."""
    errors = []

    # Collect all workflows from manifest categories
    manifest_workflows = set()
    for category in manifest.get("categories", {}).values():
        manifest_workflows.update(category.get("workflows", []))

    # Get actual workflow file names (excluding _ prefixed files)
    actual_workflows = {p.stem for p in workflow_files if not p.name.startswith("_")}

    missing_from_manifest = actual_workflows - manifest_workflows
    missing_files = manifest_workflows - actual_workflows

    for wf in missing_from_manifest:
        errors.append(f"Manifest missing workflow: {wf}")

    for wf in missing_files:
        errors.append(f"Manifest references non-existent workflow: {wf}")

    # Validate dependency graph references existing workflows
    dep_graph = manifest.get("dependency_graph", {})
    for workflow, deps in dep_graph.items():
        if workflow not in manifest_workflows:
            errors.append(f"Dependency graph contains unknown workflow: {workflow}")
        for dep in deps:
            if dep not in manifest_workflows:
                errors.append(f"Dependency '{dep}' for '{workflow}' doesn't exist")

    return errors


def validate_dependency_cycles(manifest: dict) -> list[str]:
    """Check for circular dependencies in the dependency graph."""
    errors = []
    dep_graph = manifest.get("dependency_graph", {})

    def has_cycle(node: str, visited: set, path: set) -> bool:
        visited.add(node)
        path.add(node)

        for dep in dep_graph.get(node, []):
            if dep not in visited:
                if has_cycle(dep, visited, path):
                    return True
            elif dep in path:
                errors.append(f"Circular dependency detected: {node} -> {dep}")
                return True

        path.remove(node)
        return False

    visited = set()
    for workflow in dep_graph:
        if workflow not in visited:
            has_cycle(workflow, visited, set())

    return errors


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    strict = "--strict" in sys.argv

    all_errors = []
    all_warnings = []

    # Get all workflow files (excluding _ prefixed meta files)
    workflow_files = list(WORKFLOWS_DIR.glob("*.md"))
    workflow_files = [f for f in workflow_files if not f.name.startswith("_")]
    all_workflow_names = {f.stem for f in workflow_files}

    print(f"Validating {len(workflow_files)} workflow files...")
    if verbose:
        print(f"  Directory: {WORKFLOWS_DIR}")
        print(f"  Strict mode: {strict}")
        print()

    # Validate each workflow file
    for path in sorted(workflow_files):
        content = path.read_text()
        frontmatter = load_frontmatter(content)

        fm_errors, fm_warnings = validate_frontmatter(path, frontmatter, strict)
        all_errors.extend(fm_errors)
        all_warnings.extend(fm_warnings)

        sec_errors, sec_warnings = validate_sections(path, content)
        all_errors.extend(sec_errors)
        all_warnings.extend(sec_warnings)

        all_warnings.extend(validate_code_blocks(path, content))
        all_errors.extend(validate_internal_links(path, content, all_workflow_names))

    # Validate manifest
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text())
            all_errors.extend(validate_manifest_consistency(manifest, workflow_files))
            all_errors.extend(validate_dependency_cycles(manifest))
            if verbose:
                print(f"Manifest validation: {len(manifest.get('categories', {}))} categories")
        except json.JSONDecodeError as e:
            all_errors.append(f"_manifest.json: Invalid JSON - {e}")
    else:
        all_warnings.append("_manifest.json not found (run workflow indexer to create)")

    # Report results
    print()

    if all_warnings and verbose:
        print(f"Warnings ({len(all_warnings)}):")
        for warning in sorted(all_warnings):
            print(f"  - {warning}")
        print()

    if all_errors:
        print(f"Errors ({len(all_errors)}):")
        for error in sorted(all_errors):
            print(f"  - {error}")
        print()
        print(f"Result: FAILED with {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print(f"Result: PASSED")
        if all_warnings:
            print(f"  ({len(all_warnings)} warnings - use --verbose to see)")
        sys.exit(0)


if __name__ == "__main__":
    main()
