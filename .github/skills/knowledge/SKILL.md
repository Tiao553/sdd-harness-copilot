---
name: knowledge-commands
description: 'AgentSpec commands for knowledge. Use /knowledge-commands + intent. Reads .github/config/grounding.md before executing. Commands: /create-kb, /update-kb, /refresh-stale-kbs'
license: MIT
compatibility: 'GitHub Copilot VS Code, GitHub Copilot cloud agent'
metadata:
  version: "1.0.0"
  category: commands
  migrated-from: '.github/skills/knowledge/'
---

# Knowledge Commands

> Invoke: `/knowledge-commands` + descrição da tarefa

## Regras Globais Obrigatórias

Estas regras valem para todos os comandos desta skill. Se houver conflito com blocos legados migrados, esta seção vence.

### Grounding e Agente

1. Antes de executar qualquer comando, leia `.github/config/grounding.md`.
2. Leia `.github/config/routing.json`; se nenhuma rota específica casar, use `.github/agents/architect.kb-architect.agent.md`.
3. Leia `.github/agents/architect.kb-architect.agent.md` antes de criar, atualizar ou auditar KBs.
4. Carregue somente os arquivos necessários do domínio em `.github/kb/{domain}/`; nunca carregue o diretório inteiro.
5. Toda resposta operacional deve iniciar com o bloco `[GROUNDING]` exigido por `.github/config/grounding.md`.

### Caminhos Canônicos

| Tipo | Caminho correto |
|---|---|
| Domínios KB | `.github/kb/{domain}/` |
| Templates KB | `.github/kb/_templates/*.template` |
| Registry KB | `.github/kb/_index.yaml` |
| Agente KB | `.github/agents/architect.kb-architect.agent.md` |
| Quick reference | `.github/kb/{domain}/quick-reference.md` |
| Índice do domínio | `.github/kb/{domain}/index.md` |
| Conceitos | `.github/kb/{domain}/concepts/*.md` |
| Patterns | `.github/kb/{domain}/patterns/*.md` |
| Specs | `.github/kb/{domain}/specs/*.yaml` |

### MCPs e Fontes

Use MCPs para validar conhecimento antes de gravar conteúdo técnico. Ordem recomendada:

| MCP | Uso principal | Obrigatoriedade |
|---|---|---|
| `context7` | Documentação oficial de bibliotecas, frameworks e APIs versionadas | Preferencial |
| `ref` | Referência técnica/API quando disponível | Preferencial |
| `exa` ou `tavily` | Pesquisa ampla, exemplos de produção e mudanças recentes | Complementar |
| MCP específico do domínio | Cloud, banco, plataforma ou vendor quando existir | Preferencial para domínio |

Regras de validação:

- Use pelo menos 2 fontes quando o conteúdo afetar comandos, APIs, limites, sintaxe ou comportamento versionado.
- Se só houver 1 fonte confiável, registre caveat de confiança no relatório final.
- Se fontes conflitarem, não invente resolução; registre conflito e peça decisão.
- Todo arquivo criado ou atualizado deve conter `> **MCP Validated:** YYYY-MM-DD`.
- Preserve conteúdo local relevante; atualizações devem ser incrementais e rastreáveis.

### Estrutura Mínima de um KB

```text
.github/kb/{domain}/
├── index.md
├── quick-reference.md
├── concepts/
├── patterns/
└── specs/
```

Crie arquivos a partir de `.github/kb/_templates/`:

| Saída | Template |
|---|---|
| `index.md` | `index.md.template` |
| `quick-reference.md` | `quick-reference.md.template` |
| `concepts/{name}.md` | `concept.md.template` |
| `patterns/{name}.md` | `pattern.md.template` |
| `specs/{name}.yaml` | `spec.yaml.template` |
| entrada do registry | `domain-manifest.yaml.template` |

Se `.github/kb/_index.yaml` não existir, crie com raiz `domains:` antes de registrar o primeiro domínio. Se existir, atualize apenas a entrada do domínio impactado.

## Comandos Disponíveis

| Comando | Descrição | Arquivo | Agente |
|---|---|---|---|
| `/create-kb` | Criar KB domain completo com validação MCP | `commands/create-kb.md` | `kb-architect` |
| `/update-kb` | Atualizar KB existente com mudanças validadas | `commands/update-kb.md` | `kb-architect` |
| `/refresh-stale-kbs` | Identificar e atualizar KBs desatualizados | `commands/refresh-stale-kbs.md` | `kb-architect` |

### Escalação

- Se a criação de KB revelar dependência em domínio existente, proponha merge ou cross-reference antes de duplicar.
- Se a atualização revelar reestruturação grande, proponha plano antes de editar múltiplos domínios.
- Se o refresh detectar conflitos entre fontes MCP, registre conflito e peça decisão.

## See Also

- **Agent**: `.github/agents/architect.kb-architect.agent.md`
- **Example**: `.github/kb/{domain}/`
- **Templates**: `.github/kb/_templates/`
- **Registry**: `.github/kb/_index.yaml`

---
