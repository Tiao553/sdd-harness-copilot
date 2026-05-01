---
name: validate
description: Multi-agent quality gate via Copilot-native juntas (Phase 3.5)
---

# /validate — Quality Gate (Phase 3.5)

> Orchestrates 4 hierarchical juntas to validate an implemented feature before shipping.

## Usage

```bash
/workflow-commands /validate <BUILD_REPORT_path_or_FEATURE_NAME>
```

**Examples:**
```bash
/workflow-commands /validate .github/sdd/features/BRONZE_SILVER/BUILD_REPORT_BRONZE_SILVER.md
/workflow-commands /validate BRONZE_SILVER
```

## SDD Phase Flow

```text
/brainstorm → /define → /design → /build → [/validate] → /ship
                                               ↑ you are here
```

## Prerequisites

| Prerequisite | Path |
|---|---|
| DEFINE document | `.github/sdd/features/{feature-name}/DEFINE_{FEATURE}.md` |
| DESIGN document | `.github/sdd/features/{feature-name}/DESIGN_{FEATURE}.md` |
| BUILD_REPORT | `.github/sdd/features/{feature-name}/BUILD_REPORT_{FEATURE}.md` |
| Implementation files | `projects/{feature-name}/` |

If any prerequisite is missing, **STOP** and tell the user exactly what is missing.

## Process

### Step 1: Load Contracts
1. Read `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
2. Read `.github/sdd/architecture/VALIDATE_JUNTAS_CONTRACT.yaml`

### Step 2: Activate Agent
Read and activate `.github/agents/workflow.validate-agent.agent.md`.
The agent contains the full orchestration protocol.

### Step 3: Build Frozen Evidence Pack
1. Read DEFINE, DESIGN, BUILD_REPORT from the feature directory
2. Scan `projects/{feature-name}/` to build code_tree
3. Create `_validate/` directory in the feature folder

### Step 4: Launch Parallel Juntas (Spec + Code)
Launch TWO `general-purpose` sub-agents in **background** mode:

**Spec Junta:**
- Read prompt: `.github/skills/workflow-commands/references/spec-junta.md`
- Pass frozen evidence pack
- Expected output: `01_SPEC_REPORT_{FEATURE}.json`

**Code Junta:**
- Read prompt: `.github/skills/workflow-commands/references/code-junta.md`
- Pass frozen evidence pack
- Expected output: `02_CODE_REPORT_{FEATURE}.json`

### Step 5: Launch Delivery Junta (Sequential)
After both parallel juntas complete:
- Read prompt: `.github/skills/workflow-commands/references/delivery-junta.md`
- Pass evidence pack + SpecReport + CodeReport
- Expected output: `03_DELIVERY_DELTA_{FEATURE}.json`

### Step 6: Deterministic Scoring
Compute score **without LLM** — pure arithmetic:

```
score = alignment × 0.30 + quality × 0.25 + architecture × 0.20
      + devops × 0.15 + delta × 0.10

critical_count = count(findings where severity == "CRITICAL")
```

Save: `05_SCORING_{FEATURE}.json`

### Step 7: Launch Council (Narrative Only)
- Read prompt: `.github/skills/workflow-commands/references/council-junta.md`
- Pass all reports + scoring
- Council MUST NOT change scores or eligibility
- Expected output: `04_COUNCIL_VERDICT_{FEATURE}.json`

### Step 8: Render Artifacts
Use templates from `.github/sdd/templates/` to generate:

| Score | CRITICAL | Artifact |
|-------|----------|----------|
| ≥ 90 | 0 | `VALIDATION_REPORT` + `RUNBOOK` |
| 70-89 | 0 | `VALIDATION_REPORT` + `ROADMAP` |
| < 70 | Any | `VALIDATION_REPORT` only |

## Quality Gates

```text
VALIDATE QUALITY CHECK
├─ [ ] All 4 prerequisites exist
├─ [ ] Frozen evidence pack built (identical for all juntas)
├─ [ ] Spec Junta returned valid JSON
├─ [ ] Code Junta returned valid JSON
├─ [ ] Delivery Junta returned valid JSON
├─ [ ] Deterministic scoring computed (no LLM)
├─ [ ] Council verdict received (narrative only)
├─ [ ] All 5 intermediate JSONs saved to _validate/
├─ [ ] VALIDATION_REPORT rendered from template
├─ [ ] RUNBOOK or ROADMAP rendered based on eligibility
└─ [ ] Score and verdict reported to user
```

## Output

### Intermediate (saved to `_validate/`)
```
.github/sdd/features/{feature-name}/_validate/
├── 01_SPEC_REPORT_{FEATURE}.json
├── 02_CODE_REPORT_{FEATURE}.json
├── 03_DELIVERY_DELTA_{FEATURE}.json
├── 04_COUNCIL_VERDICT_{FEATURE}.json
└── 05_SCORING_{FEATURE}.json
```

### Final (saved to feature directory)
- `VALIDATION_REPORT_{FEATURE}.md` — always generated
- `RUNBOOK_{FEATURE}.md` — if score ≥ 90 and 0 CRITICAL
- `ROADMAP_{FEATURE}.md` — if 70 ≤ score < 90 and 0 CRITICAL

## Next Step

- If PASSED (score ≥ 90, 0 CRITICAL): `/workflow-commands /ship`
- If WARNING or FAILED: Remediate issues, then `/workflow-commands /validate` again

## References

- Agent: `.github/agents/workflow.validate-agent.agent.md`
- Junta Contract: `.github/sdd/architecture/VALIDATE_JUNTAS_CONTRACT.yaml`
- Workflow Contract: `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- Templates: `.github/sdd/templates/VALIDATION_REPORT_TEMPLATE.md`
- Next: `.github/skills/workflow-commands/commands/ship.md`
