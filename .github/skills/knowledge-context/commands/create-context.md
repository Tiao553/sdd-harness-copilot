---
name: create-context
description: Create a complete knowledge context for a new project from templates
---

# Create Context Command

> Scaffold a full knowledge context for a project. Copies all templates, registers the project, and optionally sets it as active.

## Usage

```bash
/knowledge-context-commands /create-context <slug>
/knowledge-context-commands /create-context <slug> --name "<Project Name>"
/knowledge-context-commands /create-context <slug> --set-active
```

**Examples**:
```bash
/knowledge-context-commands /create-context my-api
/knowledge-context-commands /create-context data-platform --name "Data Platform v2" --set-active
/knowledge-context-commands /create-context mobile-app --name "Mobile App"
```

---

## What Happens

1. **Validate prerequisites**
   - Verificar se `.github/knowledge_context/_templates/` existe
   - Se `_registry.yaml` não existir, criar com estrutura base
   - Verificar se o slug já existe — se sim, perguntar antes de sobrescrever

2. **Normalize slug**
   - Converter para `kebab-case`
   - Ex: `My Project` → `my-project`, `DATA_PLATFORM` → `data-platform`

3. **Scaffold directory**
   - Criar `.github/knowledge_context/{slug}/`
   - Copiar todos os arquivos de `.github/knowledge_context/_templates/`
   - Substituir `{Project Name}` e `{slug}` nos arquivos copiados

4. **Register project**
   - Adicionar entrada em `_registry.yaml` com `slug`, `name`, `created_at`, `context_files`
   - Se `--set-active`: atualizar `active_project: {slug}`

5. **Report**
   - Listar arquivos criados
   - Indicar próximos campos obrigatórios a preencher em `KNOWLEDGE_CONTEXT.md`

---

## Quality Gates

Antes de criar:

- Slug deve estar em `kebab-case`.
- Slug não pode sobrescrever contexto existente sem confirmação explícita do usuário.
- Templates obrigatórios devem existir em `_templates/`.

---

## Output

```text
Knowledge Context Created: .github/knowledge_context/{slug}/
Files:
  ✅ KNOWLEDGE_CONTEXT.md    ← preencher: deployment_context, business_context
  ✅ architecture.md         ← preencher: stack, components
  ✅ rules.md                ← preencher: conventions, guardrails
  ✅ roadmap.md              ← preencher: milestones, current phase
  ✅ domain-glossary.md      ← preencher: entities, terms
  ✅ integrations.md         ← preencher: external APIs, contracts

Registry: .github/knowledge_context/_registry.yaml
Active Project: {slug} (se --set-active) | unchanged (se não)

Next: preencher KNOWLEDGE_CONTEXT.md com deployment_context antes de /brainstorm
```

---

## Next Step

`/knowledge-context-commands /check-context {slug}` — para auditar o que ainda precisa ser preenchido.

## See Also

- **Templates**: `.github/knowledge_context/_templates/`
- **Registry**: `.github/knowledge_context/_registry.yaml`
- **Design**: `.github/sdd/features/knowledge-context/DESIGN_KNOWLEDGE_CONTEXT.md`
