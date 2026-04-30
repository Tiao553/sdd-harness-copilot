# AgentSpec Documentation

AgentSpec is a GitHub Copilot runtime made of grounding rules, routed agents, slash-style skills, local knowledge bases, and SDD workflow contracts.

This documentation covers the runtime model, SDD workflow, agent delegation, quality gates, and all skill commands. Use it to understand how Copilot should operate inside this repository.

## Start Here

| Guide | Use it for |
|---|---|
| [Getting Started](getting-started/) | Running the first AgentSpec commands correctly, including Build → Validate → Ship. Covers environment setup, first skill invocation, and the mandatory validation gate. |
| [Core Concepts](concepts/) | Runtime model, routing, skills, agents, KB, SDD, delegation, and validation. Explains why each layer exists and how they compose. |
| [Tutorials](tutorials/) | Practical workflows for SDD, KB authoring, review, and visual explanations. Step-by-step walkthroughs with expected outputs. |
| [Reference](reference/) | Catalog of every agent, skill, KB domain, and validation command. The authoritative lookup for counts, paths, and invocation syntax. |

## Deep Reference

| Guide | What it explains |
|---|---|
| [Agents](reference/agents.md) | Agent categories, delegation, and why specialists exist |
| [Router](reference/router.md) | Intent routing and why `routing.json` is separate |
| [Grounding](reference/grounding.md) | Mandatory execution grounding and why it exists |
| [Workflow, Contracts and Architecture](reference/workflow-contracts-architecture.md) | SDD phases, gates, paths, contracts, and delegation |
| [Knowledge Base](reference/knowledge-base.md) | KB structure, domains, loading policy, and lifecycle |
| [Skills](reference/skills/) | One guide per slash-style skill |
| [Skills Architecture](skills-architecture.md) | Skill directory standard, routing_skill.json schema, command file patterns, quality gates, and migration history |
| [Canonical Paths](#canonical-paths) | Every well-known path in the repository and what lives there |

## Mental Model

AgentSpec gives Copilot a deterministic operating sequence:

```text
User request
  → grounding.md
  → skill priority or router intent match
  → selected agent
  → minimal KB
  → action with evidence
```

The important rule is priority:

1. A request starting with `/<skill-folder>` is controlled by that skill.
2. A request without a skill is routed by intent through `routing.json`.
3. Workflow phases are only started by `/workflow-commands`.

**Key invariants:**

- **Skill invocation always wins over routing.** If the user types `/<skill-folder>`, routing.json is bypassed and the skill's `SKILL.md` drives execution. For skills with `routing_skill.json`, the matched command's agent and KB are loaded automatically.
- **Workflow phases require `/workflow-commands` explicitly.** Asking "build the feature" in natural language does _not_ start Phase 3; Copilot replies with the exact command to run.
- **Build always writes to `./projects/{feature-name}/`.** Generated implementation files never land inside `.github/sdd/`.
- **Validate is mandatory between Build and Ship.** Phase 4 (Ship) will not proceed without an approved `VALIDATION_REPORT`.

## SDD Workflow Overview

Spec-Driven Development is a phased workflow that turns an idea into shipped, validated code:

| Phase | Name | Purpose |
|:---:|---|---|
| 0 | Brainstorm | Explore ideas collaboratively and capture raw intent |
| 1 | Define | Requirements, acceptance criteria, clarity scoring |
| 2 | Design | Architecture decisions, file manifest, agent assignments |
| 3 | Build | Execute manifest, delegate to specialists, write to `./projects/{feature-name}/` |
| 3.5 | Validate | Score implementation vs requirements (≥ 90 + 0 CRITICAL → RUNBOOK) |
| 4 | Ship | Archive artifacts, record lessons learned |
| Cross | Iterate | Update any SDD document with cascade tracking |

### Workflow Commands

| Phase | Command | Agent | Output |
|:---:|---|---|---|
| 0 | `/workflow-commands /brainstorm` | `brainstorm-agent` | `BRAINSTORM_{FEATURE}.md` |
| 1 | `/workflow-commands /define` | `define-agent` | `DEFINE_{FEATURE}.md` |
| 2 | `/workflow-commands /design` | `design-agent` | `DESIGN_{FEATURE}.md` |
| 3 | `/workflow-commands /build` | `build-agent` | code + `BUILD_REPORT_{FEATURE}.md` |
| 3.5 | `/workflow-commands /validate` | `validate-agent` | `VALIDATION_REPORT_{FEATURE}.md` |
| 4 | `/workflow-commands /ship` | `ship-agent` | `SHIPPED_{DATE}.md` |
| Cross | `/workflow-commands /iterate` | `iterate-agent` | updated SDD document |

Active and draft SDD documents live in `.github/sdd/features/{feature-name}/`. Shipped features are archived to `.github/sdd/archive/{feature-name}/`.

## Quality Gates

AgentSpec enforces a multi-layer gate system to prevent incomplete or broken work from advancing:

1. **Phase entry/exit gates** — Enforced by `WORKFLOW_CONTRACTS.yaml`. Each phase declares preconditions (required input artifacts) and postconditions (required output artifacts, minimum scores). A phase cannot start until the previous phase's exit gate is satisfied.
2. **Build delegation gates** — When `build-agent` delegates files to specialist agents (e.g., `@{container-specialist}`, `@{dbt-specialist}`), each specialist must meet its own quality gates before reporting success.
3. **Validate gate** — Mandatory between Build and Ship. The validate phase runs four specialized crews (SpecCrew, CodeCrew, DeliveryCrew, CouncilCrew) and produces a weighted score. A score ≥ 90 with zero CRITICAL findings generates a RUNBOOK; otherwise a REMEDIATION_ROADMAP is produced and Build must iterate.
4. **Ship gate** — Requires an approved `VALIDATION_REPORT` plus a `RUNBOOK`. Without these, Ship refuses to proceed.

## Delegation

During Phase 3 (Build), `build-agent` reads the `DESIGN` manifest and delegates individual files or file groups to specialist agents using `@{agent-name}` assignments.

For each delegation the build must:

- Read the assigned agent file from `.github/agents/`.
- Load the assigned `quick-reference.md` KB when declared.
- Enforce the specialist's quality gates.
- Record evidence (files produced, gates passed, issues found) in `BUILD_REPORT_{FEATURE}.md`.
- Write all generated files under `projects/{feature-name}/`.

The specialist never writes outside its assigned scope. Build-agent owns the overall manifest and is responsible for merging results and reporting.

## Canonical Paths

| Path | Purpose |
|---|---|
| `.github/config/grounding.md` | Mandatory grounding — read before every response |
| `.github/config/routing.json` | Intent-to-agent routing table |
| `.github/config/security-settings.json` | Command execution permission policy |
| `.github/agents/` | All agent definitions (62 agents + DEFAULT.AGENT.md, 8 categories, flat layout) |
| `.github/skills/` | Slash-style skill folders with `SKILL.md` entry points |
| `.github/kb/` | Knowledge base domains with `quick-reference.md` |
| `.github/sdd/features/{feature}/` | Active SDD documents (DEFINE, DESIGN, BUILD_REPORT, etc.) |
| `.github/sdd/archive/{feature}/` | Shipped and archived SDD documents |
| `.github/sdd/templates/` | SDD document templates |
| `projects/{feature-name}/` | Generated implementation output from Build phase |
| `docs/` | Public documentation (this folder) |
| `scripts/` | Utility and validation scripts |

## Current Inventory

| Area | Count |
|---|---:|
| Agents | 62 |
| Skills | 9 |
| KB domains | 26 |
| Workflow phases | 7 phase agents plus PR support through skill commands |

### Skill Architecture

Skills follow the **SKILL.md = Orchestrator, Commands = Executors** principle. SKILL.md files contain only global rules and a routing table; each command file is self-contained with Usage, Process, Quality Gates, Output, Next Step, and See Also sections.

Five skills include `routing_skill.json` for machine-readable command dispatch. See [Skills Architecture](skills-architecture.md) for the definitive reference.

| Skill | SKILL.md Lines | Commands | `routing_skill.json` | Status |
|---|---|---|---|---|
| `workflow-commands` | ~140 | 8 | ✅ | refactored (-90%) |
| `core-commands` | ~63 | 5 | ✅ | refactored (-93%) |
| `data-engineering` | ~80 | 8 | ✅ | refactored (-77%) |
| `knowledge` | ~106 | 3 | ✅ | refactored (-46%) |
| `review` | ~64 | 2 | ✅ | completed |
| `visual-explainer` | 330 | 8 | — | clean (reference impl) |
| `excalidraw-diagram` | 552 | 0 | — | clean |
| `validate` | ~110 | 0 | — | enhanced |
| `create-skills` | ~45 | 0 | — | populated |

### Agent Categories

| Category | Count | Examples |
|---|---:|---|
| architect | 8 | solution-architect, api-designer |
| cloud | 11 | aws-specialist, azure-specialist |
| data-engineering | 15 | dbt-specialist, airflow-specialist, spark-specialist |
| dev | 6 | python-developer, container-specialist |
| platform | 6 | ci-cd-specialist, infrastructure-agent |
| python | 6 | fastapi-specialist, pytest-specialist |
| test | 3 | integration-test-agent, load-test-agent |
| workflow | 6 | define-agent, build-agent, validate-agent |

## Main Capabilities

- Spec-driven development: Brainstorm, Define, Design, Build, Validate, Ship, Iterate
- Data engineering command flows for schema, pipeline, quality, lakehouse, SQL review, migration, AI pipelines, and data contracts
- KB creation and refresh workflows
- Specialist agent routing and subagent delegation
- Code review and optional judge review
- Visual explanations through HTML pages, slides, and Excalidraw diagrams
- Mandatory Phase 3.5 validation with validation report, runbook, or remediation roadmap

## Quick Validation

Run these commands to verify the runtime inventory:

```bash
find .github/agents -name "*.agent.md" | wc -l
find .github/kb -name "quick-reference.md" | wc -l
find .github/skills -maxdepth 2 -name SKILL.md | sort
python3 -m json.tool .github/config/routing.json
```

---

> For detailed walkthroughs, see [Tutorials](tutorials/). For the full agent and skill catalog, see [Reference](reference/).
