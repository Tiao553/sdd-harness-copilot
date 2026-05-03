# Global Grounding — GitHub Copilot AgentSpec

Before any operational response in this workspace:

1. Read this grounding page.
2. If the message invokes `/<name>`, the skill takes priority over intent-based routing:
   - Read `.github/skills/<name>/SKILL.md` before choosing an agent.
   - Execute the grounding sequence defined by the skill itself.
   - Use `routing.json` only when the skill requires it or when resolving a complementary agent.
3. If there is no `/<name>`, read `.github/config/routing.json` — identify the correct agent by intent.
4. Read the agent file identified at `routes[n].agent`.
5. If the task is technical, load **only** `routes[n].kb` (quick-reference).
   - Load `routes[n].kb_full` only if the quick-reference is insufficient.
   - Maximum 3 KB files per request.
6. Read `.github/config/security-settings.json` when present and apply the permissions policy before executing commands or modifying files.
7. Check `_meta/STATUS.md` and `_meta/CONTEXT.md` in the current directory or ancestors.
8. **Load Knowledge Context for the active project:**
   - Read `.github/knowledge_context/_registry.yaml` (if it exists)
   - Identify `active_project` — if empty or file absent, skip without blocking
   - Read `.github/knowledge_context/{active_project}/KNOWLEDGE_CONTEXT.md`
   - Glob `.github/knowledge_context/{active_project}/*.md` → load existing optional files (maximum 4 total)
   - Inject `deployment_context` and `business_context` into the operational grounding block as `Detected Project`
9. If no route matches, use `default_agent` from routing.json.

## Mandatory Permissions Policy

When `.github/config/security-settings.json` exists, it is a mandatory part of the operational grounding.

The agent must apply `permissions` as an execution gate:

- `alwaysAllow`: commands and tools considered safe for inspection, local validation, and reading. Can be executed without requesting new confirmation, respecting the active sandbox.
- `alwaysAsk`: commands that change state, dependencies, Git history, environment, containers, or files outside controlled edits. Must request explicit approval before executing.
- `alwaysDeny`: destructive commands, high-risk database operations, irreversible Git cleanup, force push/reset, dangerous system changes, services, registry, or processes. Must be refused unless the user explicitly requests with precise scope and an additional confirmation.

Application rules:

- The match must consider the full command and its arguments, not just the binary.
- When in doubt between categories, use the most restrictive category.
- Chained commands must be evaluated per segment; if any segment falls under `alwaysAsk` or `alwaysDeny`, the entire execution must follow the most restrictive category.
- The policy does not replace the sandbox, environment approvals, or agent security rules; it adds a mandatory layer.
- Manual edits via editing tools follow the same intent: edits within the workspace are allowed when they are part of the task; destructive edits, broad reversions, or removals must be treated as `alwaysAsk` or `alwaysDeny` based on risk.

## Skill Priority

When the input contains `/<name>`, the corresponding `SKILL.md` is the primary execution source. The agent route cannot override skill instructions.

Mandatory order with skill:

```text
1. grounding.md
2. .github/skills/<name>/SKILL.md
3. Files/agents/KB required by the skill
4. .github/config/security-settings.json when present
5. routing.json only if the skill requires additional routing
```

If the cited skill does not exist at `.github/skills/<name>/SKILL.md`, stop and report the missing path. Do not execute the flow as a generic request.

## SDD Workflow Initialization

SDD workflow phases (`/brainstorm`, `/define`, `/design`, `/build`, `/validate`, `/ship`, `/iterate`, `/create-pr`) can only be initialized via:

```text
/workflow-commands /<phase> ...
```

Natural language requests such as "do the build", "run the design", "ship this feature", or "create the define phase" must be treated as incomplete intent. Respond with the exact expected command and do not start the phase.

Exception: it is allowed to directly edit SDD documents when the user requests a specific change to a named file, without starting a workflow phase.

Every operational response must begin with:

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

## Token Budget Strategy

| Situation | Action |
|---|---|
| Simple conceptual question | Only `quick-reference.md` from the relevant KB |
| Implementation with known pattern | `quick-reference.md` + specific pattern file |
| Complex implementation / new domain | `index.md` + up to 3 files from `concepts/` or `patterns/` |
| Multi-domain task | `quick-reference.md` from each domain (max 3 domains) |
| Large Task / full SDD | Use `the-planner` to break into subtasks with individual budgets |

Never load an entire KB directory in a single call.
Always declare loaded files in the operational grounding block.

## Rules

- Do not respond from memory without reading the required files
- Do not skip the grounding block in operational responses
- Do not ignore `/<name>`; skill takes priority over intent-based routing
- Do not start SDD phases without `/workflow-commands /<phase>`
- Do not assume project context without checking `_meta/` and `.github/knowledge_context/_registry.yaml`
- Do not load full KB when quick-reference is sufficient
- Do not start BUILD without SDD gates verified when applicable
- Always prefer `COPILOT.md` as the canonical source if there is a conflict
- **Before suggesting `git commit`, always run `pre-commit run --all-files` as a security gate** — CRITICAL findings block the commit; delegate to `dev.security-guardian` when the context involves commits, secrets, or code auditing
