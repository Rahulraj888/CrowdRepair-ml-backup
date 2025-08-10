# CrowdRepair ML Service

A lightweight Flask service that clusters geo-located road reports into **hotspots** for the CrowdRepair platform.

- **Endpoint:** `POST /predict_hotspots`
- **Input:** JSON with a list of reports: `{ "reports": [ { "latitude": <float>, "longitude": <float> }, ... ] }`
- **Output:** **GeoJSON FeatureCollection** of clustered features (polygons/points), ready for map rendering.

## How it works
- Uses **DBSCAN** (`scikit-learn`) to cluster report locations.
- Geometries are built with **Shapely** and returned as **GeoJSON**.
- Invalid items (missing `latitude`/`longitude`) are ignored.
- If no clusters are found, each point is returned as a standalone Feature.

## Project Layout
```
CrowdRepair-ml-backup/
├── app.py                 # Flask app + CORS
├── config.py              # DBSCAN params + FLASK_PORT
├── clustering/
│   ├── clusterer.py       # DBSCAN + GeoJSON feature building
│   └── utils.py           # input validation helpers
└── requirements.txt
```

## Configuration
Adjust clustering and server settings in **`config.py`**:
```python
DBSCAN_EPS = 0.001         # neighborhood radius (degrees)
DBSCAN_MIN_SAMPLES = 1     # minimum points to form a cluster
FLASK_PORT = 5001          # server port
```
> Note: `EPS` is in **degrees** (WGS84). For city-scale maps, start with small values (e.g., `0.001` ~ 100m) and tune as needed.

## Setup

```bash
# 1) Create & activate a virtualenv (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the service
python app.py
# Service starts on http://localhost:5001 (configurable via config.py)
```

## Example Request

```bash
curl -X POST http://localhost:5001/predict_hotspots   -H "Content-Type: application/json"   -d '{
    "reports": [
      { "latitude": 43.6510, "longitude": -79.3470 },
      { "latitude": 43.6512, "longitude": -79.3468 },
      { "latitude": 43.7000, "longitude": -79.4000 }
    ]
  }'
```

### Example Response (shape)
```json
{
  "type": "FeatureCollection",
  "features": [
    { "type": "Feature", "geometry": { ... }, "properties": { "cluster_id": 0, "count": 2 } },
    { "type": "Feature", "geometry": { ... }, "properties": { "cluster_id": 1, "count": 1 } }
  ]
}
```

## Tuning Tips
- Increase `DBSCAN_EPS` to **merge** nearby hotspots; decrease to **split** them.
- Raise `DBSCAN_MIN_SAMPLES` to require more reports per hotspot.
- Pre-filter your input to a city/viewport to avoid clustering globally dispersed points.

## Testing
Lightweight tests can be added with **pytest**. Example (pseudo):
```python
def test_empty_returns_empty(fc):
    assert fc["features"] == []
```

## License
MIT (or your chosen license).
