---
name: knowledge-context-commands
description: 'AgentSpec commands for managing project knowledge context. Use /knowledge-context-commands + intent. Reads .github/config/grounding.md before executing. Commands: /create-context, /update-context, /check-context'
license: MIT
compatibility: 'GitHub Copilot VS Code, GitHub Copilot cloud agent'
metadata:
  version: "1.0.0"
  category: commands
  migrated-from: '.github/skills/knowledge-context/'
---

# Knowledge Context Commands

> Invoke: `/knowledge-context-commands` + descrição da tarefa

## Regras Globais Obrigatórias

Estas regras valem para todos os comandos desta skill. Se houver conflito com blocos legados migrados, esta seção vence.

### Grounding e Agente

1. Antes de executar qualquer comando, leia `.github/config/grounding.md`.
2. Leia `.github/config/routing.json`; se nenhuma rota específica casar, execute diretamente sem delegar a agente especialista.
3. Carregue apenas os arquivos de contexto necessários de `.github/knowledge_context/{slug}/`; nunca carregue todos os projetos de uma vez.
4. Toda resposta operacional deve iniciar com o bloco `[GROUNDING]` exigido por `.github/config/grounding.md`.

### Caminhos Canônicos

| Tipo | Caminho correto |
|---|---|
| Registry | `.github/knowledge_context/_registry.yaml` |
| Templates | `.github/knowledge_context/_templates/` |
| Contexto raiz | `.github/knowledge_context/{slug}/KNOWLEDGE_CONTEXT.md` |
| Arquitetura | `.github/knowledge_context/{slug}/architecture.md` |
| Regras | `.github/knowledge_context/{slug}/rules.md` |
| Roadmap | `.github/knowledge_context/{slug}/roadmap.md` |
| Glossário | `.github/knowledge_context/{slug}/domain-glossary.md` |
| Integrações | `.github/knowledge_context/{slug}/integrations.md` |

### Estrutura Mínima de um Knowledge Context

```text
.github/knowledge_context/{slug}/
├── KNOWLEDGE_CONTEXT.md     ← obrigatório
├── architecture.md          ← recomendado
├── rules.md                 ← recomendado
├── roadmap.md               ← opcional
├── domain-glossary.md       ← opcional
└── integrations.md          ← opcional
```

Crie arquivos a partir de `.github/knowledge_context/_templates/`:

| Saída | Template |
|---|---|
| `KNOWLEDGE_CONTEXT.md` | `_templates/KNOWLEDGE_CONTEXT.md` |
| `architecture.md` | `_templates/architecture.md` |
| `rules.md` | `_templates/rules.md` |
| `roadmap.md` | `_templates/roadmap.md` |
| `domain-glossary.md` | `_templates/domain-glossary.md` |
| `integrations.md` | `_templates/integrations.md` |
| entrada do registry | `_registry.yaml` campo `projects[]` |

Se `.github/knowledge_context/_registry.yaml` não existir, crie com estrutura base antes de registrar o primeiro projeto. Se existir, atualize apenas a entrada do projeto impactado.

## Comandos Disponíveis

| Comando | Descrição | Arquivo |
|---|---|---|
| `/create-context` | Criar knowledge context completo para um projeto | `commands/create-context.md` |
| `/update-context` | Atualizar arquivos de contexto de um projeto existente | `commands/update-context.md` |
| `/check-context` | Auditar o knowledge context ativo e reportar gaps | `commands/check-context.md` |

### Escalação

- Se `/create-context` revelar conflito com slug existente, pergunte antes de sobrescrever.
- Se `/update-context` revelar mudança arquitetural grande, proponha plano antes de editar múltiplos arquivos.
- Se `/check-context` detectar `active_project` apontando para slug inexistente, corrija o registry antes de continuar.

## See Also

- **Registry**: `.github/knowledge_context/_registry.yaml`
- **Templates**: `.github/knowledge_context/_templates/`
- **Design**: `.github/sdd/features/knowledge-context/DESIGN_KNOWLEDGE_CONTEXT.md`
