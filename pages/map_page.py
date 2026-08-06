from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class MapPage(BasePage):
    PATH = "/sebaran-cctv"

    # selectors
    def kecamatan_dropdown(self) -> Locator:
        return self.page.locator("#kecamatan-dropdown")

    def search_input(self) -> Locator:
        return self.page.locator("#location-search")

    def search_button(self) -> Locator:
        return self.page.locator("#search-button")

    def suggestions_list(self) -> Locator:
        return self.page.locator("#suggestions-list")

    def suggestion_items(self) -> Locator:
        return self.suggestions_list().locator("> div")

    def zoom_in_button(self) -> Locator:
        return self.page.get_by_role("button", name="Zoom in")

    def zoom_out_button(self) -> Locator:
        return self.page.get_by_role("button", name="Zoom out")

    def camera_markers(self) -> Locator:
        return self.page.get_by_role("button", name="Marker")

    def cluster_markers(self) -> Locator:
        return self.page.locator(".marker-cluster")

    def popup(self) -> Locator:
        return self.page.locator(".leaflet-popup-content")

    def popup_view_detail_button(self) -> Locator:
        return self.popup().get_by_role("button", name="Lihat Detail")

    def popup_close_button(self) -> Locator:
        return self.popup().get_by_role("button", name="Tutup")

    def video_modal(self) -> Locator:
        return self.page.locator("#videoModal")

    # navigation
    def load(self):
        self.goto(self.PATH)
        expect(self.kecamatan_dropdown()).to_be_visible()
        # wait for the map's own tiles/markers to finish rendering
        self.page.wait_for_function("() => window.map !== undefined")

    # functional
    def filter_by_district(self, district: str):
        self.page.evaluate(
            "() => { window.__districtIdle = false; window.map.once('moveend', () => { window.__districtIdle = true; }); }"
        )
        self.kecamatan_dropdown().select_option(label=district)
        self.page.wait_for_function("() => window.__districtIdle === true")

    def selected_district(self) -> str:
        return self.kecamatan_dropdown().locator("option:checked").text_content()

    def search(self, query: str):
        self.search_input().fill(query)
        # suggestions are filtered client-side with a ~500ms debounce
        self.page.wait_for_timeout(800)

    def click_first_suggestion(self):
        self.page.evaluate(
            "() => { window.__searchIdle = false; window.map.once('moveend', () => { window.__searchIdle = true; }); }"
        )
        self.suggestion_items().first.click()
        self.page.wait_for_function("() => window.__searchIdle === true")

    def total_camera_count(self) -> int:
        return self.page.evaluate("() => window.markerClusterGroup.getLayers().length")

    def get_map_center(self) -> dict:
        return self.page.evaluate("() => window.map.getCenter()")

    def zoom_in(self):
        self.zoom_in_button().click()

    def zoom_out(self):
        self.zoom_out_button().click()

    def get_zoom_level(self) -> int:
        return self.page.evaluate("() => window.map.getZoom()")

    def wait_for_zoom_level(self, level: int, timeout: float = 5000):
        self.page.wait_for_function(
            "(level) => window.map.getZoom() === level", arg=level, timeout=timeout
        )
