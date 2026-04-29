"""Shared fixtures for step definitions.

Provides page object instances backed by an authenticated Playwright page.
"""
import os

import pytest

from pages.access_record_structured_page import AccessRecordStructuredPage


@pytest.fixture
def access_record_structured_page(authenticated_page):
    """Return an AccessRecordStructuredPage backed by an authenticated browser page."""
    return AccessRecordStructuredPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def gp_connect_context():
    """Mutable dict to share state across Given/When/Then within a scenario."""
    return {}


@pytest.fixture
def api_response():
    """Mutable dict to capture API response details within a scenario."""
    return {}
