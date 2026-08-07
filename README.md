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

Tests run in parallel by default (`-n 2`, via `pytest-xdist`, configured in [pytest.ini](pytest.ini)). Override the worker count directly:

```bash
pytest -n 0      # sequential
pytest -n auto   # one worker per CPU core
```

Note: the suite drives the live `cctv.malangkota.go.id` site rather than a mock, and its backend appears to serialize requests rather than handle them concurrently — so higher worker counts (`-n auto`) can cause navigation timeouts or even run slower than `-n 2`, and `-n 2` itself isn't reliably faster than sequential. `-n 2` is the safest default we found for this target; it's kept mainly to demonstrate the framework's parallel-execution support.

The target base URL is configured via `--base-url` in [pytest.ini](pytest.ini)'s `addopts` (not the `base_url` ini key — `pytest-base-url` doesn't propagate that to `pytest-xdist` worker processes). By default Playwright runs headless; add `--headed` to watch the browser, or `--slowmo=500` to slow it down.

## Project structure

```
pages/                  # Page Object Model
  base_page.py            # shared navigation helpers
  map_page.py              # map view: district filter, search, zoom, markers
  camera_modal.py           # camera stream modal (video player)

tests/
  conftest.py              # shared fixtures (map_page)
  test_map_cluster.py       # map load, zoom in/out
  test_district_filter.py    # filtering cameras by district (kecamatan)
  test_location_search.py     # location search & suggestions
  test_camera_stream.py         # camera pin -> live video stream
```

## Notes

- Tests interact with the map's Leaflet/marker-cluster internals (`window.map`, `window.markerClusterGroup`) to wait for animations and read state deterministically instead of relying on fixed sleeps.

