# Reference Implementation — Automated Tests

This folder is a **reference implementation** that demonstrates how a supplier can automate the GP Connect consumer assurance BDD tests defined in [`assurance_tests/SCAL_technical/`](../assurance_tests/SCAL_technical/) and [`assurance_tests/clinical/`](../assurance_tests/clinical/).

It is **not** intended to be run as-is by other suppliers and **will not work out of the box** — the `.env` file containing the login credentials for the test system is not committed to the repository. Instead, it serves as a worked example showing one way to wire up the Gherkin feature files with real step definitions, page objects, and test data against a specific consumer application.

For durable coding-agent context and guardrails, see [AGENTS.md](AGENTS.md).

## How Suppliers Should Use This

1. **Read the feature files** in `assurance_tests/SCAL_technical/` and `assurance_tests/clinical/` — these define the scenarios every consumer must pass.
2. **Use this reference implementation as a guide** to understand how to:
   - Map Gherkin steps to automated actions against your own consumer UI or API.
   - Structure test data fixtures for EMIS, TPP, and Medicus provider systems.
   - Organise page objects and step definitions.
3. **Build your own implementation** targeting your consumer application — either:
   - Write it manually using whichever language, framework, and tooling you prefer, or
   - Point an AI coding agent (e.g. GitHub Copilot, Claude) at the [AGENTS.md](AGENTS.md) file in your own test environment and let it build the implementation for you using playwright-cli.
4. **Run the same `assurance_tests/SCAL_technical/` and `assurance_tests/clinical/` feature files** from your implementation to produce the assurance evidence required.

## Prerequisites — API Request/Response Observability

A significant proportion of the SCAL technical assurance tests (tagged `@skip_requires_gp_provider_api_access` in this reference) require the test framework to **observe the actual GP Connect API requests and responses** exchanged between the consumer backend and the GP provider system.

These tests cannot be satisfied by UI observation alone — they assert that:

- The consumer sends a correctly formed FHIR `$gpc.getstructuredrecord` request (correct NHS number, correct clinical area parameters, correct part-parameter values).
- The GP provider returns a conformant FHIR Bundle response.
- The consumer correctly processes and displays that response.

**Before starting automation of these tests, the test engineer must set up a mechanism to capture server-side API traffic.** Options include:

- A network proxy between the consumer backend and the GP Provider Test system.
- Structured API call logs exposed by the consumer application in its test environment.
- Any other mechanism that provides the raw outbound request and inbound response per test scenario.

Without this observability, only the UI-only subset of tests can be automated. The test framework should still drive the UI to trigger the API calls — it must not construct or fire its own requests at the GP Provider directly.

## Consumer-Specific Concepts

This reference implementation was built against a specific consumer application. Some of the patterns and page objects you see here are **specific to that application or its class of consumer** and will not apply to every GP Connect consumer.

Examples of concepts that vary:

| Concept | Why it varies |
|---------|---------------|
| **NMS episode page** (`nms_episode_page.py`) | NMS (New Medicine Service) is a pharmacy workflow. If your consumer is not a pharmacy system, you will not have an NMS screen at all. Your patient search flow may be completely different. |
| **PDS refresh before viewing GP record** | This consumer requires PDS verification to be refreshed every 24 hours before the GP record can be viewed. Other consumers may handle PDS differently, or may not expose this step to the user at all. |
| **Login flow** | The login page, authentication mechanism, and session handling are entirely application-specific. |
| **Navigation to clinical areas** | The route from patient search → GP record → medications/allergies tabs is specific to this consumer's UI structure. Your application will have its own navigation. |

Conversely, some concepts are **universal across all GP Connect consumers**:

- The feature files in `assurance_tests/` — every consumer must satisfy the same scenarios.
- The GP Connect FHIR API contract — every consumer sends the same `$gpc.getstructuredrecord` requests.

When building your own implementation, **expect to replace the entire page object layer** and much of the step definition wiring. The feature files and the general testing approach (drive the UI, assert visible data, capture evidence) are what you should carry across.

## Structure

```text
reference_implementation_of_feature_tests/
├── .env                          # Environment credentials (gitignored)
├── conftest.py                   # Playwright auth fixtures, session setup
├── pytest.ini                    # pytest config (points to ../assurance_tests/SCAL_technical/)
├── requirements.txt              # Python dependencies
├── pages/                        # Page Object Model (application-specific)
│   ├── base_page.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── nms_episode_page.py
│   ├── gp_record_page.py
│   ├── structured_record_page.py
│   └── ...
└── tests/
    ├── conftest.py               # Test patient data (EMIS, TPP, Medicus)
    └── step_defs/                # Step definitions wiring Gherkin → Playwright
        ├── conftest.py
        ├── access_record_screens.py  # Screen composition helpers
        ├── test_access_record_structured.py
        └── test_access_record_structured_extended.py
```

## Prerequisites

- Python 3.10+
- Node.js (for Playwright browsers)

## Setup

```bash
cd reference_implementation_of_feature_tests
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file in this directory with:

```text
BASE_URL=<url_of_application_under_test>
USERNAME=<your_username>
PASSWORD=<your_password>
```

## Development Workflow — playwright-cli First

> **For AI agents (Copilot, Claude, etc.)**: When building or modifying any page interactions, navigation flows, or step definitions, **always use `playwright-cli` to explore the UI first** before writing or editing Python code.
>
> Workflow:
>
> 1. Open a session: `playwright-cli -s=<session-name> open "$BASE_URL"`
> 2. Navigate and interact step-by-step to discover real selectors and page behaviour
> 3. Use `playwright-cli -s=<session-name> show-source` or inspect the generated code after each action
> 4. Translate the confirmed selectors and flow into Python page object methods
>
> Never guess selectors or navigation paths — always verify with playwright-cli first.

### Page Object Pattern (Required)

- Implement page objects per real application screen, not per feature file.
- Keep low-level interactions in screen-specific modules under `pages/`.
- Keep scenario-level composition in test-layer helpers (for example `tests/step_defs/access_record_screens.py`) instead of adding feature-named page objects in `pages/`.

## Required Delivery Workflow

For all new or changed automated tests in this reference implementation, follow this sequence:

1. Use `playwright-cli` to discover and verify the real UI flow before editing code.
2. Update `docs/ui-feature-map.md` with the confirmed navigation path and selectors.
3. Use requirements and data notes from `supporting-documentation/` (including `1_5_structured_context.csv`) while implementing steps and assertions.
4. Where available, include and use the original onboarding evidence submitted for NHS Solutions Assurance (for example request/response samples, mapping notes, and flow recordings) in `supporting-documentation/` to improve implementation accuracy.
5. Run the newly developed tests and a regression set of previously passing tests to confirm end-to-end behaviour and catch regressions.

If an MP4 flow recording exists under `supporting-documentation/`, use it as an additional guide to cross-check sequence and UI state transitions.

## Test Coverage — Current Limitations and Future Scope

### What is currently implemented

All tests that run today are **pure UI automation**: Playwright drives the consumer browser application, searches for patients by demographics, navigates to clinical areas, and asserts what is visible on screen. The GP Connect API calls happen inside the consumer's backend and the test layer never observes them directly.

### Skip tags and what they mean

The feature files use three skip tags to mark tests that cannot yet run:

| Tag | Reason |
|-----|---------|
| `@skip_requires_gp_provider_api_access` | The test requires direct access to the GP Connect API request or response, which is not exposed by this consumer application in its current configuration. See below. |
| `@skip_supplier_not_implemented_out_of_scope` | The clinical area (for example referrals, problems, consultations) has not yet been implemented in the consumer UI, so there are no screens or flows to automate. |
| `@skip_sensitive_pds_data_unavailable` | The required test patient (s-flagged on PDS) is not currently available in the test environment. |

### What `@skip_requires_gp_provider_api_access` tests actually require

Scenarios tagged `@skip_requires_gp_provider_api_access` exist to assure that the consumer constructs a **valid GP Connect API request** and correctly **processes the API response**. These include tests such as MED-01, MED-03, MED-05, INV-01–04, GEN-11–16, and all search-conformance tests.

They cannot be satisfied by UI observation alone because the assertions are about the API contract:

- The FHIR `$gpc.getstructuredrecord` request must contain the correct parameters (correct NHS number, correct clinical area parameters, correct part-parameter values, absence of parameters where required).
- The FHIR Bundle response must be received and must conform to the GP Connect specification.
- The consumer must correctly render or process the response — and the UI must reflect it.

The GP Connect API calls are made **server-side** by the consumer backend — the browser never sends them directly. This means browser-level interception (`page.route()`) cannot capture them. The correct approach is:

1. **Drive the UI** — Playwright triggers the clinical area request through the normal user flow, exactly as today.
2. **Capture server-side traffic** — a network proxy (for example mitmproxy or Charles Proxy) sits between the consumer backend and the GP Provider Test system, or the consumer supplier exposes structured API call logs from their test environment. Either way, the raw outbound FHIR request and inbound FHIR Bundle response are captured against each test run.
3. **Assert the captured request** — validate the outbound request contains the correct parameters (NHS number, correct clinical area parameter, correct part-parameter values, absence of parameters where required).
4. **Assert the captured response** — validate the returned FHIR Bundle conforms to the GP Connect specification (resource types, required fields, cardinalities, clinical area content).
5. **Assert the UI** — validate the consumer application screen correctly represents what was in that FHIR Bundle, confirming it has processed the response successfully.

At all points, the raw request body, the raw response body, and a timestamped video of the UI should be logged against the scenario ID for review.

This approach keeps the consumer application as the system under test throughout — the test framework drives it via the UI and observes what it actually sends and receives, rather than constructing requests independently. The prerequisite is an agreed mechanism with the consumer supplier and the NHS environment team to expose server-side GP Connect traffic for test observation.

### What `@skip_supplier_not_implemented_out_of_scope` tests require

These tests will become automatable using the same **pure UI approach** as current tests once the consumer supplier implements those clinical area screens. No API-layer access is needed — once referrals, problems, consultations, allergies, and immunisations appear in the UI, the step definitions can be built following the same Playwright page-object pattern used today.

---

## Running Tests

```bash
cd reference_implementation_of_feature_tests

# Run all tests
pytest

# Run a specific capability
pytest -m access_record_structured

# Run a single feature file
pytest ../assurance_tests/SCAL_technical/access_record_structured.feature

# Run with headed browser
pytest --headed
```

### Running a single test by tag i.e. the GPC ID

Use `-k` with the GPC test ID as a keyword filter. The `-k` flag does substring matching against the test name and markers, so the hyphenated GPC IDs work without escaping:

```bash
# Run a single scenario by its GPC ID tag
pytest -k "GPC-STR-TST-SRC01-02"

# Combine with headed browser for debugging
pytest -k "GPC-STR-TST-SRC01-02" --headed
```

## Markers

Tests can be filtered using pytest markers defined in `pytest.ini`:

`access_record_structured`, `access_record_structured_extended`, `medications`, `allergies`, `problems`, `immunisations`, `consultations`, `error_handling`, `warnings`
