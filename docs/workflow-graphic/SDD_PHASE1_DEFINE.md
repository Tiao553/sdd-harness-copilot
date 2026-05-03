# Fase 1 — DEFINE

```mermaid
flowchart TD
    START(["📥 Entrada"])
    START --> INPUT

    subgraph INPUT["Tipos de Input aceitos"]
        direction LR
        I1["BRAINSTORM_{FEATURE}.md"]
        I2["Notas de reunião"]
        I3["Email thread"]
        I4["Conversa direta"]
        I5["Requisito direto"]
    end

    INPUT --> G

    subgraph G["🔍 Grounding Obrigatório"]
        G1["Ler CLAUSE.md"] --> G2["Ler WORKFLOW_CONTRACTS.yaml"]
        G2 --> G3["Carregar templates (.github/sdd/templates/)"]
    end

    G --> KB

    subgraph KB["KB-First Resolution"]
        KB1["KB Discovery"] --> KB2["Template Loading"]
        KB2 --> KB3["Confidence Assignment — threshold: 0.90"]
    end

    KB --> S1

    S1["📂 Passo 1 — Load Context
    Ler BRAINSTORM (se existir)
    Carregar templates de requisitos"]

    S1 --> S2

    S2["🏷️ Passo 2 — Classify Input
    Identificar tipo de entrada
    Ajustar extração conforme o tipo"]

    S2 --> S3

    subgraph S3["📋 Passo 3 — Extract Entities"]
        direction TB
        E1["Problem Statement"]
        E2["Users — com pain points"]
        E3["Goals — priorizados por MoSCoW"]
        E4["Success Criteria — testáveis"]
        E5["Acceptance Tests"]
        E6["Constraints — técnicas e de negócio"]
        E7["Out of Scope — limites explícitos"]
    end

    S3 --> SCORE

    subgraph SCORE["📊 Passo 4 — Clarity Score (mín. 12/15)"]
        direction TB
        SC1["Problem:  0–3   (claro · específico · acionável)"]
        SC2["Users:    0–3   (identificados + pain points)"]
        SC3["Goals:    0–3   (mensuráveis + MoSCoW)"]
        SC4["Success:  0–3   (critérios testáveis)"]
        SC5["Scope:    0–3   (limites explícitos)"]
        SC_SUM["Total = soma dos 5 elementos"]
        SC1 & SC2 & SC3 & SC4 & SC5 --> SC_SUM
    end

    SC_SUM --> DECISION{"Score?"}

    DECISION -->|"0–8 🔴 LOW"| BLOCK["⛔ BLOQUEADO
    Coletar mais informações
    antes de continuar"]

    DECISION -->|"9–11 🟡 MEDIUM"| GAPS["🔎 Passo 5 — Fill Gaps
    Perguntas de fallback
    por elemento com score baixo"]

    DECISION -->|"12–15 🟢 HIGH"| S6

    GAPS --> SCORE

    S6["📝 Passo 6 — Gerar Documento
    9 seções obrigatórias abaixo"]

    S6 --> DOC

    subgraph DOC["Seções do DEFINE_{FEATURE}.md"]
        direction LR
        D1["1. Problem Statement"]
        D2["2. Users & Personas"]
        D3["3. Goals (MoSCoW)"]
        D4["4. Success Criteria"]
        D5["5. Acceptance Tests"]
        D6["6. Constraints"]
        D7["7. Out of Scope"]
        D8["8. Technical Context\n(localização · KB · IaC)"]
        D9["9. Data Engineering Context\n(se aplicável)"]
    end

    DOC --> DE_CHECK{"É um caso\nde Data Engineering?"}
    DE_CHECK -->|"✅ Sim"| DE

    subgraph DE["🔧 Data Engineering Context"]
        direction LR
        DE1["Source Inventory"]
        DE2["Freshness SLAs"]
        DE3["Schema Contracts"]
        DE4["Completeness Metrics"]
        DE5["Volume Estimates"]
    end

    DE_CHECK -->|"❌ Não"| GATE
    DE --> GATE

    subgraph GATE["✅ Quality Gate"]
        GC1{"Clarity Score ≥ 12/15?"}
        GC2{"Todos os usuários identificados?"}
        GC3{"Critérios de sucesso testáveis?"}
        GC4{"MoSCoW aplicado nos goals?"}
        GC5{"Escopo in/out explícito?"}
        GC6{"Acceptance Tests escritos?"}
        GC7{"Technical context mapeado?"}
    end

    GATE --> PASS{"Todos os itens ✅?"}
    PASS -->|"❌ Não"| GAPS
    PASS -->|"✅ Sim"| OUT

    OUT[/"📄 DEFINE_{FEATURE}.md
    Status: Ready for Design
    Clarity Score: NN/15
    Path: .github/sdd/features/{feature-name}/"/]

    OUT --> NEXT{"Próximo passo"}
    NEXT -->|"Fluxo normal"| DESIGN["➡️ /design"]
    NEXT -->|"Mudança futura"| ITERATE["🔄 /iterate"]

    subgraph MOSCOW["📐 MoSCoW Reference"]
        direction LR
        M1["MUST — obrigatório para MVP"]
        M2["SHOULD — importante mas não bloqueante"]
        M3["COULD — desejável se houver tempo"]
        M4["WON'T — fora do escopo desta entrega"]
    end

    subgraph ANTI["🚫 Anti-Patterns"]
        A1["Linguagem vaga\n('melhorar performance')"]
        A2["Critérios não testáveis\n('deve ser rápido')"]
        A3["Usuários genéricos\n('todos os usuários')"]
        A4["Detalhes de implementação\nno DEFINE"]
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

## Regras Rápidas

| # | Regra |
|---|---|
| 1 | **Clarity Score mínimo: 12/15** para avançar |
| 2 | Score 9–11: preencher gaps antes de continuar |
| 3 | Score 0–8: **bloqueado**, coletar mais info |
| 4 | Todos os goals devem ter **MoSCoW** |
| 5 | Success Criteria devem ser **testáveis** |
| 6 | Out of Scope deve ser **explícito** |
| 7 | `/design` **não pode começar** sem este documento |
| 8 | Confidence threshold: **0.90** |

## Clarity Score — Guia de Pontuação

| Elemento | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Problem | Ausente | Vago | Específico | Claro + acionável |
| Users | Ausente | Genérico | Identificados | Com pain points |
| Goals | Ausente | Vagos | Mensuráveis | MoSCoW aplicado |
| Success | Ausente | Subjetivos | Objetivos | Testáveis automaticamente |
| Scope | Ausente | Implícito | Parcial | In/out explícito |
