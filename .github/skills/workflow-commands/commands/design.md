---
name: design
description: Create architecture and technical specification (Phase 2)
---

# Design Command

> Create architecture and technical specification in one pass (Phase 2)

## Usage

```bash
/workflow-commands /design <define-file>
```

## Examples

```bash
/workflow-commands /design .github/sdd/features/notification-system/DEFINE_NOTIFICATION_SYSTEM.md
/workflow-commands /design DEFINE_USER_AUTH.md
/workflow-commands /design .github/sdd/features/search-api/DEFINE_SEARCH_API.md
```

---

## Overview

This is **Phase 2** of the 5-phase AgentSpec workflow:

```text
Phase 0: /workflow-commands /brainstorm → .github/sdd/features/{feature-name}/BRAINSTORM_{FEATURE}.md (optional)
Phase 1: /workflow-commands /define     → .github/sdd/features/{feature-name}/DEFINE_{FEATURE}.md
Phase 2: /workflow-commands /design     → .github/sdd/features/{feature-name}/DESIGN_{FEATURE}.md (THIS COMMAND)
Phase 3: /workflow-commands /build      → Code in ./projects/{feature-name}/ + .github/sdd/features/{feature-name}/BUILD_REPORT_{FEATURE}.md
Phase 3.5: /workflow-commands /validate → .github/sdd/features/{feature-name}/VALIDATION_REPORT_{FEATURE}.md
Phase 4: /workflow-commands /ship       → .github/sdd/archive/{feature-name}/SHIPPED_{DATE}.md
```

The `/workflow-commands /design` command combines what used to be Plan + Spec + ADRs into a single document with architecture decisions inline.

---

## What This Command Does

1. **Analyze** - Understand requirements from DEFINE
2. **Architect** - Design high-level solution with diagrams
3. **Decide** - Document key decisions with rationale (inline ADRs)
4. **Specify** - Create file manifest and code patterns
5. **Plan Testing** - Define testing strategy

---

## Process

### Step 1: Load Context

```markdown
Read(.github/sdd/features/{feature-name}/DEFINE_{FEATURE}.md)
Read(.github/sdd/templates/DESIGN_TEMPLATE.md)
Read(.github/copilot-instructions.md)

# Explore codebase for patterns:
Glob(**/*.py) | head -20
Grep("class |def ") | sample
```

### Step 2: Create Architecture

Design the solution:

| Component | Content |
|-----------|---------|
| **Overview** | ASCII diagram of system |
| **Components** | List of modules/services |
| **Data Flow** | How data moves through system |
| **Integration Points** | External dependencies |

### Step 3: Document Decisions (Inline ADRs)

For each significant choice:

```markdown
### Decision: {Name}

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | YYYY-MM-DD |

**Context:** Why this decision was needed

**Choice:** What we're doing

**Rationale:** Why this approach

**Alternatives Rejected:**
1. Option A - rejected because X
2. Option B - rejected because Y

**Consequences:**
- Trade-off we accept
- Benefit we gain
```

### Step 4: Create File Manifest

List all files to create/modify:

| # | File | Action | Purpose | Dependencies |
|---|------|--------|---------|--------------|
| 1 | `path/to/file.py` | Create | Main handler | None |
| 2 | `path/to/config.yaml` | Create | Configuration | None |
| 3 | `path/to/handler.py` | Create | Request handler | 1, 2 |

### Step 5: Define Code Patterns

Provide copy-paste ready code snippets for key patterns.

### Step 6: Plan Testing Strategy

| Test Type | Scope | Tools |
|-----------|-------|-------|
| Unit | Functions | pytest |
| Integration | API | pytest + requests |
| E2E | Full flow | Manual/automated |

### Step 7: Save

```markdown
Write(.github/sdd/features/{feature-name}/DESIGN_{FEATURE_NAME}.md)
```

---

## Output

| Artifact | Location |
|----------|----------|
| **DESIGN** | `.github/sdd/features/{feature-name}/DESIGN_{FEATURE_NAME}.md` |

**Next Step:** `/workflow-commands /build .github/sdd/features/{feature-name}/DESIGN_{FEATURE_NAME}.md`

---

## Quality Gate

Before saving, verify:

```text
[ ] Architecture diagram is clear
[ ] All major decisions documented with rationale
[ ] File manifest is complete (all files listed)
[ ] Code patterns are copy-paste ready
[ ] Testing strategy covers requirements
[ ] No circular dependencies in architecture
[ ] Agent assignments in file manifest validated against .github/config/routing.json
```

---

## Tips

1. **Diagram First** - ASCII art clarifies thinking
2. **Decisions Are Permanent** - Document the "why" not just "what"
3. **Self-Contained Files** - Each file should work independently
4. **Config Over Code** - Use YAML for tunables, not hardcoded values
5. **Test Early** - Design for testability from the start

---

## References

- Agent: `.github/agents/workflow.design-agent.agent.md`
- Template: `.github/sdd/templates/DESIGN_TEMPLATE.md`
- Contracts: `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- Next Phase: `.github/skills/workflow-commands/commands/build.md`
