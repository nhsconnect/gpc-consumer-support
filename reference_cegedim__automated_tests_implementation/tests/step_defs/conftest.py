"""Shared fixtures for step definitions.

Provides page object instances backed by an authenticated Playwright page.
"""
import os

import pytest

from pages.foundations_page import FoundationsPage
from pages.spine_integration_page import SpineIntegrationPage
from pages.send_document_page import SendDocumentPage
from pages.access_record_html_page import AccessRecordHtmlPage
from pages.access_record_structured_page import AccessRecordStructuredPage
from pages.access_document_page import AccessDocumentPage


@pytest.fixture
def foundations_page(authenticated_page):
    """Return a FoundationsPage backed by an authenticated browser page."""
    return FoundationsPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def spine_page(authenticated_page):
    """Return a SpineIntegrationPage backed by an authenticated browser page."""
    return SpineIntegrationPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def send_document_page(authenticated_page):
    """Return a SendDocumentPage backed by an authenticated browser page."""
    return SendDocumentPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def access_record_html_page(authenticated_page):
    """Return an AccessRecordHtmlPage backed by an authenticated browser page."""
    return AccessRecordHtmlPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def access_record_structured_page(authenticated_page):
    """Return an AccessRecordStructuredPage backed by an authenticated browser page."""
    return AccessRecordStructuredPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def access_document_page(authenticated_page):
    """Return an AccessDocumentPage backed by an authenticated browser page."""
    return AccessDocumentPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def gp_connect_context():
    """Mutable dict to share state across Given/When/Then within a scenario."""
    return {}


@pytest.fixture
def api_response():
    """Mutable dict to capture API response details within a scenario."""
    return {}
