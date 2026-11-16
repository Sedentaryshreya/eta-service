# Error analysis (synthetic validation, 200 trips)

> All data here is **fake (synthetic)**. These tables describe the invented dataset only. They do
> not show real-world accuracy. ETAs are estimates, not guaranteed arrival times.

Reproduce with (project folder, virtual environment active):

    python -m ml.eta.error_analysis

MAE is the average size of the mistake in minutes. `baselineBias` is the baseline minus the actual
time on average (negative means the baseline is too low). The model is the served Linear
Regression, used on its own here (the service answers with the baseline outside 0.52 to 21.99 km).

## Error by distance band

| Distance (km) | Trips | Baseline MAE | Model MAE | Baseline bias |
|---|---|---|---|---|
| 0 to 5 | 12 | 6.42 | 5.71 | -6.17 |
| 5 to 10 | 52 | 6.53 | 5.38 | -4.77 |
| 10 to 15 | 97 | 12.58 | 10.75 | -9.63 |
| over 15 | 39 | 15.56 | 14.61 | -10.33 |

## Error by traffic level

| Traffic | Trips | Baseline MAE | Model MAE | Baseline bias |
|---|---|---|---|---|
| high | 34 | 18.28 | 15.17 | -16.73 |
| medium | 71 | 11.44 | 9.37 | -8.25 |
| low | 95 | 8.53 | 8.21 | -5.32 |

## Error by road type

| Road type | Trips | Baseline MAE | Model MAE | Baseline bias |
|---|---|---|---|---|
| arterial | 88 | 5.50 | 5.50 | -3.59 |
| highway | 40 | 5.66 | 12.60 | 4.75 |
| local | 72 | 21.30 | 13.52 | -21.30 |

## What the tables show

* **The model is better than the baseline in every distance band**, by 0.71 to 1.83 minutes. Both
  get worse as trips get longer.
* **Heavy traffic is the hardest case** for both (baseline 18.28, model 15.17 minutes), against
  8.53 and 8.21 in low traffic.
* **On highways the model is worse than the baseline** (12.60 against 5.66 minutes, 40 trips). On
  local roads it is better (13.52 against 21.30, 72 trips). On arterial roads they are equal. The
  overall gain of 1.42 minutes hides this.
* **On local roads the baseline is too low on almost every trip** (its bias equals its MAE).
* **Probable reason (not tested):** neither method receives the road type or traffic level, so the
  model averages over all road types. Both are fields the API does not get (see
  `docs/data_inspection.md`).
* **The worst trips** (for example trip ids 254, 374 and 22) took 69 to 93 minutes for 12 to 16 km,
  and both methods predicted far too low. The cause was not investigated.

## Cautions

* Some groups are small (12 to 97 trips), and this uses one 800/200 split. No significance test was
  run on these differences.
* Everything is on invented data. Real trips are needed to know whether any of this holds.