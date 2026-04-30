---
name: review-commands
description: 'AgentSpec review commands. Use /review-commands + command. Commands: /review, /judge'
license: MIT
compatibility: 'GitHub Copilot VS Code, GitHub Copilot cloud agent'
metadata:
  version: "1.0.0"
  category: commands
---

# Review Commands

Invoke as:

```text
/review-commands /review <file-or-directory>
/review-commands /judge <file> [--context "..."] [--model <openrouter-model>]
/review-commands /judge --ledger
```

## Grounding

1. Read `.github/config/grounding.md`.
2. Treat this skill as the primary routing source.
3. For `/review`, use `.github/agents/python.code-reviewer.agent.md`.
4. For `/judge`, use `.github/agents/dev.judge-agent.agent.md`.
5. Load only the KB files required by the selected agent or by the reviewed domain.

## /review

Use for code review, config review, migration review, and documentation review.

Execution:

1. Read the target file or directory.
2. Use the code-review stance: findings first, ordered by severity.
3. Cite concrete file paths and line numbers.
4. Include missing tests or residual risks.

## /judge

Use for a second opinion on high-risk or ambiguous output.

Execution:

1. Read `.github/agents/dev.judge-agent.agent.md`.
2. If the request targets a file, read the file before judging.
3. If an external judge runtime is configured and `OPENROUTER_API_KEY` is available, run that runtime.
4. If the runtime or key is missing, stop and report the missing prerequisite instead of inventing an external verdict.
5. Write ledger entries only to `.github/storage/judge-ledger.jsonl`.

## Comandos Disponíveis

| Comando | Descrição | Arquivo | Agente |
|---|---|---|---|
| `/review` | Code review com findings por severidade | `commands/review.md` | `code-reviewer` |
| `/judge` | Segunda opinião via judge runtime externo | `commands/judge.md` | `judge-agent` |

## Constraints

- Do not use `#skill:` or `skill:` syntax.
- Do not use `.claude/**` paths.
- Do not initiate SDD workflow phases from this skill.
