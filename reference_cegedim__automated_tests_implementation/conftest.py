"""Root conftest.py for GP Connect Consumer Support Tests.

Provides session-level fixtures, Playwright browser setup, and
authentication for the Cegedim Pharmacy Services consumer system.
"""
import os

import pytest
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH, override=False)

BASE_URL = os.getenv("BASE_URL", "")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")


# HTML Report Customization
def pytest_html_report_title(report) -> None:
    report.title = "GP Connect Consumer Test Automation Report"


@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the consumer system under test."""
    return BASE_URL


@pytest.fixture(scope="session")
def credentials():
    """Return login credentials for the consumer system."""
    return {"username": USERNAME, "password": PASSWORD}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default Playwright browser context settings."""
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def authenticated_context(browser, base_url, credentials):
    """Create a browser context that is already authenticated.

    Performs the Keycloak OIDC login once per session and stores the
    auth state so all tests reuse the same session cookie.
    """
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    # Navigate to the app – Keycloak will redirect to login
    page.goto(base_url, wait_until="networkidle")

    # Fill the Keycloak login form
    page.fill("#username", credentials["username"])
    page.fill("#password", credentials["password"])
    page.click("#kc-login")

    # Wait for redirect back to the consumer app
    page.wait_for_url(f"**/{base_url.split('/')[-1]}**", timeout=30_000)
    page.wait_for_load_state("networkidle")

    # Store the auth state for reuse
    storage = context.storage_state()
    page.close()
    context.close()

    # Return a new context pre-loaded with the auth cookies
    authenticated = browser.new_context(
        storage_state=storage,
        ignore_https_errors=True,
        viewport={"width": 1920, "height": 1080},
    )
    yield authenticated
    authenticated.close()


@pytest.fixture
def authenticated_page(authenticated_context):
    """Provide a fresh page within the authenticated browser context."""
    page = authenticated_context.new_page()
    yield page
    page.close()
