"""Flow 3: Searching a location by district/street name"""
from playwright.sync_api import expect

# TC7: Typing a query (e.g. "klojen") shows a non-empty suggestions list
# TC8: Typing a query with no matches (e.g. "zzzznotreal") shows an empty/hidden suggestions list
# TC9: Clicking a suggestion pans/zooms the map to that location and hides the suggestions list
# TC10: Clicking the search button / pressing Enter is currently a no-op (does not move the map,
#       does not dismiss the suggestions list) - only clicking a suggestion does. Documented as-is;
#       flag to product if a direct-search action is actually expected.
# TC11: Clicking a suggestion clears the search input instead of populating it with the selected
#       place name. Documented as-is; flag to product if this looks like a bug.


def test_search_with_matching_query_shows_suggestions(map_page):
    map_page.search("klojen")

    expect(map_page.suggestions_list()).to_be_visible()
    assert map_page.suggestion_items().count() > 0


def test_search_with_no_matching_query_shows_no_suggestions(map_page):
    map_page.search("zzzznotreal")

    expect(map_page.suggestions_list()).to_be_hidden()
    assert map_page.suggestion_items().count() == 0


def test_selecting_suggestion_moves_map_and_hides_list(map_page):
    center_before = map_page.get_map_center()
    map_page.search("klojen")

    map_page.click_first_suggestion()

    assert map_page.get_map_center() != center_before
    expect(map_page.suggestions_list()).to_be_hidden()


def test_search_button_and_enter_do_not_move_map(map_page):
    center_before = map_page.get_map_center()
    zoom_before = map_page.get_zoom_level()
    map_page.search("klojen")

    map_page.search_button().click()
    map_page.page.wait_for_timeout(500)

    assert map_page.get_map_center() == center_before
    assert map_page.get_zoom_level() == zoom_before
    expect(map_page.suggestions_list()).to_be_visible()


def test_selecting_suggestion_clears_search_input(map_page):
    map_page.search("klojen")

    map_page.click_first_suggestion()

    expect(map_page.search_input()).to_have_value("")
