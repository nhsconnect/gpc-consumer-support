# AGENTS.md — Cegedim Reference Implementation Context

This file stores durable context for coding agents working in this folder.

## Scope

- Primary implementation scope is focused on:
  - `consumer_tests/access_record_structured.feature`
  - `consumer_tests/access_record_structured_extended.feature`
- Keep supporting code and docs aligned to these two features unless requirements change.

## Working Directory

- Main folder: `reference_cegedim__automated_tests_implementation/`
- Typical run location for commands: this folder (contains `pytest.ini`).

## Core Commands

```bash
# Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Run tests
pytest
pytest -m access_record_structured
pytest tests/step_defs/test_access_record_structured.py
pytest tests/step_defs/test_access_record_structured_extended.py
```

## Execution Guardrails

- Verify UI flow and selectors with `playwright-cli` before editing page objects or step definitions.
- Do not guess selectors; confirm behavior in the live UI first.
- Prefer minimal edits and avoid reformatting unrelated code.
- Keep scenario-to-step mapping clear and traceable.
- Create a top-level execution folder for each run under `test-results/` named `test-suite-execution-YYYYMMDD-HHMMSS`.
- Store all artefacts for that run inside its execution folder (for example `report.html`, `results.json`, and `videos-manual/`).
- Name scenario-level artefacts (for example videos) using the scenario test ID plus timestamp (for example `@GPC-STR-TST-GEN-09+YYYYMMDD-HHMMSS`) so evidence is easy to review.
- Each time a new test is added or an existing test is changed, rerun the relevant previously passing tests (or a broader regression subset) before finishing work to catch regressions early.
- Store video evidence for each executed test scenario under the current run folder at `test-results/test-suite-execution-*/videos-manual/` and keep these recordings available for review.

## Test Data Notes

- Primary provider patient anchors currently used:
  - EMIS: 9730147140
  - TPP: 9692136744
  - Medicus: 9693646525
- Dedicated scenario-specific anchors:
  - GEN-06 stale-PDS flow: family-name search `Smith` only. Keep this patient reserved for GEN-06 and do not refresh PDS in other tests.
  - GEN-06 automation currently covers the blocked `>24h` stale-PDS branch with the reserved `Smith` patient.
  - GEN-09 is currently skipped in automation: NHS `9690938533` and `9690938541` are not presently s-marked in PDS, so the blocked sensitive-trace branch cannot be validated until suitable data is restored.
  - PDS verification state branches to account for in future scenarios:
    - Never verified: UI shows `Verify patient via PDS` and message `The patient's details have not been PDS verified`.
    - Previously verified but stale: UI shows `Refresh patient data via PDS`.
- Source references:
  - `tests/conftest.py`
  - `supporting-documentation/1_5_structured_context.csv`

## Files to Keep in Sync

When updating flow, selectors, or assertions, update these together where relevant:

- `pages/access_record_structured_page.py`
- `tests/step_defs/test_access_record_structured.py`
- `tests/step_defs/test_access_record_structured_extended.py`
- `docs/ui-feature-map.md`

## Documentation Pointers

- Repo overview: `../README.md`
- Local implementation guide: `README.md`
- Feature sources: `../consumer_tests/`

## Change Management

- If feature scope expands beyond the two access record structured files, update this file first.
- Record any new durable assumptions here so context survives session resets.
