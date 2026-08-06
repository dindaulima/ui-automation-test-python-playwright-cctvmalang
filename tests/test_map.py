"""Flow 1: the map loads and renders the CCTV network"""
from playwright.sync_api import expect

# TC1 - Map loads on first visit — district dropdown, search box, zoom controls visible; markers/clusters render; default district filter is "SELURUH KECAMATAN"
def test_map_loads_on_first_visit(map_page):
    expect(map_page.kecamatan_dropdown()).to_be_visible()
    expect(map_page.search_input()).to_be_visible()
    expect(map_page.zoom_in_button()).to_be_visible()
    expect(map_page.zoom_out_button()).to_be_visible()

    # the district filter defaults to showing every camera
    assert map_page.selected_district() == "SELURUH KECAMATAN"

    # the network is rendered as either clustered or individual markers
    marker_count = map_page.camera_markers().count()
    cluster_count = map_page.cluster_markers().count()
    assert marker_count + cluster_count > 0, "expected at least one marker or cluster on the map"

# TC2 - Zoom in increases map zoom level by 1
def test_map_zoom_in_increases_zoom_level(map_page):
    initial_zoom = map_page.get_zoom_level()

    map_page.zoom_in()

    map_page.wait_for_zoom_level(initial_zoom + 1)

# TC3 - Zoom out decreases map zoom level by 1
def test_map_zoom_out_decreases_zoom_level(map_page):
    initial_zoom = map_page.get_zoom_level()

    map_page.zoom_out()

    map_page.wait_for_zoom_level(initial_zoom - 1)
