# Fase 4 — SHIP

```mermaid
flowchart TD
    START(["📦 /ship {FEATURE}"])

    START --> PREREQ

    subgraph PREREQ["🔒 GATE — 6 pré-requisitos obrigatórios"]
        direction LR
        PR1["DEFINE_{FEATURE}.md"]
        PR2["DESIGN_{FEATURE}.md"]
        PR3["BUILD_REPORT_{FEATURE}.md\n(100% completo)"]
        PR4["VALIDATION_REPORT_{FEATURE}.md\nscore ≥ 90, CRITICAL = 0"]
        PR5["RUNBOOK_{FEATURE}.md\n(existe)"]
        PR6["Todos os testes passando"]
    end

    PREREQ --> GATE{"Todos os 6 critérios
    atendidos?"}

    GATE -->|"❌ Qualquer falha"| BLOCK["⛔ BLOQUEADO
    Informar exatamente
    o que está faltando"]

    GATE -->|"✅ Todos OK"| S1

    S1["📋 Passo 1 — Verify Completion
    Ler todos os artefatos da feature
    Confirmar que BUILD_REPORT mostra
    100% dos tasks completos"]

    S1 --> S2

    S2["📁 Passo 2 — Create Archive
    mkdir -p .github/sdd/archive/{feature-name}/"]

    S2 --> S3

    subgraph S3["📂 Passo 3 — Copy Artifacts to Archive"]
        direction TB
        CP1["DEFINE_{FEATURE}.md"]
        CP2["DESIGN_{FEATURE}.md"]
        CP3["BUILD_REPORT_{FEATURE}.md"]
        CP4["VALIDATION_REPORT_{FEATURE}.md"]
        CP5["RUNBOOK_{FEATURE}.md"]
    end

    S3 --> S4

    subgraph S4["📝 Passo 4 — Document Lessons Learned"]
        direction TB
        LL1["Process: o que funcionou no fluxo"]
        LL2["Technical: decisões técnicas que valeram"]
        LL3["Communication: clarificações que evitaram retrabalho"]
        LL4["Tools: bibliotecas/ferramentas que simplificaram"]
        LL_OUT["Salvar em SHIPPED_{DATE}.md"]
        LL1 & LL2 & LL3 & LL4 --> LL_OUT
    end

    S4 --> S5

    S5["🔄 Passo 5 — Update Document Statuses
    DEFINE → Status: ✅ Shipped
    DESIGN → Status: ✅ Shipped
    Adicionar revisão: 'Shipped and archived'"]

    S5 --> S6

    S6["🧹 Passo 6 — Clean Up
    rm -rf .github/sdd/features/{feature-name}/"]

    S6 --> S7

    S7["💾 Passo 7 — Save SHIPPED Document
    Write: .github/sdd/archive/{feature-name}/SHIPPED_{DATE}.md"]

    S7 --> OUT

    OUT[/"📦 SHIPPED_{DATE}.md
    Path: .github/sdd/archive/{feature-name}/
    Status: ✅ Feature Archived"/]

    OUT --> METRICS

    subgraph METRICS["📊 SHIPPED_{DATE}.md contém"]
        direction LR
        M1["Feature name + date"]
        M2["Validation score final"]
        M3["Lines of code, files created"]
        M4["Lessons learned (4 categorias)"]
        M5["Links para todos os artefatos arquivados"]
    end

    METRICS --> NEXT["🆕 Nova feature?
    /workflow-commands /define 'próxima ideia'"]

    subgraph ARCHIVE_STRUCTURE["📁 Estrutura do Archive"]
        direction TB
        A1[".github/sdd/archive/{feature-name}/"]
        A2["├── SHIPPED_{DATE}.md"]
        A3["├── DEFINE_{FEATURE}.md      (Status: ✅ Shipped)"]
        A4["├── DESIGN_{FEATURE}.md      (Status: ✅ Shipped)"]
        A5["├── BUILD_REPORT_{FEATURE}.md"]
        A6["├── VALIDATION_REPORT_{FEATURE}.md"]
        A7["└── RUNBOOK_{FEATURE}.md"]
        A1 --> A2 & A3 & A4 & A5 & A6 & A7
    end

    subgraph GATE_QUALITY["✅ Quality Gate"]
        GC1{"BUILD_REPORT mostra 100%?"}
        GC2{"VALIDATION_REPORT score ≥ 90?"}
        GC3{"CRITICAL issues = 0?"}
        GC4{"RUNBOOK existe?"}
        GC5{"Testes passando?"}
        GC6{"Artefatos copiados para archive?"}
        GC7{"SHIPPED_{DATE}.md criado?"}
        GC8{"Features dir removido?"}
    end

    classDef step fill:#1b5e20,stroke:#43a047,color:#fff
    classDef gate fill:#1a237e,stroke:#5c6bc0,color:#fff
    classDef out fill:#004d40,stroke:#26a69a,color:#fff
    classDef block fill:#b71c1c,stroke:#fff,color:#fff
    classDef archive fill:#0d47a1,stroke:#42a5f5,color:#fff
    classDef next fill:#4a148c,stroke:#ba68c8,color:#fff

    class S1,S2,S5,S6,S7 step
    class GATE gate
    class OUT out
    class BLOCK block
    class S3,CP1,CP2,CP3,CP4,CP5 archive
    class NEXT next
```

## Regras Rápidas

| # | Regra |
|---|---|
| 1 | **6 pré-requisitos** — qualquer um faltando → bloqueado |
| 2 | `VALIDATION_REPORT` com **score ≥ 90 E CRITICAL = 0** é obrigatório |
| 3 | `RUNBOOK_{FEATURE}.md` deve existir (gerado pelo /validate) |
| 4 | **Lessons learned** documentadas em 4 categorias |
| 5 | Artefatos são **copiados** para archive, não movidos direto |
| 6 | DEFINE e DESIGN recebem **Status: ✅ Shipped** antes de arquivar |
| 7 | `.github/sdd/features/{feature-name}/` é **removido** após arquivar |
| 8 | Código permanece em `./projects/{feature-name}/` — não é removido |

## Lessons Learned — Guia

| Categoria | Exemplos de entrada |
|---|---|
| **Process** | "Quebrar em chunks menores ajudou" · "Mais checkpoints no brainstorm" |
| **Technical** | "Config via YAML > env vars" · "Specialist X foi crucial para Y" |
| **Communication** | "Clarificar escopo antes do design evitou retrabalho" |
| **Tools** | "Biblioteca X simplificou Z" · "Usar pattern do KB economizou tempo" |

## Archive vs Features

```text
Durante desenvolvimento:
  .github/sdd/features/{feature-name}/   ← artefatos ativos

Após /ship:
  .github/sdd/archive/{feature-name}/    ← artefatos permanentes
  .github/sdd/features/{feature-name}/   ← REMOVIDO
  ./projects/{feature-name}/             ← código permanece
```
