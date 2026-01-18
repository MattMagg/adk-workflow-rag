---
description: Add new corpus/corpora to the RAG database end-to-end
---

# Add Corpora Workflow

Add a new SDK or documentation source to the RAG pipeline with proper configuration, ingestion, and documentation updates.

---

## Overview

Each SDK typically requires TWO corpora:

| Corpus Type | Embedding Model | Purpose |
|-------------|-----------------|---------|
| `{sdk}_docs` | `voyage-context-3` | Documentation |
| `{sdk}_python` | `voyage-code-3` | Source code |

The `kind` field in configuration determines which embedding model is used.

---

## Step 1: Add Repository as Git Submodule

```bash
git submodule add https://github.com/{org}/{repo}.git corpora/{directory-name}
```

This creates an entry in `.gitmodules` and allows users to fetch all corpora with:
```bash
git submodule update --init --recursive
```

---

## Step 2: Update `config/settings.yaml`

**Location:** Find `ingestion:` → `corpora:`. Add at END of existing list.

### Docs Corpus

```yaml
    # =========================================================================
    # {SDK Display Name}
    # =========================================================================

    {sdk}_docs:
      root: "corpora/{directory-name}"
      corpus: "{sdk}_docs"
      repo: "{org}/{repo}"
      kind: "doc"
      ref: "main"
      include_globs:
        - "README.md"
        - "docs/**/*.md"
      exclude_globs:
        - "**/.git/**"
      allowed_exts: [".md", ".mdx"]
      max_file_bytes: 500000
```

### Code Corpus

```yaml
    {sdk}_python:
      root: "corpora/{directory-name}"
      corpus: "{sdk}_python"
      repo: "{org}/{repo}"
      kind: "code"
      ref: "main"
      include_globs:
        - "src/**/*.py"
        - "examples/**/*.py"
      exclude_globs:
        - "**/.git/**"
        - "**/tests/**"
      allowed_exts: [".py", ".toml"]
      max_file_bytes: 500000
```

**Customize `include_globs`** based on actual repository structure.

---

## Step 3: Update `src/grounding/contracts/chunk.py`

**Find:** `SourceCorpus = Literal[...]` (~lines 20-35)

**Add** at end before `]`:

```python
    # {SDK Display Name}
    "{sdk}_docs",
    "{sdk}_python",
```

---

## Step 4: Update `src/grounding/query/query.py`

### Find `CORPUS_GROUPS` (~line 119)

Add before closing `}`:

```python
    "{sdk}": ["{sdk}_docs", "{sdk}_python"],
```

### Find `ALL_CORPORA` (~line 138)

Add at end before `]`:

```python
    "{sdk}_docs",
    "{sdk}_python",
```

---

## Step 5: Update Documentation

### Files to update:

| File | What to add |
|------|-------------|
| `README.md` | Query example, SDK table row, stats, project structure |
| `GEMINI.md` | Query example, SDK table row |
| `CLAUDE.md` | SDK ecosystem bullet, query example |
| `AGENTS.md` | Query example, SDK list |
| `docs/rag-query.md` | Query example, SDK table row, corpora table rows |

**Pattern:** Search for existing `--sdk` examples and add yours in the same format.

---

## Step 6: Verify and Ingest

```bash
# Verify config
python -m src.grounding.scripts.01_print_effective_config | grep -A 10 "{sdk}"

# Update schema
python -m src.grounding.scripts.02_ensure_collection_schema

# Ingest
python -m src.grounding.scripts.03_ingest_corpus --corpus {sdk}_docs
python -m src.grounding.scripts.03_ingest_corpus --corpus {sdk}_python

# Test
python -m src.grounding.query.query "test query" --sdk {sdk} --verbose
```

---

## Step 7: Commit

```bash
git add \
  .gitmodules \
  corpora/{directory-name} \
  config/settings.yaml \
  src/grounding/contracts/chunk.py \
  src/grounding/query/query.py \
  README.md GEMINI.md CLAUDE.md AGENTS.md docs/rag-query.md

git commit -m "feat(corpora): add {SDK Display Name}

- Added {org}/{repo} as git submodule
- Created {sdk}_docs and {sdk}_python corpus configs
- New SDK flag: --sdk {sdk}"

git push origin main
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Config fails | Check YAML indentation (2 spaces) |
| Zero files | Adjust `include_globs` |
| 502 error | Retry (idempotent) |
| Empty query | Verify corpus names match in all 3 files |
