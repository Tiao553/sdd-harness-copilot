# DESIGN: Local Analytics Stack

> Technical design for implementing Local Analytics Stack

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | LOCAL_ANALYTICS_STACK |
| **Date** | 2026-04-28 |
| **Author** | design-agent |
| **DEFINE** | [DEFINE_LOCAL_ANALYTICS_STACK.md](./DEFINE_LOCAL_ANALYTICS_STACK.md) |
| **Status** | Ready for Build |
| **Build Output Root** | `./projects/local-analytics-stack/` |

---

## Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────┐
│                   LOCAL ANALYTICS STACK DIAGRAM                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Python Faker Script] → [Postgres DB] ←→ [Supabase DB]             │
│          ↓                           ↑                              │
│  [dbt Models (stg_/int_/fct_/dim_)] ←→ [Airflow DAG]                 │
│          ↓                           ↑                              │
│  [Transformed Data] ←→ [Airflow UI (localhost:8080)]                │
│                                                                     │
│  All orchestrated via Docker Compose with resource limits          │
│  (Postgres: 2GB, Supabase: 2GB, Airflow: 2GB, dbt: 2GB)             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- **Data Generation:** Python script with Faker generates synthetic customers, transactions, products
- **Storage:** Dual Postgres instances (raw data + Supabase extended features)
- **Transformation:** dbt Core models in medallion architecture (staging → intermediate → marts)
- **Orchestration:** Airflow 3.0 with TaskFlow API for daily dbt runs
- **Containerization:** Docker Compose with explicit CPU/memory limits for reproducibility

---

## Components

| Component | Purpose | Technology | Resource Limits |
|-----------|---------|------------|-----------------|
| Postgres | Primary database for raw and transformed data | PostgreSQL 15+ | 2GB RAM, 2 CPUs |
| Supabase | Extended Postgres with auth/realtime (simplified local) | Supabase Docker | 2GB RAM, 2 CPUs |
| Airflow | Orchestration and scheduling of dbt pipelines | Apache Airflow 3.0+ | 2GB RAM, 1 CPU |
| dbt | Data transformation and modeling | dbt Core 1.9+ | 2GB RAM, 1 CPU |
| Data Generator | Synthetic data creation script | Python 3.9+ with Faker | N/A (runs on host or container) |

---

## Key Decisions

### Decision 1: Container Orchestration with Docker Compose

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-28 |

**Context:** Need simple, reproducible local environment that mirrors production without complexity. Manual setup leads to inconsistencies between dev machines and CI/CD.

**Choice:** Docker Compose with explicit resource limits per service.

**Rationale:** 
- Single `docker-compose up` command for zero-setup startup
- Resource limits ensure consistent performance across machines
- Easy replication via git clone + docker-compose up
- Supports both M1/M2 Macs and Linux x86_64 via multi-platform images

**Alternatives Rejected:**
1. Manual local installs - Rejected because inconsistent environments and onboarding friction
2. Kubernetes (k3s) - Rejected because overkill for local dev; adds complexity without benefits
3. Podman/Colima - Rejected because less mature ecosystem and potential compatibility issues

**Consequences:**
- Trade-off: Docker dependency (acceptable, widely available)
- Benefit: Perfect parity between local dev and CI/CD pipelines

### Decision 2: Dual Postgres Setup (Postgres + Supabase)

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-28 |

**Context:** Need to validate data transformations work identically across different Postgres variants.

**Choice:** Two Postgres instances - standard Postgres for raw/transformed data, Supabase for extended features.

**Rationale:**
- Supabase provides auth, realtime, and other extensions beyond standard Postgres
- Dual sink validation ensures transformations work across Postgres variants
- Local Supabase instance simplifies testing without cloud dependency

**Alternatives Rejected:**
1. Single Postgres only - Rejected because misses Supabase-specific features and validation
2. Supabase cloud - Rejected because adds external dependency and cost for local dev

**Consequences:**
- Trade-off: Higher resource usage (4GB total for DBs)
- Benefit: Comprehensive testing of Postgres ecosystem compatibility

### Decision 3: Medallion Architecture in dbt

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-28 |

**Context:** Need structured data transformation from raw sources to business-ready marts.

**Choice:** dbt medallion layers: staging (stg_) → intermediate (int_) → marts (fct_/dim_).

**Rationale:**
- Staging: 1:1 with sources, rename/cast only
- Intermediate: Business logic transformations
- Marts: Facts (events) and dimensions (descriptors) for analytics
- Follows modern data warehouse best practices

**Alternatives Rejected:**
1. Direct SQL queries - Rejected because no reusability or testing
2. One Big Table - Rejected because inflexible for multiple use cases

**Consequences:**
- Trade-off: More models to maintain
- Benefit: Modular, testable, and BI-ready data structures

### Decision 4: Airflow 3.0 with TaskFlow API

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-28 |

**Context:** Need reliable orchestration of dbt runs with modern Pythonic syntax.

**Choice:** Airflow 3.0 GA with TaskFlow API (@task decorator).

**Rationale:**
- TaskFlow API provides Pythonic, readable DAG definitions
- Asset-aware scheduling for event-driven triggers (future-proof)
- Modern UI with better debugging capabilities
- Compatible with dbt Core via BashOperator

**Alternatives Rejected:**
1. Airflow 2.x - Rejected because older version lacks modern features
2. Prefect - Rejected because Airflow is more established in data engineering

**Consequences:**
- Trade-off: Learning curve for new TaskFlow syntax
- Benefit: More maintainable and feature-rich orchestration

### Decision 5: Python Faker for Synthetic Data

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-04-28 |

**Context:** Need realistic seed data for testing without production dependencies.

**Choice:** Python script using Faker library to generate customers, transactions, products.

**Rationale:**
- Deterministic generation with --seed parameter for reproducibility
- Realistic data types (names, emails, amounts, dates)
- Foreign key relationships properly maintained
- Configurable counts and database connections

**Alternatives Rejected:**
1. CSV files only - Rejected because no relationships or variety
2. Production data export - Rejected because privacy concerns and dependencies

**Consequences:**
- Trade-off: Synthetic data may not catch all edge cases
- Benefit: Fast, safe, and reproducible testing environment

---

## File Manifest

> Build path rule: all files below are resolved relative to `./projects/local-analytics-stack/`.
> Example: `docker-compose.yml` must be created as `./projects/local-analytics-stack/docker-compose.yml`.

| # | File | Action | Purpose | Agent | Dependencies |
|---|------|--------|---------|-------|--------------|
| 1 | `docker-compose.yml` | Create | Container orchestration with resource limits | @{container-specialist} | None |
| 2 | `Dockerfile.dbt` | Create | dbt container image with dependencies | @{container-specialist} | None |
| 3 | `airflow/dags/daily_analytics_dag.py` | Create | Airflow DAG for daily dbt pipeline execution | @{airflow-specialist} | 1 |
| 4 | `dbt/models/staging/stg_customers.sql` | Create | dbt staging model for customers | @{dbt-specialist} | 2 |
| 5 | `dbt/models/staging/stg_transactions.sql` | Create | dbt staging model for transactions | @{dbt-specialist} | 2 |
| 6 | `dbt/models/staging/stg_products.sql` | Create | dbt staging model for products | @{dbt-specialist} | 2 |
| 7 | `dbt/models/intermediate/int_customer_metrics.sql` | Create | Business logic for customer aggregations | @{dbt-specialist} | 4 |
| 8 | `dbt/models/marts/fct_transactions.sql` | Create | Fact table for transaction events | @{dbt-specialist} | 5, 7 |
| 9 | `dbt/models/marts/dim_customers.sql` | Create | Dimension table for customer attributes | @{dbt-specialist} | 4, 7 |
| 10 | `dbt/models/marts/dim_products.sql` | Create | Dimension table for product attributes | @{dbt-specialist} | 6 |
| 11 | `scripts/generate_fake_data.py` | Create | Python script for synthetic data generation | @{python-developer} | None |
| 12 | `dbt/profiles.yml` | Create | dbt connection profiles for Postgres/Supabase | @{dbt-specialist} | 1 |
| 13 | `airflow/docker-compose.override.yml` | Create | Airflow-specific configuration | @{airflow-specialist} | 1 |
| 14 | `tests/test_data_generation.py` | Create | Unit tests for data generation script | @{python-developer} | 11 |
| 15 | `tests/test_dbt_models.py` | Create | dbt model tests (data + unit) | @{dbt-specialist} | 4-10 |

**Total Files:** 15

---

## Agent Assignment Rationale

> Agents discovered from `.github/agents/` - Build phase invokes matched specialists.

| Agent | Files Assigned | Why This Agent |
|-------|----------------|----------------|
| @{airflow-specialist} | 3, 13 | Airflow DAG creation and configuration patterns |
| @{dbt-specialist} | 4-10, 12, 15 | dbt model development, profiles, and testing |
| @{python-developer} | 11, 14 | Python scripting and unit testing |
| @{container-specialist} | 1, 2 | Docker Compose, Dockerfile, and container runtime configuration |

**Agent Discovery:**
- Scanned: `.github/agents/*.agent.md`
- Matched by: File type (.sql for dbt, .py for Python, .yml for infra), purpose keywords (DAG, model, script), KB domains (airflow, dbt, python)

---

## Code Patterns

### Pattern 1: dbt Staging Model

```sql
-- models/staging/stg_customers.sql
-- 1:1 with source, rename + cast only

with source as (
    select * from {{ source('raw', 'customers') }}
),

renamed as (
    select
        customer_id::int as customer_id,
        first_name::varchar(50) as first_name,
        last_name::varchar(50) as last_name,
        email::varchar(100) as email,
        signup_date::date as signup_date
    from source
)

select * from renamed
```

### Pattern 2: dbt Fact Table with Incremental

```sql
-- models/marts/fct_transactions.sql
-- Incremental materialization for large fact tables

{{
    config(
        materialized='incremental',
        unique_key='transaction_id',
        incremental_strategy='merge'
    )
}}

with transactions as (
    select * from {{ ref('stg_transactions') }}
    {% if is_incremental() %}
    where transaction_date >= (select max(transaction_date) from {{ this }})
    {% endif %}
)

select
    transaction_id,
    customer_id,
    product_id,
    amount,
    transaction_date
from transactions
```

### Pattern 3: Airflow TaskFlow DAG

```python
# dags/daily_analytics_dag.py
from airflow.sdk import DAG, task
from datetime import datetime

@task
def run_dbt_models():
    """Run all dbt models"""
    import subprocess
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    return "dbt run success"

@task
def test_dbt_models():
    """Test all dbt models"""
    import subprocess
    result = subprocess.run(["dbt", "test"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt test failed: {result.stderr}")
    return "dbt test success"

with DAG(
    dag_id="daily_analytics",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:
    run_task = run_dbt_models()
    test_task = test_dbt_models()
    
    run_task >> test_task
```

### Pattern 4: Python Data Generation with Faker

```python
# scripts/generate_fake_data.py
import psycopg2
from faker import Faker
import click

@click.command()
@click.option('--entity', required=True, type=click.Choice(['customers', 'transactions', 'products']))
@click.option('--count', default=1000, type=int)
@click.option('--seed', default=42, type=int)
def generate_data(entity, count, seed):
    fake = Faker()
    fake.seed_instance(seed)
    
    conn = psycopg2.connect("host=localhost dbname=analytics user=postgres password=postgres")
    cur = conn.cursor()
    
    if entity == 'customers':
        for _ in range(count):
            cur.execute("""
                INSERT INTO customers (first_name, last_name, email, signup_date)
                VALUES (%s, %s, %s, %s)
            """, (
                fake.first_name(),
                fake.last_name(),
                fake.email(),
                fake.date_between(start_date='-2y')
            ))
    
    conn.commit()
    cur.close()
    conn.close()
    click.echo(f"Generated {count} {entity}")

if __name__ == '__main__':
    generate_data()
```

### Pattern 5: Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: analytics
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'

  supabase:
    image: supabase/postgres:15
    environment:
      POSTGRES_DB: analytics
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5433:5432"
    volumes:
      - supabase_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'

volumes:
  postgres_data:
  supabase_data:
```

---

## Data Flow

```text
1. Container Startup
   │
   ▼
2. Python Faker Script Generates Seed Data
   │ (customers.csv, transactions.csv, products.csv)
   │
   ▼
3. Data Loaded into Postgres via SQL COPY
   │
   ▼
4. dbt run Executes Models in DAG Order
   │ stg_ → int_ → fct_/dim_
   │
   ▼
5. Transformed Data Available in Both Postgres + Supabase
   │
   ▼
6. Airflow DAG Triggers Daily Pipeline
   │ (run dbt + tests)
   │
   ▼
7. Results Verified via UI and Queries
```

---

## Integration Points

| External System | Integration Type | Authentication |
|-----------------|-----------------|----------------|
| Docker Hub | Image pulls | None (public images) |
| GitHub Actions | CI/CD workflow triggers | GITHUB_TOKEN |
| Local filesystem | Volume mounts for data persistence | None |

---

## Testing Strategy

| Test Type | Scope | Files | Tools | Coverage Goal |
|-----------|-------|-------|-------|---------------|
| Unit | Python functions (data generation) | `tests/test_data_generation.py` | pytest | 80% |
| Data Quality | dbt model outputs | `dbt/tests/` | dbt test | 100% (all models) |
| Integration | End-to-end pipeline | Manual + `tests/test_dbt_models.py` | pytest + dbt | Key paths |
| E2E | Full stack startup | Manual | docker-compose + queries | Happy path |

---

## Error Handling

| Error Type | Handling Strategy | Retry? |
|------------|-------------------|--------|
| Docker resource exhaustion | Container restart with lower limits | No |
| dbt model failure | Log error, stop pipeline | No |
| Database connection timeout | Retry with exponential backoff | Yes (3x) |
| Airflow task failure | Email alert, manual intervention | No |

---

## Configuration

| Config Key | Type | Default | Description |
|------------|------|---------|-------------|
| `POSTGRES_DB` | string | analytics | Database name |
| `POSTGRES_USER` | string | postgres | Database user |
| `POSTGRES_PASSWORD` | string | postgres | Database password |
| `AIRFLOW__CORE__EXECUTOR` | string | LocalExecutor | Airflow executor |
| `DBT_PROFILES_DIR` | string | /dbt | dbt profiles directory |

---

## Security Considerations

- Database passwords stored in environment (acceptable for local dev)
- No external network exposure (all ports localhost)
- Supabase runs in dev mode (auth disabled)
- No sensitive data in synthetic generation

---

## Observability

| Aspect | Implementation |
|--------|----------------|
| Logging | Airflow UI logs, dbt console output, container logs |
| Metrics | Docker stats for resource usage, dbt run timings |
| Monitoring | Airflow UI for DAG status, manual query verification |

---

## Next Phase

Ready for `#skill:workflow-commands /build DESIGN_LOCAL_ANALYTICS_STACK.md`

This design provides:
- ✅ Complete architecture with Docker Compose orchestration
- ✅ 5 key decisions with rationale and alternatives
- ✅ 15-file manifest with agent assignments
- ✅ 5 code patterns from KB domains
- ✅ Testing strategy covering unit/integration/E2E
- ✅ Data flow and integration points documented
