
# Architecture Overview

## Objective

The Actuarial Life Model Engine is designed as a modular actuarial and quantitative risk infrastructure platform.

The project prioritises:

- stable interfaces
- modular assumptions infrastructure
- explicit modelling contracts
- reproducible valuation workflows
- scenario extensibility
- institutional-style design discipline
- configuration-driven execution
- workflow-owned orchestration

The architecture is intentionally designed to separate:

- modelling mechanics
- assumptions infrastructure
- scenario infrastructure
- analytics
- validation
- orchestration
- ingestion

This separation allows the engine to evolve toward broader risk and capital modelling capabilities without requiring rewrites of the core modelling engine.

---

# Core Engine Flow

```text
Policy
→ ProjectionRow
→ ProjectionResult
→ ValuationRow
→ ValuationResult
→ Portfolio
→ PortfolioResult
```

Each layer has explicitly scoped responsibilities and stable interfaces.

---

# Configuration Layer

The engine now includes a dedicated configuration layer which centralises workflow execution inputs while preserving modular provider composition.

Current configuration architecture:

```text
CapitalWorkflowConfig
├── AssumptionConfig
├── ScenarioConfig
├── CorrelationConfig
└── execution settings
```

The configuration layer is responsible for:

- workflow execution ownership
- assumption ingestion ownership
- scenario calibration ownership
- correlation configuration ownership
- frontend/backend execution contracts

The configuration layer intentionally does NOT:

- perform projection logic
- perform valuation logic
- perform stress calculations
- perform aggregation calculations

This separation allows frontend and orchestration infrastructure to evolve independently of actuarial mechanics.

---

# Core Design Principles

## 1. Projection Must Remain Assumption-Agnostic

Projection logic must never know:

- CSV structures
- segmentation logic
- provider implementation details
- scenario implementation
- market-data conventions

Projection consumes ONLY stable interfaces:

```python
assumptions.qx(policy, age)
assumptions.lapse_rate(policy, t)
assumptions.expenses(policy, t)
```

This abstraction boundary is one of the most important architectural principles in the project.

---

## 2. Valuation Must Remain Curve-Agnostic

Valuation logic must never know:

- yield curve structure
- interpolation mechanics
- market-data formatting
- scenario implementation
- calibration methodology

Valuation consumes ONLY:

```python
assumptions.discount_factor(t)
```

This allows interest assumptions to evolve independently of the valuation engine.

---

## 3. Provider-Based Assumptions

The engine uses provider-based assumptions infrastructure.

Correct dependency direction:

```text
External Data
→ Loader
→ Validation
→ Provider
→ AssumptionSet
→ Projection / Valuation
```

Projection and valuation depend only on the unified assumptions interface.

---

## 4. Stable Result Contracts

Result objects are intentionally structured and explicit.

Result contracts:

- separate modelling from analytics
- support downstream processing
- improve reproducibility
- support future persistence frameworks
- support future capital modelling infrastructure

The project intentionally avoids returning raw dictionaries or dataframes from core engine components.

---

## 5. Scenario Infrastructure Must Remain Externalised

Scenario logic should modify assumptions providers rather than modelling mechanics.

Correct architecture:

```text
Base Assumptions
↓
Scenario Overlay
↓
Scenario-Adjusted Assumptions
↓
Projection
↓
Valuation
↓
BEL
```

Projection and valuation remain completely scenario-agnostic.

---

## 6. Pandas Must Remain Outside The Core Engine

Pandas is permitted only in:

- ingestion
- validation
- analytics
- notebooks

Core modelling components operate on:

- structured objects
- stable interfaces
- explicit contracts

NOT dataframes.

---

## 7. Validation Occurs Only At Ingestion Boundaries

Validation belongs only in:

- loaders
- ingestion
- external data handling

Core engine logic assumes validated structured inputs.

---

## 8. Workflow Configuration Must Remain Centralised

Workflow execution inputs should be centralised through structured configuration contracts.

Correct architecture:

```text
CapitalWorkflowConfig
↓
workflow orchestration
↓
provider composition
↓
projection / valuation / capital
```

Incorrect architecture:

```text
notebook
↓
manual orchestration wiring
↓
multiple workflow arguments
```

The workflow layer owns orchestration while core modelling remains infrastructure-agnostic.

---

# Layer Responsibilities

## Policy Layer

Responsibilities:

- hold policy attributes
- support segmentation
- represent model points

Does NOT:

- perform projection logic
- perform valuation logic
- contain analytics

---

## Projection Layer

Responsibilities:

- project expected cashflows
- apply multi-decrement runoff
- track unconditional probabilities

Projection currently supports:

- mortality decrement
- lapse decrement
- expense emergence

Projection intentionally contains:

- no discounting logic
- no scenario logic
- no analytics

---

## Valuation Layer

Responsibilities:

- consume projected cashflows
- apply discounting
- aggregate present values
- produce structured valuation outputs

Valuation intentionally contains:

- no projection mechanics
- no scenario calibration
- no analytics

---

## Portfolio Layer

Responsibilities:

- aggregate policy-level valuation results
- support weighted model points
- produce portfolio-level outputs

Portfolio aggregation intentionally contains:

- no actuarial mechanics
- no valuation logic
- no analytics

---

## Analytics Layer

Responsibilities:

- dataframe conversion
- emergence analysis
- summary metrics
- visualisation support

Analytics consume structured outputs only.

---

# Current Modelling Philosophy

The project prioritises:

- clarity
- explicitness
- transparency
- modularity
- reproducibility
- extensibility

The project intentionally avoids:

- hidden dependencies
- tightly coupled logic
- notebook-driven modelling
- premature optimisation
- convenience-driven shortcuts

---

# Long-Term Direction

The long-term target architecture is:

```text
CapitalWorkflowConfig
↓
Workflow Layer
↓
Scenario Engine
↓
Scenario-Adjusted Assumptions
↓
Projection
↓
Valuation
↓
BEL
↓
SCR Generation
↓
SCR Aggregation
↓
Capital Framework
```

The project is intentionally evolving from:

```text
actuarial modelling engine
```

toward:

```text
institutional-style actuarial and risk infrastructure platform
```

The current architecture prioritises:

- stable execution contracts
- modular provider infrastructure
- configuration-driven orchestration
- reusable workflow infrastructure
- extensible capital modelling
