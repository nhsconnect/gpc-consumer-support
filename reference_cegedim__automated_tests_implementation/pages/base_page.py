"""Base page object for GP Connect Consumer Support tests.

Wraps a Playwright Page and provides common interaction helpers
used by all capability-specific page objects.
"""
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, path: str = "") -> None:
        """Navigate to a path relative to the base URL."""
        url = f"{self.base_url}/{path}".rstrip("/")
        self.page.goto(url, wait_until="networkidle")

    def reload(self) -> None:
        self.page.reload(wait_until="networkidle")

    @property
    def current_url(self) -> str:
        return self.page.url

    @property
    def title(self) -> str:
        return self.page.title()

    # ------------------------------------------------------------------
    # Element helpers
    # ------------------------------------------------------------------

    def click(self, selector: str, **kwargs) -> None:
        self.page.click(selector, **kwargs)

    def fill(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)

    def select_option(self, selector: str, value: str) -> None:
        self.page.select_option(selector, value)

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector) or ""

    def get_input_value(self, selector: str) -> str:
        return self.page.input_value(selector)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def is_enabled(self, selector: str) -> bool:
        return self.page.is_enabled(selector)

    # ------------------------------------------------------------------
    # Wait helpers
    # ------------------------------------------------------------------

    def wait_for_selector(self, selector: str, **kwargs):
        return self.page.wait_for_selector(selector, **kwargs)

    def wait_for_url(self, pattern: str, **kwargs) -> None:
        self.page.wait_for_url(pattern, **kwargs)

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("networkidle")

    # ------------------------------------------------------------------
    # Assertions (Playwright expect wrappers)
    # ------------------------------------------------------------------

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_contain_text(text)

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}**")

    # ------------------------------------------------------------------
    # Common UI patterns
    # ------------------------------------------------------------------

    def get_error_message(self) -> str:
        """Return any displayed error/alert message text."""
        for sel in [".alert-danger", ".error-message", '[role="alert"]']:
            if self.is_visible(sel):
                return self.get_text(sel).strip()
        return ""

    def get_success_message(self) -> str:
        """Return any displayed success message text."""
        for sel in [".alert-success", ".success-message"]:
            if self.is_visible(sel):
                return self.get_text(sel).strip()
        return ""

    def dismiss_modal(self) -> None:
        """Close any visible modal dialog."""
        for sel in [".modal .close", ".modal .btn-close", 'button[data-dismiss="modal"]']:
            if self.is_visible(sel):
                self.click(sel)
                break
