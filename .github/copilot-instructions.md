# AgentSpec Copilot Instructions

This repository is an AgentSpec runtime for GitHub Copilot. Treat `.github/` as the operating system for the workspace: grounding, routing, skills, agents, knowledge bases, and SDD workflow artifacts all live there.

## Mandatory Grounding

**Before any operational response, read `.github/config/grounding.md`.** It owns all detailed rules: permissions policy, token budget strategy, skill priority, SDD lifecycle, pre-commit security gate, and commit rules.

Every operational response must start with:

```markdown
> **Specialist Activated:** `[Agent Name]`
> **Path:** `[Agent Path]`
>
> **Execution Grounding**
>
> | Property | Value |
> |---|---|
> | Router | `✓` |
> | Skill | `<name\|none>` |
> | Active Agent | `<name\|N/A>` |
> | Knowledge Base | `<domain\|none>` |
> | Files Loaded | `<n>` |
> | Detected Project | `<detected name\|none>` |
> | Execution Tier | `CRITICAL \| IMPORTANT \| STANDARD` |
> | Prompt Tokens | `~<estimate>` |
```

## Skill Invocation

```text
/<skill-folder> /<command> <args>
```

| Skill | Entry Command |
|---|---|
| `workflow-commands` | `/workflow-commands /define`, `/design`, `/build`, `/validate`, `/ship`, `/iterate`, `/brainstorm` |
| `data-engineering-commands` | `/data-engineering-commands /pipeline`, `/schema`, `/sql-review` |
| `knowledge-commands` | `/knowledge-commands /create-kb`, `/update-kb` |
| `review-commands` | `/review-commands /review`, `/judge` |
| `visual-explainer` | `/visual-explainer /generate-web-diagram` |
| `core-commands` | `/core-commands /status`, `/memory` |
| `create-skills` | `/create-skills` |

Do not use `.claude/`, `/agentspec:*`, `#skill:*`, or `skill:*` conventions.

## SDD Workflow

SDD phases can only be started via `/workflow-commands`. Respond with the exact command if asked in natural language.

| Phase | Command | Agent |
|---|---|---|
| 0 — Brainstorm | `/workflow-commands /brainstorm` | `workflow.brainstorm-agent` |
| 1 — Define | `/workflow-commands /define` | `workflow.define-agent` |
| 2 — Design | `/workflow-commands /design` | `workflow.design-agent` |
| 3 — Build | `/workflow-commands /build` | `workflow.build-agent` |
| 3.5 — Validate | `/workflow-commands /validate` | `workflow.validate-agent` |
| 4 — Ship | `/workflow-commands /ship` | `workflow.ship-agent` |
| Cross-phase | `/workflow-commands /iterate` | `workflow.iterate-agent` |

## Runtime Inventory

- **63 agents** + DEFAULT under `.github/agents/` (flat layout, dot-prefixed categories)
- **7 skills** under `.github/skills/`
- **26 KB domains** under `.github/kb/`
- Router, grounding, and security settings under `.github/config/`
- SDD templates, features, and archives under `.github/sdd/`

See `AGENTS.md` for full inventory, build delegation patterns, and structure details.

## Security Gate

Before suggesting `git commit`, **always** delegate to `dev.security-guardian` to run `pre-commit run --all-files`. CRITICAL findings (secrets, credentials, private keys) block the commit. See grounding.md → Regras for the full policy.

## Git Commit Trailer

Always include this trailer in commit messages:

```
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```
