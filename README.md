# CCTV Malang UI Automation

End-to-end UI tests for the [Sebaran CCTV Malang](https://cctv.malangkota.go.id/sebaran-cctv) map, built with Python, Playwright, and pytest using the Page Object Model.

## Requirements

- Python 3.10+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Running the tests

```bash
pytest
```

Run a single file or test:

```bash
pytest tests/test_map.py
pytest tests/test_district_filter.py::test_selecting_district_filters_camera_count
```

Run in parallel (via `pytest-xdist`):

```bash
pytest -n auto
```

The target base URL is configured in [pytest.ini](pytest.ini). By default Playwright runs headless; add `--headed` to watch the browser, or `--slowmo=500` to slow it down.

## Project structure

```
pages/                  # Page Object Model
  base_page.py            # shared navigation helpers
  map_page.py              # map view: district filter, search, zoom, markers
  camera_modal.py           # camera stream modal (video player)

tests/
  conftest.py              # shared fixtures (map_page)
  test_map.py               # map load, zoom in/out
  test_district_filter.py    # filtering cameras by district (kecamatan)
  test_location_search.py     # location search & suggestions
  test_map_cluster_marker.py   # marker/cluster popup interactions (planned)
  test_camera_stream.py         # camera pin -> live video stream (planned)
```

## Notes

- Tests interact with the map's Leaflet/marker-cluster internals (`window.map`, `window.markerClusterGroup`) to wait for animations and read state deterministically instead of relying on fixed sleeps.
- `test_map_cluster_marker.py` and `test_camera_stream.py` currently only document their planned test cases (TC12–TC19) and are not yet implemented.
