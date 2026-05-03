# Fase 0 — BRAINSTORM

```mermaid
flowchart TD
    START(["💡 Ideia / Requisito bruto"])
    START --> G

    subgraph G["🔍 Grounding Obrigatório"]
        G1["Ler CLAUDE.md"] --> G2["Ler WORKFLOW_CONTRACTS.yaml"]
        G2 --> G3["Carregar KB domains relevantes (≤ 3)"]
    end

    G --> KB

    subgraph KB["KB-First Resolution"]
        KB1["KB Discovery\nDomínio relevante existe?"]
        KB2["Codebase Exploration\nPadrões já implementados?"]
        KB3["Confidence Assignment\n0.0 → 1.0"]
        KB4["MCP Validation\nse confidence < 0.85"]
        KB1 --> KB2 --> KB3 --> KB4
    end

    KB --> S1

    S1["📌 Passo 1 — Gather Context
    BRAINSTORM anterior existe?
    Carregar contexto do projeto"]

    S1 --> S2

    S2["❓ Passo 2 — Discovery Questions
    Mínimo 3 perguntas obrigatórias
    Preferir múltipla escolha
    Uma pergunta por vez (sem question dump)"]

    S2 --> S3

    S3["🗂️ Passo 3 — Sample Collection
    Coletar inputs, outputs e ground truth
    Necessário para grounding do LLM"]

    S3 --> S4

    S4["⚖️ Passo 4 — Explore Approaches
    Apresentar 2 a 3 abordagens
    Cada uma com trade-offs claros
    Nunca apresentar abordagem única"]

    S4 --> S5

    S5["✂️ Passo 5 — Apply YAGNI
    'Precisa disso para o MVP?'
    Eliminar complexidade desnecessária"]

    S5 --> S6

    S6["🔁 Passo 6 — Validate Incrementally
    Mínimo 2 checkpoints com o usuário
    Apresentar progresso antes de finalizar"]

    S6 --> S7

    S7["💾 Passo 7 — Gerar Documento
    Salvar BRAINSTORM_{FEATURE}.md"]

    S7 --> GATE

    subgraph GATE["✅ Quality Gate"]
        GC1{"Problema claro e específico?"}
        GC2{"Usuários identificados?"}
        GC3{"≥ 2 abordagens com trade-offs?"}
        GC4{"YAGNI aplicado?"}
        GC5{"Samples coletados?"}
        GC6{"≥ 2 checkpoints validados?"}
    end

    GATE --> PASS{"Todos os itens ✅?"}
    PASS -->|"❌ Não"| S2
    PASS -->|"✅ Sim"| OUT

    OUT[/"📄 BRAINSTORM_{FEATURE}.md
    Status: Ready for Define
    Path: .github/sdd/features/{feature-name}/"/]

    OUT --> NEXT{"Próximo passo"}
    NEXT -->|"Fluxo normal"| DEFINE["➡️ /define"]
    NEXT -->|"Mudança futura"| ITERATE["🔄 /iterate"]

    subgraph ANTI["🚫 Anti-Patterns"]
        A1["Question dump\n(várias perguntas de uma vez)"]
        A2["Assumir respostas\nsem perguntar"]
        A3["Apresentar\napenas 1 abordagem"]
        A4["Ignorar\nconstraints técnicos"]
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

## Regras Rápidas

| # | Regra |
|---|---|
| 1 | Mínimo **3 perguntas** de discovery |
| 2 | Sempre **múltipla escolha** nas perguntas |
| 3 | Apresentar **2–3 abordagens** com trade-offs |
| 4 | Aplicar **YAGNI** — cortar o que não é MVP |
| 5 | **≥ 2 checkpoints** de validação com o usuário |
| 6 | Confidence threshold: **0.85** |
| 7 | Nunca fazer question dump — **uma pergunta por vez** |
