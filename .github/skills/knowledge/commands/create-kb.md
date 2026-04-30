---
name: create-kb
description: Create a complete KB domain from scratch with MCP validation
---

# Create Knowledge Base Command

> Create a complete KB section from scratch with MCP validation.

## Usage

```bash
/knowledge-commands /create-kb <DOMAIN>
/knowledge-commands /create-kb <DOMAIN> --source <library-or-doc-id>
/knowledge-commands /create-kb <DOMAIN> --topics "<topic-1>, <topic-2>"
```

**Examples**: `/knowledge-commands /create-kb redis`, `/knowledge-commands /create-kb pandas`, `/knowledge-commands /create-kb authentication`

## What Happens

1. **Valida pré-requisitos** — verifica `.github/kb/_templates/` e cria `.github/kb/_index.yaml` se necessário
2. **Resolve fontes MCP** — usa `context7`/`ref` para docs oficiais e `exa`/`tavily` para sinais recentes quando útil
3. **Planeja escopo** — define conceitos, patterns e specs mínimos para o domínio
4. **Cria estrutura** — gera diretórios e arquivos a partir dos templates
5. **Atualiza registry** — adiciona ou atualiza entrada em `.github/kb/_index.yaml`
6. **Valida saída** — checa links, limites de linhas, datas MCP e score

## Quality Gates

Antes de escrever:

- O domínio deve estar normalizado em `kebab-case`.
- O domínio não pode sobrescrever KB existente sem confirmação explícita.
- As fontes MCP devem atingir confiança mínima de `0.80`.
- Os templates obrigatórios devem existir.

## Output

```text
KB Domain Created: .github/kb/{domain}/
Files: index.md, quick-reference.md, concepts/*, patterns/*, specs/*
Registry: .github/kb/_index.yaml
MCP Sources: context7/ref/exa/tavily
Validation Score: NN/100
```

## Next Step

`/knowledge-commands /update-kb <domain>` — para atualizar o domínio recém-criado com conteúdo adicional.

## See Also

- **Agent**: `.github/agents/architect.kb-architect.agent.md`
- **Templates**: `.github/kb/_templates/`
- **Registry**: `.github/kb/_index.yaml`
- **Example KB**: `.github/kb/{domain}/`
