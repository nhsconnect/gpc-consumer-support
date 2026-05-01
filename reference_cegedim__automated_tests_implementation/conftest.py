"""Root conftest.py for GP Connect Consumer Support Tests.

Provides session-level fixtures, Playwright browser setup, and
authentication for the Cegedim Pharmacy Services consumer system.
"""
import os
import re
from datetime import datetime

import pytest
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH, override=True)

BASE_URL = os.getenv("BASE_URL", "")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
TEST_RESULTS_ROOT = Path("test-results")
EXECUTION_DIR_PREFIX = "test-suite-execution"
EXECUTION_DIR_ENV = "TEST_SUITE_EXECUTION_DIR"

TEST_ID_PATTERN = re.compile(r"GPC[-_]STR[-_]TST[-_][A-Z0-9]+[-_]\d+(?:[-_]\d+)?", re.IGNORECASE)


def _sanitize_for_filename(value: str) -> str:
    """Return a filesystem-safe label while preserving test-id readability."""
    safe = re.sub(r"[^A-Za-z0-9@+._-]", "-", value.strip())
    safe = re.sub(r"-+", "-", safe).strip("-")
    return safe or "unnamed-test"


def _extract_test_id(node) -> str:
    """Extract the canonical GPC test ID marker from a pytest node."""
    candidates = [
        *[m.name for m in node.iter_markers()],
        *[str(k) for k in node.keywords.keys()],
        node.name,
        node.nodeid,
    ]

    for candidate in candidates:
        match = TEST_ID_PATTERN.search(candidate)
        if match:
            test_id = match.group(0).upper().replace("_", "-")
            return f"@{test_id}"

    return "@UNMAPPED-TEST"


def _build_execution_dir() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    execution_dir = TEST_RESULTS_ROOT / f"{EXECUTION_DIR_PREFIX}-{timestamp}"

    counter = 1
    while execution_dir.exists():
        execution_dir = TEST_RESULTS_ROOT / f"{EXECUTION_DIR_PREFIX}-{timestamp}-{counter}"
        counter += 1

    execution_dir.mkdir(parents=True, exist_ok=True)
    return execution_dir


def pytest_configure(config) -> None:
    """Configure per-run artefact folder paths for pytest plugins and Playwright."""
    execution_dir = _build_execution_dir()
    os.environ[EXECUTION_DIR_ENV] = str(execution_dir)

    # Keep all run artefacts in one folder for easier review.
    video_dir = execution_dir / "videos-manual"
    video_dir.mkdir(parents=True, exist_ok=True)
    os.environ["PLAYWRIGHT_VIDEO_DIR"] = str(video_dir)

    if hasattr(config.option, "htmlpath"):
        config.option.htmlpath = str(execution_dir / "report.html")

    if hasattr(config.option, "json_report_file"):
        config.option.json_report_file = str(execution_dir / "results.json")


def pytest_bdd_apply_tag(tag, function):
    """Map selected Gherkin tags to pytest skip markers with explicit reasons."""
    skip_reasons = {
        "skip_audit_logs_unavailable": (
            "GEN-05 temporarily skipped: audit logs are not accessible in this environment, "
            "so creation/conformance assertions cannot be validated."
        ),
        "skip_sensitive_pds_data_unavailable": (
            "GEN-09 temporarily skipped: NHS 9690938533 and 9690938541 are currently "
            "not s-marked in PDS, so the blocked sensitive-trace path cannot be validated."
        ),
        "skip_api_access_not_exposed": "To be implemented once API access is exposed",
    }

    reason = skip_reasons.get(tag)
    if reason:
        pytest.mark.skip(reason=reason)(function)
        return True

    # Fall back to pytest-bdd's default tag handling.
    return None


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
    video_dir = os.getenv("PLAYWRIGHT_VIDEO_DIR", "").strip()

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
    context_options = {
        "storage_state": storage,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
    }
    if video_dir:
        Path(video_dir).mkdir(parents=True, exist_ok=True)
        context_options["record_video_dir"] = video_dir

    authenticated = browser.new_context(**context_options)
    yield authenticated
    authenticated.close()


@pytest.fixture
def authenticated_page(authenticated_context, request):
    """Provide a fresh page within the authenticated browser context."""
    page = authenticated_context.new_page()
    video = page.video
    yield page

    page.close()

    if not video:
        return

    source_path = Path(video.path())
    if not source_path.exists():
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    test_id = _extract_test_id(request.node)
    target_name = _sanitize_for_filename(f"{test_id}+{timestamp}")
    target_path = source_path.with_name(f"{target_name}{source_path.suffix}")

    counter = 1
    while target_path.exists():
        target_path = source_path.with_name(f"{target_name}-{counter}{source_path.suffix}")
        counter += 1

    source_path.rename(target_path)
