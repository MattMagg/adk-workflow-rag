#!/usr/bin/env python3
"""
Help agents select the appropriate workflow based on user intent.

Usage:
    python .agent/scripts/select_workflow.py "user query here"
    python .agent/scripts/select_workflow.py "create a new agent with tools" --verbose
    python .agent/scripts/select_workflow.py --list-categories

Examples:
    python .agent/scripts/select_workflow.py "add a function tool"
    python .agent/scripts/select_workflow.py "deploy to cloud run"
    python .agent/scripts/select_workflow.py "multi-agent system"
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional


MANIFEST_PATH = Path(__file__).parent.parent / "workflows" / "_manifest.json"


def load_manifest() -> dict:
    """Load the workflow manifest."""
    if not MANIFEST_PATH.exists():
        print(f"Error: Manifest not found at {MANIFEST_PATH}")
        print("Run the workflow indexer to create it.")
        sys.exit(1)
    return json.loads(MANIFEST_PATH.read_text())


def match_workflow(query: str, manifest: dict) -> list[tuple[str, float, list[str]]]:
    """
    Match query to workflows with confidence scores.

    Returns list of (workflow_name, score, matched_keywords)
    """
    query_lower = query.lower()
    matches = []

    routing = manifest.get("routing_keywords", {})

    for pattern, workflow in routing.items():
        keywords = pattern.split("|")
        matched = []
        score = 0

        for kw in keywords:
            kw_lower = kw.lower().strip()
            if kw_lower in query_lower:
                # Exact word boundary match scores higher
                if re.search(rf'\b{re.escape(kw_lower)}\b', query_lower):
                    score += 2
                    matched.append(kw)
                else:
                    score += 1
                    matched.append(f"~{kw}")  # Partial match

        if score > 0:
            # Normalize by pattern complexity
            normalized_score = score / (len(keywords) ** 0.5)
            matches.append((workflow, normalized_score, matched))

    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:5]  # Top 5


def get_dependencies(workflow: str, manifest: dict, visited: Optional[set] = None) -> list[str]:
    """
    Get ordered list of dependencies for a workflow (topologically sorted).
    """
    if visited is None:
        visited = set()

    if workflow in visited:
        return []  # Avoid cycles

    visited.add(workflow)
    deps = manifest.get("dependency_graph", {}).get(workflow, [])
    all_deps = []

    for dep in deps:
        # Recursively get dependencies of dependencies
        sub_deps = get_dependencies(dep, manifest, visited.copy())
        for sd in sub_deps:
            if sd not in all_deps:
                all_deps.append(sd)
        if dep not in all_deps:
            all_deps.append(dep)

    return all_deps


def get_category_info(workflow: str, manifest: dict) -> Optional[str]:
    """Get the category a workflow belongs to."""
    for cat_name, cat_info in manifest.get("categories", {}).items():
        if workflow in cat_info.get("workflows", []):
            return cat_name
    return None


def print_workflow_chain(workflow: str, deps: list[str], indent: int = 0) -> None:
    """Print workflow chain with visual formatting."""
    prefix = "  " * indent
    if deps:
        chain = " → ".join(deps + [workflow])
        print(f"{prefix}{chain}")
    else:
        print(f"{prefix}{workflow}")


def list_categories(manifest: dict) -> None:
    """List all workflow categories."""
    print("Available Workflow Categories:\n")
    for cat_name, cat_info in sorted(manifest.get("categories", {}).items()):
        desc = cat_info.get("description", "")
        entry = cat_info.get("entry_point", "")
        workflows = cat_info.get("workflows", [])
        print(f"  {cat_name}:")
        print(f"    Description: {desc}")
        print(f"    Entry point: {entry}")
        print(f"    Workflows: {', '.join(workflows)}")
        print()


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    manifest = load_manifest()

    if "--list-categories" in sys.argv:
        list_categories(manifest)
        sys.exit(0)

    if "--list-all" in sys.argv:
        print("All Workflows:\n")
        for cat_name, cat_info in sorted(manifest.get("categories", {}).items()):
            print(f"  [{cat_name}]")
            for wf in cat_info.get("workflows", []):
                deps = get_dependencies(wf, manifest)
                deps_str = f" (requires: {', '.join(deps)})" if deps else ""
                print(f"    - {wf}{deps_str}")
            print()
        sys.exit(0)

    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Get query from remaining args
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print("Usage: python select_workflow.py 'user query'")
        print("       python select_workflow.py --list-categories")
        print("       python select_workflow.py --list-all")
        sys.exit(1)

    query = " ".join(args)
    matches = match_workflow(query, manifest)

    print(f"Query: \"{query}\"\n")

    if not matches:
        print("No matching workflows found.")
        print("\nSuggestions:")
        print("  - Try /adk-master for general guidance")
        print("  - Use --list-categories to see available categories")
        print("  - Use --list-all to see all workflows")
        sys.exit(0)

    print("Matched Workflows:")
    print("-" * 50)

    for i, (workflow, score, matched_kws) in enumerate(matches):
        deps = get_dependencies(workflow, manifest)
        category = get_category_info(workflow, manifest)

        print(f"\n{i+1}. {workflow}")
        print(f"   Score: {score:.2f}")
        if category:
            print(f"   Category: {category}")
        if verbose and matched_kws:
            print(f"   Matched: {', '.join(matched_kws)}")
        if deps:
            print(f"   Prerequisites: {' → '.join(deps)}")
        print(f"   Full chain: {' → '.join(deps + [workflow])}")

    # Primary recommendation
    best = matches[0]
    deps = get_dependencies(best[0], manifest)

    print("\n" + "=" * 50)
    print("RECOMMENDATION:")
    print(f"  Primary: /{best[0]}")
    if deps:
        print(f"  Execute in order:")
        for i, d in enumerate(deps, 1):
            print(f"    {i}. /{d}")
        print(f"    {len(deps)+1}. /{best[0]}")


if __name__ == "__main__":
    main()
