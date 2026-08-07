"""Flow 2: filtering map by district"""

# TC5: Selecting a district (e.g. "KLOJEN") re-centers the map and filters markers to that district only
def test_selecting_district_recenters_map(map_page):
    center_before = map_page.get_map_center()

    map_page.filter_by_district("KLOJEN")

    assert map_page.selected_district() == "KLOJEN"
    center_after = map_page.get_map_center()
    assert center_after != center_before

# TC6: Selecting a district changes the marker count vs. "SELURUH KECAMATAN" (fewer markers shown)
def test_selecting_district_filters_camera_count(map_page):
    total_count = map_page.total_camera_count()

    map_page.filter_by_district("KLOJEN")
    district_count = map_page.total_camera_count()

    assert 0 < district_count < total_count

# TC7: Switching back to "SELURUH KECAMATAN" restores the full marker set
def test_switching_back_to_all_districts_restores_full_count(map_page):
    total_count = map_page.total_camera_count()

    map_page.filter_by_district("KLOJEN")
    assert map_page.total_camera_count() < total_count

    map_page.filter_by_district("SELURUH KECAMATAN")
    assert map_page.selected_district() == "SELURUH KECAMATAN"
    assert map_page.total_camera_count() == total_count
