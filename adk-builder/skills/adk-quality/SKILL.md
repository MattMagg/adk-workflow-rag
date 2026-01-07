---
name: ADK Quality
description: This skill should be used when the user asks about "testing agents", "evaluation", "evals", "benchmarks", "tracing", "Cloud Trace", "logging", "observability", "AgentOps", "LangSmith", "user simulation", or needs guidance on testing, debugging, monitoring, or evaluating ADK agent quality.
version: 1.0.0
---

# ADK Quality

Guide for testing, evaluating, and monitoring ADK agents.

## Quality Components

| Component | Purpose |
|-----------|---------|
| **Evals** | Test agent behavior against criteria |
| **Tracing** | Debug execution flow |
| **Logging** | Capture events and errors |
| **Observability** | Third-party monitoring (AgentOps, etc.) |
| **User Simulation** | Automated testing with synthetic users |

## Evaluations

Test agent quality with eval sets:

```python
from google.adk.evals import EvalSet, EvalCase

eval_set = EvalSet(
    name="basic_tests",
    cases=[
        EvalCase(
            input="What's the capital of France?",
            expected_output_contains=["Paris"],
        ),
        EvalCase(
            input="Calculate 2+2",
            expected_output_contains=["4"],
        ),
    ],
)

# Run evals
results = eval_set.run(agent)
print(f"Pass rate: {results.pass_rate}%")
```

## Tracing

Debug with Cloud Trace:

```python
from google.adk.tracing import enable_tracing

enable_tracing(project_id="my-project")

# Agent calls now traced
# View in Cloud Console → Trace
```

## Logging

Enable structured logging:

```python
from google.adk.plugins import LoggingPlugin

agent = LlmAgent(
    model="gemini-3-flash",
    name="agent",
    plugins=[LoggingPlugin(level="DEBUG")],
)
```

## References

For detailed guides:
- `references/evals.md` - Evaluation framework
- `references/tracing.md` - Cloud Trace integration
- `references/logging.md` - Structured logging
- `references/observability.md` - Third-party integrations
- `references/user-sim.md` - Synthetic user testing
