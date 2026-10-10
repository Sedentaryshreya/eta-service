# ETA Service (AI/ML) — Emergency & Home Healthcare Platform

Distance and baseline ETA estimates, a synthetic-trip evaluation, a simple
regression model comparison, and a FastAPI `POST /eta` endpoint.

> **Important:** ETA values are estimates, not guaranteed real arrival times.
> All data in this project is fake/synthetic. Results on synthetic data must
> not be described as validated real-world traffic predictions.

**Status:** Phase 0 (project setup) only. No ETA logic exists yet.

## Setup

Requires Python 3.11 or newer.

```bash
# 1. Create an isolated environment
python -m venv .venv

# 2. Activate it
#    macOS / Linux / Git Bash:   source .venv/bin/activate
#    Windows PowerShell:         .venv\Scripts\Activate.ps1
#    Windows Command Prompt:     .venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Check the setup
pytest
```

## Freezing versions

After the first successful install, record exact versions so teammates get
the same ones:

```bash
pip freeze > requirements.lock.txt
```

## Project layout

See the roadmap: `ml/eta/` (logic), `api/` (FastAPI), `data/` (CSV files),
`notebooks/`, `tests/`, `docs/`.