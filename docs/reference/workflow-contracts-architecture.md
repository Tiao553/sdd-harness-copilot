# Workflow, Contracts and Architecture

The AgentSpec SDD lives in `.github/sdd/` and organizes development into traceable phases. The formal architecture appears in `.github/sdd/architecture/`, especially `WORKFLOW_CONTRACTS.yaml`, which describes phases, agents, inputs, outputs, gates, templates, and transition rules. The Validate phase is mandatory between Build and Ship.

Having workflow and contracts separate from implementation is essential to avoid code without specification. The runtime treats SDD documents as the source of truth: Define explains what and why, Design explains how, Build executes the manifest, and Ship archives with evidence. This chain allows reviewing a decision without relying solely on the final diff.

## SDD pipeline

```mermaid
flowchart TD
    A["Raw idea"] --> B["Phase 0<br/>Brainstorm"]
    B --> C["BRAINSTORM_{FEATURE}.md"]
    A --> D["Phase 1<br/>Define"]
    C --> D
    D --> E["DEFINE_{FEATURE}.md"]
    E --> F["Phase 2<br/>Design"]
    F --> G["DESIGN_{FEATURE}.md"]
    G --> H["Phase 3<br/>Build"]
    H --> I["projects/{feature-name}/"]
    H --> J["BUILD_REPORT_{FEATURE}.md"]
    I --> K["Phase 3.5<br/>Validate"]
    J --> K
    K --> L["VALIDATION_REPORT<br/>RUNBOOK or ROADMAP"]
    L --> M["Phase 4<br/>Ship"]
    M --> N[".github/sdd/archive/{feature-name}/"]
```

## Contracts per phase

| Phase | Required input | Required output | Main gate |
|---|---|---|---|
| Brainstorm | Idea, problem, or notes | `BRAINSTORM_{FEATURE}.md` | Questions, samples, approaches, and YAGNI |
| Define | Direct input or brainstorm | `DEFINE_{FEATURE}.md` | Sufficient clarity and defined scope |
| Design | `DEFINE_{FEATURE}.md` | `DESIGN_{FEATURE}.md` | Decisions, architecture, manifest, and tests |
| Build | `DESIGN_{FEATURE}.md` | Code + `BUILD_REPORT_{FEATURE}.md` | All manifest files and evidence |
| Validate | Define, design, build report, and code | `VALIDATION_REPORT_{FEATURE}.md` + `RUNBOOK` or `ROADMAP` | Score >= 90 and zero CRITICAL to Ship |
| Ship | Complete artifacts and approved validation | `SHIPPED_{DATE}.md` | Complete build, approved validation, runbook, and no blockers |
| Iterate | Existing SDD document | Same document updated | Cascade analysis and history |

## Canonical paths

```mermaid
flowchart LR
    A[".github/sdd/features/{feature-name}/"] --> B["BRAINSTORM"]
    A --> C["DEFINE"]
    A --> D["DESIGN"]
    A --> E["BUILD_REPORT"]
    A --> F["VALIDATION_REPORT"]
    A --> G["RUNBOOK or ROADMAP"]
    H["projects/{feature-name}/"] --> I["Implementation"]
    J[".github/sdd/archive/{feature-name}/"] --> K["Shipped artifacts"]
```

Build output must go to `projects/{feature-name}/`. Build reports stay alongside the feature in `.github/sdd/features/{feature-name}/` until ship. This separation avoids mixing specification, reports, and runtime.

## Delegation architecture

```mermaid
flowchart TD
    A["DESIGN manifest"] --> B{"Line has @{agent-name}?"}
    B -->|no| C["build-agent executes directly"]
    B -->|yes| D["build-agent reads specialist agent"]
    D --> E["loads declared KB quick-reference"]
    E --> F["delegation via agent/runSubagent"]
    F --> G["specialist returns file + evidence"]
    C --> H["verification"]
    G --> H
    H --> I["BUILD_REPORT"]
```

The contract protects against two errors: writing implementation outside `projects/` and delegating without evidence. Each specialist must leave verifiable traces in the build report, especially for containers, dbt, Airflow, Python, and other domains with their own gates.

## Architectural files

| File | Role |
|---|---|
| `.github/sdd/architecture/ARCHITECTURE.md` | Visual and conceptual overview of the workflow |
| `.github/sdd/architecture/WORKFLOW_CONTRACTS.yaml` | Structured contract of phases, gates, and artifacts |
| `.github/sdd/templates/*.md` | Templates used by the phases |
| `.github/sdd/features/` | Features in progress |
| `.github/sdd/archive/` | Shipped features |
