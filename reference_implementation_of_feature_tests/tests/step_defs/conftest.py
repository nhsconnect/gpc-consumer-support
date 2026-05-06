"""Shared fixtures for step definitions.

Provides page object instances backed by an authenticated Playwright page.
"""
import os

import pytest

from pages.gp_record_page import GpRecordPage
from pages.home_page import HomePage
from pages.nms_episode_page import NmsEpisodePage
from pages.structured_record_page import StructuredRecordPage
from tests.step_defs.access_record_screens import AccessRecordScreens


@pytest.fixture
def home_page(authenticated_page):
    """Return HomePage backed by an authenticated browser page."""
    return HomePage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def nms_episode_page(authenticated_page):
    """Return NmsEpisodePage backed by an authenticated browser page."""
    return NmsEpisodePage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def gp_record_page(authenticated_page):
    """Return GpRecordPage backed by an authenticated browser page."""
    return GpRecordPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def structured_record_page(authenticated_page):
    """Return StructuredRecordPage backed by an authenticated browser page."""
    return StructuredRecordPage(authenticated_page, os.getenv("BASE_URL", ""))


@pytest.fixture
def access_record_structured_page(
    home_page,
    nms_episode_page,
    gp_record_page,
    structured_record_page,
):
    """Compatibility fixture for existing steps, composed from screen-level pages."""
    return AccessRecordScreens(
        home_page=home_page,
        nms_episode_page=nms_episode_page,
        gp_record_page=gp_record_page,
        structured_record_page=structured_record_page,
    )


@pytest.fixture
def gp_connect_context():
    """Mutable dict to share state across Given/When/Then within a scenario."""
    return {}


@pytest.fixture
def api_response():
    """Mutable dict to capture API response details within a scenario."""
    return {}
