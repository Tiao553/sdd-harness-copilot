# Fase 3 — BUILD

```mermaid
flowchart TD
    START(["📄 DESIGN_{FEATURE}.md"])

    START --> GATE{"🔒 GATE OBRIGATÓRIO
    DESIGN_{FEATURE}.md existe?
    File manifest presente?"}

    GATE -->|"❌ NÃO"| BLOCK["⛔ BLOQUEADO
    Execute /design primeiro"]

    GATE -->|"✅ SIM"| S1

    S1["📂 Passo 1 — Load Context
    Ler DESIGN_{FEATURE}.md
    Ler DEFINE_{FEATURE}.md
    Ler copilot-instructions.md"]

    S1 --> S2

    subgraph S2["📋 Passo 2 — Planning & Task (OBRIGATÓRIO antes de qualquer código)"]
        direction TB
        P1["Criar implementation_plan.md
        • Todas as decisões técnicas
        • Agent assignments por arquivo
        • Links para specialist .agent.md"]
        P2["Criar task.md
        • Sub-tasks granulares por chunk
        • Agente responsável por sub-task
        • Status inicial: ⏳ Pending"]
        P1 --> P2
    end

    S2 --> S3

    S3["🔍 Passo 3 — Isolate Next Chunk
    Identificar próximo chunk ⏳ Pending
    no BUILD_REPORT_{FEATURE}.md
    Executar APENAS este chunk"]

    S3 --> S4

    subgraph S4["⚙️ Passo 4 — Execute Chunk"]
        direction TB
        E0["mkdir -p ./projects/{feature-name}/"]
        E1["Para cada arquivo do chunk:"]
        E2["1. JIT Persona Delegation
        Ler implementation_plan.md
        Identificar agente do arquivo"]
        E3["2. Reference Check (OBRIGATÓRIO)
        Ler specialist .agent.md
        Ler routing.json"]
        E4["3. Banner Protocol
        Print: Invoking Specialist: [Agent]"]
        E5["4. Write
        Criar arquivo em ./projects/{feature-name}/
        Aplicar code patterns do DESIGN"]
        E6["5. Verify
        ruff check . / mypy . / pytest"]
        E7["6. Mark Complete
        Atualizar task.md"]
        E0 --> E1 --> E2 --> E3 --> E4 --> E5 --> E6
        E6 --> RETRY{"Verificação passou?"}
        RETRY -->|"❌ Fail (retry ≤ 3)"| E5
        RETRY -->|"✅ Pass"| E7
        RETRY -->|"❌ Fail após 3 tentativas"| BLOCKER["🛑 Registrar bloqueio
        Parar e reportar"]
    end

    S4 --> S5

    S5["💾 Passo 5 — Persist State (OBRIGATÓRIO após cada arquivo)
    Atualizar BUILD_REPORT_{FEATURE}.md
    Este é o System of Record (SoR)
    Permite retomar o trabalho via Git"]

    S5 --> S6

    S6["📊 Passo 6 — Report
    Atualizar Chunk Execution Log
    ✅ Passed ou ❌ Failed
    PARAR e perguntar ao usuário
    se deve avançar para próximo chunk"]

    S6 --> MORE{"Mais chunks pending?"}
    MORE -->|"✅ Sim"| S3
    MORE -->|"✅ Todos completos"| OUT

    OUT[/"📁 Artefatos gerados
    Código: ./projects/{feature-name}/
    BUILD_REPORT_{FEATURE}.md
    Status: Ready for Validate"/]

    OUT --> NEXT["➡️ /validate"]

    subgraph DELEGATE["🤖 JIT Delegation — Especialistas disponíveis"]
        direction LR
        D1["@container-specialist
        Docker, Compose, infra"]
        D2["@dbt-specialist
        Modelos, testes, docs"]
        D3["@airflow-specialist
        DAGs, operators, scheduling"]
        D4["@python-developer
        Scripts, testes, CLI"]
    end

    subgraph GATE_QUALITY["✅ Quality Gate"]
        GC1{"Todos os arquivos do manifest criados?"}
        GC2{"Todos em ./projects/{feature-name}/?"}
        GC3{"Lint passa (ruff)?"}
        GC4{"Type check passa (mypy)?"}
        GC5{"Testes passam (pytest)?"}
        GC6{"Sem TODO no código?"}
        GC7{"BUILD_REPORT gerado e atualizado?"}
        GC8{"Quality gates dos specialists met?"}
    end

    subgraph ISSUE_HANDLING["⚠️ Handling Issues"]
        direction LR
        I1["Requisito ausente → /iterate DEFINE"]
        I2["Problema arquitetural → /iterate DESIGN"]
        I3["Bug simples → Fix e continuar"]
        I4["Bloqueio maior → Parar e reportar"]
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

## Regras Rápidas

| # | Regra |
|---|---|
| 1 | **GATE DURO**: sem `DESIGN_{FEATURE}.md` com manifest → bloqueado |
| 2 | `implementation_plan.md` e `task.md` **obrigatórios antes de qualquer código** |
| 3 | Executar **apenas o próximo chunk pending** — nunca o projeto inteiro de uma vez |
| 4 | Todo arquivo vai para `./projects/{feature-name}/` — nunca na raiz |
| 5 | `BUILD_REPORT` é o **System of Record** — atualizar após cada arquivo |
| 6 | Verificação falha → retry até **3 vezes** antes de registrar bloqueio |
| 7 | Cada arquivo tem um **specialist agent** definido no implementation_plan |
| 8 | PARAR após cada chunk e perguntar ao usuário antes de continuar |

## Execution Loop

```text
BUILD_REPORT (SoR)
      │
      ▼
Próximo chunk ⏳ Pending
      │
      ▼
Para cada arquivo do chunk:
  → JIT delegate → write → verify → persist
      │                         │
      │ ✅                      │ ❌ (retry ≤ 3)
      ▼                         ▼
  task.md updated          fix + retry
      │
      ▼
BUILD_REPORT updated → STOP → aguardar usuário
```
