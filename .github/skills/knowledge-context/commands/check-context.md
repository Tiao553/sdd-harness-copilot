---
name: check-context
description: Audit the knowledge context of a project — reports completeness, gaps, and health score
---

# Check Context Command

> Audit the knowledge context for a project. Reports which files exist, which fields are filled, and produces a health score with actionable gaps.

## Usage

```bash
/knowledge-context-commands /check-context
/knowledge-context-commands /check-context <slug>
/knowledge-context-commands /check-context --all
```

**Examples**:
```bash
/knowledge-context-commands /check-context
/knowledge-context-commands /check-context data-platform
/knowledge-context-commands /check-context --all
```

---

## What Happens

1. **Resolve target**
   - Sem argumento: usar `active_project` do `_registry.yaml`
   - Com `<slug>`: auditar esse projeto específico
   - Com `--all`: auditar todos os projetos registrados

2. **Registry check**
   - `_registry.yaml` existe?
   - `active_project` aponta para slug válido?
   - Projeto tem entrada no registry?

3. **File check** — para cada arquivo do projeto:

   | Arquivo | Obrigatório | Verificar |
   |---|---|---|
   | `KNOWLEDGE_CONTEXT.md` | ✅ Sim | `deployment_context` preenchido? `business_context` preenchido? `Last Updated` recente? |
   | `architecture.md` | Recomendado | Stack definida? Component map presente? |
   | `rules.md` | Recomendado | Conventions listadas? Anti-patterns definidos? |
   | `roadmap.md` | Opcional | Current phase definida? Milestones listados? |
   | `domain-glossary.md` | Opcional | Entidades principais definidas? |
   | `integrations.md` | Opcional | APIs externas documentadas? |

4. **Health score** — cálculo determinístico (0–100):

   | Item | Peso |
   |---|---|
   | `KNOWLEDGE_CONTEXT.md` existe e completo | 30 |
   | `architecture.md` existe e preenchida | 25 |
   | `rules.md` existe e preenchida | 20 |
   | `roadmap.md` existe | 10 |
   | `domain-glossary.md` existe | 8 |
   | `integrations.md` existe | 7 |

5. **Gap report** — listar campos com `{placeholder}` ou vazios como ações concretas

6. **Cascade warning** — se `active_project` mudou recentemente, alertar sobre features em andamento

---

## Quality Gates

Antes de reportar:

- Se `_registry.yaml` não existir: reportar como gap crítico, sugerir `/create-context`.
- Se `active_project` não tiver diretório correspondente: reportar como gap crítico.
- Nunca inferir dados — reportar o que existe literalmente.

---

## Output

```text
╔══════════════════════════════════════════════════╗
║  Knowledge Context Audit: {slug}                ║
║  Active: {"yes" | "no"}                         ║
╚══════════════════════════════════════════════════╝

Registry
  ✅ _registry.yaml exists
  ✅ active_project: {slug}

Files
  ✅ KNOWLEDGE_CONTEXT.md    — complete
  ✅ architecture.md         — complete
  ⚠️  rules.md               — exists but anti-patterns section empty
  ⬜ roadmap.md              — missing
  ⬜ domain-glossary.md      — missing
  ⬜ integrations.md         — missing

Fields Gap (KNOWLEDGE_CONTEXT.md)
  ⚠️  deployment_context.entry_points — still placeholder
  ✅ deployment_context.stack         — filled
  ✅ business_context                 — filled

Health Score: 72/100  🟡 MEDIUM

Action Items
  1. Fill deployment_context.entry_points in KNOWLEDGE_CONTEXT.md
  2. Complete rules.md anti-patterns section
  3. Create roadmap.md — run: /knowledge-context-commands /update-context {slug} --file roadmap.md

Next /brainstorm will inject: stack, entry_points, business_context automatically.
```

---

## Next Steps

- Gaps encontrados → `/knowledge-context-commands /update-context {slug} --file <filename>`
- Projeto não existe → `/knowledge-context-commands /create-context {slug}`

## See Also

- **Registry**: `.github/knowledge_context/_registry.yaml`
- **Create command**: `.github/skills/knowledge-context/commands/create-context.md`
- **Update command**: `.github/skills/knowledge-context/commands/update-context.md`
- **Design**: `.github/sdd/features/knowledge-context/DESIGN_KNOWLEDGE_CONTEXT.md`
