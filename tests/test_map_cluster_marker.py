"""Flow 4:  Marker & cluster interaction"""
import pytest

from pages.map_page import MapPage

#TC12: Clicking a cluster marker zooms the map in (cluster expansion)
#TC13: Clicking an individual camera marker opens a popup showing district, label, and location text
#TC14: Popup has "Lihat Detail" and "Tutup" buttons
#TC15: Clicking "Tutup" closes the popup