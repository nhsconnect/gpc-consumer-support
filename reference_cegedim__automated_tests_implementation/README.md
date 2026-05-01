# Reference Implementation — Cegedim Automated Tests

This folder is a **reference implementation** that demonstrates how a supplier can automate the GP Connect consumer assurance BDD tests defined in [`consumer_tests/`](../consumer_tests/).

It is **not** intended to be run as-is by other suppliers and **will not work out of the box** — the `.env` file containing the login credentials for the test system is not committed to the repository. Instead, it serves as a worked example showing one way to wire up the Gherkin feature files with real step definitions, page objects, and test data against a specific consumer application (Cegedim Pharmacy Services).

For durable coding-agent context and guardrails, see [AGENTS.md](AGENTS.md).

## How Suppliers Should Use This

1. **Read the feature files** in `consumer_tests/` — these define the scenarios every consumer must pass.
2. **Use this reference implementation as a guide** to understand how to:
   - Map Gherkin steps to automated actions against your own consumer UI or API.
   - Structure test data fixtures for EMIS, TPP, and Medicus provider systems.
   - Organise page objects and step definitions.
3. **Build your own implementation** targeting your consumer application, using whichever language, framework, and tooling you prefer.
4. **Run the same `consumer_tests/` feature files** from your implementation to produce the assurance evidence required.

## Structure

```
reference_cegedim__automated_tests_implementation/
├── .env                          # Environment credentials (gitignored)
├── conftest.py                   # Playwright auth fixtures, session setup
├── pytest.ini                    # pytest config (points to ../consumer_tests/)
├── requirements.txt              # Python dependencies
├── pages/                        # Page Object Model (Cegedim-specific)
│   ├── base_page.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── nms_episode_page.py
│   ├── gp_record_page.py
│   ├── structured_record_page.py
│   └── access_record_structured_page.py   # Compatibility facade
└── tests/
    ├── conftest.py               # Test patient data (EMIS, TPP, Medicus)
    └── step_defs/                # Step definitions wiring Gherkin → Playwright
        ├── conftest.py
        ├── test_access_record_structured.py
        └── test_access_record_structured_extended.py
```

## Prerequisites

- Python 3.10+
- Node.js (for Playwright browsers)

## Setup

```bash
cd reference_cegedim__automated_tests_implementation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file in this directory with:

```
GP_CONNECT_BASE_URL=https://pharmacyservices.cegedim.cloud/pharmacy/home
GP_CONNECT_USERNAME=<your_username>
GP_CONNECT_PASSWORD=<your_password>
```

## Development Workflow — playwright-cli First

> **For AI agents (Copilot, Claude, etc.)**: When building or modifying any page interactions, navigation flows, or step definitions, **always use `playwright-cli` to explore the UI first** before writing or editing Python code.
>
> Workflow:
> 1. Open a session: `playwright-cli -s=<session-name> open "$BASE_URL"`
> 2. Navigate and interact step-by-step to discover real selectors and page behaviour
> 3. Use `playwright-cli -s=<session-name> show-source` or inspect the generated code after each action
> 4. Translate the confirmed selectors and flow into Python page object methods
>
> Never guess selectors or navigation paths — always verify with playwright-cli first.

### Page Object Pattern (Required)

- Implement page objects per real application screen, not per feature file.
- Keep low-level interactions in screen-specific modules under `pages/`.
- Keep feature-oriented facades (for example `access_record_structured_page.py`) thin and delegation-only to preserve step-definition compatibility.

## Required Delivery Workflow

For all new or changed automated tests in this reference implementation, follow this sequence:

1. Use `playwright-cli` to discover and verify the real UI flow before editing code.
2. Update `docs/ui-feature-map.md` with the confirmed navigation path and selectors.
3. Use requirements and data notes from `supporting-documentation/1_5_structured_context.csv` while implementing steps and assertions.
4. Run the newly developed tests and a regression set of previously passing tests to confirm end-to-end behaviour and catch regressions.

If an MP4 flow recording exists under `supporting-documentation/`, use it as an additional guide to cross-check sequence and UI state transitions.

## Running Tests

```bash
cd reference_cegedim__automated_tests_implementation

# Run all tests
pytest

# Run a specific capability
pytest -m access_record_structured

# Run a single feature file
pytest tests/step_defs/test_access_record_structured.py

# Run with headed browser
pytest --headed
```

## Markers

Tests can be filtered using pytest markers defined in `pytest.ini`:

`access_record_structured`, `access_record_structured_extended`, `medications`, `allergies`, `problems`, `immunisations`, `consultations`, `error_handling`, `warnings`
