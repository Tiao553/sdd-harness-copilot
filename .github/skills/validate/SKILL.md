---
name: validate
description: >
  Multi-agent quality gate for AgentSpec SDD Phase 3.5.
  Orchestrates four specialized CrewAI crews (SpecCrew, CodeCrew, DeliveryCrew, CouncilCrew)
  to validate that an implemented feature matches its DEFINE requirements and DESIGN intent.
  Produces a weighted validation score plus JSON artifact guidance; the skill renders
  VALIDATION_REPORT, RUNBOOK, or ROADMAP documents from templates.
entrypoint: scripts/main.py
tools:
  - run_command
---

# Validate Skill

## Purpose

This skill executes the `/validate` multi-agent quality gate. It reads SDD artifacts from disk,
builds an immutable `ValidateContext`, and passes it through a four-crew pipeline.

## Global Rules

1. `ValidateContext` é imutável uma vez construído — nenhum crew pode alterar o contexto de entrada.
2. Todas as saídas dos crews devem ser JSON puro — sem markdown, sem escrita direta de arquivos.
3. Subprocess whitelist: apenas `python3`, `ruff`, `mypy` são permitidos.
4. Isolamento de crews: sem comunicação cross-crew exceto via `ValidateContext`.
5. Leia `WORKFLOW_CONTRACTS.yaml` como fonte canônica para Phase 3.5.
6. Score >= 90 + 0 CRITICAL → RUNBOOK eligible → Ship permitido.
7. Não relaxe gates sem registrar bloqueio e pedir decisão do usuário.

## Required Workflow Contract

Before running validation, read `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml`.
That file is the canonical source for Phase 3.5 inputs, outputs, score gates,
required artifacts, and Ship blocking rules. If this skill's local examples drift
from the contract, the contract wins.

## Directory Structure

```
.github/skills/validate/
├── SKILL.md               ← This file (skill descriptor)
├── README.md              ← Operator-facing skill guide
└── scripts/               ← All executable code lives here
    ├── __init__.py        ← ValidateSkill entry class
    ├── main.py            ← CLI entry point (Typer)
    ├── schemas.py         ← Pydantic contracts (ValidateContext, reports)
    ├── tools.py           ← SDD file readers, ruff/mypy wrappers
    ├── spec_crew.py       ← (legacy flat file, superseded by crews/)
    ├── code_crew.py       ← (legacy flat file, superseded by crews/)
    └── crews/
        ├── __init__.py
        ├── spec_crew.py   ← Hierarchical · 4 agents (MGR, ARC, ENG, SWE)
        ├── code_crew.py   ← Hierarchical · 4 agents (MGR, SWE, ENG, OPS)
        ├── delivery_crew.py ← Sequential · 2 agents (CMP, GAP)
        └── council_crew.py  ← Sequential · 3 agents (JDG, RPT, PRD)
```

## Invocation

The skill is invoked by `/workflow-commands /validate` as SDD Phase 3.5.
The workflow calls:

```bash
python3 .github/skills/validate/scripts/main.py <FEATURE_NAME>
```

Where `<FEATURE_NAME>` is the upper snake case feature identifier (e.g. `VALIDATE_WORKFLOW`).

Direct `/validate <FEATURE_NAME>` is reserved for local operator use; SDD workflow
execution should prefer `/workflow-commands /validate` so the Build -> Validate -> Ship
contract remains explicit.

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | LLM provider API key (OpenRouter, OpenAI, etc.) |
| `OPENAI_API_BASE` | Optional: Override base URL (e.g. `https://openrouter.ai/api/v1`) |

## Crew Pipeline

```
ValidateContext (built from DEFINE + DESIGN + BUILD_REPORT + code_tree)
       │
       ├──[parallel]── SpecCrew  → SpecReport  (alignment_score, architecture_score)
       │                            Hierarchical · 4 agents
       │
       └──[parallel]── CodeCrew  → CodeReport  (quality_score, devops_score)
                                    Hierarchical · 4 agents
                  │
                  ▼
            DeliveryCrew → DeliveryDelta (missing_files, requirement_map, delta_score)
                           Sequential · 2 agents
                  │
                  ▼
            CouncilCrew  → ValidationReport (final score, runbook_eligible, roadmap_eligible)
                           Sequential · 3 agents
```

## Scoring Formula

| Dimension | Weight | Source |
|-----------|--------|--------|
| Spec Alignment | 30% | `SpecReport.alignment_score` |
| Code Quality | 25% | `CodeReport.quality_score` |
| Architecture Fidelity | 20% | `SpecReport.architecture_score` |
| Security & DevOps | 15% | `CodeReport.devops_score` |
| Production Readiness | 10% | `DeliveryDelta.delta_score` |

## Artifact Contract

The crews must return JSON only. They must not write files or return full markdown documents.
`ValidationReport.artifact_plan` guides deterministic skill-side rendering from
`.github/sdd/templates/`.

## Artifact Eligibility

| Score | No CRITICAL Issues | Artifact Generated |
|-------|-------------------|-------------------|
| Any | Any | `VALIDATION_REPORT_{FEATURE}.md` |
| ≥ 90 | ✅ | `RUNBOOK_{FEATURE}.md` |
| 70-89 | ✅ | `ROADMAP_{FEATURE}.md` |
| < 70 | Any | Validation report only, Exit code 1 |

## Workflow Contract

- Validate always runs after Build and before Ship.
- Ship must not proceed without `VALIDATION_REPORT_{FEATURE}.md`.
- Ship approval requires score >= 90 and zero CRITICAL issues.
- A ROADMAP result sends the feature back to remediation and a later Build/Validate loop.
