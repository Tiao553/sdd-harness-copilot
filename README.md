# Spec Driven Developing for Copilot

AgentSpec is a GitHub Copilot operating layer for spec-driven development. It transforms any repository into a routed multi-agent workspace where every response is grounded through a mandatory context protocol, intent is matched to the right specialist agent, slash-style skills expose structured command groups, 26 local knowledge-base domains provide on-demand reference material, and a full SDD (Spec-Driven Development) workflow carries features from initial brainstorm through validated build to shipped archive — all inside your IDE.

---

## What It Provides

| Capability | What it does |
|---|---|
| **Grounding** | Forces every operational response through `.github/config/grounding.md`, ensuring the AI always loads mandatory context, security policy, and execution-tier metadata before acting |
| **Routing** | Maps user intent to the correct specialist agent via `.github/config/routing.json`, so requests reach domain experts automatically |
| **Skills** | Exposes 10 slash-invoked command groups — workflow, knowledge context, data engineering, knowledge management, review, core utilities, validation, visual explanation, Excalidraw diagrams, and skill scaffolding — with `routing_skill.json` for machine-readable command dispatch |
| **Agents** | Provides 62 specialist agent definitions + DEFAULT.AGENT.md across 8 categories in a flat layout (`{category}.{name}.agent.md`) |
| **Knowledge Bases** | Provides 26 KB domains with quick references, concepts, patterns, and specs — loaded lazily to minimize token usage |
| **Knowledge Context** | Persistent per-project context (stack, architecture, rules, roadmap, glossary, integrations) automatically injected into every Brainstorm session — supports N projects via registry |
| **SDD Workflow** | Drives the complete feature lifecycle: Brainstorm → Define → Design → Build → Validate → Ship, plus cross-phase Iterate and PR creation |
| **Delegation** | Lets the Build phase hand scoped work to specialist agents (`@{agent-name}`) with required evidence and per-agent quality gates |
| **Review** | Supports automated code review and optional cross-model judging for high-risk or critical work |
| **Visual Explanation** | Generates self-contained HTML visual plans, architecture diagrams, comparison tables, slides, fact checks, and Excalidraw JSON diagrams |

---

## How It Works

Every interaction follows a deterministic grounding chain:

```text
User request
  → grounding.md loaded (mandatory context, security policy, execution tier)
  → knowledge_context/_registry.yaml loaded → active project context injected
  → skill priority check: if the user invokes /<skill>, load SKILL.md first
  → otherwise: routing.json matches intent to the best agent
  → selected agent activated with its quality gates and stop conditions
  → minimal KB loaded (quick-reference.md only, deeper layers on demand)
  → action executed with evidence collection and quality gate enforcement
```

This chain guarantees that the AI never operates without context, never picks an arbitrary agent, and never loads more knowledge than necessary. The grounding block — printed at the top of every operational response — makes the active agent, loaded KB, execution tier, and token budget visible to the user.

---

## SDD Workflow

Spec-Driven Development is the core methodology. Every feature progresses through explicit phases, each gated by entry and exit criteria. Workflow phases can **only** be started through `/workflow-commands`.

### Lifecycle

```text
Phase 0:   Brainstorm  → Knowledge Checkpoint + explore ideas + identify approaches
Phase 1:   Define      → Capture requirements, acceptance criteria, clarity scoring (min 12/15)
Phase 2:   Design      → Architecture decisions, ADRs, file manifest, agent assignments
Phase 3:   Build       → Execute manifest chunk-by-chunk, delegate to specialists
Phase 3.5: Validate    → 4-junta scoring (score ≥ 90 + 0 CRITICAL → RUNBOOK)
Phase 4:   Ship        → Archive artifacts, capture lessons learned
Cross:     Iterate     → Update any SDD document with cascade awareness
```

### Phase Diagrams

Detailed Mermaid flow diagrams with all rules, gates, and mental models:

| Phase | Diagram |
|---|---|
| Overview (all phases) | [docs/workflow-graphic/SDD_WORKFLOW_GRAPH.md](docs/workflow-graphic/SDD_WORKFLOW_GRAPH.md) |
| Phase 0 — Brainstorm | [docs/workflow-graphic/SDD_PHASE0_BRAINSTORM.md](docs/workflow-graphic/SDD_PHASE0_BRAINSTORM.md) |
| Phase 1 — Define | [docs/workflow-graphic/SDD_PHASE1_DEFINE.md](docs/workflow-graphic/SDD_PHASE1_DEFINE.md) |
| Phase 2 — Design | [docs/workflow-graphic/SDD_PHASE2_DESIGN.md](docs/workflow-graphic/SDD_PHASE2_DESIGN.md) |
| Phase 3 — Build | [docs/workflow-graphic/SDD_PHASE3_BUILD.md](docs/workflow-graphic/SDD_PHASE3_BUILD.md) |
| Phase 3.5 — Validate | [docs/workflow-graphic/SDD_PHASE35_VALIDATE.md](docs/workflow-graphic/SDD_PHASE35_VALIDATE.md) |
| Phase 4 — Ship | [docs/workflow-graphic/SDD_PHASE4_SHIP.md](docs/workflow-graphic/SDD_PHASE4_SHIP.md) |

### Commands

| Phase | Command | Agent | Output |
|---|---|---|---|
| 0 | `/workflow-commands /brainstorm` | `brainstorm-agent` | `BRAINSTORM_{FEATURE}.md` |
| 1 | `/workflow-commands /define` | `define-agent` | `DEFINE_{FEATURE}.md` |
| 2 | `/workflow-commands /design` | `design-agent` | `DESIGN_{FEATURE}.md` |
| 3 | `/workflow-commands /build` | `build-agent` | Code in `./projects/{feature-name}/` + `BUILD_REPORT_{FEATURE}.md` |
| 3.5 | `/workflow-commands /validate` | `validate-agent` | `VALIDATION_REPORT_{FEATURE}.md` + `RUNBOOK` or `ROADMAP` |
| 4 | `/workflow-commands /ship` | `ship-agent` | `SHIPPED_{DATE}.md` in archive |
| X | `/workflow-commands /iterate` | `iterate-agent` | Updated SDD document |
| — | `/workflow-commands /create-pr` | — | Pull request with conventional commits |

Active and draft SDD documents live in `.github/sdd/features/{feature-name}/`. Shipped features are moved to `.github/sdd/archive/{feature-name}/`. Implementation source code is always written under `./projects/{feature-name}/`.

---

## Knowledge Context

The Knowledge Context system gives each project a persistent context layer that is automatically injected into every Brainstorm session — eliminating the need to re-explain the project stack, architecture, and rules on every conversation.

### Knowledge Context Flow

```text
/knowledge-context-commands /create-context my-project --set-active
  → scaffolds .github/knowledge_context/my-project/ from templates
  → registers in _registry.yaml as active_project

Next /brainstorm session:
  → grounding.md loads _registry.yaml
  → KNOWLEDGE_CONTEXT.md injected automatically (Step 0 — Knowledge Checkpoint)
  → stack, entry_points, business_context available without re-typing
```

### Context Files (per project)

| File | Purpose | Required |
|---|---|---|
| `KNOWLEDGE_CONTEXT.md` | Stack, entry points, business context | ✅ Yes |
| `architecture.md` | Component map, stack decisions, forbidden patterns | Recommended |
| `rules.md` | Code conventions, branch rules, anti-patterns | Recommended |
| `roadmap.md` | Current phase, milestones, feature backlog | Optional |
| `domain-glossary.md` | Business entities, terms, anti-terms | Optional |
| `integrations.md` | External APIs, queues, data sources, secrets | Optional |

### Knowledge Context Commands

| Command | What it does |
|---|---|
| `/knowledge-context-commands /create-context <slug>` | Scaffold full context from templates, register in registry |
| `/knowledge-context-commands /update-context <slug>` | Update specific file or field; detects cascade impact |
| `/knowledge-context-commands /check-context [slug]` | Audit completeness, health score 0–100, gap report |

### Multi-Project Support

The `_registry.yaml` file at `.github/knowledge_context/_registry.yaml` tracks all projects and which one is currently active. Switch between projects with:

```text
/knowledge-context-commands /create-context other-project --set-active
```

---

## Quality Gates

AgentSpec enforces a multi-layer quality gate system that prevents incomplete or broken work from advancing:

- **Phase entry/exit gates** — each SDD phase has mandatory criteria. Define requires clarity score ≥ 12/15; Design requires a complete file manifest; Build requires DESIGN with manifest.
- **Specialist quality gates** — when Build delegates a file to a specialist agent (e.g., `@{dbt-specialist}`), that agent's own quality gates must be satisfied and evidence recorded.
- **Validate is mandatory** — the Build → Ship transition is blocked until Phase 3.5 Validate has been executed and approved.
- **Score-based validation** — Validate orchestrates four specialized crews (SpecCrew, CodeCrew, DeliveryCrew, CouncilCrew) to produce a weighted score. The pass criteria are: **score ≥ 90** and **0 CRITICAL findings**. A passing validation produces a `RUNBOOK`; a failing one produces a `ROADMAP` of required fixes.
- **Ship is gated** — Ship will not proceed without an approved validation report and RUNBOOK.

---

## Delegation

The Build phase supports automatic delegation to specialist agents for scoped work:

1. The **DESIGN** document contains a file manifest with `@{agent-name}` assignments — for example, `@{container-specialist}` for Dockerfiles, `@{dbt-specialist}` for dbt models, `@{airflow-specialist}` for DAGs.
2. When Build processes the manifest, it reads the assigned specialist agent file and loads the agent's required KB domain.
3. The specialist executes its scope under its own quality gates and stop conditions.
4. All evidence — files written, tests passed, linting results — is recorded in `BUILD_REPORT_{FEATURE}.md`.
5. If a specialist's quality gates are not met, the build halts and reports the failure.

---

## Build Output

All generated artifacts follow a strict path convention:

```text
Implementation files   → ./projects/{feature-name}/
SDD feature artifacts  → .github/sdd/features/{feature-name}/
Archived artifacts     → .github/sdd/archive/{feature-name}/
Build reports          → .github/sdd/features/{feature-name}/ (or archive after ship)
Knowledge context      → .github/knowledge_context/{project-slug}/
```

Implementation code never lives inside `.github/`. SDD documents never live inside `projects/`. This separation keeps the operating layer clean and the generated code portable.

---

## Invocation

Skills are invoked by folder name using slash syntax:

```text
/<skill-folder> /<command> <args>
```

### Examples

```text
# Knowledge Context setup (run once per project)
/knowledge-context-commands /create-context my-project --set-active
/knowledge-context-commands /check-context
/knowledge-context-commands /update-context my-project --file architecture.md

# SDD workflow
/workflow-commands /brainstorm "real-time order tracking pipeline"
/workflow-commands /define .github/sdd/features/order-tracking/BRAINSTORM_ORDER_TRACKING.md
/workflow-commands /design .github/sdd/features/order-tracking/DEFINE_ORDER_TRACKING.md
/workflow-commands /build .github/sdd/features/order-tracking/DESIGN_ORDER_TRACKING.md
/workflow-commands /validate order-tracking
/workflow-commands /ship .github/sdd/features/order-tracking/DEFINE_ORDER_TRACKING.md
/workflow-commands /create-pr

# Data engineering
/data-engineering-commands /schema "star schema for order analytics"
/data-engineering-commands /pipeline "Daily orders ETL with Airflow"
/data-engineering-commands /data-quality "validate customer dimension"

# Knowledge management
/knowledge-commands /create-kb containers
/knowledge-commands /update-kb airflow

# Review
/review-commands /review
/review-commands /judge .github/sdd/archive/example/BUILD_REPORT_EXAMPLE.md

# Visuals and utilities
/visual-explainer /generate-web-diagram "medallion architecture"
/excalidraw-diagram "CI/CD pipeline flow"
/core-commands /status
```

> **Important:** Do not use `#skill:`, `skill:`, `/agentspec:*`, or `.claude/` conventions. Slash-folder invocation is the only supported format.

---

## Runtime Structure

| Path | Purpose |
|---|---|
| `.github/copilot-instructions.md` | Workspace instructions for GitHub Copilot |
| `.github/config/` | Grounding protocol, intent router, and security settings |
| `.github/skills/` | Slash-style command groups (10 skills, 6 with `routing_skill.json`) |
| `.github/agents/` | Specialist agent definitions (62 agents + DEFAULT.AGENT.md, flat layout) |
| `.github/kb/` | Local domain knowledge bases (26 domains) |
| `.github/knowledge_context/` | Per-project persistent context — registry + templates + project directories |
| `.github/sdd/` | SDD templates, active feature specs, architecture contracts, and archives |
| `projects/` | Implementation output generated by Build (`./projects/{feature-name}/`) |
| `docs/` | Operator and reference documentation |
| `scripts/` | Utility and validation scripts |

---

## Agent Categories

62 agents organized into 8 specialist categories:

| Category | Count | Focus |
|---|---:|---|
| architect | 8 | Planning, schemas, lakehouse, medallion, GenAI, KB architecture |
| cloud | 11 | AWS, GCP, Supabase, containers, CI/CD, Lambda, deployment |
| data-engineering | 15 | dbt, Airflow, Spark, Lakeflow, SQL, streaming, vector search |
| dev | 6 | Routing, exploration, review, judge, meeting analysis, shell scripts |
| platform | 6 | Microsoft Fabric architecture, security, AI, pipelines, logging, CI/CD |
| python | 6 | Python development, cleanup, review, docs, prompts, LLM work |
| test | 3 | Tests, data quality, data contracts |
| workflow | 7 | Brainstorm, Define, Design, Build, Validate, Ship, Iterate |

---

## Main Skills

All skills follow the **SKILL.md = Orchestrator, Commands = Executors** architecture. Skills with subcommands include a `routing_skill.json` for machine-readable command dispatch. See [Skills Architecture](docs/skills-architecture.md) for the full reference.

| Skill | Commands | `routing_skill.json` |
|---|---|---|
| `/workflow-commands` | `/brainstorm`, `/define`, `/design`, `/build`, `/validate`, `/ship`, `/iterate`, `/create-pr` | ✅ |
| `/knowledge-context-commands` | `/create-context`, `/update-context`, `/check-context` | ✅ |
| `/data-engineering-commands` | `/pipeline`, `/schema`, `/data-quality`, `/lakehouse`, `/sql-review`, `/ai-pipeline`, `/data-contract`, `/migrate` | ✅ |
| `/core-commands` | `/status`, `/meeting`, `/memory`, `/sync-context`, `/readme-maker` | ✅ |
| `/knowledge-commands` | `/create-kb`, `/update-kb`, `/refresh-stale-kbs` | ✅ |
| `/review-commands` | `/review`, `/judge` | ✅ |
| `/visual-explainer` | Visual plans, diagrams, slides, fact checks, recaps | — |
| `/excalidraw-diagram` | Excalidraw JSON diagrams | — |
| `/validate` | Phase 3.5 validation runtime (Python CLI) | — |
| `/create-skills` | Skill scaffolding tool | — |

---

## Quick Start

### First Time — Configure Project Context

```text
# 1. Create context for your project (once per project)
/knowledge-context-commands /create-context my-project --set-active

# 2. Fill in KNOWLEDGE_CONTEXT.md (stack, entry points, business context)
# 3. Optionally fill architecture.md, rules.md, roadmap.md

# 4. Verify
/knowledge-context-commands /check-context
```

### Run a Feature End-to-End

```text
# Phase 0: Brainstorm (context auto-injected from knowledge_context/)
/workflow-commands /brainstorm "my feature idea"

# Phase 1: Define requirements
/workflow-commands /define .github/sdd/features/my-feature/BRAINSTORM_MY_FEATURE.md

# Phase 2: Design architecture
/workflow-commands /design .github/sdd/features/my-feature/DEFINE_MY_FEATURE.md

# Phase 3: Build (chunk by chunk)
/workflow-commands /build .github/sdd/features/my-feature/DESIGN_MY_FEATURE.md

# Phase 3.5: Validate (score ≥ 90 required)
/workflow-commands /validate my-feature

# Phase 4: Ship
/workflow-commands /ship .github/sdd/features/my-feature/DEFINE_MY_FEATURE.md
```

Each command produces an artifact that feeds the next phase. If validation fails, use `/workflow-commands /iterate` to update the relevant SDD document and re-run Build.

---

## Documentation

| Guide | Purpose |
|---|---|
| [docs/](docs/) | Documentation entrypoint |
| [Getting Started](docs/getting-started/) | First usage flow and command conventions |
| [Concepts](docs/concepts/) | Grounding, skills, agents, KB, SDD, routing, delegation |
| [Tutorials](docs/tutorials/) | Practical AgentSpec workflows |
| [Reference](docs/reference/) | Full skills, agents, KB, routing, and validation catalog |
| [Skills Architecture](docs/skills-architecture.md) | Skill directory standard, routing_skill.json schema, command patterns, quality gates |
| [SDD Phase Diagrams](docs/workflow-graphic/SDD_WORKFLOW_GRAPH.md) | Mermaid flowcharts for all SDD phases |

---

## Canonical Paths

| Type | Path |
|---|---|
| Active features | `.github/sdd/features/{feature-name}/` |
| Implementation code | `./projects/{feature-name}/` |
| Shipped archive | `.github/sdd/archive/{feature-name}/` |
| Templates | `.github/sdd/templates/` |
| Contracts | `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml` |
| Agents | `.github/agents/` |
| KB domains | `.github/kb/` |
| Skills | `.github/skills/` |
| Config | `.github/config/` |
| Knowledge Context registry | `.github/knowledge_context/_registry.yaml` |
| Knowledge Context templates | `.github/knowledge_context/_templates/` |
| Knowledge Context (per project) | `.github/knowledge_context/{project-slug}/` |

---

## Validate The Workspace

```bash
find .github/agents -name "*.agent.md" | wc -l
find .github/kb -name "quick-reference.md" | wc -l
find .github/skills -maxdepth 2 -name SKILL.md | sort
python3 -m json.tool .github/config/routing.json
find projects -maxdepth 2 -type f | sort
# Knowledge context
cat .github/knowledge_context/_registry.yaml
```

---

## Contributing

Contributions are welcome. When adding new agents, skills, or KB domains:

1. Follow the existing naming conventions (`{name}.agent.md`, `SKILL.md`, `quick-reference.md`).
2. Register new agents in `routing.json` if they should be reachable by intent.
3. Run the workspace validation commands above to confirm inventory counts.
4. Use `/workflow-commands /create-pr` to generate a pull request with conventional commits.

## License

See [LICENSE](LICENSE) if present in the repository root.
