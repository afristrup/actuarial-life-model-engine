
# Assumptions Framework

## Overview

The assumptions framework provides a modular abstraction layer between:

- external assumption data
- actuarial modelling mechanics

The objective is to ensure that projection and valuation remain independent of:

- CSV structures
- segmentation logic
- market-data conventions
- provider internals
- scenario implementation

---

# Core Assumption Flow

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

---

# AssumptionSet

The `AssumptionSet` acts as the unified interface consumed by the engine.

Projection and valuation depend only on this interface.

Current interface:

```python
assumptions.qx(policy, age)
assumptions.discount_factor(t)
assumptions.lapse_rate(policy, t)
assumptions.expenses(policy, t)
```

This stable contract is one of the core architectural principles of the project.

---

# Assumption Configuration

Workflow execution now consumes assumptions through:

```text
AssumptionConfig
```

Responsibilities include:

- centralising assumption file paths
- workflow ingestion ownership
- scalable assumption extensibility

The configuration layer intentionally remains separate from provider implementation and actuarial mechanics.

---

# Assumption Responsibility Mapping

| Assumption Type | Affects Projection | Affects Valuation | Mechanism |
|---|---|---|---|
| Mortality | Yes | Indirectly | `qx()` |
| Lapse | Yes | Indirectly | `lapse_rate()` |
| Expenses | Yes | Indirectly | `expenses()` |
| Interest / Yield Curve | No | Yes | `discount_factor()` |

This separation is intentional and central to the architecture.

---

# Mortality Framework

Implemented mortality functionality includes:

- age-based mortality
- gender segmentation
- smoker adjustments
- provider-level mortality parameter composition
- provider-based lookup
- externally configurable assumptions

Current mortality structure:

```text
(gender, age) → base qx
```

Additional adjustments:

```text
smoker_status → mortality multiplier
```

Final mortality:

```text
final_qx = base_qx × smoker_multiplier
```

Mortality parameter composition occurs inside the mortality provider layer rather than inside workflow orchestration or projection logic.

Projection remains unaware of:

- mortality table structure
- segmentation implementation
- adjustment composition
- ingestion mechanics

---

# Lapse Framework

Implemented lapse functionality includes:

- segmented lapse assumptions
- duration-based segmentation
- provider-based lookup
- externally configurable lapse tables

Current segmentation dimensions:

- product_type
- smoker_status
- duration ranges

Projection consumes only:

```python
assumptions.lapse_rate(policy, t)
```

Projection remains unaware of segmentation mechanics.

---

# Yield Curve Framework

Implemented interest functionality includes:

- CSV-driven yield curve ingestion
- spot-rate discounting
- float maturity support
- terminal extrapolation
- provider-based discounting

Current provider:

```text
YieldCurve
```

Current interface:

```python
assumptions.discount_factor(t)
```

Valuation remains unaware of:

- curve structure
- interpolation mechanics
- market-data formatting
- scenario mechanics

---

# Expense Framework

Implemented expense functionality includes:

- acquisition expenses
- maintenance expenses
- fixed expenses
- premium percentage expenses
- provider-based resolution

Projection consumes expenses through:

```python
assumptions.expenses(policy, t)
```

Projection remains unaware of:

- expense table structures
- expense composition logic
- segmentation mechanics

---

# Validation Philosophy

Validation occurs only at ingestion boundaries.

Validation framework currently supports:

- required columns
- no null validation
- numeric validation
- rate validation
- duplicate segment detection
- overlapping range detection
- non-negative validation

Core modelling logic assumes validated structured inputs.

---

# Design Philosophy

The assumptions architecture prioritises:

- modularity
- explicit provider boundaries
- stable contracts
- externalised assumptions
- composability
- extensibility

The objective is to support future provider enhancement without modifying projection or valuation mechanics.
