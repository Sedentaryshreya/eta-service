# Data inspection, missing fields and required data

> All data in this project is **fake (synthetic)**. This note says what data exists today, what the
> API receives, what is missing, and what real data would be needed. ETAs are estimates, not
> guaranteed arrival times, and this service is not for real emergency dispatch.

## What data exists today

No real trip or location history was available, so the project uses only a synthetic dataset:
`data/synthetic_trips.csv` (1000 invented trips, seed 42). Every row has `dataSource = "synthetic"`.
No approved historical data has been provided so far.

## The columns and how they are used

| Column | Sent in the API request? | Used by the served model? | Note |
|---|---|---|---|
| `tripId` | No | No | Row number only |
| `dataSource` | No | No | Always `synthetic`; marks the data as fake |
| `fromLat`, `fromLng`, `toLat`, `toLng` | Yes | Indirectly | Used to compute `distanceKm` (Haversine) |
| `distanceKm` | Computed from the coordinates | Yes | Straight-line distance |
| `hour` | Yes | Yes | Turned into a peak / off-peak flag |
| `ambulanceType` | Yes | No | Only `BLS` exists, so it carries no signal |
| `dayOfWeek` | No | No | In the dataset, but not in the request |
| `trafficLevel` | No | No | In the dataset, but not in the request |
| `roadType` | No | No | In the dataset, but not in the request |
| `travelTimeMinutes` | No | Target | The value the model learns to predict |

The served Linear Regression uses only values the API can compute from a request: `distanceKm`, a
peak-hour flag, and distance multiplied by that flag. `dayOfWeek`, `trafficLevel` and `roadType`
are kept out on purpose, because the API cannot know them at request time and using them would
make the evaluation look better than the service can really be.

## Missing fields (what the API does not receive)

* **Traffic level at the time of the trip**: no source exists.
* **Road type of the route**: no routing is done; distance is a straight line.
* **Day of week or date**: the request has only an hour.
* **Real route distance**: straight-line distance ignores detours, so the baseline runs about 8.3
  minutes low on the synthetic data.
* **Other ambulance types**: only `BLS` is supported.

## Real data that would be needed to validate or improve the model

These are suggestions to confirm with the mentor and the project lead:

1. Real completed trips with a measured travel time (start time, arrival time, start and end
   coordinates), anonymised, with no patient information.
2. Enough trips across all hours, weekdays, and short and long distances. The model has only seen
   0.52 to 21.99 km.
3. If traffic level, day of week or road type are to be used, a source for them that is also
   available when a request arrives.
4. Agreement on the allowed data source and privacy rules before any real data is used.

Until this exists, model results describe the invented dataset only and must not be described as
real-world accuracy.