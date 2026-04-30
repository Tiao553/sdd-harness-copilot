# BRAINSTORM: Local Analytics Stack

> Exploratory session to clarify intent and approach before requirements capture

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | LOCAL_ANALYTICS_STACK |
| **Date** | 2026-04-28 |
| **Author** | brainstorm-agent |
| **Status** | Approaches Identified / Ready for Define |

---

## Initial Idea

**Raw Input:** "Quero montar um ambiente analítico local com dbt, airflow, postgres e supabase"

**Translation:** Setup a local analytics environment with dbt, Airflow, Postgres, and Supabase

**Context Gathered:**
- User is working in AgentSpec (Data Engineering framework with 58 specialized agents)
- Robust KBs available for dbt, Airflow, SQL patterns, data modeling
- Project values spec-first development (BRAINSTORM → DEFINE → DESIGN → BUILD)
- User has experience with analytics stack components

**Technical Context Observed:**

| Aspect | Observation | Implication |
|--------|-------------|-------------|
| Likely Location | `.github/infra/docker-compose.yml` + `dbt/` + `airflow/dags/` | Services managed in repo root |
| Relevant KB Domains | dbt, airflow, postgres, supabase, lakehouse, testing, terraform | Multi-domain orchestration needed |
| IaC Patterns | Docker/Docker Compose expected for local + GitHub Actions for CI/CD | Container-first approach |
| Stack Maturity | dbt Core 1.9+, Airflow 3.0 GA, Postgres 15+ | Modern versions assumed |

---

## Discovery Questions & Answers

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | Primary goal: Dev/POC/Full Stack/Learning? | **(c) Full Stack** — Replicate production stack locally for E2E testing | Drives resource allocation & architecture decisions |
| 2 | Users: Solo/Team/CI/CD/Multiple? | **(d) Multiple** — Dev local + CI/CD pipelines | Must support both interactive dev and automated execution |
| 3 | Main constraint: Simplicity/Parity/Resources/Time? | **(e) Multiple concerns** — Simplicidade + resources definidos + fácil replicação | Docker Compose ideal for balancing these |
| 4 | Sample data: Fixtures/Schema/Synthetic/External? | **(c) Synthetic do zero** — Generate sample data from scratch | No external dependencies, fully reproducible |

**Validation checkpoints:**
1. ✅ User confirmed Approach A (Docker Compose) aligns with all answers
2. ✅ User explicitly chose Approach A over Approach B (venv + Docker)

---

## Sample Data Inventory

> Samples improve LLM accuracy through in-context learning. Here we define what WILL be created.

| Type | Location | Count | Notes |
|------|----------|-------|-------|
| Input seed files | `dbt/seeds/` | 3 CSV | customers, transactions, products (synthetic) |
| dbt models | `dbt/models/` | ~8 models | staging → marts pipeline |
| Test fixtures | `dbt/tests/` | ~5 fixtures | Data quality + unit tests |
| Airflow DAG | `airflow/dags/main_pipeline.py` | 1 DAG | Orchestrates dbt run + Postgres queries |
| Docker seed scripts | `docker/postgres-init/` | 2 SQL | Initial schema + data generation |
| CI/CD reference | `.github/workflows/` | 1 workflow | Local → CI/CD parity verification |

**How samples will be used:**
- Few-shot examples in Airflow DAG definition (task structure, error handling)
- Schema reference for dbt staging layer
- Test fixtures for data quality validation in CI/CD
- Docker entrypoint scripts for reproducible seed data

---

## Approaches Explored

### Approach A: Docker Compose (All-in-One) ⭐ **SELECTED**

**Description:** Single `docker-compose.yml` orchestrates 4 containers (Postgres, Supabase, Airflow, dbt) with defined CPU/memory limits. dbt runs via CLI in Airflow tasks or host. Synthetic data generated via SQL scripts in container entrypoint.

**Architecture:**
```yaml
services:
  postgres:              # Data warehouse (8GB reserved)
  supabase:              # Analytics platform (8GB reserved) 
  airflow-webserver:     # Orchestrator (4GB reserved)
  airflow-scheduler:
  dbt:                   # Transformation CLI (2GB reserved, volume mount)
  
volumes:
  postgres_data:
  supabase_data:
  dbt_artifacts:
  airflow_logs:
```

**Pros:**
- ✅ **Simplicidade máxima:** 1 command (`docker-compose up`), fully self-contained
- ✅ **Resources defined:** Each service has explicit CPU/memory limits
- ✅ **Easy replication:** Clone repo + docker-compose up (works anywhere Docker runs)
- ✅ **CI/CD ready:** GitHub Actions can run via Docker or docker-compose plugin
- ✅ **Synthetic data:** Generated via SQL/Python entrypoint scripts (no external sources)
- ✅ **Development velocity:** Hot-reload for dbt + Airflow DAG changes
- ✅ **Production parity:** Services run same versions as production

**Cons:**
- ❌ **Docker dependency:** Requires Docker Desktop or daemon
- ❌ **Less flexibility:** Tuning per developer requires compose override files
- ❌ **Supabase weight:** Full Supabase stack in Docker adds ~2-3GB overhead
- ❌ **Initial startup time:** First `docker-compose up` takes ~60-90s

**Why Recommended:**
- Balances **simplicity + resources + replication** perfectly
- Covers both dev (local hot-reload) + CI/CD (GitHub Actions) use cases
- Synthetic data strategy eliminates external dependencies
- KB patterns (dbt + Airflow) align with this architecture

---

### Approach B: Local venv + Docker for Storage

**Description:** dbt and Airflow run in local Python venv; only Postgres/Supabase in Docker. Lighter containerization, more control over Python dependencies.

**Pros:**
- ✅ Faster iteration (local venv = Python hot-reload native)
- ✅ Smaller Docker footprint (only DB services)
- ✅ Supabase feature control (Auth, Realtime selectively enabled)
- ✅ GitHub Actions native (pip install is standard)

**Cons:**
- ❌ More setup steps (create venvs, install dbt-postgres, airflow)
- ❌ Less portable (Python 3.10+ required on host; packages may differ)
- ❌ Harder CI/CD parity (different envs locally vs. Actions)

**Why not recommended for your case:**
- You emphasized **simplicidad** — this requires more manual steps
- You need **CI/CD parity** — easier with full Docker Compose
- KB patterns favor orchestrated Docker setups

---

### Approach C: Kubernetes (Helm/k3s) — Overkill

**Description:** Mini-cluster with k3s + Helm charts for maximum production parity.

**Cons:**
- ❌ **Over-engineering:** Too complex for "local simples"
- ❌ **Unnecessary overhead:** k3s/Minikube adds 5-10GB+ overhead
- ❌ **Setup time:** Steep learning curve
- ❌ **Not truly local:** Becomes mini-cluster, loses simplicity

**Status:** Explicitly rejected during exploration.

---

## Features Considered but Removed (YAGNI)

> Scope reduction for MVP — focusing on core analytics loop

| Feature | Why Considered | Why Removed | Deferred To |
|---------|---|---|---|
| dbt-cloud integration | Prod uses dbt Cloud | Local uses dbt Core (simpler) | Phase 2 (optional prod sync) |
| Spark / PySpark support | Scalability | Postgres sufficient for local testing | Future phase if needed |
| Multi-region setup | Prod replication | Single region (localhost) sufficient | Production deployment |
| minio / S3-compatible storage | Data lake pattern | Not needed for MVP (Postgres suffices) | Phase 2 if medallion architecture needed |
| Observability stack (Prometheus/Grafana) | Prod best practice | Out of scope for analytics MVP | Phase 3 (monitoring) |
| Kubernetes-style orchestration | Production parity | Docker Compose adequate for local | Future phase if scaling to team |

---

## Validation Checkpoints

**Checkpoint 1:** ✅ Completed
- **Check:** User confirmed Full Stack (not Dev/POC) as goal
- **Result:** Drives need for production-like resource allocation

**Checkpoint 2:** ✅ Completed
- **Check:** User confirmed both local dev + CI/CD use cases
- **Result:** Docker Compose supports both patterns natively

**Checkpoint 3:** ✅ Completed
- **Check:** User confirmed Approach A aligns with constraints (simplicity + resources + replication)
- **Result:** Proceeding with Docker Compose as foundation

---

## Identified KB Domains (For Define Phase)

- `.github/kb/dbt/` — Model structure, materialization strategy, testing
- `.github/kb/airflow/` — DAG patterns, TaskFlow API, scheduling
- `.github/kb/supabase/` — Postgres integration, Auth mocking
- `.github/kb/data-modeling/` — Star schema, dimension tables
- `.github/kb/testing/` — Data quality tests, dbt tests
- `.github/kb/terraform/` — IaC for infrastructure as code (optional production deploy)

---

## Draft Requirements (For Define Phase)

Based on exploration, these will be formalized in DEFINE:

### Functional Requirements
1. Local dbt project runs transformations against Postgres
2. Airflow DAG orchestrates daily dbt run + data quality checks
3. Supabase provides secondary analytics DB with same schema
4. Synthetic seed data (customers, transactions, products) auto-generates on startup
5. dbt models follow medallion architecture (bronze/silver/gold layers)

### Non-Functional Requirements
1. **Resources:** Docker Compose reserves exactly: Postgres 8GB, Supabase 8GB, Airflow 4GB, dbt 2GB
2. **Reproducibility:** Running `docker-compose up` from cloned repo requires 0 external setup
3. **Development velocity:** Changes to dbt models reflected in <30s (no full rebuild needed)
4. **CI/CD compatibility:** GitHub Actions can run full test suite in <5 min

### Success Criteria
1. ✅ `docker-compose up` starts all services successfully
2. ✅ `dbt run` completes in <2 min with 0 errors
3. ✅ `dbt test` runs and reports data quality status
4. ✅ Airflow UI accessible at `localhost:8080`
5. ✅ Both Postgres + Supabase contain identical transformed data
6. ✅ GitHub Actions workflow completes in <5 min

---

## Next Step

👉 **Ready for:** `#skill:workflow-commands /define BRAINSTORM_LOCAL_ANALYTICS_STACK.md`

This BRAINSTORM document captures:
- ✅ All 4 discovery questions + validation
- ✅ 3 approaches with clear trade-off analysis
- ✅ Approach A explicitly selected
- ✅ YAGNI applied (features removed)
- ✅ Sample data strategy defined
- ✅ KB domains identified
- ✅ Draft requirements ready for formalization

Proceeding to DEFINE phase will capture formal acceptance criteria, resource constraints, and integration points.

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-28 | brainstorm-agent | Initial brainstorm exploration |
