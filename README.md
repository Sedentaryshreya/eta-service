# ETA Service (AI/ML) — Emergency & Home Healthcare Platform

Distance and baseline ETA estimates, a synthetic-trip evaluation, a simple
regression model comparison, and a FastAPI `POST /eta` endpoint.

> **Important:** ETA values are estimates, not guaranteed real arrival times.
> They use straight-line (Haversine) distance and assumed average speeds, not
> live traffic or real roads. All speeds and peak hours are illustrative
> assumptions, not measured data. All data in this project is fake/synthetic.
> Results on synthetic data must not be described as validated real-world
> traffic predictions. Not for real emergency dispatch.

## Status

- Done: project setup, configuration and input validation, Haversine distance
  and baseline `predict_eta` (`ml/eta/eta.py`).
- Not built yet: synthetic dataset and baseline evaluation, regression model,
  FastAPI `POST /eta`.

## Setup

Developed and tested on Python 3.13.7. Python 3.11 or newer is expected to work
but has not been tested.

```bash
# 1. Create an isolated environment
python -m venv .venv

# 2. Activate it
#    macOS / Linux / Git Bash:   source .venv/bin/activate
#    Windows PowerShell:         .venv\Scripts\Activate.ps1
#    Windows Command Prompt:     .venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Run the tests
pytest
```

## Try the baseline ETA

```python
from ml.eta.eta import predict_eta

print(predict_eta(28.6139, 77.2090, 28.5355, 77.3910, 14, "BLS"))
# {'etaMinutes': 29.69, 'distanceKm': 19.8}
```

- Inputs: `fromLat`, `fromLng`, `toLat`, `toLng`, `hour` (whole number 0-23),
  `ambulanceType` (exactly `"BLS"`, the only supported type for now).
- Outputs: `etaMinutes` and `distanceKm`, rounded to 2 decimals.
- Invalid input raises `InvalidInputError`.

## Freezing versions

After the first successful install, record exact versions so teammates get
the same ones:

```bash
pip freeze > requirements.lock.txt
```

## Project layout

See the roadmap: `ml/eta/` (logic), `api/` (FastAPI), `data/` (CSV files),
`notebooks/`, `tests/`, `docs/`.