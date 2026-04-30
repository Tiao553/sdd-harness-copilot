---
description: "Use this agent when the user needs a cross-model second opinion on code correctness, schema migrations, IAM policies, or high-risk outputs.\n\nTrigger phrases include:\n- 'judge this file'\n- 'get a second opinion'\n- 'review with external model'\n\nExamples:\n- User says 'judge this migration file' → invoke this agent to send the file for external model review and return a PASS/FAIL verdict\n- User asks 'get a second opinion on this Terraform module' → invoke this agent to validate correctness via OpenRouter"
name: dev.judge-agent
tools: ['shell', 'read', 'search', 'edit', 'task', 'skill', 'web_search', 'web_fetch', 'ask_user']
---

## Grounding

Antes de responder, ler `@.github/config/grounding.md`.
KB deste agente: none. Grounding global: `@.github/config/grounding.md`

---

# Judge Command (V0)

> Get a second opinion from a non-GitHub Copilot model on code or content GitHub Copilot just produced.

## Usage

```bash
/review-commands /judge <file>                              # Judge a file with default model
/review-commands /judge <file> --context "building DLT CDC" # Add context about the task
/review-commands /judge <file> --model anthropic/claude-3.5-sonnet  # Override model (still via OpenRouter)
/review-commands /judge --ledger                             # Show today's budget usage
```

---

## What This Command Does

Sends the target file + optional task context to a non-GitHub Copilot model via OpenRouter. That model returns a structured verdict:

| Field | Meaning |
|-------|---------|
| **Verdict** | `PASS` (no high-severity issues, confidence ≥ 0.70) or `FAIL` |
| **Confidence** | 0.0 – 1.0, judge's own self-assessment |
| **Summary** | One-sentence gist |
| **Concerns** | Table of issues (severity + evidence citing line numbers or quoted strings) |
| **Suggested fixes** | Concrete repairs |

The verdict renders as markdown in the chat. A ledger entry goes to `.github/storage/judge-ledger.jsonl`.

---

## When to Use

**Good fits:**
- Schema migrations or DDL you're about to run
- IAM / RLS policies — security-sensitive
- Complex SQL that touches production data
- Terraform / CloudFormation before apply
- Any output where "confidently wrong" would be expensive

**Skip it for:**
- Trivial edits, renames, formatting
- Documentation prose (judge is tuned for code/config correctness)
- Anything under ~20 lines (not enough signal)

The judge is **advisory**. GitHub Copilot is the author; you make the final call.

---

## Setup

```bash
# One-time: get an OpenRouter key at https://openrouter.ai/keys
export OPENROUTER_API_KEY=sk-or-v1-...

# Optional: change default model (default is openai/gpt-4o-mini — cheap + capable)
export JUDGE_MODEL=openai/gpt-4o

# Optional: change daily budget ceiling (default 10 calls/day)
export JUDGE_BUDGET=25
```

Full setup guide: `docs/getting-started/judge-setup.md`

---

## Examples

### Example 1: Judge a schema migration

```bash
/review-commands /judge migrations/2026_04_20_add_user_roles.sql --context "Postgres migration adding role column with backfill"
```

Returns a PASS/FAIL on whether the migration handles concurrency, nullability, and indexing properly.

### Example 2: Judge a Terraform module

```bash
/review-commands /judge infra/iam/s3_writer_role.tf --context "Least-privilege role for Lambda writing to S3 bucket"
```

### Example 3: See what you've used today

```bash
/review-commands /judge --ledger
```

Output:
```
Judge Ledger — .github/storage/judge-ledger.jsonl
  Today (2026-04-20):  3 / 10 calls
  All-time:            17 calls

  Today's calls:
    [PASS] openai/gpt-4o-mini  migrations/2026_04_20_add_user_roles.sql
    [FAIL] openai/gpt-4o-mini  infra/iam/s3_writer_role.tf
    [PASS] openai/gpt-4o-mini  models/staging/stg_orders.sql
```

---

## Execution

The command delegates to an external judge runtime when one is configured:

```bash
judge-runner "$ARGUMENTS"
```

If no judge runtime is configured, report the missing prerequisite and do not fabricate a judge result.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Verdict = PASS |
| 1 | Verdict = FAIL |
| 2 | Config error (missing key, bad args) |
| 3 | Daily budget exhausted |
| 4 | Network / OpenRouter API error |

Non-zero exit codes let this command compose into shell pipelines and CI later.

---

## Roadmap

This is **V0** — opt-in, per-file, single model. Future versions:

- **V1** — graduates to a `--judge[=model]` flag on `/workflow-commands /design`, `/workflow-commands /build`, `/workflow-commands /ship` once the Flag System ships
- **V2** — multi-model ensembles (`--judge=ensemble` queries GPT + Gemini, requires consensus)
- **V3** — opt-in PostToolUse hook for specific file patterns
- **V4** — MCP server wrapper + high-stakes classifier using agent tier signal

See `tasks/backlog.md` → Judge Layer via OpenRouter for the full roadmap.
