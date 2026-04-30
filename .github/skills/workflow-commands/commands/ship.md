---
name: ship
description: Archive completed feature with lessons learned (Phase 4)
---

# Ship Command

> Archive completed feature with lessons learned (Phase 4)

## Usage

```bash
/workflow-commands /ship <define-file>
```

## Examples

```bash
/workflow-commands /ship .github/sdd/features/notification-system/DEFINE_NOTIFICATION_SYSTEM.md
/workflow-commands /ship DEFINE_USER_AUTH.md
```

---

## Overview

This is **Phase 4** of the 5-phase AgentSpec workflow:

```text
Phase 0: /workflow-commands /brainstorm → .github/sdd/features/{feature-name}/BRAINSTORM_{FEATURE}.md (optional)
Phase 1: /workflow-commands /define     → .github/sdd/features/{feature-name}/DEFINE_{FEATURE}.md
Phase 2: /workflow-commands /design     → .github/sdd/features/{feature-name}/DESIGN_{FEATURE}.md
Phase 3: /workflow-commands /build      → Code in ./projects/{feature-name}/ + .github/sdd/features/{feature-name}/BUILD_REPORT_{FEATURE}.md
Phase 3.5: /workflow-commands /validate → .github/sdd/features/{feature-name}/VALIDATION_REPORT_{FEATURE}.md
Phase 4: /workflow-commands /ship       → .github/sdd/archive/{feature-name}/SHIPPED_{DATE}.md (THIS COMMAND)
```

The `/workflow-commands /ship` command archives all feature artifacts and captures lessons learned.

---

## What This Command Does

1. **Verify** - Confirm all artifacts exist and build passed
2. **Archive** - Move feature documents to archive folder
3. **Document** - Create SHIPPED summary with lessons learned
4. **Clean** - Remove working files from features folder

---

## Process

### Step 1: Verify Completion

```markdown
Read(.github/copilot-instructions.md)
Read(.github/sdd/features/{feature-name}/DEFINE_{FEATURE}.md)
Read(.github/sdd/features/{feature-name}/DESIGN_{FEATURE}.md)
Read(.github/sdd/features/{feature-name}/BUILD_REPORT_{FEATURE}.md)
Read(.github/sdd/features/{feature-name}/VALIDATION_REPORT_{FEATURE}.md)
Read(.github/sdd/features/{feature-name}/RUNBOOK_{FEATURE}.md)

# Verify build report shows success and validation score >= 90
```

### Step 2: Create Archive Folder

```bash
mkdir -p .github/sdd/archive/{feature-name}/
```

### Step 3: Copy Artifacts to Archive

```bash
cp .github/sdd/features/{feature-name}/DEFINE_{FEATURE}.md .github/sdd/archive/{feature-name}/
cp .github/sdd/features/{feature-name}/DESIGN_{FEATURE}.md .github/sdd/archive/{feature-name}/
cp .github/sdd/features/{feature-name}/BUILD_REPORT_{FEATURE}.md .github/sdd/archive/{feature-name}/
cp .github/sdd/features/{feature-name}/VALIDATION_REPORT_{FEATURE}.md .github/sdd/archive/{feature-name}/
cp .github/sdd/features/{feature-name}/RUNBOOK_{FEATURE}.md .github/sdd/archive/{feature-name}/
```

### Step 4: Generate SHIPPED Document

Create summary with:

| Section | Content |
|---------|---------|
| **Summary** | What was built |
| **Timeline** | Start → Ship dates |
| **Metrics** | Lines of code, files created |
| **Lessons Learned** | What went well, what to improve |
| **Artifacts** | List of all archived documents |

### Step 5: Update Document Statuses

Update archived documents to "Shipped" status:

```markdown
Edit: .github/sdd/archive/{feature-name}/DEFINE_{FEATURE}.md
  - Status: → "✅ Shipped"
  - Add revision: "Shipped and archived"

Edit: .github/sdd/archive/{feature-name}/DESIGN_{FEATURE}.md
  - Status: → "✅ Shipped"
  - Add revision: "Shipped and archived"
```

### Step 6: Clean Up Working Files

```bash
rm -rf .github/sdd/features/{feature-name}/
```

### Step 7: Save SHIPPED Document

```markdown
Write(.github/sdd/archive/{feature-name}/SHIPPED_{DATE}.md)
```

---

## Output

| Artifact | Location |
|----------|----------|
| **SHIPPED** | `.github/sdd/archive/{feature-name}/SHIPPED_{DATE}.md` |
| **DEFINE** | `.github/sdd/archive/{feature-name}/DEFINE_{FEATURE}.md` |
| **DESIGN** | `.github/sdd/archive/{feature-name}/DESIGN_{FEATURE}.md` |
| **BUILD_REPORT** | `.github/sdd/archive/{feature-name}/BUILD_REPORT_{FEATURE}.md` |
| **VALIDATION_REPORT** | `.github/sdd/archive/{feature-name}/VALIDATION_REPORT_{FEATURE}.md` |
| **RUNBOOK** | `.github/sdd/archive/{feature-name}/RUNBOOK_{FEATURE}.md` |

**Next Step:** Start new feature with `/workflow-commands /define`

---

## Quality Gate

Before shipping, verify:

```text
[ ] BUILD_REPORT shows all tasks completed
[ ] No critical issues in build report
[ ] VALIDATION_REPORT exists with score >= 90 and 0 CRITICAL issues
[ ] RUNBOOK_{FEATURE}.md exists
[ ] All tests passing
[ ] Code deployed (if applicable)
```

---

## When to Ship

Ship when:
- All acceptance tests from DEFINE pass
- Build report shows 100% completion
- VALIDATION_REPORT shows score >= 90 with 0 CRITICAL issues
- No blocking issues remain

---

## Lessons Learned Categories

Document lessons in these areas:

| Category | Example |
|----------|---------|
| **Process** | "Breaking tasks into smaller chunks helped" |
| **Technical** | "Config files work better than env vars" |
| **Communication** | "Early clarification saved rework" |
| **Tools** | "Using X library simplified Y" |

---

## Tips

1. **Don't Skip This** - Lessons learned prevent future mistakes
2. **Be Honest** - Document what didn't work too
3. **Be Specific** - "Better planning" → "Create architecture diagram before coding"
4. **Archive Everything** - Future you will thank present you

---

## References

- Agent: `.github/agents/workflow.ship-agent.agent.md`
- Template: `.github/sdd/templates/SHIPPED_TEMPLATE.md`
- Contracts: `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- Previous Phase: `.github/skills/workflow-commands/commands/build.md`
