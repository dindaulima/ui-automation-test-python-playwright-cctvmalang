import pytest

from pages.map_page import MapPage


@pytest.fixture
def map_page(page) -> MapPage:
    mp = MapPage(page)
    mp.load()
    return mp
