import pytest

from pages.camera_modal import CameraStreamModal
from pages.map_page import MapPage


@pytest.fixture
def map_page(page) -> MapPage:
    mp = MapPage(page)
    mp.load()
    return mp


@pytest.fixture
def camera_modal(page) -> CameraStreamModal:
    return CameraStreamModal(page)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "ignore_https_errors": True}
