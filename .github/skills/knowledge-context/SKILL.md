---
name: knowledge-context-commands
description: 'AgentSpec commands for managing project knowledge context. Use /knowledge-context-commands + intent. Reads .github/config/grounding.md before executing. Commands: /create-context, /update-context, /check-context'
license: MIT
compatibility: 'GitHub Copilot VS Code, GitHub Copilot cloud agent'
metadata:
  version: "1.0.0"
  category: commands
  migrated-from: '.github/skills/knowledge-context/'
---

# Knowledge Context Commands

> Invoke: `/knowledge-context-commands` + task description

## Mandatory Global Rules

These rules apply to all commands in this skill. If there is a conflict with migrated legacy blocks, this section wins.

### Grounding and Agent

1. Before executing any command, read `.github/config/grounding.md`.
2. Read `.github/config/routing.json`; if no specific route matches, execute directly without delegating to a specialist agent.
3. Load only the necessary context files from `.github/knowledge_context/{slug}/`; never load all projects at once.
4. Every operational response must begin with the `[GROUNDING]` block required by `.github/config/grounding.md`.

### Canonical Paths

| Type | Correct path |
|---|---|
| Registry | `.github/knowledge_context/_registry.yaml` |
| Templates | `.github/knowledge_context/_templates/` |
| Root context | `.github/knowledge_context/{slug}/KNOWLEDGE_CONTEXT.md` |
| Architecture | `.github/knowledge_context/{slug}/architecture.md` |
| Rules | `.github/knowledge_context/{slug}/rules.md` |
| Roadmap | `.github/knowledge_context/{slug}/roadmap.md` |
| Glossary | `.github/knowledge_context/{slug}/domain-glossary.md` |
| Integrations | `.github/knowledge_context/{slug}/integrations.md` |

### Minimum Knowledge Context Structure

```text
.github/knowledge_context/{slug}/
├── KNOWLEDGE_CONTEXT.md     ← required
├── architecture.md          ← recommended
├── rules.md                 ← recommended
├── roadmap.md               ← optional
├── domain-glossary.md       ← optional
└── integrations.md          ← optional
```

Create files from `.github/knowledge_context/_templates/`:

| Output | Template |
|---|---|
| `KNOWLEDGE_CONTEXT.md` | `_templates/KNOWLEDGE_CONTEXT.md` |
| `architecture.md` | `_templates/architecture.md` |
| `rules.md` | `_templates/rules.md` |
| `roadmap.md` | `_templates/roadmap.md` |
| `domain-glossary.md` | `_templates/domain-glossary.md` |
| `integrations.md` | `_templates/integrations.md` |
| registry entry | `_registry.yaml` field `projects[]` |

If `.github/knowledge_context/_registry.yaml` does not exist, create it with a base structure before registering the first project. If it exists, update only the entry for the impacted project.

## Available Commands

| Command | Description | File |
|---|---|---|
| `/create-context` | Create a complete knowledge context for a project | `commands/create-context.md` |
| `/update-context` | Update context files for an existing project | `commands/update-context.md` |
| `/check-context` | Audit the active knowledge context and report gaps | `commands/check-context.md` |

### Escalation

- If `/create-context` reveals a conflict with an existing slug, ask before overwriting.
- If `/update-context` reveals a large architectural change, propose a plan before editing multiple files.
- If `/check-context` detects `active_project` pointing to a non-existent slug, fix the registry before continuing.

## See Also

- **Registry**: `.github/knowledge_context/_registry.yaml`
- **Templates**: `.github/knowledge_context/_templates/`
- **Design**: `.github/sdd/features/knowledge-context/DESIGN_KNOWLEDGE_CONTEXT.md`
