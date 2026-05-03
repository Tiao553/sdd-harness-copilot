---
name: update-context
description: Update context files for an existing project — full file or targeted section
---

# Update Context Command

> Update one or more context files for an existing project. Supports full file update or targeted section edit.

## Usage

```bash
/knowledge-context-commands /update-context <slug>
/knowledge-context-commands /update-context <slug> --file <filename>
/knowledge-context-commands /update-context <slug> --file architecture.md
/knowledge-context-commands /update-context <slug> --set-active
```

**Examples**:
```bash
/knowledge-context-commands /update-context my-api
/knowledge-context-commands /update-context data-platform --file architecture.md
/knowledge-context-commands /update-context mobile-app --file rules.md
/knowledge-context-commands /update-context my-api --set-active
```

---

## What Happens

1. **Load current state**
   - Read `_registry.yaml` and verify the slug exists
   - If `--file` specified: load only that file
   - If not specified: load `KNOWLEDGE_CONTEXT.md` + list existing files and ask which one to update

2. **Identify changes**
   - Show current content of the file(s)
   - Ask what needs to be updated (field, section, or full file)
   - Classify impact: Additive (new field) / Modifying (change existing) / Architectural (stack or structure change)

3. **Apply update**
   - Edit the specified fields/sections
   - Update the `Last Updated: YYYY-MM-DD` field in `KNOWLEDGE_CONTEXT.md`
   - If `--set-active`: update `active_project` in `_registry.yaml`

4. **Cascade check**
   - If `deployment_context` or stack changed: warn that in-progress features (BRAINSTORM/DEFINE/DESIGN) may need `/iterate`

5. **Report**
   - List modified fields
   - Indicate whether a cascade was detected

---

## Quality Gates

Before updating:

- Slug must exist in `_registry.yaml`.
- Architectural changes (stack, cloud, structure) must be confirmed before applying.
- `Last Updated` field must be updated on every edit to `KNOWLEDGE_CONTEXT.md`.

---

## Output

```text
Knowledge Context Updated: .github/knowledge_context/{slug}/
Changes:
  ✅ {filename} — {changed fields}

Last Updated: YYYY-MM-DD

Cascade Warning (if applicable):
  ⚠️  deployment_context changed — review in-progress BRAINSTORM/DEFINE/DESIGN with /iterate
```

---

## Next Step

`/knowledge-context-commands /check-context {slug}` — to confirm the context is complete after the update.

## See Also

- **Registry**: `.github/knowledge_context/_registry.yaml`
- **Iterate command**: `.github/skills/workflow-commands/commands/iterate.md`
- **Design**: `.github/sdd/features/knowledge-context/DESIGN_KNOWLEDGE_CONTEXT.md`
