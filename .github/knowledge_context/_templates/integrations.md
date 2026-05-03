# Integrations: {Project Name}

> APIs externas, serviços de terceiros e contratos de integração. Referência para o /design ao propor arquitetura.

---

## External APIs

| Service | Purpose | Auth Method | Base URL | Docs |
|---|---|---|---|---|
| {Service 1} | {Para que serve} | {API Key / OAuth / mTLS} | {https://...} | {link} |
| {Service 2} | {Para que serve} | {Auth method} | {https://...} | {link} |

---

## Internal Services

| Service | Purpose | Protocol | Contract Location |
|---|---|---|---|
| {Service A} | {Para que serve} | {REST / gRPC / Event} | {path/to/contract} |
| {Service B} | {Para que serve} | {REST / gRPC / Event} | {path/to/contract} |

---

## Event Bus / Queue

| Topic / Queue | Producer | Consumer | Schema |
|---|---|---|---|
| {topic-name} | {Serviço produtor} | {Serviço consumidor} | {path/to/schema} |

---

## Data Sources

| Source | Type | Access Method | Freshness | Owner |
|---|---|---|---|---|
| {Source 1} | {Postgres / S3 / API / etc.} | {Direct / CDC / Batch} | {Real-time / Hourly / Daily} | {time} |

---

## Rate Limits & SLAs

| Service | Rate Limit | SLA / Uptime | Notes |
|---|---|---|---|
| {Service 1} | {1000 req/min} | {99.9%} | {região, tier} |

---

## Auth & Secrets Management

| Secret | Storage | Rotation | Notes |
|---|---|---|---|
| {Secret name} | {Vault / AWS Secrets / etc.} | {Manual / Auto} | — |
