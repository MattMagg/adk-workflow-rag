---
name: ADK Getting Started
description: This skill should be used when the user asks about "creating a new ADK project", "initializing ADK", "setting up Google ADK", "adk create command", "ADK project structure", "YAML agent configuration", or needs guidance on bootstrapping an ADK development environment, authentication setup, or choosing between Python code and YAML-based agent definitions.
version: 1.0.0
---

# ADK Getting Started

Guide for initializing and setting up Google Agent Development Kit (ADK) projects.

## Overview

ADK projects can be created in two ways:
1. **Python Code** (`adk create`) - Full flexibility, custom tools, advanced patterns
2. **YAML Config** - Quick setup, no-code agents, declarative definition

## Quick Start

### Prerequisites

- Python 3.10+ (3.11+ recommended)
- Virtual environment
- Google API key or GCP credentials

### Initialize Project

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install ADK
pip install google-adk

# Verify installation
adk --version

# Create new agent project
adk create my_agent
```

### Authentication Options

**Option A: Google AI Studio (Simplest)**
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=YOUR_API_KEY
```

**Option B: Vertex AI (Production)**
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
```

### Run Your Agent

```bash
# Interactive CLI
adk run my_agent

# Web UI (recommended for development)
adk web

# API server
adk api_server
```

## Project Structure

```
my_agent/
├── __init__.py      # Package marker
├── agent.py         # Agent definition (root_agent)
└── .env             # Authentication credentials
```

## Decision Guide

| If you need... | Use |
|----------------|-----|
| Custom Python tools | `adk create` (Python) |
| Quick prototyping | YAML config |
| Full control | Python code |
| No-code approach | YAML config |

## References

For detailed guides:
- `references/init.md` - Complete initialization workflow
- `references/create-project.md` - Python project scaffolding
- `references/yaml-config.md` - YAML-based configuration
