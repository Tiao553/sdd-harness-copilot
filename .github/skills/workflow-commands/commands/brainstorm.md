---
name: brainstorm
description: Explore ideas through collaborative dialogue before requirements capture (Phase 0)
---

# Brainstorm Command

> Collaborative exploration before requirements capture (Phase 0)

## Usage

```bash
/workflow-commands /brainstorm <idea-or-request>
/workflow-commands /brainstorm "Build a real-time notification system"
/workflow-commands /brainstorm notes/rough-idea.txt
```

## Examples

```bash
# From a direct idea
/workflow-commands /brainstorm "I want to automate data quality checks"

# From a file with notes
/workflow-commands /brainstorm docs/meeting-notes.md

# From a problem statement
/workflow-commands /brainstorm "Our team spends too much time on manual data entry"
```

---

## Overview

This is **Phase 0** of the 5-phase AgentSpec workflow:

```text
Phase 0: /workflow-commands /brainstorm → .github/sdd/features/{feature-name}/BRAINSTORM_{FEATURE}.md (THIS COMMAND)
Phase 1: /workflow-commands /define     → .github/sdd/features/{feature-name}/DEFINE_{FEATURE}.md
Phase 2: /workflow-commands /design     → .github/sdd/features/{feature-name}/DESIGN_{FEATURE}.md
Phase 3: /workflow-commands /build      → Code in ./projects/{feature-name}/ + .github/sdd/features/{feature-name}/BUILD_REPORT_{FEATURE}.md
Phase 3.5: /workflow-commands /validate → .github/sdd/features/{feature-name}/VALIDATION_REPORT_{FEATURE}.md
Phase 4: /workflow-commands /ship       → .github/sdd/archive/{feature-name}/SHIPPED_{DATE}.md
```

The `/workflow-commands /brainstorm` command explores ideas through dialogue before capturing formal requirements.

---

## What This Command Does

0. **Knowledge Checkpoint** - Load active project context from `.github/knowledge_context/` and inject into session
1. **Explore** - Understand project context and existing patterns
2. **Question** - Ask one question at a time to clarify intent
3. **Collect** - Gather sample files, ground truth, or reference data for LLM grounding
4. **Propose** - Present 2-3 approaches with trade-offs
5. **Simplify** - Apply YAGNI to remove unnecessary features
6. **Validate** - Incrementally confirm understanding
7. **Document** - Generate BRAINSTORM document for /workflow-commands /define

---

## Process

### Step 0: Knowledge Checkpoint (executes before everything else)

```markdown
1. Read(.github/knowledge_context/_registry.yaml)
   - If file does not exist → skip this step entirely, continue to Step 1
   - If exists → read active_project field

2. Read(.github/knowledge_context/{active_project}/KNOWLEDGE_CONTEXT.md)
   - If active_project is empty or file missing → skip, continue to Step 1

3. Validate required fields in KNOWLEDGE_CONTEXT.md:
   - deployment_context.stack filled?
   - deployment_context.entry_points filled?

4. If any required field is empty or still a {placeholder}:
   - Ask ONE question only:
     "Para contextualizar a ideia: em qual módulo ou serviço você imagina que essa feature vai viver?"
   - Save answer to deployment_context.entry_points in KNOWLEDGE_CONTEXT.md

5. Inject into BRAINSTORM_{FEATURE}.md header (Technical Context Observed section):
   - stack, entry_points, business_context from KNOWLEDGE_CONTEXT.md
```

**Rule:** This step never blocks the brainstorm. If the registry or KNOWLEDGE_CONTEXT.md is absent, proceed normally. One question maximum — never ask more than one during the checkpoint.

---

### Step 1: Gather Context

```markdown
Read(.github/copilot-instructions.md)
Read(.github/sdd/templates/BRAINSTORM_TEMPLATE.md)
Explore project structure, recent commits, existing patterns
```

### Step 2: Discovery Questions

Ask questions ONE AT A TIME:

| Question Type | When to Use |
|---------------|-------------|
| Multiple Choice | When options are clear (preferred) |
| Open-Ended | When exploring unknown territory |
| Clarifying | When answer was vague |

**Minimum:** 3 questions before proposing approaches

### Step 3: Sample Collection (LLM Grounding)

Ask about available samples to improve AI/LLM accuracy:

```markdown
"Do you have any samples that could help ground the solution?
(a) Sample input files
(b) Expected output examples
(c) Ground truth / verified data
(d) None available"
```

If samples exist, analyze and document them in the BRAINSTORM output.

### Step 4: Explore Approaches

Present 2-3 distinct approaches:

```markdown
### Approach A: {Name} ⭐ Recommended
**Why:** {Reasoning}
**Pros:** {Benefits}
**Cons:** {Trade-offs}

### Approach B: {Name}
**Why not recommended:** {Reasoning}
```

### Step 5: Apply YAGNI

For each feature, ask:
- Do we need this for MVP?
- Does this solve the core problem?

Remove features that don't pass. Document what was removed and why.

### Step 6: Validate Incrementally

Present design in sections (200-300 words each):

```text
Section → Check with user → Adjust if needed → Next section
```

**Minimum:** 2 validation checkpoints

### Step 7: Generate Document

```markdown
Write(.github/sdd/features/{feature-name}/BRAINSTORM_{FEATURE}.md)
```

---

## Output

| Artifact | Location |
|----------|----------|
| **Brainstorm Document** | `.github/sdd/features/{feature-name}/BRAINSTORM_{FEATURE}.md` |

**Next Step:** `/workflow-commands /define .github/sdd/features/{feature-name}/BRAINSTORM_{FEATURE}.md`

---

## Quality Gate

Before marking complete:

```text
[ ] Knowledge Checkpoint executed (or skipped gracefully if registry absent)
[ ] deployment_context injected into BRAINSTORM header (if context available)
[ ] Minimum 3 discovery questions asked
[ ] Sample collection question asked
[ ] At least 2 approaches explored
[ ] YAGNI applied (features removed)
[ ] Minimum 2 validations completed
[ ] User confirmed selected approach
[ ] KB domains relevant to the idea identified and listed
[ ] Draft requirements included
```

---

## Interaction Style

### One Question at a Time

```markdown
GOOD:
"What's the primary use case?
(a) Internal reporting
(b) Customer-facing
(c) Both"

BAD:
"What's the use case? Who are the users? What's the timeline?"
```

### Lead with Recommendation

```markdown
GOOD:
"I recommend Approach A because [reasoning].
Here are the alternatives to consider..."

BAD:
"Here are three approaches. Which one do you want?"
```

### Be Ready to Go Back

```markdown
GOOD:
"That's different from what I understood. Let me revise..."

BAD:
"Moving on to the next section..."
```

---

## When to Use /brainstorm vs /define

| Scenario | Use |
|----------|-----|
| Vague idea, need to explore | `/workflow-commands /brainstorm` |
| Clear requirements, ready to capture | `/workflow-commands /define` directly |
| Existing BRAINSTORM document | `/workflow-commands /define <brainstorm-file>` |
| Meeting notes with clear asks | `/workflow-commands /define` directly |
| "I want to build something but not sure what" | `/workflow-commands /brainstorm` |

---

## Tips

1. **Take your time** - Exploration is about understanding, not speed
2. **Ask why** - "Why do you need this?" reveals true requirements
3. **Challenge scope** - Most features aren't needed for MVP
4. **Trust the user** - They know their domain, you know patterns
5. **Document removed features** - They might come back later

---

## Handling Different Inputs

| Input Type | Approach |
|------------|----------|
| Vague idea | Start with "Tell me more about..." |
| Specific request | Validate understanding, then explore approaches |
| Problem statement | Focus on pain points, then solutions |
| Feature request | Question the need, explore alternatives |
| Comparison request | Explore trade-offs, make recommendation |

---

## References

- Agent: `.github/agents/workflow.brainstorm-agent.agent.md`
- Template: `.github/sdd/templates/BRAINSTORM_TEMPLATE.md`
- Contracts: `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- Next Phase: `.github/skills/workflow-commands/commands/define.md`
