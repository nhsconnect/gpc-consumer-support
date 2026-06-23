"""Page object for top-level home navigation."""
from pages.base_page import BasePage


class HomePage(BasePage):
    """Encapsulates navigation from home into an NMS episode."""

    def open_new_nms_episode(self) -> None:
        self.navigate()
        self.page.get_by_role("link", name="New Medicine Service").click()
        self.wait_for_load()

        start_btn = self.page.get_by_role("button", name="Start New NMS")
        start_btn.wait_for(state="visible", timeout=15000)
        start_btn.click()
        self.wait_for_load()

        name_search_button = self.page.get_by_role("button", name="NAME SEARCH")
        if name_search_button.is_visible():
            aria_pressed = name_search_button.get_attribute("aria-pressed")
            if aria_pressed != "true":
                name_search_button.click()
                self.wait_for_load()
