# ETA API contract (v0.1)

> ETAs are **estimates**, not guaranteed arrival times. The model behind them was trained
> on **fake (synthetic) data**. This service is not for real emergency dispatch.

Run locally (project folder, virtual environment active):

```
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Interactive page: http://127.0.0.1:8000/docs

## POST /eta

Request (JSON). All six fields are required. Extra fields are ignored.

| Field | Type | Rule |
|---|---|---|
| `fromLat` | number | -90 to 90 |
| `fromLng` | number | -180 to 180 |
| `toLat` | number | -90 to 90 |
| `toLng` | number | -180 to 180 |
| `hour` | integer | whole number 0 to 23 (`8.0`, `"8"` and `true` are rejected) |
| `ambulanceType` | string | exactly `"BLS"` (upper case; `"bls"` and `"ALS"` are rejected) |

Example request:

```json
{"fromLat": 28.6139, "fromLng": 77.2090, "toLat": 28.5355, "toLng": 77.3910, "hour": 14, "ambulanceType": "BLS"}
```

Success: HTTP 200

```json
{"etaMinutes": 44.11, "distanceKm": 19.8}
```

Both numbers are rounded to 2 decimals. `distanceKm` is the straight-line (Haversine) distance.

Optional response header `X-ETA-Source`: `model` (learned model answered) or `baseline`
(simple speed-based rule answered). The body is the same shape either way.

The baseline answers when: the model file could not be loaded at startup; the trip distance is
outside the range the model was trained on (about 0.52 to 21.99 km, including identical start and
end points); or the model failed on that request.

Identical start and end points return `{"etaMinutes": 0.0, "distanceKm": 0.0}`
(**unconfirmed with Naga**).

## Errors

Invalid input returns HTTP **422** in the usual FastAPI shape, but without the submitted value:

```json
{"detail": [{"loc": ["body", "hour"], "msg": "hour must be a whole number (integer).", "type": "value_error"}]}
```

* Only the first problem is reported for bad values (checked in this order: `fromLat`,
  `fromLng`, `toLat`, `toLng`, `hour`, `ambulanceType`). A missing field is reported by the
  framework with `"type": "missing"`.
* The error body never repeats what was sent.
* An unexpected server bug returns HTTP 500 with no details.

## GET /health

```json
{"status": "ok", "modelLoaded": true}
```

`modelLoaded` is `false` when the service is running on the baseline only.

## Open points for Naga

1. Identical start and end points return `0.0` / `0.0`: is that acceptable?
2. `ambulanceType` must be exactly `"BLS"`.
3. `hour` must be a JSON integer. If the Node side sends `8.0` or `"8"` it will get a 422.