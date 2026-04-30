# Reference

Current catalog for the AgentSpec GitHub Copilot runtime.

## Skill Commands

| Skill | Commands | Purpose |
|---|---|---|
| [`/workflow-commands`](skills/workflow-commands.md) | `/brainstorm`, `/define`, `/design`, `/build`, `/validate`, `/ship`, `/iterate`, `/create-pr` | SDD lifecycle control |
| [`/validate`](skills/validate.md) | Phase 3.5 validation runtime | Build-to-Ship quality gate |
| [`/data-engineering-commands`](skills/data-engineering-commands.md) | `/ai-pipeline`, `/data-contract`, `/data-quality`, `/lakehouse`, `/migrate`, `/pipeline`, `/schema`, `/sql-review` | Data engineering workflows |
| [`/knowledge-commands`](skills/knowledge-commands.md) | `/create-kb`, `/update-kb`, `/refresh-stale-kbs` | KB lifecycle management |
| [`/core-commands`](skills/core-commands.md) | `/meeting`, `/memory`, `/readme-maker`, `/status`, `/sync-context` | Workspace operations |
| [`/review-commands`](skills/review-commands.md) | `/review`, `/judge` | Review and second-opinion flows |
| [`/visual-explainer`](skills/visual-explainer.md) | visual plans, web diagrams, slides, diff review, fact check, project recap | HTML visual explanations |
| [`/excalidraw-diagram`](skills/excalidraw-diagram.md) | diagram generation | Excalidraw JSON diagrams |

Detailed guides:

| Guide | Purpose |
|---|---|
| [Agents](agents.md) | Why agents exist, how categories work, and how build delegation records evidence |
| [Router](router.md) | Why routing is separated from grounding and how intent maps to agents |
| [Grounding](grounding.md) | Mandatory execution protocol and response grounding block |
| [Workflow, Contracts and Architecture](workflow-contracts-architecture.md) | SDD phases, Validate gate, paths, workflow contracts, and delegation architecture |
| [Knowledge Base](knowledge-base.md) | KB domains, quick-reference policy, and lifecycle |

## Agent Catalog

### Architect

| Agent | Role |
|---|---|
| `data-platform-engineer` | Cloud data platform architecture across warehouses, lakehouses, and infrastructure decisions |
| `genai-architect` | Production GenAI systems, multi-agent orchestration, and agentic workflows |
| `kb-architect` | KB creation, refresh, validation, and structure |
| `lakehouse-architect` | Open table formats, catalogs, governance, Iceberg, and Delta Lake |
| `medallion-architect` | Bronze/Silver/Gold design and data quality progression |
| `pipeline-architect` | Pipeline and orchestration architecture |
| `schema-designer` | Dimensional modeling, Data Vault, SCD, and schema evolution |
| `the-planner` | Strategic planning, roadmaps, architecture decisions, and risk assessment |

### Cloud

| Agent | Role |
|---|---|
| `ai-data-engineer-cloud` | Cloud AI data pipelines and architecture |
| `ai-data-engineer-gcp` | GCP AI/data architecture and document processing |
| `ai-prompt-specialist-gcp` | Gemini, Vertex AI, OCR, extraction, and multimodal prompts |
| `aws-data-architect` | AWS data architecture with Lambda, S3, Glue, Redshift, and MWAA |
| `aws-deployer` | AWS CLI and SAM deployment execution with validation |
| `aws-lambda-architect` | SAM templates and least-privilege Lambda architecture |
| `ci-cd-specialist` | DevOps, Terraform, Azure DevOps, Databricks bundles, and promotion flows |
| `container-specialist` | Docker, Docker Compose, Kubernetes, Helm, images, and charts |
| `gcp-data-architect` | BigQuery, Cloud Run, Pub/Sub, GCS, Dataflow, and Vertex AI |
| `lambda-builder` | Python Lambda implementation for file processing and Parquet outputs |
| `supabase-specialist` | Supabase, pgvector, RLS, Edge Functions, Auth, Realtime, and database design |

### Data Engineering

| Agent | Role |
|---|---|
| `ai-data-engineer` | RAG, vector databases, feature stores, LLMOps, and AI pipelines |
| `airflow-specialist` | Airflow DAGs, assets, scheduling, and event-driven orchestration |
| `dbt-specialist` | dbt models, tests, macros, packages, and Cloud/Core practices |
| `lakeflow-architect` | Databricks Lakeflow medallion pipeline architecture |
| `lakeflow-expert` | Lakeflow development, CDC, quality, and production deployment |
| `lakeflow-pipeline-builder` | DLT pipeline implementation |
| `lakeflow-specialist` | Declarative pipelines, materialized views, streaming tables, and expectations |
| `qdrant-specialist` | Qdrant collections, points, payload filters, search, and RAG integration |
| `spark-engineer` | PySpark and Spark SQL implementation |
| `spark-performance-analyzer` | Spark tuning, partitions, joins, memory, and I/O |
| `spark-specialist` | Spark architecture, troubleshooting, and optimization |
| `spark-streaming-architect` | Structured Streaming, Kafka, and real-time pipelines |
| `spark-troubleshooter` | OOM, skew, shuffle, failures, and long-running Spark jobs |
| `sql-optimizer` | Cross-dialect SQL review, query plans, windows, and performance |
| `streaming-engineer` | Kafka, Flink, Spark Streaming, RisingWave, and CDC |

### Dev

| Agent | Role |
|---|---|
| `agent-router` | Intent routing, grounding selection, and minimal KB loading |
| `codebase-explorer` | Codebase analysis, executive summaries, and deep dives |
| `judge-agent` | Cross-model second opinion for risky or ambiguous outputs |
| `meeting-analyst` | Meeting notes into decisions, action items, and structured documentation |
| `prompt-crafter` | Prompt and task design with SDD-lite phases |
| `shell-script-specialist` | Production-grade Bash scripting |

### Platform

| Agent | Role |
|---|---|
| `fabric-ai-specialist` | Microsoft Fabric AI, Copilot, ML, AI Skills, and Azure OpenAI |
| `fabric-architect` | End-to-end Microsoft Fabric solution architecture |
| `fabric-cicd-specialist` | Fabric Git integration, CI/CD, and deployments |
| `fabric-logging-specialist` | Fabric monitoring, logging, KQL, and observability |
| `fabric-pipeline-developer` | Fabric Data Factory pipelines and ETL workflows |
| `fabric-security-specialist` | Fabric security, governance, and compliance |

### Python

| Agent | Role |
|---|---|
| `ai-prompt-specialist` | Prompt engineering, extraction, structured output, and few-shot design |
| `code-cleaner` | Python cleanup and modernization |
| `code-documenter` | Production-ready documentation |
| `code-reviewer` | Code review for quality, security, and maintainability |
| `llm-specialist` | LLM prompts, reasoning patterns, and AI extraction |
| `python-developer` | Python architecture for data engineering systems |

### Test

| Agent | Role |
|---|---|
| `data-contracts-engineer` | ODCS, schema governance, SLA enforcement, and producer-consumer contracts |
| `data-quality-analyst` | Great Expectations, Soda, dbt tests, contracts, and observability |
| `test-generator` | pytest unit tests, integration tests, and fixtures |

### Workflow

| Agent | Role |
|---|---|
| `brainstorm-agent` | Phase 0 exploration |
| `define-agent` | Phase 1 requirements extraction |
| `design-agent` | Phase 2 architecture and technical specification |
| `build-agent` | Phase 3 implementation execution and delegation |
| `ship-agent` | Phase 4 verification, archive, and lessons learned |
| `validate-agent` | Phase 3.5 validation gate before Ship |
| `iterate-agent` | Cross-phase updates and cascading changes |

## KB Domains

| Domain | Focus |
|---|---|
| `ai-data-engineering` | AI-assisted data engineering patterns |
| `airflow` | orchestration, DAGs, scheduling, sensors, and assets |
| `aws` | AWS data and serverless patterns |
| `cloud-platforms` | cross-cloud platform decisions |
| `containers` | Docker, Compose, Kubernetes, Helm, images, and charts |
| `data-modeling` | dimensional modeling, Data Vault, SCD, schema evolution |
| `data-quality` | validation, contracts, observability, and test patterns |
| `dataviz` | visualization guidance |
| `dbt` | dbt models, tests, macros, and project structure |
| `gcp` | Google Cloud data and AI services |
| `genai` | RAG, agents, LLM systems, embeddings |
| `lakeflow` | Databricks Lakeflow and DLT |
| `lakehouse` | open table formats, catalogs, Iceberg, Delta |
| `medallion` | Bronze/Silver/Gold architecture |
| `microsoft-fabric` | Fabric architecture and operations |
| `modern-stack` | modern data stack architecture |
| `prompt-engineering` | prompt design and evaluation |
| `pydantic` | Pydantic patterns |
| `python` | Python language and architecture patterns |
| `shared` | shared KB conventions |
| `spark` | Spark architecture, performance, and troubleshooting |
| `sql-patterns` | SQL design, optimization, and dialect patterns |
| `streaming` | Kafka, Flink, CDC, stream processing |
| `supabase` | Supabase database, auth, RLS, realtime, pgvector |
| `terraform` | infrastructure as code |
| `testing` | test strategy and automation |

## Routing Files

| File | Purpose |
|---|---|
| `.github/config/grounding.md` | mandatory execution protocol |
| `.github/config/routing.json` | intent-to-agent mapping |
| `.github/copilot-instructions.md` | Copilot workspace instructions |

## Validation Commands

```bash
find .github/agents -name "*.agent.md" | wc -l
find .github/kb -name "quick-reference.md" | wc -l
find .github/skills -maxdepth 2 -name SKILL.md | sort
python3 -m json.tool .github/config/routing.json
```
