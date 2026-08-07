import pytest

from pages.camera_modal import CameraStreamModal
from pages.map_page import MapPage


@pytest.fixture
def map_page(page) -> MapPage:
    # the live site loads several third-party CDN scripts plus a backend AJAX
    # call for camera data, which can comfortably exceed Playwright's 30s
    # default under concurrent (parallel) load
    page.set_default_navigation_timeout(60000)
    mp = MapPage(page)
    mp.load()
    return mp


@pytest.fixture
def camera_modal(page) -> CameraStreamModal:
    return CameraStreamModal(page)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "ignore_https_errors": True}
