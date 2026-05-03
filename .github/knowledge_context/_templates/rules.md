# Rules: {Project Name}

## Code Conventions

- {Convenção 1 — ex: snake_case para variáveis e funções}
- {Convenção 2 — ex: PascalCase para classes}
- {Convenção 3 — ex: type hints obrigatórios em Python}
- {Convenção 4 — ex: sem magic numbers, sempre usar constantes nomeadas}

---

## File & Module Organization

- {Regra 1 — ex: um arquivo por responsabilidade}
- {Regra 2 — ex: models em src/models/, handlers em src/handlers/}

---

## Branch & PR Rules

- {Regra 1 — ex: feature/* para novas features}
- {Regra 2 — ex: fix/* para correções}
- {Regra 3 — ex: PR com ao menos 1 reviewer antes de merge}
- {Regra 4 — ex: squash merge para manter histórico limpo}

---

## Testing Requirements

- {Regra 1 — ex: cobertura mínima de 80% para módulos de negócio}
- {Regra 2 — ex: testes unitários obrigatórios para funções de transformação}
- {Regra 3 — ex: testes de integração para toda rota HTTP}

---

## Security Guardrails

- {Regra 1 — ex: sem secrets em código, usar Vault / Secret Manager}
- {Regra 2 — ex: sem logging de dados sensíveis (PII)}
- {Regra 3 — ex: validar input em toda boundary externa}

---

## Anti-Patterns (proibidos neste projeto)

| Anti-Pattern | Motivo | Alternativa |
|---|---|---|
| {Padrão proibido 1} | {Por quê é problemático} | {O que usar no lugar} |
| {Padrão proibido 2} | {Por quê é problemático} | {O que usar no lugar} |

---

## Tooling Standards

| Tool | Purpose | Config File |
|---|---|---|
| {linter} | {formatação / lint} | {.pylintrc / .eslintrc} |
| {formatter} | {formatação} | {pyproject.toml / .prettierrc} |
| {test runner} | {testes} | {pytest.ini / jest.config.js} |
