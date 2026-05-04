# AGENTS.md - AgentSpec Copilot Runtime

> AgentSpec for GitHub Copilot. Spec-driven development for data engineering with local agents, skills, and KB domains under `.github/`.

## Runtime Rule Sources

Operational rules live in `.github/config/grounding.md`. That file is the single normative source for routing order, skill priority, permissions, response format, language policy, SDD start rules, and token controls.

This `AGENTS.md` file is descriptive runtime documentation: use it for inventory, repository structure, examples, and delegation conventions.

## Skill Invocation

Skills are invoked by folder name. Examples:

```text
/workflow-commands /build .github/sdd/features/my-feature/DESIGN_MY_FEATURE.md
/data-engineering-commands /pipeline "Daily orders ETL with Airflow"
/knowledge-commands /create-kb containers
/review-commands /review
/visual-explainer /generate-web-diagram "Medallion architecture"
/core-commands /status
```

Canonical invocation and routing behavior are defined in `.github/config/grounding.md`.

## SDD Workflow

Workflow phases start through `/workflow-commands`. The authoritative operational rule is defined in `.github/config/grounding.md`; this section is a catalog reference.

| Phase | Command | Agent | Artifact |
|---|---|---|---|
| 0 - Brainstorm | `/workflow-commands /brainstorm ...` | `workflow.brainstorm-agent` | `BRAINSTORM_{FEATURE}.md` |
| 1 - Define | `/workflow-commands /define ...` | `workflow.define-agent` | `DEFINE_{FEATURE}.md` |
| 2 - Design | `/workflow-commands /design ...` | `workflow.design-agent` | `DESIGN_{FEATURE}.md` |
| 3 - Build | `/workflow-commands /build ...` | `workflow.build-agent` | code + `BUILD_REPORT_{FEATURE}.md` |
| 3.5 - Validate | `/workflow-commands /validate ...` | `workflow.validate-agent` | `VALIDATION_REPORT_{FEATURE}.md` |
| 4 - Ship | `/workflow-commands /ship ...` | `workflow.ship-agent` | `SHIPPED_{DATE}.md` |
| Cross-phase | `/workflow-commands /iterate ...` | `workflow.iterate-agent` | updated SDD doc |

Rules:

- Active and draft SDD documents live in `.github/sdd/features/{feature-name}/`.
- Shipped features live in `.github/sdd/archive/{feature-name}/`.
- Build implementation files must be written under `projects/{feature-name}/`.
- Build reports remain with the SDD feature or archive, not under `projects/`.

## Repository Structure

```text
agentspec/
├── AGENTS.md
├── README.md
├── docs/
├── projects/
│   └── {feature-name}/              # generated implementation output
├── .github/
│   ├── copilot-instructions.md
│   ├── config/
│   │   ├── grounding.md
│   │   ├── routing.json
│   │   └── security-settings.json
│   ├── agents/                       # flat: {category}.{name}.agent.md + DEFAULT.AGENT.md
│   ├── skills/
│   ├── kb/
│   ├── sdd/
│   └── workflows/
└── scripts/
```

## Current Inventory

| Area | Count | Notes |
|---|---:|---|
| Agents | 63 + 1 DEFAULT | Flat layout in `.github/agents/` (dot-prefixed categories) |
| Skills | 7 | Folder-invoked commands under `.github/skills/` |
| KB domains | 26 | Domain folders under `.github/kb/` excluding `_templates` |
| SDD workflow agents | 6 | Brainstorm, define, design, build, validate, ship, iterate |

Agent categories:

| Category | Count |
|---|---:|
| architect | 8 |
| cloud | 11 |
| data-engineering | 15 |
| dev | 7 |
| platform | 6 |
| python | 6 |
| test | 3 |
| workflow | 6 |

## Build And Validation

Use `python3`; `python` may not exist in this environment. On Windows, use PowerShell equivalents:

```powershell
# Count agents
(Get-ChildItem .github/agents -Filter "*.agent.md").Count

# Count KB quick-references
(Get-ChildItem .github/kb -Recurse -Filter "quick-reference.md").Count

# Validate routing.json
python3 -m json.tool .github/config/routing.json

# List skill SKILL.md files
Get-ChildItem .github/skills -Recurse -Filter "SKILL.md" | Select-Object FullName

# List generated project files
Get-ChildItem projects -Recurse -File | Select-Object FullName

# Run tests (when present)
python3 -m pytest tests
```

## Build Delegation

`build-agent` delegates via GitHub Copilot's built-in `agent` tool and `runSubagent` action. The build manifest uses `@{agent-name}` assignments, for example:

```text
@{container-specialist}
@{dbt-specialist}
@{airflow-specialist}
@{python-developer}
```

For delegated files, the build must:

- Read the assigned agent file.
- Load the assigned quick-reference KB when declared.
- Enforce the assigned agent quality gates.
- Record evidence in `BUILD_REPORT_{FEATURE}.md`.
- Write generated files under `projects/{feature-name}/`.

## Security

The mandatory security and commit gate policy is defined in `.github/config/grounding.md` and enforced through `dev.security-guardian`.

## Local Analytics Stack

The current shipped example is `local-analytics-stack`:

```text
.github/sdd/archive/local-analytics-stack/
projects/local-analytics-stack/
```

The design assigns Docker and Compose work to `container-specialist`, dbt models to `dbt-specialist`, Airflow files to `airflow-specialist`, and Python scripts/tests to `python-developer`.
