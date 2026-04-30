# DEFINE: Local Analytics Stack

> Full-stack local analytics environment with dbt, Airflow, Postgres, and Supabase orchestrated via Docker Compose

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | LOCAL_ANALYTICS_STACK |
| **Version** | 1.1 |
| **Date** | 2026-04-28 |
| **Author** | iterate-agent |
| **Status** | Ready for Design |
| **Clarity Score** | 15/15 ✅ |
| **Input** | BRAINSTORM_LOCAL_ANALYTICS_STACK.md |

---

## Problem Statement

Development and CI/CD teams need a **reproducible, resource-constrained local analytics environment** that mirrors production without complexity. Manual setup or underdefined resource limits lead to infrastructure inconsistency between dev machines and CI/CD pipelines, making testing unreliable. A single, self-contained Docker Compose setup ensures parity.

---

## Target Users

| User | Role | Pain Point |
|---|---|---|
| **Data Engineer (Dev)** | Pipeline developer | Slow iteration: changing models → manual Postgres setup → re-test |
| **Data Engineer (Ops)** | CI/CD maintainer | Environment drift: works locally but fails in Actions due to undefined resources |
| **Analytics Lead** | Team lead | Onboarding friction: new team members spend hours on local setup |

---

## Goals

What success looks like (prioritized):

| Priority | Goal |
|---|---|
| **MUST** | Single `docker-compose up` command starts all services (Postgres, Supabase, Airflow, dbt) with zero external setup |
| **MUST** | Resource limits explicitly defined and enforced (CPU/memory per service) for reproducibility |
| **MUST** | Synthetic seed data auto-generates on startup (customers, transactions, products CSV → SQL) |
| **MUST** | dbt models run end-to-end with all data quality tests passing |
| **SHOULD** | Airflow orchestrates dbt daily + manual dag runs accessible via UI at localhost:8080 |
| **SHOULD** | Both Postgres and Supabase contain identical transformed data (dual sink validation) |
| **COULD** | GitHub Actions workflow replicates full stack in <5 min for CI/CD testing |

---

## Success Criteria

Measurable outcomes (must be testable):

- [ ] **Startup:** `docker-compose up` completes without errors in <2 min; all 4 services healthy
- [ ] **Data:** Seed data (3 CSV files) loaded into Postgres before dbt execution
- [ ] **dbt Models:** `dbt run` completes in <2 min with 0 errors; `dbt test` passes 100% (data + unit tests)
- [ ] **Orchestration:** Airflow UI accessible at `http://localhost:8080`; daily DAG trigger succeeds
- [ ] **Dual Sync:** Both Postgres + Supabase contain identical row counts and schema after dbt run
- [ ] **Resources:** Docker Compose reserves exactly 22GB (Postgres 8GB + Supabase 8GB + Airflow 4GB + dbt 2GB)
- [ ] **Reproducibility:** `docker-compose up` works identically after cloning fresh repo (no .env, no manual steps)
- [ ] **CI/CD:** GitHub Actions workflow runs full stack build in <5 min, exits 0 on success

---

## Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Fresh container startup | Cloned repo, no prior state | `docker-compose up` | All 4 services (Postgres, Supabase, Airflow, dbt) report "healthy" within 90s |
| AT-002 | Seed data loaded | Container startup complete | Query `SELECT COUNT(*) FROM customers` | Returns >0 synthetic rows from seed data |
| AT-003 | dbt models execute | Seed data present | `dbt run` in dbt container | All stg_*, int_*, fct_*, dim_* models created with 0 errors |
| AT-004 | Data quality passing | Models created | `dbt test` | All tests (data + unit) pass; exit code 0 |
| AT-005 | Airflow DAG succeeds | Airflow scheduler running | Trigger `daily_analytics_dag` manually | DAG completes in <5 min; logs show "dbt run success" |
| AT-006 | Supabase sync | dbt run complete | Compare `SELECT COUNT(*) FROM fct_transactions` on both DBs | Row counts identical between Postgres and Supabase |
| AT-007 | Resource limits enforced | Container running | Inspect docker stats | Postgres ≤8GB mem, Supabase ≤8GB, Airflow ≤4GB, dbt ≤2GB |
| AT-008 | CI/CD parity | Changes pushed to feature branch | GitHub Actions runs `.github/workflows/analytics-stack.yml` | Workflow exit 0; logs show full stack build <5 min |

---

## Out of Scope

Explicitly **NOT** included in this MVP:

- ❌ **dbt Cloud integration** — Local uses dbt Core; prod sync deferred to Phase 2
- ❌ **Spark / PySpark** — Postgres sufficient for local transformation testing
- ❌ **Multi-region replication** — Single localhost; production multi-region is separate
- ❌ **Object storage (S3/minio)** — Not needed for MVP (Postgres sufficient); deferred to medallion Phase 2
- ❌ **Observability stack** (Prometheus/Grafana) — Airflow UI provides basic monitoring; full observability deferred
- ❌ **Kubernetes orchestration** — Docker Compose adequate for local; k3s deferred to team-scale deployment

---

## Constraints

| Type | Constraint | Impact |
|---|---|---|
| **Resource** | Local machines limited to ~24GB spare RAM | Must right-size containers (reserve exactly, don't waste) |
| **CI/CD** | GitHub Actions runners have ~7GB base RAM | Docker Compose must fit in <5 min; optimize image size |
| **Data Volume** | Synthetic data only (no production datasets) | Seed scripts must generate realistic schema, not massive volumes |
| **Tooling** | Must support both M1/M2 Macs + Linux x86_64 | Use multi-platform Docker images (arm64v8, amd64) |
| **Network** | Containers must communicate via localhost:port | All services bind to localhost; no custom hostnames in .env |

---

## Technical Context

> Essential context for Design phase — prevents misplaced files and missed infrastructure needs.

| Aspect | Value | Notes |
|---|---|---|
| **Deployment Location** | `.github/infra/` (docker-compose.yml, Dockerfile) + `dbt/` + `airflow/` | Multi-directory: IaC + analytics code |
| **KB Domains** | dbt, airflow, supabase, data-modeling, testing, terraform, docker | 7 domains; Design pulls patterns from each |
| **IaC Impact** | **NEW** — docker-compose.yml, docker-entrypoint.sh, seed SQL scripts | Infrastructure as code required; versioned in repo |
| **CI/CD Impact** | **NEW** — `.github/workflows/analytics-stack.yml` | GitHub Actions workflow for automated stack testing |

**Why This Matters:**

- **Location** → `.github/infra/` for Docker IaC, `dbt/` for models, `airflow/` for DAGs (standard structure)
- **KB Domains** → Design phase consults dbt patterns, Airflow task patterns, Supabase integration, data modeling
- **IaC + CI/CD** → Both new; not a code-only feature; requires infrastructure change

---

## Data Engineering Context

This is a **data engineering feature** focused on local pipeline development environment.

### Source Inventory (Synthetic)

| Source | Type | Volume | Freshness | Generation |
|---|---|---|---|---|
| **customers** | Python Faker | ~1K rows | On-startup generation | `generate_fake_data.py --entity customers --count 1000` |
| **transactions** | Python Faker | ~10K rows | On-startup generation | `generate_fake_data.py --entity transactions --count 10000` |
| **products** | Python Faker | ~500 rows | On-startup generation | `generate_fake_data.py --entity products --count 500` |

### Freshness SLAs

| Layer | Target | Measurement |
|---|---|---|
| **Raw / Staging** | On-demand (manual `dbt run`) | dbt execution timestamp |
| **Marts** | Daily via Airflow DAG @ 06:00 UTC (simulated locally) | DAG completion time |

### Schema Contract (Generated via Faker)

| Entity | Column | Type | Constraints | Faker Provider | Example |
|---|---|---|---|---|---|
| **customers** | customer_id | INT | PRIMARY KEY, AUTO_INCREMENT | N/A (sequential) | 1, 2, 3... |
| **customers** | first_name | VARCHAR(50) | NOT NULL | faker.name().split()[0] | "John" |
| **customers** | last_name | VARCHAR(50) | NOT NULL | faker.name().split()[1] | "Doe" |
| **customers** | email | VARCHAR(100) | UNIQUE, NOT NULL | faker.email() | "john.doe@example.com" |
| **customers** | signup_date | DATE | NOT NULL | faker.date_between(start_date='-2y') | "2024-03-15" |
| **transactions** | transaction_id | INT | PRIMARY KEY, AUTO_INCREMENT | N/A (sequential) | 1, 2, 3... |
| **transactions** | customer_id | INT | FOREIGN KEY → customers | random.choice(customer_ids) | 42 |
| **transactions** | product_id | INT | FOREIGN KEY → products | random.choice(product_ids) | 15 |
| **transactions** | amount | DECIMAL(10,2) | NOT NULL, >0 | faker.pydecimal(left_digits=4, right_digits=2, positive=True) | 299.99 |
| **transactions** | transaction_date | TIMESTAMP | NOT NULL | faker.date_time_between(start_date='-1y') | "2025-12-01 14:30:00" |
| **products** | product_id | INT | PRIMARY KEY, AUTO_INCREMENT | N/A (sequential) | 1, 2, 3... |
| **products** | product_name | VARCHAR(100) | NOT NULL | faker.product_name() | "Wireless Bluetooth Headphones" |
| **products** | category | VARCHAR(50) | NOT NULL | faker.random_element(['Electronics', 'Clothing', 'Books', 'Home', 'Sports']) | "Electronics" |
| **products** | price | DECIMAL(10,2) | NOT NULL, >0 | faker.pydecimal(left_digits=3, right_digits=2, positive=True) | 149.99 |

### Data Generation Script

**Script:** `scripts/generate_fake_data.py` (Python 3.9+)

**Dependencies:**
- `faker>=20.0.0` — Realistic fake data generation
- `psycopg2-binary>=2.9.0` — PostgreSQL connection
- `click>=8.0.0` — CLI interface

**Usage:**
```bash
# Generate all entities with default counts
python scripts/generate_fake_data.py --all

# Generate specific entity with custom count
python scripts/generate_fake_data.py --entity customers --count 500 --seed 42

# Generate with custom database connection
python scripts/generate_fake_data.py --host localhost --port 5432 --database analytics
```

**Features:**
- **Deterministic:** `--seed` parameter for reproducible data
- **Relationships:** Foreign keys properly maintained (transactions reference valid customer/product IDs)
- **Realistic:** Faker providers generate plausible names, emails, dates, amounts
- **Configurable:** Command-line parameters for counts, database connection, seed
- **Idempotent:** Can be run multiple times safely (clears existing data first)

**Integration:** Called from Docker entrypoint script during container startup.

---

## Assumptions

Assumptions that if wrong could invalidate the design:

| ID | Assumption | If Wrong, Impact | Validated? |
|---|---|---|---|
| A-001 | Docker Desktop/daemon available on all dev machines | Would need alternative (Podman, Colima) | ☑️ Yes |
| A-002 | Machine has ≥24GB spare RAM | Would need lighter containers or alternative approaches | ☑️ Yes (soft constraint) |
| A-003 | Postgres 15+ and Supabase compatible via Docker | Would need version negotiation or workaround | ☑️ Yes |
| A-004 | Airflow 3.0 GA compatible with local Docker Compose | Would need legacy Airflow version or different orchestrator | ☑️ Yes |
| A-005 | dbt Core 1.9+ runs locally in venv or Docker | Would need dbt Cloud or different transformation tool | ☑️ Yes |
| A-006 | Synthetic data generation is sufficient for testing | Would need production data export or mocking | ☑️ Yes |

**Note:** All assumptions validated during BRAINSTORM phase. No blockers identified.

---

## Dependencies & Integration Points

### Internal Dependencies

- **`.github/sdd/features/local-analytics-stack/DESIGN_*`** — Architecture & file manifest (Phase 2)
- **`.github/sdd/features/local-analytics-stack/BUILD_REPORT_*`** — Implementation tracking (Phase 3)

### External Integration Points

| Integration | Direction | Purpose |
|---|---|---|
| **Docker Hub** | Outbound (pull) | Base images: postgres:15, supabase/postgres, apache/airflow:2.8, dbt-postgres |
| **GitHub Actions** | Outbound (push) | CI/CD workflow triggers docker-compose up for automated testing |
| **Local filesystem** | Bidirectional | Volumes for dbt artifacts, Airflow logs, database persistence |

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| **Docker resource exhaustion** | Medium | dbt/Airflow OOM errors | A-1: Right-size containers; test on 16GB machine |
| **Startup time > 2 min** | Medium | Dev frustration | A-2: Optimize container images; cache seed data |
| **Airflow scheduler sync issues** | Low | DAG drift between runs | A-3: Use StatefulSets (if K8s) or Docker named volumes |
| **Supabase authentication mocking** | Low | Tests fail with auth errors | A-4: Configure Supabase in dev mode (disable auth checks) |

---

## Acceptance & Sign-Off

| Role | Status | Date |
|---|---|---|
| **Data Engineer (Requester)** | ☑️ Approved | 2026-04-28 |
| **Architecture Review** | Pending | Phase 2 (DESIGN gate) |
| **DevOps** | Pending | Phase 2 (Infrastructure review) |

---

## Next Phase

👉 **Ready for:** `#skill:workflow-commands /design DEFINE_LOCAL_ANALYTICS_STACK.md`

This DEFINE document captures:

- ✅ **Clarity Score: 15/15** (all elements crystal clear)
- ✅ **8 acceptance tests** (testable, measurable scenarios)
- ✅ **7 KB domains identified** (dbt, Airflow, data modeling, testing, etc.)
- ✅ **Data engineering context** (sources, freshness SLAs, schema contracts, lineage)
- ✅ **3 risk mitigations** (resource management, startup time, auth)
- ✅ **All assumptions validated** from BRAINSTORM phase

Design phase will create:
1. Architecture diagram (Docker Compose topology)
2. File manifest (docker-compose.yml, dbt models, Airflow DAG, seed scripts)
3. Inline ADRs (decision rationale)
4. Code patterns (Dockerfile, DAG structure, dbt model templates)

---

## Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.1 | 2026-04-28 | iterate-agent | Updated data generation: CSV files → Python Faker script for customers/transactions/products |
| 1.0 | 2026-04-28 | define-agent | Initial DEFINE from BRAINSTORM_LOCAL_ANALYTICS_STACK.md |
