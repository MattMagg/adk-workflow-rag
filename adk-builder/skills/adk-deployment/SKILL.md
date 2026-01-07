---
name: ADK Deployment
description: This skill should be used when the user asks about "deploying", "production", "Agent Engine", "Vertex AI", "Cloud Run", "GKE", "Kubernetes", "hosting", "scaling", or needs guidance on deploying ADK agents to production environments.
version: 1.0.0
---

# ADK Deployment

Guide for deploying ADK agents to production.

## Deployment Options

| Platform | Best For | Complexity |
|----------|----------|------------|
| **Agent Engine** | Managed hosting, integrated services | Recommended |
| **Cloud Run** | Container control, serverless | Intermediate |
| **GKE** | Kubernetes, enterprise scale | Advanced |

## Agent Engine (Recommended)

Fully managed deployment with integrated Vertex AI services:

```bash
# Deploy to Agent Engine
adk deploy --project=my-project --region=us-central1

# Or via Python
from google.adk.deploy import deploy_to_agent_engine

deploy_to_agent_engine(
    agent=root_agent,
    project_id="my-project",
    location="us-central1",
)
```

### Benefits
- Auto-scaling
- Built-in session management
- Integrated with Vertex AI Search, Memory
- No infrastructure management

## Cloud Run

For more container control:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install google-adk
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8080"]
```

```bash
gcloud run deploy my-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## Decision Guide

| If you need... | Use |
|----------------|-----|
| Simplest deployment | Agent Engine |
| Custom container | Cloud Run |
| Kubernetes control | GKE |
| Integrated Vertex services | Agent Engine |

## References

For detailed guides:
- `references/agent-engine.md` - Vertex AI Agent Engine
- `references/cloudrun.md` - Cloud Run deployment
- `references/gke.md` - Kubernetes deployment
