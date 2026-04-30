# AGENTS.md - AgentSpec Copilot Runtime

> AgentSpec for GitHub Copilot. Spec-driven development for data engineering with local agents, skills, and KB domains under `.github/`.

## Grounding

Before any operational response in this workspace:

1. Read `.github/config/grounding.md`.
2. If the user invokes a skill as `/<skill-folder>`, read `.github/skills/<skill-folder>/SKILL.md` first.
3. If no skill is invoked, read `.github/config/routing.json` and route by intent.
4. Read the selected agent file from `.github/agents/` (flat layout: `{category}.{name}.agent.md`).
5. Load only the route quick-reference KB unless the route or skill requires more.
6. Check `_meta/STATUS.md` and `_meta/CONTEXT.md` when present.

Responses must start with the grounding block required by `.github/config/grounding.md`, including `Skill`.

## Skill Invocation

Skills are invoked by folder name:

```text
/workflow-commands /build .github/sdd/features/my-feature/DESIGN_MY_FEATURE.md
/data-engineering-commands /pipeline "Daily orders ETL with Airflow"
/knowledge-commands /create-kb containers
/review-commands /review
/visual-explainer /generate-web-diagram "Medallion architecture"
/core-commands /status
```

Do not use `#skill:` or `skill:`. Those are not the active invocation format in this repo.

## SDD Workflow

Workflow phases can only start through `/workflow-commands`.

| Phase | Command | Agent | Artifact |
|---|---|---|---|
| 0 - Brainstorm | `/workflow-commands /brainstorm ...` | `workflow.brainstorm-agent` | `BRAINSTORM_{FEATURE}.md` |
| 1 - Define | `/workflow-commands /define ...` | `workflow.define-agent` | `DEFINE_{FEATURE}.md` |
| 2 - Design | `/workflow-commands /design ...` | `workflow.design-agent` | `DESIGN_{FEATURE}.md` |
| 3 - Build | `/workflow-commands /build ...` | `workflow.build-agent` | code + `BUILD_REPORT_{FEATURE}.md` |
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
| Agents | 62 + 1 DEFAULT | Flat layout in `.github/agents/` (dot-prefixed categories) |
| Skills | 7 | Folder-invoked commands under `.github/skills/` |
| KB domains | 26 | Domain folders under `.github/kb/` excluding `_templates` |
| SDD workflow agents | 6 | Brainstorm, define, design, build, ship, iterate |

Agent categories:

| Category | Count |
|---|---:|
| architect | 8 |
| cloud | 11 |
| data-engineering | 15 |
| dev | 6 |
| platform | 6 |
| python | 6 |
| test | 3 |
| workflow | 6 |

## Build And Validation

Use `python3`; `python` may not exist in this environment.

```bash
find .github/agents -name "*.agent.md" | wc -l
find .github/kb -name "quick-reference.md" | wc -l
python3 -m json.tool .github/config/routing.json
find .github/skills -maxdepth 2 -name SKILL.md | sort
find projects -maxdepth 2 -type f | sort
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

## Local Analytics Stack

The current shipped example is `local-analytics-stack`:

```text
.github/sdd/archive/local-analytics-stack/
projects/local-analytics-stack/
```

The design assigns Docker and Compose work to `container-specialist`, dbt models to `dbt-specialist`, Airflow files to `airflow-specialist`, and Python scripts/tests to `python-developer`.
