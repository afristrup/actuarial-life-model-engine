
# Scenario Framework

## Overview

The scenario framework introduces reusable stress and scenario infrastructure while preserving:

- projection stability
- valuation stability
- assumptions abstraction boundaries

The scenario framework is intentionally designed so that:

- projection does not know scenarios exist
- valuation does not know scenarios exist

Scenarios operate entirely through assumption overlays.

---

# Core Scenario Philosophy

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

Incorrect architecture:

```text
Scenario
↓
Projection Rewrite
↓
Valuation Rewrite
```

The project intentionally avoids embedding stress logic into modelling mechanics.

---

# Current Scenario Components

```text
model/scenarios/
    scenario_definition.py
    stressed_assumptions.py
    scenario_runner.py
```

Implemented components:

- ScenarioDefinition
- StressedMortalityTable
- StressedLapseTable
- StressedYieldCurve
- StressedExpenseTable
- build_scenario_assumptions()
- run_scenario()

---

# Current Supported Stress Types

The current framework supports:

- mortality stresses
- lapse stresses
- interest stresses
- expense stresses

All stresses are implemented through provider overlays.

---

# Scenario Configuration

Scenario execution is now centrally configured through:

```text
ScenarioConfig
```

Scenario calibration remains fully externalised through:

```text
data/scenarios/
```

This allows:

- calibration-driven SCR execution
- extensible stress infrastructure
- workflow-owned orchestration
- frontend-compatible execution

---

# BEL Framework

The scenario framework currently supports stressed BEL calculations.

Current outputs include:

- BEL
- PVFP
- net value

Current BEL definition:

```text
BEL = PV(claims + expenses - premiums)
```

Current PVFP definition:

```text
PVFP = -BEL
```

---

# Externalised Stress Philosophy

Stress calibration should remain external to modelling mechanics.

Future target structure:

```text
data/scenarios/
    standard_formula.csv
```

Scenario calibration should NOT be hardcoded into:

- projection
- valuation
- assumptions providers

---

# Future Direction

The scenario framework is intended to support:

```text
Base BEL
↓
Scenario Execution
↓
Stressed BEL
↓
SCRResult
↓
Correlation Aggregation
↓
Basic SCR
↓
CapitalWorkflowResult
```

Future expansion may include:

- market stresses
- catastrophe stresses
- asset-side stresses
- ESG frameworks
- internal model experimentation

without modifying the core modelling engine.

---

# Design Principles

## Projection Must Remain Scenario-Agnostic

Projection must NEVER know:

- which scenario is running
- which SCR is being calculated
- which stresses are applied

---

## Valuation Must Remain Scenario-Agnostic

Valuation must NEVER know:

- stress types
- calibration methodology
- scenario orchestration

---

## Infrastructure Before Realism

The project currently prioritises:

- reusable infrastructure
- abstraction stability
- modular architecture

before:

- advanced realism
- stochastic modelling
- optimisation
- calibration sophistication
