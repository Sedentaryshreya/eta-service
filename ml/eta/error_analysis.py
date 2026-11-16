"""Extra error analysis for the baseline and the Linear Regression.

ALL DATA IS FAKE (synthetic). These tables describe the invented dataset only and say
nothing about real-world accuracy.

Run from the project folder (virtual environment active):
    python -m ml.eta.error_analysis

It only prints tables. It does not change any file.
"""

import numpy as np
import pandas as pd

from ml.eta.evaluate import DEFAULT_DATA_DIR, baseline_predictions, split_train_validation
from ml.eta.model import build_feature_matrix, load_model
from ml.eta.synthetic import load_trips_csv

DISTANCE_BANDS = [0, 5, 10, 15, np.inf]  # km; the last band is "over 15 km"
WORST_CASES = 5


def build_error_table(validation: pd.DataFrame, group: pd.Series) -> pd.DataFrame:
    """MAE of the baseline and the model, and the baseline's average error, per group."""
    rows = []
    for name, part in validation.groupby(group, observed=True):
        rows.append(
            {
                "group": str(name),
                "trips": len(part),
                "baselineMAE": round(float(part["baselineAbsError"].mean()), 2),
                "modelMAE": round(float(part["modelAbsError"].mean()), 2),
                "baselineBias": round(float(part["baselineError"].mean()), 2),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    trips = load_trips_csv(DEFAULT_DATA_DIR / "synthetic_trips.csv")
    _, validation = split_train_validation(trips)
    validation = validation.copy()

    actual = validation["travelTimeMinutes"].to_numpy(dtype=float)
    baseline = baseline_predictions(validation).to_numpy(dtype=float)
    loaded = load_model()
    model = loaded.estimator.predict(build_feature_matrix(validation))

    validation["baselineEta"] = baseline
    validation["modelEta"] = np.asarray(model, dtype=float)
    validation["baselineError"] = validation["baselineEta"] - actual
    validation["baselineAbsError"] = validation["baselineError"].abs()
    validation["modelAbsError"] = (validation["modelEta"] - actual).__abs__()

    print("FAKE (synthetic) data. Validation trips:", len(validation))
    print("baselineBias = baseline minus actual (negative = baseline too low).\n")

    bands = pd.cut(validation["distanceKm"], bins=DISTANCE_BANDS)
    print("--- Error by distance band (km) ---")
    print(build_error_table(validation, bands).to_string(index=False))

    print("\n--- Error by traffic level ---")
    print(build_error_table(validation, validation["trafficLevel"]).to_string(index=False))

    print("\n--- Error by road type ---")
    print(build_error_table(validation, validation["roadType"]).to_string(index=False))

    columns = ["tripId", "distanceKm", "hour", "travelTimeMinutes", "baselineEta", "modelEta"]
    print(f"\n--- {WORST_CASES} worst trips for the baseline ---")
    worst_baseline = validation.nlargest(WORST_CASES, "baselineAbsError")[columns]
    print(worst_baseline.round(2).to_string(index=False))

    print(f"\n--- {WORST_CASES} worst trips for the model ---")
    worst_model = validation.nlargest(WORST_CASES, "modelAbsError")[columns]
    print(worst_model.round(2).to_string(index=False))


if __name__ == "__main__":
    main()