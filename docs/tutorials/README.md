# Tutorials

These tutorials show how to use AgentSpec as a Copilot operating model.

## Tutorial 1: Route A Request Correctly

Use a skill when you know the command family:

```text
/data-engineering-commands /schema "star schema for subscription analytics"
```

Expected behavior:

1. Copilot reads `grounding.md`.
2. The `data-engineering-commands` skill takes priority.
3. The skill chooses the right agent and KB.
4. The response starts with the operational grounding block.

Use natural language only when you want the router to choose:

```text
Review this SQL model for performance and cross-dialect issues.
```

The router should select a SQL or review specialist based on intent.

## Tutorial 2: Run The SDD Lifecycle

Start with a brainstorm:

```text
/workflow-commands /brainstorm "customer analytics platform"
```

Move through the phases:

```text
/workflow-commands /define .github/sdd/features/customer-analytics/BRAINSTORM_CUSTOMER_ANALYTICS.md
/workflow-commands /design .github/sdd/features/customer-analytics/DEFINE_CUSTOMER_ANALYTICS.md
/workflow-commands /build .github/sdd/features/customer-analytics/DESIGN_CUSTOMER_ANALYTICS.md
/workflow-commands /validate .github/sdd/features/customer-analytics/BUILD_REPORT_CUSTOMER_ANALYTICS.md
/workflow-commands /ship .github/sdd/features/customer-analytics/DEFINE_CUSTOMER_ANALYTICS.md
```

Do not skip Validate. It is the Phase 3.5 gate that produces `VALIDATION_REPORT_CUSTOMER_ANALYTICS.md` and, when approved, `RUNBOOK_CUSTOMER_ANALYTICS.md`. Ship should be blocked when validation score is below 90 or any CRITICAL issue remains.

Use iterate when requirements or design change:

```text
/workflow-commands /iterate .github/sdd/features/customer-analytics/DESIGN_CUSTOMER_ANALYTICS.md "add data quality gates"
```

## Tutorial 3: Create A Knowledge Base Domain

Create a new KB:

```text
/knowledge-commands /create-kb containers
```

Update an existing KB:

```text
/knowledge-commands /update-kb dbt --topic "incremental model strategy"
```

Refresh stale KBs:

```text
/knowledge-commands /refresh-stale-kbs --max-age-days 90
```

Good KB domains include:

- `quick-reference.md` for fast decisions
- `concepts/` for durable explanations
- `patterns/` for implementation guidance
- `specs/` for standards and compatibility notes

## Tutorial 4: Delegate Build Work To Specialists

In a DESIGN manifest, assign ownership using agent names:

```text
| Artifact | Intent | Owner |
|---|---|---|
| runtime configuration | container orchestration | @{container-specialist} |
| transformation models | analytics modeling | @{dbt-specialist} |
| orchestration workflow | scheduled execution | @{airflow-specialist} |
| Python module | data generation or utilities | @{python-developer} |
```

During Build, `build-agent` should:

1. Read the assigned agent file.
2. Load the assigned quick-reference KB.
3. Delegate with Copilot's `agent` and `runSubagent`.
4. Require quality-gate evidence.
5. Record the evidence in the Build report.

## Tutorial 5: Review High-Risk Work

Use local review first:

```text
/review-commands /review .github/agents/cloud.container-specialist.agent.md
```

Use judge for a second opinion when the risk justifies it:

```text
/review-commands /judge .github/sdd/archive/example/BUILD_REPORT_EXAMPLE.md --context "multi-agent build report"
```

Judge requires OpenRouter configuration. See [Judge Setup](../getting-started/judge-setup.md).

## Tutorial 6: Generate A Visual Explanation

Use the visual skill when text would be too dense:

```text
/visual-explainer /generate-web-diagram "AgentSpec grounding and routing flow"
/visual-explainer /generate-slides "AgentSpec architecture overview"
/visual-explainer /fact-check .github/sdd/features/customer-analytics/DESIGN_CUSTOMER_ANALYTICS.md
```

Use Excalidraw when you need an editable diagram artifact:

```text
/excalidraw-diagram "SDD lifecycle with skill priority and agent routing"
```

## Common Mistakes

| Mistake | Correct |
|---|---|
| `#skill:workflow-commands` | `/workflow-commands` |
| `skill:data-engineering-commands` | `/data-engineering-commands` |
| `/build` | `/workflow-commands /build` |
| Shipping right after Build | Run `/workflow-commands /validate` first |
| Starting workflow from vague prose | Ask for the exact `/workflow-commands /<phase>` invocation |
| Loading full KB folders by default | Start with `quick-reference.md` |
