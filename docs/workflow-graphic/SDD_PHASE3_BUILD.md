# Phase 3 — BUILD

```mermaid
flowchart TD
    START(["📄 DESIGN_{FEATURE}.md"])

    START --> GATE{"🔒 MANDATORY GATE
    DESIGN_{FEATURE}.md exists?
    File manifest present?"}

    GATE -->|"❌ NO"| BLOCK["⛔ BLOCKED
    Run /design first"]

    GATE -->|"✅ YES"| S1

    S1["📂 Step 1 — Load Context
    Read DESIGN_{FEATURE}.md
    Read DEFINE_{FEATURE}.md
    Read copilot-instructions.md"]

    S1 --> S2

    subgraph S2["📋 Step 2 — Planning & Task (MANDATORY before any code)"]
        direction TB
        P1["Create implementation_plan.md
        • All technical decisions
        • Agent assignments per file
        • Links to specialist .agent.md"]
        P2["Create task.md
        • Granular sub-tasks per chunk
        • Responsible agent per sub-task
        • Initial status: ⏳ Pending"]
        P1 --> P2
    end

    S2 --> S3

    S3["🔍 Step 3 — Isolate Next Chunk
    Identify next ⏳ Pending chunk
    in BUILD_REPORT_{FEATURE}.md
    Execute ONLY this chunk"]

    S3 --> S4

    subgraph S4["⚙️ Step 4 — Execute Chunk"]
        direction TB
        E0["mkdir -p ./projects/{feature-name}/"]
        E1["For each file in the chunk:"]
        E2["1. JIT Persona Delegation
        Read implementation_plan.md
        Identify the file's agent"]
        E3["2. Reference Check (MANDATORY)
        Read specialist .agent.md
        Read routing.json"]
        E4["3. Banner Protocol
        Print: Invoking Specialist: [Agent]"]
        E5["4. Write
        Create file in ./projects/{feature-name}/
        Apply code patterns from DESIGN"]
        E6["5. Verify
        ruff check . / mypy . / pytest"]
        E7["6. Mark Complete
        Update task.md"]
        E0 --> E1 --> E2 --> E3 --> E4 --> E5 --> E6
        E6 --> RETRY{"Verification passed?"}
        RETRY -->|"❌ Fail (retry ≤ 3)"| E5
        RETRY -->|"✅ Pass"| E7
        RETRY -->|"❌ Fail after 3 attempts"| BLOCKER["🛑 Register blocker
        Stop and report"]
    end

    S4 --> S5

    S5["💾 Step 5 — Persist State (MANDATORY after each file)
    Update BUILD_REPORT_{FEATURE}.md
    This is the System of Record (SoR)
    Allows resuming work via Git"]

    S5 --> S6

    S6["📊 Step 6 — Report
    Update Chunk Execution Log
    ✅ Passed or ❌ Failed
    STOP and ask user
    whether to advance to next chunk"]

    S6 --> MORE{"More chunks pending?"}
    MORE -->|"✅ Yes"| S3
    MORE -->|"✅ All complete"| OUT

    OUT[/"📁 Generated artifacts
    Code: ./projects/{feature-name}/
    BUILD_REPORT_{FEATURE}.md
    Status: Ready for Validate"/]

    OUT --> NEXT["➡️ /validate"]

    subgraph DELEGATE["🤖 JIT Delegation — Available Specialists"]
        direction LR
        D1["@container-specialist
        Docker, Compose, infra"]
        D2["@dbt-specialist
        Models, tests, docs"]
        D3["@airflow-specialist
        DAGs, operators, scheduling"]
        D4["@python-developer
        Scripts, tests, CLI"]
    end

    subgraph GATE_QUALITY["✅ Quality Gate"]
        GC1{"All files from manifest created?"}
        GC2{"All in ./projects/{feature-name}/?"}
        GC3{"Lint passes (ruff)?"}
        GC4{"Type check passes (mypy)?"}
        GC5{"Tests pass (pytest)?"}
        GC6{"No TODO in code?"}
        GC7{"BUILD_REPORT generated and updated?"}
        GC8{"Specialist quality gates met?"}
    end

    subgraph ISSUE_HANDLING["⚠️ Handling Issues"]
        direction LR
        I1["Missing requirement → /iterate DEFINE"]
        I2["Architectural problem → /iterate DESIGN"]
        I3["Simple bug → Fix and continue"]
        I4["Major blocker → Stop and report"]
    end

    classDef step fill:#0d1b2a,stroke:#1e88e5,color:#fff
    classDef gate fill:#1a237e,stroke:#1e88e5,color:#fff
    classDef out fill:#1b5e20,stroke:#43a047,color:#fff
    classDef block fill:#b71c1c,stroke:#fff,color:#fff
    classDef exec fill:#0d2137,stroke:#29b6f6,color:#fff
    classDef next fill:#1b5e20,stroke:#fff,color:#fff

    class S1,S3,S5,S6 step
    class GATE,MORE,RETRY gate
    class OUT out
    class BLOCK,BLOCKER block
    class S4,E0,E1,E2,E3,E4,E5,E6,E7 exec
    class NEXT next
```

## Quick Rules

| # | Rule |
| --- | --- |
| 1 | **HARD GATE**: without `DESIGN_{FEATURE}.md` with manifest → blocked |
| 2 | `implementation_plan.md` and `task.md` **mandatory before any code** |
| 3 | Execute **only the next pending chunk** — never the entire project at once |
| 4 | Every file goes to `./projects/{feature-name}/` — never in the root |
| 5 | `BUILD_REPORT` is the **System of Record** — update after each file |
| 6 | Verification fails → retry up to **3 times** before registering a blocker |
| 7 | Each file has a **specialist agent** defined in the implementation_plan |
| 8 | STOP after each chunk and ask the user before continuing |

## Execution Loop

```text
BUILD_REPORT (SoR)
      │
      ▼
Next chunk ⏳ Pending
      │
      ▼
For each file in the chunk:
  → JIT delegate → write → verify → persist
      │                         │
      │ ✅                      │ ❌ (retry ≤ 3)
      ▼                         ▼
  task.md updated          fix + retry
      │
      ▼
BUILD_REPORT updated → STOP → wait for user
```
