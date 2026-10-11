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
  and baseline `predict_eta` (`ml/eta/eta.py`), synthetic dataset and baseline
  evaluation (`ml/eta/synthetic.py`, `ml/eta/evaluate.py`).
- Not built yet: regression model, FastAPI `POST /eta`.

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

## Synthetic data and baseline evaluation

All trips are **fake**, generated from an invented model. Create the dataset and
evaluate the baseline (the dataset must exist before `pytest`, because a few tests
check the saved files):

```bash
python -m ml.eta.synthetic     # data/synthetic_trips.csv (1000 fake trips, seed 42)
python -m ml.eta.evaluate      # data/baseline_metrics.json + data/baseline_examples.csv
```

The reported MAE measures the baseline against the invented synthetic world only.
It is not a measure of real-world accuracy. Fields, assumptions and limitations
are in `docs/dataset.md`.

## Freezing versions

After the first successful install, record exact versions so teammates get
the same ones:

```bash
pip freeze > requirements.lock.txt
```

## Project layout

See the roadmap: `ml/eta/` (logic), `api/` (FastAPI), `data/` (CSV and JSON
files), `notebooks/`, `tests/`, `docs/`.