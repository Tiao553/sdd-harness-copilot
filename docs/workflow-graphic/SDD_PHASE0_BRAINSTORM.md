# Phase 0 — BRAINSTORM

```mermaid
flowchart TD
    START(["💡 Idea / Raw Requirement"])
    START --> G

    subgraph G["🔍 Mandatory Grounding"]
        G1["Read CLAUDE.md"] --> G2["Read WORKFLOW_CONTRACTS.yaml"]
        G2 --> G3["Load relevant KB domains (≤ 3)"]
    end

    G --> KB

    subgraph KB["KB-First Resolution"]
        KB1["KB Discovery\nDoes a relevant domain exist?"]
        KB2["Codebase Exploration\nPatterns already implemented?"]
        KB3["Confidence Assignment\n0.0 → 1.0"]
        KB4["MCP Validation\nif confidence < 0.85"]
        KB1 --> KB2 --> KB3 --> KB4
    end

    KB --> S1

    S1["📌 Step 1 — Gather Context
    Does a previous BRAINSTORM exist?
    Load project context"]

    S1 --> S2

    S2["❓ Step 2 — Discovery Questions
    Minimum 3 mandatory questions
    Prefer multiple choice
    One question at a time (no question dump)"]

    S2 --> S3

    S3["🗂️ Step 3 — Sample Collection
    Collect inputs, outputs, and ground truth
    Required for LLM grounding"]

    S3 --> S4

    S4["⚖️ Step 4 — Explore Approaches
    Present 2 to 3 approaches
    Each with clear trade-offs
    Never present a single approach"]

    S4 --> S5

    S5["✂️ Step 5 — Apply YAGNI
    'Do we need this for MVP?'
    Eliminate unnecessary complexity"]

    S5 --> S6

    S6["🔁 Step 6 — Validate Incrementally
    Minimum 2 checkpoints with the user
    Present progress before finalizing"]

    S6 --> S7

    S7["💾 Step 7 — Generate Document
    Save BRAINSTORM_{FEATURE}.md"]

    S7 --> GATE

    subgraph GATE["✅ Quality Gate"]
        GC1{"Problem clear and specific?"}
        GC2{"Users identified?"}
        GC3{"≥ 2 approaches with trade-offs?"}
        GC4{"YAGNI applied?"}
        GC5{"Samples collected?"}
        GC6{"≥ 2 checkpoints validated?"}
    end

    GATE --> PASS{"All items ✅?"}
    PASS -->|"❌ No"| S2
    PASS -->|"✅ Yes"| OUT

    OUT[/"📄 BRAINSTORM_{FEATURE}.md
    Status: Ready for Define
    Path: .github/sdd/features/{feature-name}/"/]

    OUT --> NEXT{"Next step"}
    NEXT -->|"Normal flow"| DEFINE["➡️ /define"]
    NEXT -->|"Future change"| ITERATE["🔄 /iterate"]

    subgraph ANTI["🚫 Anti-Patterns"]
        A1["Question dump\n(multiple questions at once)"]
        A2["Assuming answers\nwithout asking"]
        A3["Presenting\nonly 1 approach"]
        A4["Ignoring\ntechnical constraints"]
    end

    classDef step fill:#1a1a2e,stroke:#e94560,color:#fff
    classDef gate fill:#16213e,stroke:#e94560,color:#fff
    classDef out fill:#533483,stroke:#e94560,color:#fff
    classDef anti fill:#c0392b,stroke:#fff,color:#fff
    classDef next fill:#27ae60,stroke:#fff,color:#fff

    class S1,S2,S3,S4,S5,S6,S7 step
    class GATE,PASS gate
    class OUT out
    class ANTI,A1,A2,A3,A4 anti
    class DEFINE,ITERATE next
```

## Quick Rules

| # | Rule |
| --- | --- |
| 1 | Minimum **3 discovery questions** |
| 2 | Always **multiple choice** in questions |
| 3 | Present **2–3 approaches** with trade-offs |
| 4 | Apply **YAGNI** — cut what is not MVP |
| 5 | **≥ 2 validation checkpoints** with the user |
| 6 | Confidence threshold: **0.85** |
| 7 | Never do a question dump — **one question at a time** |
