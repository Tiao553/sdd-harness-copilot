# Architecture: {Project Name}

## Stack

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Language | {Python / Node / Go} | {x.x} | — |
| Framework | {FastAPI / Express / etc.} | {x.x} | {camada de API} |
| Database | {PostgreSQL / MongoDB / etc.} | {x.x} | {store principal} |
| Queue / Stream | {Kafka / SQS / Pub/Sub} | — | {se aplicável} |
| Infra / IaC | {Terraform / CDK / Pulumi} | {x.x} | {cloud provider} |
| Observability | {Datadog / CloudWatch / etc.} | — | — |

---

## Component Map

```text
[Componente A] → [Componente B] → [DB]
                      ↓
                 [Queue] → [Worker] → [Storage]
```

---

## Key Architecture Decisions

| Decision | Choice | Reason |
|---|---|---|
| {Decisão 1} | {Escolha} | {Motivo} |
| {Decisão 2} | {Escolha} | {Motivo} |

---

## Deployment Topology

| Environment | Region | Notes |
|---|---|---|
| dev | {region} | {detalhes} |
| staging | {region} | {detalhes} |
| prod | {region} | {detalhes} |

---

## Forbidden Patterns

> O que NÃO fazer neste projeto.

- {Anti-pattern 1 — ex: não usar ORM para queries analíticas}
- {Anti-pattern 2}
