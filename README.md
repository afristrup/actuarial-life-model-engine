# Actuarial Life Model Engine

A modular Python-based actuarial life insurance modelling and capital engine designed using institutional-style software architecture principles.

The project focuses not only on actuarial mechanics, but also on building a clean, extensible modelling framework with stable interfaces, externalised assumptions, structured outputs, and disciplined separation of concerns.

The project has evolved beyond a traditional actuarial cashflow model toward a reusable actuarial scenario, valuation, and capital aggregation framework with calibration-driven stress infrastructure and modular risk architecture.

---

# Core Objectives

- Build a modular actuarial modelling engine using clean software architecture principles
- Separate modelling mechanics from ingestion, analytics, and orchestration
- Externalise assumptions through provider-based interfaces
- Produce structured, reusable valuation outputs
- Preserve transparency and reproducibility of calculations
- Build reusable scenario, stress, and capital aggregation infrastructure

---

# Current Architecture

The engine is built using layered structured outputs:

```text
CapitalWorkflowConfig
↓
Workflow Layer
↓
Policy
→ ProjectionRow
→ ProjectionResult
→ ValuationRow
→ ValuationResult
→ Portfolio
→ PortfolioResult
→ SCRResult
→ AggregatedSCRResult
→ CapitalWorkflowResult
```

Core modelling logic is intentionally isolated from:
- pandas
- CSV ingestion
- validation
- analytics
- notebook orchestration
- assumption source structure

---

# Current Architecture Status

The current architecture is considered structurally stable across:

- projection
- valuation
- assumptions infrastructure
- scenario execution
- SCR generation
- capital aggregation
- workflow orchestration
- configuration-driven execution

Current development focus has shifted from core architecture toward:

- richer stresses
- reporting infrastructure
- frontend integration
- realism enhancements
- asset-side modelling

---

# Configuration Layer

The engine now includes a dedicated configuration-driven execution layer.

Current workflow configuration architecture:

```text
CapitalWorkflowConfig
├── AssumptionConfig
├── ScenarioConfig
├── CorrelationConfig
└── execution settings
```

The configuration layer centralises:

- workflow execution inputs
- assumption ingestion ownership
- scenario calibration ownership
- correlation configuration ownership

while preserving:

- provider abstraction
- stable modelling contracts
- scenario-agnostic projection
- scenario-agnostic valuation

Workflow orchestration is intentionally separated from actuarial mechanics.

---

# Current Features

## Projection Engine

- Expected cashflow projection using unconditional probabilities
- Multi-decrement runoff framework
- Mortality and lapse decrement support
- Structured projection outputs
- Explicit expense cashflow decomposition

Projection logic remains completely assumption-agnostic.

---

## Valuation Engine

- Discounted present value calculations
- Structured valuation outputs
- Explicit expense present value decomposition
- Profit emergence support
- Portfolio-level aggregation

Valuation consumes only abstract discount factor interfaces.

---

## Scenario & Capital Framework

The engine now supports calibration-driven stress testing and hierarchical capital aggregation.

Scenario infrastructure is intentionally separated from:
- projection mechanics
- valuation mechanics
- aggregation logic

Current scenario workflow:

```text
CapitalWorkflowConfig
↓
Workflow Layer
↓
Base assumptions
↓
Scenario overlays
↓
Scenario-adjusted assumptions
↓
Projection
↓
Valuation
↓
Stressed BEL
↓
SCRResult
↓
Diversified aggregation
↓
CapitalWorkflowResult
```

Projection and valuation remain completely scenario-agnostic.

Implemented scenario infrastructure:
- ScenarioDefinition
- scenario_loader
- scenario_validation
- stress_registry
- stressed assumption overlays

Implemented stressed providers:
- mortality stresses
- lapse stresses
- interest stresses
- expense stresses

Current capital framework supports:
- univariate SCR calculation
- life diversification
- market diversification
- BSCR aggregation
- dynamic correlation matrix subsetting

Aggregation is metadata-driven and consumes:
- SCRResult objects
- correlation matrices

The aggregation layer does NOT:
- apply stresses
- run projections
- run valuations

---

## Capital Aggregation

- Calibration-driven stress scenario execution
- Structured SCR result contracts
- Dynamic correlation matrix subsetting
- Life SCR aggregation
- Market SCR aggregation
- Hierarchical BSCR aggregation
- Metadata-driven diversification workflow

---

## Assumptions Infrastructure

### Mortality

- CSV-driven mortality ingestion
- Gender-segmented mortality tables
- Contextual mortality resolution
- Smoker mortality overlays

### Interest Rates

- CSV-driven yield curve ingestion
- Float maturity support
- Spot-rate discounting
- Terminal extrapolation beyond observable maturities

### Lapse

- CSV-driven lapse assumptions
- Product segmentation
- Smoker segmentation
- Duration-based lapse ranges

### Expenses

- CSV-driven expense assumptions
- Structured expense provider abstraction
- Acquisition and maintenance expense support
- Fixed and premium-linked expense mechanics
- Future extensible segmentation architecture

---

# Assumptions Architecture

The engine consumes only stable provider interfaces:

```python
assumptions.qx(policy, age)
assumptions.discount_factor(t)
assumptions.lapse_rate(policy, t)
assumptions.expenses(policy, t)
```

Projection and valuation layers remain completely unaware of:
- CSV structure
- segmentation mechanics
- market-data formatting
- assumption source logic
- provider implementation details

This abstraction boundary is a core design principle of the project.

---

# Data Ingestion Architecture

Assumption ingestion follows the architecture below:

```text
Config
↓
Loader
↓
Validation
↓
Provider
↓
AssumptionSet
↓
Projection / Valuation
```

Validation occurs only at ingestion boundaries.

The core engine assumes validated structured inputs.

---

# Design Principles

## Assumption-Agnostic Projection

Projection logic consumes only stable provider interfaces and remains unaware of:
- segmentation mechanics
- expense composition logic
- assumption storage structure
- provider implementation details

This allows new assumption dimensions and provider extensions to integrate without redesigning projection or valuation mechanics.

## Stable Interfaces

Projection and valuation depend only on explicit assumption interfaces.

New assumption structures should integrate without requiring engine rewrites.

---

## Centralised Workflow Configuration

Workflow execution is centrally orchestrated through structured configuration contracts.

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

The workflow layer owns orchestration while modelling mechanics remain infrastructure-agnostic.

---

## Separation of Concerns

Distinct responsibilities are maintained across:
- modelling
- ingestion
- validation
- analytics
- orchestration

---

## No Pandas In Core Engine

Pandas is restricted to:
- ingestion
- validation
- analytics
- notebook layers

Core engine logic operates on structured domain objects only.

---

## Structured Result Contracts

Projection and valuation outputs are represented through structured result objects rather than raw dataframes.

This supports:
- analytics reuse
- serialisation
- debugging
- downstream extensions

---

## Externalised Assumptions

Mortality, lapse, expense, and yield curve assumptions are externally configurable and provider-driven.

Projection and valuation remain assumption-source agnostic.

---

# Example Project Structure

```text
actuarial-life-model-engine/

├── model/
│
│   ├── capital/
│   │   ├── aggregation.py
│   │   ├── correlation.py
│   │   ├── correlation_loader.py
│   │   ├── capital_workflow.py
│   │   ├── workflow_results.py
│   │   └── scr_calculator.py
│   
│   ├── config/
│   │   ├── __init__.py
│   │   ├── assumption_config.py
│   │   ├── scenario_config.py
│   │   ├── correlation_config.py
│   │   └── workflow_config.py
│
│
│   ├── assumptions/
│   │   ├── __init__.py
│   │   ├── assumption_set.py
│   │   ├── mortality.py
│   │   ├── interest.py
│   │   ├── lapse.py
│   │   ├── assumption_loader.py
│   │   └── assumption_validation.py
│   │
│   ├── analysis/
│   │   └── profit_analysis.py
│   │
│   ├── data/
│   │   ├── portfolio_loader.py
│   │   └── portfolio_validation.py
│   │
│   ├── results/
│   │   ├── projection_results.py
│   │   ├── portfolio_results.py
│   │   ├── capital_results.py
│   │   └── valuation_results.py
│   │
│   ├── scenarios/
│   │   ├── scenario_definition.py
│   │   ├── scenario_loader.py
│   │   ├── scenario_validation.py
│   │   ├── stress_registry.py
│   │   ├── scenario_runner.py
│   │   └── stressed_assumptions.py
│   │
│   ├── policy.py
│   ├── projection.py
│   ├── valuation.py
│   └── portfolio.py
│
├── data/
│   ├── mortality_tables/
│   ├── mortality_parameters/
│   ├── yield_curves/
│   ├── lapse_tables/
│   ├── portfolios/
│   ├── correlations/
│   ├── scenarios/
│   └── results_snapshots/
│
├── notebooks/
│   ├── single_policy_run.ipynb
│   └── multiple_policy_run.ipynb
│
└── README.md
```

---

# Example Workflow

```python
CapitalWorkflowConfig
↓
workflow orchestration
↓
assumption loading
↓
scenario execution
↓
projection
↓
valuation
↓
SCR generation
↓
correlation aggregation
↓
BSCR
↓
CapitalWorkflowResult
↓
analytics
```

---

# Current Scope

Implemented:
- deterministic projection engine
- multi-decrement cashflow modelling
- portfolio valuation
- structured result objects
- mortality table ingestion
- yield curve ingestion
- segmented lapse assumptions
- expense assumption infrastructure
- fulfilment cashflow valuation
- validation framework
- reusable analytics layer
- BEL / PVFP framework
- scenario overlay infrastructure
- calibration-driven scenario loading
- stress validation registry
- univariate SCR framework
- correlation matrix ingestion
- dynamic matrix subsetting
- life SCR aggregation
- market SCR aggregation
- BSCR aggregation
- workflow orchestration layer
- config-driven execution architecture
- centralised workflow configuration contracts
- structured workflow result packaging

---

# Current Intentional Limitations

The following are intentionally excluded from the current version:

- stochastic economic scenarios
- curve-based interest stresses
- equity/spread/property risk mechanics
- worst-of lapse stress selection
- mass lapse mechanics
- dynamic policyholder behaviour
- IFRS17 mechanics

The current focus is architectural stability and modular extensibility before introducing additional modelling complexity.

---

# Planned Extensions

Potential future directions include:
- stochastic scenario infrastructure
- advanced expense segmentation
- inflation-linked expense assumptions
- stochastic expense overlays
- ALM extensions
- vectorised portfolio valuation
- regression testing
- parallelised valuation frameworks
- richer market risk framework
- calibration governance
- reporting infrastructure
- capital attribution analytics
- regression testing infrastructure

---

# Running The Project

Tested using Python 3.11.

Dependencies are listed in `requirements.txt`.

## Clone repository

```bash
git clone https://github.com/asehdev1994/actuarial-life-model-engine.git
cd actuarial-life-model-engine
```

---

## Create virtual environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
.\venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Launch notebooks

```bash
jupyter notebook
```
## Quick Start

After launching Jupyter:

1. Open `single_policy_run.ipynb`
2. Run all cells
3. Review projection and valuation outputs

The notebooks now act primarily as lightweight configuration and analysis layers on top of the reusable workflow execution framework.

Primary execution is now designed around configuration-driven workflow orchestration through:

- CapitalWorkflowConfig
- AssumptionConfig
- ScenarioConfig
- CorrelationConfig

Primary notebooks:
- `single_policy_run.ipynb`
- `multiple_policy_run.ipynb`
- `scenario_and_scr_workflow`

The notebook `scenario_and_scr_workflow` demonstrates modular actuarial projection, valuation, stress testing, and capital aggregation workflows using calibration-driven assumptions and scenario infrastructure.

---

# Development Philosophy

The project prioritises:
- clarity over shortcuts
- explicitness over hidden behaviour
- stable interfaces over convenience
- incremental extensibility over premature complexity

The long-term objective is to evolve toward reusable actuarial and quantitative risk infrastructure while preserving modelling transparency and architectural discipline.

---

# Disclaimer

This is a personal engineering and actuarial modelling project intended for learning, experimentation, and architecture exploration.

It is not intended for production, regulatory, or financial reporting use.

---

# Author

Ajay Sehdev