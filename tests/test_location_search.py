"""Flow 3: Searching a location by district/street name"""
from playwright.sync_api import expect

# TC8: Typing a query (e.g. "klojen") shows a non-empty suggestions list
def test_search_with_matching_query_shows_suggestions(map_page):
    map_page.search("klojen")

    expect(map_page.suggestions_list()).to_be_visible()
    assert map_page.suggestion_items().count() > 0

# TC9: Typing a query with no matches (e.g. "zzzznotreal") shows an empty/hidden suggestions list
def test_search_with_no_matching_query_shows_no_suggestions(map_page):
    map_page.search("zzzznotreal")

    expect(map_page.suggestions_list()).to_be_hidden()
    assert map_page.suggestion_items().count() == 0

# TC10: Clicking a suggestion pans/zooms the map to that location and hides the suggestions list
def test_selecting_suggestion_moves_map_and_hides_list(map_page):
    center_before = map_page.get_map_center()
    map_page.search("klojen")

    map_page.click_first_suggestion()

    assert map_page.get_map_center() != center_before
    expect(map_page.suggestions_list()).to_be_hidden()

# TC11: Clicking the search button should perform the search and move the map to the result
def test_search_button_moves_map_to_result(map_page):
    center_before = map_page.get_map_center()
    zoom_before = map_page.get_zoom_level()
    map_page.search("klojen")

    map_page.click_search_button()

    assert map_page.get_map_center() != center_before or map_page.get_zoom_level() != zoom_before
    expect(map_page.suggestions_list()).to_be_hidden()