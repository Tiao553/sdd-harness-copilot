# DESIGN_COPILOT_MIGRATION

## Feature

Destructive migration from the Claude Code AgentSpec harness to the native GitHub Copilot layout.

## Source Of Truth

- `prompt-claude-to-copilot-v4.md`
- `CLAUDE.md`
- `.claude/agents/README.md`
- `.claude/skills/agent-router/routing.json`
- `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml`

## Target Architecture

Create `.github/` as the active Copilot runtime:

- `.github/copilot-instructions.md` bootstraps into `COPILOT.md`
- `.github/config/routing.json` maps intents to `.agent.md` files and minimal KB quick references
- `.github/config/grounding.md` defines the required `[GROUNDING]` block and token budget
- `.github/agents/*.agent.md` contains migrated agents with Copilot frontmatter and grounding sections (flat layout: `{category}.{name}.agent.md`)
- `.github/skills/**/SKILL.md` replaces Claude slash commands through `#skill:<name>`
- `.github/kb/**` contains copied KB domains with no skill wrapper
- `.github/workflows/copilot-sdd.yml` enables label-driven Copilot SDD issues

Preserve `.claude/sdd/` in place as the SDD artifact workspace.

## Agent Assignments

| Area | Agent | Responsibility |
|---|---|---|
| Overall migration sequencing | `architect/the-planner` | Enforce phase order and validation gates |
| Router and grounding | `dev/codebase-explorer` + `architect/the-planner` | Convert routing paths and define grounding protocol |
| Agents | category specialists | Preserve full source prompts while adding Copilot frontmatter and grounding |
| Commands to skills | workflow and domain agents | Consolidate command files into `SKILL.md` packs |
| KB migration | `kb-architect` | Copy KB domains exactly, no wrappers |
| Validation | `python/code-reviewer` | Run structural, JSON, and archive checks |

## Execution Plan

1. Create the `.github/` foundation without touching `.claude/`.
2. Migrate original skills and consolidate commands into Copilot skills.
3. Copy `.claude/kb/` into `.github/kb/`.
4. Convert every Claude agent to `.github/agents/{category}.{name}.agent.md`, including `judge-agent`.
5. Validate counts, required files, JSON, grounding blocks, and absence of incorrect command instruction files.
6. Rename `CLAUDE.md` to `COPILOT.md` and apply content substitutions.
7. Archive `.claude/agents`, `.claude/commands`, `.claude/skills`, `.claude/kb`, and `.claude/settings.json` into `.claude-archive/`, leaving `.claude/sdd/` intact.
8. Remove Claude-only archived scripts because they are not part of this Copilot runtime.
9. Run final validation after deactivation.

## Risks And Controls

| Risk | Control |
|---|---|
| Truncating agent or command content | Mechanical migration preserves full source bodies after generated headers |
| Moving SDD artifacts accidentally | Archive commands explicitly exclude `.claude/sdd/` |
| Creating wrong Copilot command mechanism | Commands become `#skill` packs only, no `.instructions.md` command files |
| Invalid router JSON | Validate with `python -m json.tool` before archive and after archive |
| Insufficient KB count | Validate quick-reference count and domain directory count |

## Acceptance Criteria

- `COPILOT.md` exists and `CLAUDE.md` does not.
- `.github/copilot-instructions.md`, `.github/config/routing.json`, and `.github/config/grounding.md` exist.
- `.github/agents` contains at least 60 `.agent.md` files.
- `.github/skills` contains migrated original skills, five command skills, and `sdd-templates`.
- `.github/kb` contains copied KB domains and no `SKILL.md`.
- `.claude/sdd/` remains intact.
- `.claude-archive/` contains the deactivated Claude runtime.
- No `scripts/archive/` runtime remains in the active repository.
