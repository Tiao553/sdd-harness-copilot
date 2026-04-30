# Getting Started

This workspace is already configured as AgentSpec for GitHub Copilot. There is no separate runtime install step. The important part is using the correct invocation format and letting the grounding rules choose the right execution path.

## Prerequisites

- GitHub Copilot Chat or Copilot coding agent with access to this repository
- Git
- Python 3 for validation commands
- Domain tools only when a selected agent or workflow requires them

## Command Format

Invoke skills by folder name:

```text
/<skill-folder> /<command> <args>
```

Examples:

```text
/workflow-commands /brainstorm "customer analytics platform"
/workflow-commands /define .github/sdd/features/customer-analytics/BRAINSTORM_CUSTOMER_ANALYTICS.md
/workflow-commands /design .github/sdd/features/customer-analytics/DEFINE_CUSTOMER_ANALYTICS.md
/workflow-commands /build .github/sdd/features/customer-analytics/DESIGN_CUSTOMER_ANALYTICS.md
/workflow-commands /validate .github/sdd/features/customer-analytics/BUILD_REPORT_CUSTOMER_ANALYTICS.md
/data-engineering-commands /schema "star schema for customer orders"
/knowledge-commands /create-kb containers
/review-commands /review .github/agents/data-engineering.dbt-specialist.agent.md
```

Do not use `#skill:`, `skill:`, `/agentspec:*`, or direct workflow commands such as `/build`.

## First SDD Flow

### 1. Brainstorm

```text
/workflow-commands /brainstorm "customer analytics platform"
```

Creates an exploratory SDD artifact with assumptions, options, risks, and open questions.

### 2. Define

```text
/workflow-commands /define .github/sdd/features/customer-analytics/BRAINSTORM_CUSTOMER_ANALYTICS.md
```

Creates requirements, scope, constraints, acceptance criteria, and quality gates.

### 3. Design

```text
/workflow-commands /design .github/sdd/features/customer-analytics/DEFINE_CUSTOMER_ANALYTICS.md
```

Creates architecture, decisions, patterns, KB references, and an implementation manifest with `@{agent-name}` assignments.

### 4. Build

```text
/workflow-commands /build .github/sdd/features/customer-analytics/DESIGN_CUSTOMER_ANALYTICS.md
```

Build executes the design manifest, delegates specialized work to agents, validates quality gates, and records evidence.

### 5. Validate

```text
/workflow-commands /validate .github/sdd/features/customer-analytics/BUILD_REPORT_CUSTOMER_ANALYTICS.md
```

Validate is the mandatory Phase 3.5 quality gate. It compares DEFINE, DESIGN, BUILD_REPORT, and the code under `projects/customer-analytics/`. It always creates `VALIDATION_REPORT_CUSTOMER_ANALYTICS.md`; if the score is at least 90 with zero CRITICAL issues, it also creates `RUNBOOK_CUSTOMER_ANALYTICS.md`.

### 6. Ship

```text
/workflow-commands /ship .github/sdd/features/customer-analytics/DEFINE_CUSTOMER_ANALYTICS.md
```

Ship verifies the approved validation report and runbook, archives the SDD artifacts, and records lessons learned.

## Direct Specialist Commands

Use direct skills when you do not need the full SDD lifecycle:

```text
/data-engineering-commands /pipeline "daily orders ETL with Airflow"
/data-engineering-commands /data-quality "checks for customer dimension"
/data-engineering-commands /sql-review "review a complex revenue query"
/knowledge-commands /update-kb dbt --topic "incremental models"
/visual-explainer /generate-web-diagram "AgentSpec routing flow"
/core-commands /status
```

## What Copilot Should Do

For every operational request, Copilot should:

1. Read `.github/config/grounding.md`.
2. Prefer an invoked skill over intent routing.
3. Load the selected agent.
4. Load only minimal KB.
5. Start the response with the operational grounding block.
6. Execute or explain the exact command required.

## Validate The Workspace

```bash
find .github/agents -name "*.agent.md" | wc -l
find .github/kb -name "quick-reference.md" | wc -l
find .github/skills -maxdepth 2 -iname "SKILL.md" | sort
python3 -m json.tool .github/config/routing.json
python3 -m pytest tests
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| Copilot starts a workflow from natural language | Ask it to use `/workflow-commands /<phase>` |
| Copilot ignores a skill invocation | Ensure the skill folder exists under `.github/skills/` |
| Copilot loads too much context | Remind it to use quick-reference KB first |
| Agent assignment fails | Confirm the target `.agent.md` file exists |
| Ship is blocked | Run `/workflow-commands /validate` and resolve any CRITICAL issues or score below 90 |
| Validation uses `python` | Use `python3` |
