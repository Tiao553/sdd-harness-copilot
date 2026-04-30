---
name: core-commands
description: 'AgentSpec commands for core. Use /core-commands + intent. Reads .github/config/grounding.md before executing. Commands: /meeting, /memory, /readme-maker, /status, /sync-context'
license: MIT
compatibility: 'GitHub Copilot VS Code, GitHub Copilot cloud agent'
metadata:
  version: "2.0.0"
  category: commands
  migrated-from: '.github/skills/core-commands/commands/'
---

# Core Commands

> Invoke: `/core-commands` + descrição da tarefa

## Regras Globais Obrigatórias

Estas regras valem para todos os comandos desta skill.

### Grounding e Roteamento

1. Antes de executar qualquer comando, leia `.github/config/grounding.md`.
2. Leia `.github/config/routing.json` e selecione o agente pelo comando solicitado.
3. Leia o arquivo do agente selecionado em `.github/agents/`.
4. Toda resposta operacional deve iniciar com o bloco `[GROUNDING]` exigido por `.github/config/grounding.md`.

### Caminhos Canônicos

| Tipo | Caminho correto |
|---|---|
| Storage persistente | `.github/storage/` |
| Memória do projeto | `.github/storage/memory/` |
| Status do projeto | `_meta/STATUS.md` |
| Contexto do projeto | `_meta/CONTEXT.md` |
| Instruções Copilot | `.github/copilot-instructions.md` |
| Agentes | `.github/agents/{category}/{name}.agent.md` |
| KB domains | `.github/kb/{domain}/` |

### Regras de Caminho

- Nunca use caminhos `.claude/**`, `.agents/**` ou `GEMINI.md`.
- Storage local usa `.github/storage/`, não a raiz do repositório.
- Artefatos de documentação (README, docs/) seguem convenções do repositório.

### Constraints

- Não inicie fases SDD a partir desta skill.
- Não use sintaxe `#skill:` ou `skill:`.
- Se o comando exigir um agente que não existe, pare e reporte ao invés de inventar.

## Comandos Disponíveis

| Comando | Descrição | Arquivo | Agente |
|---|---|---|---|
| `/meeting` | Análise de transcrições de reunião | `commands/meeting.md` | `meeting-analyst` |
| `/memory` | Gestão de memória e contexto do projeto | `commands/memory.md` | `codebase-explorer` |
| `/readme-maker` | Geração e atualização de README | `commands/readme-maker.md` | `codebase-explorer` |
| `/status` | Status e saúde do projeto | `commands/status.md` | `codebase-explorer` |
| `/sync-context` | Sincronização de contexto entre sessões | `commands/sync-context.md` | `codebase-explorer` |

### Execução

Para cada comando, leia o arquivo correspondente em `commands/` e siga as instruções detalhadas contidas nele. O arquivo do comando é a fonte autoritativa de lógica, passos e formato de saída.
