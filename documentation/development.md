
# Development Guide

## Overview

This project prioritises:

- architectural discipline
- reproducibility
- stable interfaces
- explicit abstraction boundaries
- modular extensibility

Development practices are intentionally designed to support long-term maintainability.

---

# Notebook Discipline

Notebooks are configuration and analysis only.

Allowed notebook responsibilities:

- imports
- dependency composition
- scenario setup
- diagnostics
- charts
- visualisation
- analysis
- workflow configuration

Not allowed:

- actuarial mechanics
- projection logic
- valuation logic
- assumption calculations

---

# Notebook Testing Discipline

All notebooks should run successfully from:

- a fresh kernel
- a clean notebook state

Notebook setup should explicitly include:

```python
import sys
import os

sys.path.append(os.path.abspath(".."))
```

Notebook tests should avoid relying on:

- previously executed cells
- implicit notebook state
- cached variables

---

# Import Discipline

Preferred import style:

```python
import model.valuation as valuation_module
```

Avoid importing individual functions directly into notebook scope where possible.

---

# Workflow Configuration Discipline

Workflow execution should occur through:

```python
CapitalWorkflowConfig
```

Avoid:

- manual workflow orchestration
- duplicated execution wiring
- direct notebook-owned ingestion

Workflow orchestration belongs inside the workflow layer.

---

# Repository Path Discipline

Implementation examples should:

- use project-relative paths
- align with repository structure
- remain executable from notebook context

Avoid:

- machine-specific paths
- ambiguous relative paths
- hidden setup assumptions

---

# Pandas Boundary Rules

Pandas should remain outside the core engine.

Pandas is permitted only in:

- ingestion
- validation
- analytics
- notebook orchestration

Core modelling logic should operate on:

- structured objects
- stable interfaces
- explicit contracts

---

# Git Workflow

Recommended workflow:

```bash
git checkout main
git pull origin main
git checkout -b feature/feature-name
```

Development guidelines:

- keep feature branches isolated
- commit logical milestones
- avoid unrelated structural changes
- merge completed features cleanly

---

# Environment Discipline

Recommended practices:

- use a dedicated virtual environment
- verify the correct Python executable
- use the correct notebook kernel
- pull latest changes before development

Avoid:

- mixed environments
- shared environments
- hidden dependency drift

---

# Architectural Extension Philosophy

New functionality should integrate through:

- provider abstraction
- stable interfaces
- structured contracts

New features should avoid:

- rewriting projection
- rewriting valuation
- introducing hidden dependencies
- tightly coupling engine layers

---

# Current Development Priorities

Current priorities are:

- scenario infrastructure
- SCR framework design
- modular assumptions infrastructure
- stable result contracts
- reusable capital modelling architecture

Current priorities are NOT:

- HPC
- multiprocessing
- vectorisation
- Monte Carlo
- advanced stochastic modelling

Infrastructure stability currently takes priority over realism and optimisation.
