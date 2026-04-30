# Skills Architecture Reference

This document is the definitive reference for understanding, creating, and maintaining AgentSpec skills. It covers the directory standard, the orchestrator/executor separation, routing, command patterns, quality gates, and delegation.

---

## Architecture Principle

**SKILL.md = Orchestrator. Commands = Executors.**

A skill's `SKILL.md` file contains only global rules, shared context, and a routing table that maps command names to their executor files. Each command file is fully self-contained — it declares its own usage, process steps, quality gates, output format, next steps, and cross-references. This separation keeps SKILL.md lean (typically 60–140 lines) and makes each command independently executable.

### Why This Matters

- **Token efficiency:** Loading SKILL.md to determine which command to run costs 60–140 lines, not 500+.
- **Independent commands:** A command file can be read and executed without loading other commands.
- **Single responsibility:** Global rules (security, escalation, defaults) live in one place; per-command logic lives in another.
- **Scalability:** Adding a command means adding a file and a routing table entry — no SKILL.md rewrite needed.

---

## Directory Structure Standard

Every skill follows this layout:

```text
.github/skills/{skill-name}/
├── SKILL.md                  # Orchestrator — global rules + routing table
├── routing_skill.json        # Machine-readable command routing (optional)
└── commands/                 # Executor files — one per command
    ├── command-a.md
    ├── command-b.md
    └── command-c.md
```

Skills without subcommands (e.g., `excalidraw-diagram`, `validate`, `create-skills`) may omit the `commands/` directory entirely. Their `SKILL.md` acts as both orchestrator and executor.

---

## SKILL.md Template

A SKILL.md should contain exactly these sections:

```markdown
# {Skill Name} Skill

> One-line description.

## Global Rules
- Rule 1 (applies to ALL commands)
- Rule 2

## Routing Table

| Command | File | Agent | Purpose |
|---|---|---|---|
| `/command-a` | `commands/command-a.md` | `agent-path` | Brief description |
| `/command-b` | `commands/command-b.md` | `agent-path` | Brief description |

## Execution Flow
1. Read this SKILL.md
2. Match the user's command against the routing table
3. Load the matched command file
4. Load the assigned agent
5. Execute per the command file's process

## Cross-Command Escalation
- When to escalate between commands or to workflow agents
```

**What goes in SKILL.md:**
- Global rules that apply to every command in the skill
- The routing table mapping commands to files, agents, and KBs
- Cross-command escalation logic
- Shared dependencies (grounding.md, routing.json)

**What does NOT go in SKILL.md:**
- Per-command process steps
- Per-command quality gates
- Per-command output templates
- Examples specific to a single command

---

## routing_skill.json

The `routing_skill.json` file provides a machine-readable version of the SKILL.md routing table. It enables programmatic command dispatch and tooling integration.

### Schema

```json
{
  "skill": "skill-name",
  "priority": "high | medium | low",
  "commands": {
    "/command-name": {
      "file": "commands/command-name.md",
      "agent": ".github/agents/{category}.{name}.agent.md",
      "kb": [".github/kb/{domain}/quick-reference.md"],
      "input": "Description of expected input",
      "output": "Description of expected output"
    }
  },
  "conditions": [
    "When this skill should activate"
  ],
  "dependencies": [
    ".github/config/grounding.md",
    ".github/config/routing.json"
  ]
}
```

### Fields

| Field | Required | Description |
|---|---|---|
| `skill` | Yes | Skill folder name |
| `priority` | Yes | Execution priority when multiple skills match |
| `commands` | Yes | Map of command names to their routing metadata |
| `commands.*.file` | Yes | Path to the command executor file, relative to the skill folder |
| `commands.*.agent` | Yes | Path to the agent that executes this command |
| `commands.*.kb` | No | Array of KB quick-reference paths to load |
| `commands.*.input` | Yes | Human-readable description of expected input |
| `commands.*.output` | Yes | Human-readable description of expected output |
| `conditions` | Yes | Array of natural-language conditions for skill activation |
| `dependencies` | Yes | Array of files that must be loaded before the skill runs |

### Current Inventory

Five skills have `routing_skill.json`:

| Skill | Commands Routed |
|---|---|
| `workflow-commands` | 8 |
| `core-commands` | 5 |
| `data-engineering` | 8 |
| `knowledge` | 3 |
| `review` | 2 |

Skills without routing files (`visual-explainer`, `excalidraw-diagram`, `validate`, `create-skills`) either have no subcommands or handle routing internally in SKILL.md.

---

## Command File Standard Pattern

Every command file under `commands/` must include these sections:

```markdown
# /command-name

> One-line purpose.

## Usage
\`\`\`text
/{skill-name} /command-name <arguments>
\`\`\`

## Process
1. Step-by-step execution instructions
2. What to load, validate, and produce

## Quality Gates
- [ ] Gate 1: specific pass/fail criterion
- [ ] Gate 2: specific pass/fail criterion

## Output
Description or template of the expected output artifact.

## Next Step
What the user should do after this command completes.
Typically the next SDD phase or a related command.

## See Also
- Links to related commands, agents, or KB domains
```

### Section Purpose

| Section | Purpose |
|---|---|
| **Usage** | Exact invocation syntax with argument placeholders |
| **Process** | Numbered steps the agent follows — the command's algorithm |
| **Quality Gates** | Checkboxes the agent must verify before declaring success |
| **Output** | What artifact is produced and where it is written |
| **Next Step** | Guides the user to the logical next action |
| **See Also** | Cross-references for discovery and navigation |

---

## Quality Gates as a First-Class Concept

Quality gates are not optional annotations — they are enforcement points that block progression:

1. **Command-level gates** — defined in each command file. The agent must verify all gates before producing output.
2. **Agent-level gates** — defined in the agent's `.agent.md` file. These apply regardless of which command invoked the agent.
3. **Workflow-level gates** — defined in `WORKFLOW_CONTRACTS.yaml`. These gate SDD phase transitions.
4. **Validation gates** — the Phase 3.5 Validate step runs four specialized crews and produces a weighted score. Score ≥ 90 with 0 CRITICAL → RUNBOOK; otherwise → ROADMAP.

Gates compose: a Build command must satisfy its own gates, the assigned specialist agent's gates, and the workflow contract's exit criteria.

---

## Agent Delegation Pattern

Skills delegate execution to agents defined under `.github/agents/`. The delegation chain:

```text
User invokes /{skill} /{command}
  → SKILL.md routing table identifies the agent
  → routing_skill.json confirms agent path and required KB
  → Command file is loaded as the executor
  → Agent file is loaded for quality gates and stop conditions
  → KB quick-reference is loaded if declared
  → Agent executes the command's process steps
  → Evidence is collected against quality gates
```

### Build-Phase Delegation

During `/workflow-commands /build`, the `build-agent` reads the DESIGN manifest and delegates individual files to specialist agents using `@{agent-name}` assignments. Each specialist:

- Reads its own agent file from `.github/agents/` (flat: `{category}.{name}.agent.md`)
- Loads its declared KB domain
- Executes under its own quality gates
- Reports evidence back to `BUILD_REPORT_{FEATURE}.md`
- Writes output under `projects/{feature-name}/`

---

## Cross-Command Escalation

Some commands naturally chain into others. The escalation rules are defined in SKILL.md's global rules section:

- **Workflow chaining:** `/brainstorm` → `/define` → `/design` → `/build` → `/validate` → `/ship`
- **Iteration:** Any phase can escalate to `/iterate` when changes affect upstream documents
- **Review escalation:** `/review` can escalate to `/judge` for high-risk or critical findings
- **KB lifecycle:** `/create-kb` → `/update-kb` → `/refresh-stale-kbs`

Escalation is always suggested via the **Next Step** section — it is never automatic.

---

## Reference Implementation: visual-explainer

The `visual-explainer` skill is the model implementation for the orchestrator/executor architecture:

- **SKILL.md:** 330 lines — includes global rules, 8 command routing entries, shared HTML requirements, and cross-command escalation
- **Commands:** 8 self-contained executor files under `commands/`
- **No routing_skill.json:** Routing is handled entirely within SKILL.md (acceptable for skills with stable command sets)
- **Quality gates:** Each command defines its own output validation criteria
- **Agent delegation:** Commands reference the appropriate agent for visual generation

Use `visual-explainer` as a template when creating new skills with multiple commands.

---

## Refactoring Metrics

The skill architecture was formalized through a comprehensive refactoring of all 9 skills:

### SKILL.md Deduplication Results

| Skill | Before | After | Reduction |
|---|---|---|---|
| workflow-commands | 1,465 lines | ~140 lines | **-90%** |
| core-commands | 871 lines | ~63 lines | **-93%** |
| data-engineering | 349 lines | ~80 lines | **-77%** |
| knowledge | 195 lines | ~106 lines | **-46%** |

### Refactoring Actions

- **5 skills refactored:** workflow-commands, core-commands, data-engineering, knowledge, review
- **1 skill completed:** review/judge command created
- **1 skill populated:** create-skills SKILL.md with global rules
- **2 skills confirmed clean:** visual-explainer, excalidraw-diagram
- **Path fixes applied:** All `.agents/`, `.claude/`, `GEMINI.md` references replaced with `.github/` paths
- **Empty commands populated:** knowledge/update-kb.md, knowledge/refresh-stale-kbs.md
- **routing_skill.json created:** For 5 skills with subcommands

### Migration History

The skill system evolved through three platform phases:

1. **`.claude/` era** — Skills were defined using Claude-specific conventions with `#skill:` invocation syntax
2. **`.agents/` era** — Migrated to a generic agents directory with mixed invocation patterns
3. **`.github/` era (current)** — All skills, agents, KB, and config live under `.github/` with slash-folder invocation (`/{skill-folder} /{command}`)

All legacy path references (`.claude/`, `.agents/`, `GEMINI.md`) have been purged from skill files.

---

## Skill Inventory

| Skill | Status | SKILL.md Lines | Commands | routing_skill.json |
|---|---|---|---|---|
| `workflow-commands` | ✅ refactored | ~140 | 8 | ✅ |
| `core-commands` | ✅ refactored | ~63 | 5 | ✅ |
| `data-engineering` | ✅ refactored | ~80 | 8 | ✅ |
| `knowledge` | ✅ refactored | ~106 | 3 | ✅ |
| `review` | ✅ completed | ~64 | 2 | ✅ |
| `visual-explainer` | ✅ clean | 330 | 8 | — |
| `excalidraw-diagram` | ✅ clean | 552 | 0 | — |
| `validate` | ✅ enhanced | ~110 | 0 (Python CLI) | — |
| `create-skills` | ✅ populated | ~45 | 0 (scaffold) | — |

---

## Creating a New Skill

1. Create the skill folder: `.github/skills/{skill-name}/`
2. Write `SKILL.md` following the template above — global rules and routing table only
3. Create `commands/` directory with one `.md` file per command
4. Each command file must include: Usage, Process, Quality Gates, Output, Next Step, See Also
5. Create `routing_skill.json` if the skill has 2+ subcommands
6. Register the skill in `.github/copilot-instructions.md` and `AGENTS.md`
7. Add a reference doc under `docs/reference/skills/`
8. Run workspace validation to confirm inventory counts

Use `/create-skills` to scaffold the initial structure automatically.
