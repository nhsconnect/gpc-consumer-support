"""Base page object for GP Connect Consumer Support tests.

Wraps a Playwright Page and provides common interaction helpers
used by all capability-specific page objects.
"""
import uuid

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects."""

    UI_READY_OBSERVE_MS = 750
    UI_READY_STABLE_MS = 500

    UI_READY_CHECK = r"""
        ({ observeMs, stableMs }) => {
            const isVisible = element => {
                if (!element || !element.isConnected) {
                    return false;
                }

                const style = window.getComputedStyle(element);
                if (
                    style.display === 'none'
                    || style.visibility === 'hidden'
                    || style.opacity === '0'
                ) {
                    return false;
                }

                const rect = element.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0;
            };

            const spinnerSelectors = [
                '.MuiCircularProgress-root[role="progressbar"]',
                '[role="progressbar"]:not([aria-label="notification timer"])',
            ];

            const visibleSpinners = spinnerSelectors.flatMap(selector => {
                return Array.from(document.querySelectorAll(selector)).filter(isVisible);
            });

            const stateKey = '__copilotUiReadyState';
            const now = Date.now();
            const state = window[stateKey] || {
                startedAt: now,
                noSpinnerSince: null,
            };

            if (visibleSpinners.length === 0) {
                state.noSpinnerSince = state.noSpinnerSince ?? now;
            } else {
                state.noSpinnerSince = null;
            }

            window[stateKey] = state;

            const observedLongEnough = now - state.startedAt >= observeMs;
            const spinnerGoneLongEnough = state.noSpinnerSince !== null && now - state.noSpinnerSince >= stableMs;

            if (observedLongEnough && spinnerGoneLongEnough) {
                delete window[stateKey];
                return true;
            }

            return false;
        }
    """

    JWT_STORAGE_LOOKUP = r"""
        () => {
            const jwtPattern = /^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/;
            const visited = new Set();

            const collectCandidates = value => {
                if (value == null) {
                    return [];
                }

                if (typeof value === 'string') {
                    const trimmed = value.trim();
                    if (!trimmed) {
                        return [];
                    }

                    const direct = trimmed.replace(/^Bearer\s+/i, '');
                    if (jwtPattern.test(direct)) {
                        return [direct];
                    }

                    try {
                        return collectCandidates(JSON.parse(trimmed));
                    } catch {
                        return [];
                    }
                }

                if (typeof value !== 'object') {
                    return [];
                }

                if (visited.has(value)) {
                    return [];
                }
                visited.add(value);

                if (Array.isArray(value)) {
                    return value.flatMap(collectCandidates);
                }

                return Object.values(value).flatMap(collectCandidates);
            };

            const findInStorage = storage => {
                const results = [];
                for (let index = 0; index < storage.length; index += 1) {
                    const key = storage.key(index);
                    results.push(...collectCandidates(storage.getItem(key)));
                }
                return results;
            };

            return [...findInStorage(window.localStorage), ...findInStorage(window.sessionStorage)][0] || null;
        }
    """

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
        self.wait_for_load()


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

    def wait_for_load(self, timeout: int = 15_000) -> None:
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        self.page.wait_for_function(
            self.UI_READY_CHECK,
            arg={
                "observeMs": self.UI_READY_OBSERVE_MS,
                "stableMs": self.UI_READY_STABLE_MS,
            },
            timeout=timeout,
        )

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

    # ------------------------------------------------------------------
    # API helpers
    # ------------------------------------------------------------------

    def get_bearer_token(self) -> str | None:
        token = self.page.evaluate(self.JWT_STORAGE_LOOKUP)
        if not token:
            return None
        return str(token)

    def perform_authenticated_get(
        self,
        path: str,
        params: dict[str, str],
        *,
        include_empty_params: bool = False,
        extra_headers: dict[str, str] | None = None,
    ) -> dict:
        token = self.get_bearer_token()
        headers = {
            "Accept": "application/json, text/plain, */*",
            "x-correlation-id": str(uuid.uuid4()),
        }
        if extra_headers:
            headers.update(extra_headers)
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return self.page.evaluate(
            """async ({ path, params, headers, includeEmptyParams }) => {
                const url = new URL(path, window.location.origin);
                for (const [key, value] of Object.entries(params)) {
                    const hasValue = value !== null && value !== undefined && value !== '';
                    if (hasValue || includeEmptyParams) {
                        url.searchParams.set(key, value);
                    }
                }

                const response = await fetch(url.toString(), {
                    method: 'GET',
                    headers,
                    credentials: 'include',
                });

                const contentType = response.headers.get('content-type') || '';
                let body;
                if (contentType.includes('application/json')) {
                    body = await response.json();
                } else {
                    body = await response.text();
                }

                return {
                    ok: response.ok,
                    status: response.status,
                    statusText: response.statusText,
                    url: response.url,
                    headers: Object.fromEntries(response.headers.entries()),
                    body,
                };
            }""",
            {
                "path": path,
                "params": params,
                "headers": headers,
                "includeEmptyParams": include_empty_params,
            },
        )

    def dismiss_modal(self) -> None:
        """Close any visible modal dialog."""
        for sel in [".modal .close", ".modal .btn-close", 'button[data-dismiss="modal"]']:
            if self.is_visible(sel):
                self.click(sel)
                break
