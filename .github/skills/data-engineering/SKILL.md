---
name: data-engineering-commands
description: 'AgentSpec commands for data-engineering. Use /data-engineering-commands + intent. Reads .github/config/grounding.md before executing. Commands: /ai-pipeline, /data-contract, /data-quality, /lakehouse, /migrate, /pipeline, /schema, /sql-review'
license: MIT
compatibility: 'GitHub Copilot VS Code, GitHub Copilot cloud agent'
metadata:
  version: "1.1.0"
  category: commands
  migrated-from: '.github/skills/data-engineering/'
---

# Data-Engineering Commands

> Invoke: `/data-engineering-commands` + descrição da tarefa

## Regras Globais Obrigatórias

Estas regras valem para todos os comandos desta skill.

### Grounding e Roteamento

1. Antes de executar qualquer comando, leia `.github/config/grounding.md`.
2. Leia `.github/config/routing.json` e selecione o agente pelo comando solicitado.
3. Leia o arquivo do agente selecionado (ver tabela de comandos abaixo).
4. Carregue KB quick-reference do domínio indicado na tabela de routing (lazy loading).
5. Toda resposta operacional deve iniciar com o bloco `[GROUNDING]` exigido por `.github/config/grounding.md`.

### Delegação de Agentes

Cada comando delega a um agente primário. Se o escopo exigir, o agente primário pode escalar para agentes complementares:

- **Agente primário**: executa o core da tarefa
- **Agente de escalação**: ativado para edge cases, cross-domain, ou validação complementar
- Cada agente delegado deve ler seu agent file e carregar KB quick-reference se declarado

### Caminhos Canônicos

| Tipo | Caminho correto |
|---|---|
| Agentes data-engineering | `.github/agents/data-engineering.{name}.agent.md` |
| Agentes architect | `.github/agents/architect.{name}.agent.md` |
| Agentes test | `.github/agents/test.{name}.agent.md` |
| KB domains | `.github/kb/{domain}/quick-reference.md` |
| Templates | `.github/sdd/templates/*.md` |
| Instruções Copilot | `.github/copilot-instructions.md` |

### Regras de Caminho

- Nunca use caminhos `.claude/**` ou `.agents/**`.
- KB loading é lazy: carregue apenas quick-reference.md do domínio relevante.
- Se um domínio KB não existir, registre e continue sem ele.

### Constraints

- Não inicie fases SDD a partir desta skill.
- Não use sintaxe `#skill:` ou `skill:`.
- Output de comandos que geram código deve ir para `./projects/{feature-name}/` quando em contexto de build.

## Comandos Disponíveis

| Comando | Descrição | Arquivo | Agente Primário | KB Domains |
|---|---|---|---|---|
| `/ai-pipeline` | RAG, embeddings, vector DBs, feature stores | `commands/ai-pipeline.md` | `ai-data-engineer` | `ai-data-engineering`, `streaming` |
| `/data-contract` | Contratos de dados (ODCS), SLAs, governance | `commands/data-contract.md` | `data-contracts-engineer` | `data-quality`, `data-modeling` |
| `/data-quality` | Regras de qualidade, expectations, test suites | `commands/data-quality.md` | `data-quality-analyst` | `data-quality`, `dbt`, `data-modeling` |
| `/lakehouse` | Table formats, catalogs, medallion architecture | `commands/lakehouse.md` | `lakehouse-architect` | `lakehouse`, `cloud-platforms`, `spark` |
| `/migrate` | Migrações de ETL legado para stacks modernos | `commands/migrate.md` | `dbt-specialist` / `spark-engineer` | `dbt`, `spark`, `airflow`, `sql-patterns` |
| `/pipeline` | Orquestração de pipelines (Airflow, dbt, etc.) | `commands/pipeline.md` | `pipeline-architect` | `airflow`, `dbt`, `data-quality` |
| `/schema` | Design de schema, modelagem dimensional | `commands/schema.md` | `schema-designer` | `data-modeling`, `sql-patterns`, `data-quality` |
| `/sql-review` | Review de SQL, performance, anti-patterns | `commands/sql-review.md` | `code-reviewer` | `sql-patterns`, `data-quality`, `dbt` |

### Escalação Cross-Command

Quando um comando detectar necessidade de outro domínio:

- Pipeline + qualidade → delegue checks para `/data-quality`
- Schema + contratos → delegue governance para `/data-contract`
- Migration + lakehouse → delegue table format para `/lakehouse`

O agente deve informar a escalação e continuar ou pedir confirmação, dependendo do impacto.
