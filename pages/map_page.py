from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class MapPage(BasePage):
    PATH = "/sebaran-cctv"

    # selectors
    def kecamatan_dropdown(self) -> Locator:
        return self.page.locator("#kecamatan-dropdown")

    def search_input(self) -> Locator:
        return self.page.locator("#location-search")

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

    def popup_heading(self) -> Locator:
        return self.popup().locator("h3")

    def popup_view_detail_button(self) -> Locator:
        return self.popup().get_by_role("button", name="Lihat Detail")

    def popup_close_button(self) -> Locator:
        return self.popup().get_by_role("button", name="Tutup")


    # navigation
    def load(self):
        self.goto(self.PATH)
        expect(self.kecamatan_dropdown()).to_be_visible()
        # window.map exists before the camera list AJAX call resolves; wait for
        # markers to actually be populated so callers see a fully loaded map
        self.page.wait_for_function("() => window.map !== undefined")
        self.page.wait_for_function(
            "() => window.markerClusterGroup !== undefined && window.markerClusterGroup.getLayers().length > 0"
        )


    # functional
    def filter_by_district(self, district: str):
        self.page.evaluate(
            "() => { window.__districtIdle = false; window.map.once('moveend', () => { window.__districtIdle = true; }); }"
        )
        self.kecamatan_dropdown().select_option(label=district)
        self.page.wait_for_function("() => window.__districtIdle === true")
        self.page.wait_for_function("() => window.markerClusterGroup.getLayers().length >0")

    def selected_district(self) -> str:
        return self.kecamatan_dropdown().locator("option:checked").text_content()

    def search(self, query: str):
        # suggestions are rendered synchronously by the page's oninput handler,
        # so the fill's dispatched input event leaves the list already up to date
        self.search_input().fill(query)

    def click_first_suggestion(self):
        self.page.evaluate(
            "() => { window.__searchIdle = false; window.map.once('moveend', () => { window.__searchIdle = true; }); }"
        )
        self.suggestion_items().first.click()
        self.page.wait_for_function("() => window.__searchIdle === true")

    def click_largest_cluster(self):
        self.page.evaluate(
            "() => { window.__clusterZoomed = false; window.map.once('zoomend', () => { window.__clusterZoomed = true; }); }"
        )
        self.page.evaluate(
            "() => { const clusters = [...document.querySelectorAll('.marker-cluster')];"
            " clusters.reduce((a, b) => (parseInt(b.textContent) > parseInt(a.textContent) ? b : a)).click(); }"
        )
        self.page.wait_for_function("() => window.__clusterZoomed === true")

    def click_first_camera_marker(self):
        # clicked via JS: Playwright's pointer-based click moves real focus onto the marker icon,
        # which trips a "panOnFocus" bug in the site's Leaflet setup (NaN LatLng) and silently
        # swallows the popup open; a plain DOM click sidesteps that.
        self.page.wait_for_function("() => document.querySelectorAll('img[alt=\"Marker\"]').length > 0")
        self.page.evaluate("() => document.querySelector('img[alt=\"Marker\"]').click()")

    def hover_first_visible_camera_marker(self):
        # cluster expansion scatters markers across a much larger area than the viewport;
        # only hover one that Playwright can actually move the mouse onto.
        self.page.wait_for_function("() => document.querySelectorAll('img[alt=\"Marker\"]').length > 0")
        viewport = self.page.viewport_size
        markers = self.camera_markers()
        for i in range(markers.count()):
            box = markers.nth(i).bounding_box()
            if box and 0 <= box["x"] < viewport["width"] and 0 <= box["y"] < viewport["height"]:
                markers.nth(i).hover()
                return
        raise AssertionError("no camera marker is within the visible viewport")

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
