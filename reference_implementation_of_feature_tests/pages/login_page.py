"""Page object for Keycloak OIDC login on the consumer system."""
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Handles authentication via the Keycloak login form."""

    # Selectors for the Keycloak login page
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#kc-login"
    ERROR_MESSAGE = "#input-error"

    def login(self, username: str, password: str) -> None:
        """Fill credentials and submit the Keycloak login form."""
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def is_on_login_page(self) -> bool:
        """Check whether the current page is the Keycloak login form."""
        return self.page.is_visible(self.USERNAME_INPUT)

    def get_login_error(self) -> str:
        """Return any authentication error shown on the login page."""
        if self.page.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE).strip()
        return ""
