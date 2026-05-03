# Phase 1 — DEFINE

```mermaid
flowchart TD
    START(["📥 Input"])
    START --> INPUT

    subgraph INPUT["Accepted input types"]
        direction LR
        I1["BRAINSTORM_{FEATURE}.md"]
        I2["Meeting notes"]
        I3["Email thread"]
        I4["Direct conversation"]
        I5["Direct requirement"]
    end

    INPUT --> G

    subgraph G["🔍 Mandatory Grounding"]
        G1["Read CLAUSE.md"] --> G2["Read WORKFLOW_CONTRACTS.yaml"]
        G2 --> G3["Load templates (.github/sdd/templates/)"]
    end

    G --> KB

    subgraph KB["KB-First Resolution"]
        KB1["KB Discovery"] --> KB2["Template Loading"]
        KB2 --> KB3["Confidence Assignment — threshold: 0.90"]
    end

    KB --> S1

    S1["📂 Step 1 — Load Context
    Read BRAINSTORM (if exists)
    Load requirements templates"]

    S1 --> S2

    S2["🏷️ Step 2 — Classify Input
    Identify input type
    Adjust extraction according to type"]

    S2 --> S3

    subgraph S3["📋 Step 3 — Extract Entities"]
        direction TB
        E1["Problem Statement"]
        E2["Users — with pain points"]
        E3["Goals — prioritized by MoSCoW"]
        E4["Success Criteria — testable"]
        E5["Acceptance Tests"]
        E6["Constraints — technical and business"]
        E7["Out of Scope — explicit boundaries"]
    end

    S3 --> SCORE

    subgraph SCORE["📊 Step 4 — Clarity Score (min. 12/15)"]
        direction TB
        SC1["Problem:  0–3   (clear · specific · actionable)"]
        SC2["Users:    0–3   (identified + pain points)"]
        SC3["Goals:    0–3   (measurable + MoSCoW)"]
        SC4["Success:  0–3   (testable criteria)"]
        SC5["Scope:    0–3   (explicit boundaries)"]
        SC_SUM["Total = sum of 5 elements"]
        SC1 & SC2 & SC3 & SC4 & SC5 --> SC_SUM
    end

    SC_SUM --> DECISION{"Score?"}

    DECISION -->|"0–8 🔴 LOW"| BLOCK["⛔ BLOCKED
    Collect more information
    before continuing"]

    DECISION -->|"9–11 🟡 MEDIUM"| GAPS["🔎 Step 5 — Fill Gaps
    Fallback questions
    for each low-score element"]

    DECISION -->|"12–15 🟢 HIGH"| S6

    GAPS --> SCORE

    S6["📝 Step 6 — Generate Document
    9 mandatory sections below"]

    S6 --> DOC

    subgraph DOC["Sections of DEFINE_{FEATURE}.md"]
        direction LR
        D1["1. Problem Statement"]
        D2["2. Users & Personas"]
        D3["3. Goals (MoSCoW)"]
        D4["4. Success Criteria"]
        D5["5. Acceptance Tests"]
        D6["6. Constraints"]
        D7["7. Out of Scope"]
        D8["8. Technical Context\n(location · KB · IaC)"]
        D9["9. Data Engineering Context\n(if applicable)"]
    end

    DOC --> DE_CHECK{"Is this a\nData Engineering case?"}
    DE_CHECK -->|"✅ Yes"| DE

    subgraph DE["🔧 Data Engineering Context"]
        direction LR
        DE1["Source Inventory"]
        DE2["Freshness SLAs"]
        DE3["Schema Contracts"]
        DE4["Completeness Metrics"]
        DE5["Volume Estimates"]
    end

    DE_CHECK -->|"❌ No"| GATE
    DE --> GATE

    subgraph GATE["✅ Quality Gate"]
        GC1{"Clarity Score ≥ 12/15?"}
        GC2{"All users identified?"}
        GC3{"Testable success criteria?"}
        GC4{"MoSCoW applied to goals?"}
        GC5{"Explicit in/out scope?"}
        GC6{"Acceptance Tests written?"}
        GC7{"Technical context mapped?"}
    end

    GATE --> PASS{"All items ✅?"}
    PASS -->|"❌ No"| GAPS
    PASS -->|"✅ Yes"| OUT

    OUT[/"📄 DEFINE_{FEATURE}.md
    Status: Ready for Design
    Clarity Score: NN/15
    Path: .github/sdd/features/{feature-name}/"/]

    OUT --> NEXT{"Next step"}
    NEXT -->|"Normal flow"| DESIGN["➡️ /design"]
    NEXT -->|"Future change"| ITERATE["🔄 /iterate"]

    subgraph MOSCOW["📐 MoSCoW Reference"]
        direction LR
        M1["MUST — mandatory for MVP"]
        M2["SHOULD — important but not blocking"]
        M3["COULD — desirable if time allows"]
        M4["WON'T — out of scope for this delivery"]
    end

    subgraph ANTI["🚫 Anti-Patterns"]
        A1["Vague language\n('improve performance')"]
        A2["Non-testable criteria\n('should be fast')"]
        A3["Generic users\n('all users')"]
        A4["Implementation details\nin DEFINE"]
    end

    classDef step fill:#16213e,stroke:#0f3460,color:#fff
    classDef score fill:#0f3460,stroke:#533483,color:#fff
    classDef out fill:#533483,stroke:#e94560,color:#fff
    classDef block fill:#c0392b,stroke:#fff,color:#fff
    classDef next fill:#27ae60,stroke:#fff,color:#fff
    classDef anti fill:#7f1d1d,stroke:#fff,color:#fff

    class S1,S2,S6 step
    class SCORE,SC_SUM,DECISION score
    class OUT out
    class BLOCK block
    class DESIGN,ITERATE next
    class ANTI,A1,A2,A3,A4 anti
```

## Quick Rules

| # | Rule |
| --- | --- |
| 1 | **Minimum Clarity Score: 12/15** to advance |
| 2 | Score 9–11: fill gaps before continuing |
| 3 | Score 0–8: **blocked**, collect more info |
| 4 | All goals must have **MoSCoW** |
| 5 | Success Criteria must be **testable** |
| 6 | Out of Scope must be **explicit** |
| 7 | `/design` **cannot start** without this document |
| 8 | Confidence threshold: **0.90** |

## Clarity Score — Scoring Guide

| Element | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Problem | Absent | Vague | Specific | Clear + actionable |
| Users | Absent | Generic | Identified | With pain points |
| Goals | Absent | Vague | Measurable | MoSCoW applied |
| Success | Absent | Subjective | Objective | Automatically testable |
| Scope | Absent | Implicit | Partial | Explicit in/out |
