"""Flow 4: opening a camera pin and watching its live stream."""
from playwright.sync_api import expect


#TC12 - hovering a camera pin to show the popup modal
def test_hovering_marker_shows_popup(map_page):
    map_page.click_largest_cluster()

    map_page.hover_first_visible_camera_marker()

    expect(map_page.popup()).to_be_visible()
    expect(map_page.popup_heading()).to_be_visible()
    expect(map_page.popup()).to_contain_text("LABEL:")
    expect(map_page.popup()).to_contain_text("LOKASI:")

#TC13: Popup has "Lihat Detail" and "Tutup" buttons
def test_popup_has_view_detail_and_close_buttons(map_page):
    map_page.click_largest_cluster()
    map_page.click_first_camera_marker()

    expect(map_page.popup_view_detail_button()).to_be_visible()
    expect(map_page.popup_close_button()).to_be_visible()

#TC14 - Opening a camera and watch live video
def test_opening_camera_plays_live_video(map_page, camera_modal):
    map_page.click_largest_cluster()
    map_page.click_first_camera_marker()

    map_page.popup_view_detail_button().click()

    expect(camera_modal.root()).to_be_visible()
    expect(camera_modal.address).not_to_be_empty()
    expect(camera_modal.video).to_be_visible()
    expect(camera_modal.video).to_have_js_property("paused", False)

#TC15 - Closing the live video
def test_closing_video_hides_stream_modal(map_page, camera_modal):
    map_page.click_largest_cluster()
    map_page.click_first_camera_marker()
    map_page.popup_view_detail_button().click()
    expect(camera_modal.video).to_be_visible()

    camera_modal.close()

    expect(camera_modal.root()).to_be_hidden()

#TC16 - closing the popup modal camera pin
def test_closing_popup_after_watching_stream(map_page, camera_modal):
    map_page.click_largest_cluster()
    map_page.click_first_camera_marker()
    map_page.popup_view_detail_button().click()
    camera_modal.close()
    expect(map_page.popup()).to_be_visible()

    map_page.popup_close_button().click()

    expect(map_page.popup()).not_to_be_attached()
