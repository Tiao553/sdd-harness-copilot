---
name: update-context
description: Update context files for an existing project — full file or targeted section
---

# Update Context Command

> Update one or more context files for an existing project. Supports full file update or targeted section edit.

## Usage

```bash
/knowledge-context-commands /update-context <slug>
/knowledge-context-commands /update-context <slug> --file <filename>
/knowledge-context-commands /update-context <slug> --file architecture.md
/knowledge-context-commands /update-context <slug> --set-active
```

**Examples**:
```bash
/knowledge-context-commands /update-context my-api
/knowledge-context-commands /update-context data-platform --file architecture.md
/knowledge-context-commands /update-context mobile-app --file rules.md
/knowledge-context-commands /update-context my-api --set-active
```

---

## What Happens

1. **Load current state**
   - Ler `_registry.yaml` e verificar que o slug existe
   - Se `--file` especificado: carregar apenas esse arquivo
   - Se não especificado: carregar `KNOWLEDGE_CONTEXT.md` + listar arquivos existentes e perguntar qual atualizar

2. **Identify changes**
   - Apresentar conteúdo atual do(s) arquivo(s)
   - Perguntar o que precisa ser atualizado (campo, seção ou arquivo completo)
   - Classificar impacto: Additive (novo campo) / Modifying (alterar existente) / Architectural (mudança de stack ou estrutura)

3. **Apply update**
   - Editar campos/seções especificados
   - Atualizar campo `Last Updated: YYYY-MM-DD` em `KNOWLEDGE_CONTEXT.md`
   - Se `--set-active`: atualizar `active_project` em `_registry.yaml`

4. **Cascade check**
   - Se mudança em `deployment_context` ou stack: alertar que features em andamento (BRAINSTORM/DEFINE/DESIGN) podem precisar de `/iterate`

5. **Report**
   - Listar campos modificados
   - Indicar se cascade foi detectado

---

## Quality Gates

Antes de atualizar:

- Slug deve existir em `_registry.yaml`.
- Mudanças arquiteturais (stack, cloud, estrutura) devem ser confirmadas antes de aplicar.
- Campo `Last Updated` deve ser atualizado em toda edição de `KNOWLEDGE_CONTEXT.md`.

---

## Output

```text
Knowledge Context Updated: .github/knowledge_context/{slug}/
Changes:
  ✅ {filename} — {campos alterados}

Last Updated: YYYY-MM-DD

Cascade Warning (se aplicável):
  ⚠️  deployment_context mudou — revisar BRAINSTORM/DEFINE/DESIGN em andamento com /iterate
```

---

## Next Step

`/knowledge-context-commands /check-context {slug}` — para confirmar que o contexto está completo após a atualização.

## See Also

- **Registry**: `.github/knowledge_context/_registry.yaml`
- **Iterate command**: `.github/skills/workflow-commands/commands/iterate.md`
- **Design**: `.github/sdd/features/knowledge-context/DESIGN_KNOWLEDGE_CONTEXT.md`
