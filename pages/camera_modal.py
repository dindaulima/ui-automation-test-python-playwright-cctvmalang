from playwright.sync_api import Locator, expect

from pages.base_page import BasePage

class CameraStreamModal(BasePage):
    #selector
    def root(self) -> Locator:
        return self.page.locator("#videoModal")

    @property
    def address(self) -> Locator:
        return self.page.locator("#camera_address")

    @property
    def video(self) -> Locator:
        return self.page.locator("#cctv-stream-video")

    @property
    def refresh_button(self) -> Locator:
        return self.page.locator("#refreshBtn")

    @property
    def close_button(self) -> Locator:
        return self.page.locator(".close-modal")

    #functional
    def refresh(self) -> None:
        self.refresh_button.click()

    def close(self) -> None:
        self.close_button.click()
        expect(self.video).not_to_be_attached()