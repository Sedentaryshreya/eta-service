"""Training and serving must use the same feature definitions (all data is fake)."""

from __future__ import annotations

import numpy as np
import pytest

from ml.eta.evaluate import DEFAULT_DATA_DIR, split_train_validation
from ml.eta.eta import haversine_distance_km
from ml.eta.model import (
    FEATURE_NAMES,
    ModelPredictionError,
    build_feature_matrix,
    build_feature_row,
    load_model,
    predict_eta_with_model,
)
from ml.eta.synthetic import load_trips_csv

SAMPLE_SIZE = 60


@pytest.fixture(scope="module")
def validation():
    trips = load_trips_csv(DEFAULT_DATA_DIR / "synthetic_trips.csv")
    _, validation_trips = split_train_validation(trips)
    return validation_trips.iloc[:SAMPLE_SIZE].copy()


@pytest.fixture(scope="module")
def loaded():
    return load_model()


def test_training_matrix_rows_equal_the_single_trip_feature_row(validation):
    matrix = build_feature_matrix(validation)
    for position, row in enumerate(validation.itertuples(index=False)):
        distance = haversine_distance_km(row.fromLat, row.fromLng, row.toLat, row.toLng)
        expected = build_feature_row(distance, int(row.hour))
        assert matrix[position].tolist() == pytest.approx(expected)


def test_batch_prediction_matches_the_api_path_prediction(validation, loaded):
    batch = loaded.estimator.predict(build_feature_matrix(validation))
    compared = 0
    for position, row in enumerate(validation.itertuples(index=False)):
        if batch[position] < 0.0:
            continue  # the API path refuses negative predictions on purpose
        try:
            single = predict_eta_with_model(
                loaded,
                row.fromLat,
                row.fromLng,
                row.toLat,
                row.toLng,
                int(row.hour),
                "BLS",
            )
        except ModelPredictionError:
            continue
        assert single["etaMinutes"] == pytest.approx(float(batch[position]), abs=0.01)
        compared += 1
    assert compared >= 20


def test_saved_feature_names_match_the_code(loaded):
    assert list(loaded.metadata["featureNames"]) == list(FEATURE_NAMES)


def test_features_ignore_columns_the_api_does_not_receive(validation):
    changed = validation.copy()
    changed["trafficLevel"] = "high"
    changed["roadType"] = "local"
    changed["dayOfWeek"] = 0
    changed["travelTimeMinutes"] = 0.0
    assert np.array_equal(build_feature_matrix(validation), build_feature_matrix(changed))