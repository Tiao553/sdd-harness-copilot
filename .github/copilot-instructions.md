# AgentSpec Copilot Instructions

This repository is an AgentSpec runtime for GitHub Copilot. Treat `.github/` as the operating system for the workspace: grounding, routing, skills, agents, knowledge bases, and SDD workflow artifacts all live there.

## Mandatory Grounding

Before any operational response:

1. Read `.github/config/grounding.md`.
2. If the user invokes `/<skill-folder>`, read `.github/skills/<skill-folder>/SKILL.md` first.
3. If no skill is invoked, read `.github/config/routing.json` and select the route by intent.
4. Read the selected agent file.
5. Load only the route quick-reference KB unless the skill or agent explicitly requires more.
6. Check `_meta/STATUS.md` and `_meta/CONTEXT.md` when present.

Every operational response must start with this block:

```markdown
> **Specialist Activated:** `[Agent Name]`  
> **Path:** `[Agent Path]`
>
> **Execution Grounding**W
>
> | Property | Value |
> |---|---|
> | Router | `✓` |
> | Skill | `<nome\|none>` |
> | Active Agent | `<nome\|N/A>` |
> | Knowledge Base | `<dominio\|none>` |
> | Files Loaded | `<n>` |
> | Detected Project | `<nome detectado\|none>` |
> | Execution Tier | `CRÍTICO \| IMPORTANTE \| PADRÃO` |
> | Prompt Tokens | `~<estimativa>` |W
```

## Invocation Rules

Skills are invoked by folder name:

```text
/<skill-folder> /<command> <args>
```

Use these formats:

```text
/workflow-commands /define ...
/workflow-commands /design ...
/workflow-commands /build ...
/workflow-commands /validate ...
/data-engineering-commands /schema ...
/knowledge-commands /create-kb ...
/review-commands /judge ...
/visual-explainer /generate-web-diagram ...
/core-commands /status
```

Do not use `.claude/`, `/agentspec:*`, `#skill:*`, or `skill:*` conventions.

## Workflow Control

SDD workflow phases can only be started by `/workflow-commands`.

If the user asks in natural language to run a workflow phase, answer with the exact command they should run. Do not start the phase implicitly.

| Phase | Command | Agent |
|---|---|---|
| Brainstorm | `/workflow-commands /brainstorm` | `brainstorm-agent` |
| Define | `/workflow-commands /define` | `define-agent` |
| Design | `/workflow-commands /design` | `design-agent` |
| Build | `/workflow-commands /build` | `build-agent` |
| Validate | `/workflow-commands /validate` | `validate-agent` |
| Ship | `/workflow-commands /ship` | `ship-agent` |
| Iterate | `/workflow-commands /iterate` | `iterate-agent` |

## Runtime Inventory

- 62 agents + DEFAULT.AGENT.md under `.github/agents/` (flat layout, dot-prefixed categories)
- 8 skills under `.github/skills/`
- 26 KB domains under `.github/kb/`
- Router and grounding under `.github/config/`
- SDD templates, features, architecture contracts, and archives under `.github/sdd/`

## Agent Behavior

Use the routed agent as the active specialist. Follow that agent's quality gates, stop conditions, and escalation rules.

Build work may delegate to specialist agents through Copilot's built-in `agent` tool and `runSubagent`. When delegating, pass the target artifact, purpose, relevant DESIGN context, required KB references, quality gates, and expected evidence.

## Local Copilot Configuration

This workspace ports the Antigravity `.gemini` local setup to Copilot/VS Code:

- MCP servers live in `.vscode/mcp.json`.
- `context7` is for current framework and API documentation lookup.
- `sequential-thinking` is for structured planning, debugging, and complex analysis.
- `github` is for repository, pull request, issue, and code search integration.
- Secrets must stay outside version control. Use `.env` for `GITHUB_PERSONAL_ACCESS_TOKEN`.

### Execution Policy

Copilot must read `.github/config/security-settings.json` when present and enforce its full `permissions` policy before command execution:

- `permissions.alwaysAllow`: safe inspection, read-only discovery, and local validation commands.
- `permissions.alwaysAsk`: state-changing, dependency-changing, Git history, deployment, Docker lifecycle, and file-moving commands.
- `permissions.alwaysDeny`: destructive filesystem operations, high-risk database operations, force-push/reset/clean, package unpublish, system/service/registry/process termination commands.

If a command is ambiguous or appears in multiple categories by partial match, apply the most restrictive category. For chained commands, evaluate each segment and apply the most restrictive category to the whole execution.

## Knowledge Base Policy

Use KB lazily:

1. Prefer `.github/kb/{domain}/quick-reference.md`.
2. Load `index.md`, `concepts/`, `patterns/`, or `specs/` only when the quick reference is insufficient.
3. Never load an entire KB domain by default.
4. For external or version-sensitive technology decisions, validate against current official docs when the skill or agent requires it.

## Documentation Policy

Keep public documentation focused on AgentSpec: runtime architecture, skill commands, agents, KB domains, workflow phases, routing, validation, and extension points.

README should stay concise. Detailed inventories and walkthroughs belong under `docs/`.

## Validation

Use `python3`, not `python`:

```bash
find .github/agents -name "*.agent.md" | wc -l
find .github/kb -name "quick-reference.md" | wc -l
find .github/skills -maxdepth 2 -iname "SKILL.md" | sort
python3 -m json.tool .github/config/routing.json
python3 -m pytest tests
```
