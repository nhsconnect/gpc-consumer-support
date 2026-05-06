# AGENTS.md — Reference Implementation Context

This file guides coding agents on building step definitions for the feature files in the top-level `consumer_tests` directory and stores durable context for agents working in this folder.

## Scope

- Primary implementation scope is focused on:
  - `consumer_tests/access_record_structured.feature`
  - `consumer_tests/access_record_structured_extended.feature`
- Keep supporting code and docs aligned to these two features unless requirements change.

## Working Directory

- Main folder: `reference_implementation_of_feature_tests/`
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

### Mandatory Visual Evidence Rule

- Verify UI flow and selectors with `playwright-cli` before editing page objects or step definitions. Do not guess selectors.
- For every assertion against visible UI text, highlight the exact asserted text (including positive assertions and empty-state/error assertions) so recorded evidence shows what was validated.
- Do not finish implementation until highlighted assertion evidence is present in the executed scenario video.
- Keep scenario-to-step mapping clear and traceable.
- Prefer minimal edits and avoid reformatting unrelated code.
- Model page objects by real application screens, not by feature file. Keep UI interaction logic in screen-specific page object classes; keep scenario composition helpers in `tests/step_defs/`, not `pages/`.
- For each test run, create `test-results/test-suite-execution-YYYYMMDD-HHMMSS` and store all artefacts for that run inside it (for example `report.html`, `results.json`, `videos-manual/`).
- Name scenario-level artefacts using `@<TEST-ID>+YYYYMMDD-HHMMSS` so evidence is easy to review.
- Rerun relevant previously passing tests (or a broader regression subset) after any new or changed test before finishing work.
- For INV-06 UI validation, click the top investigation item and highlight a visible top-item text anchor rather than trying to match a full multi-line row payload.
- Do not use broad exception swallowing (for example `try: ... except Exception: pass`) to make tests pass. If UI state can vary, assert explicit accepted alternatives and fail with a clear reason when none are present.

## Test Data Notes

- Primary provider patient anchors currently used:
  - EMIS: 9730147140
  - TPP: 9692136744
  - Medicus: 9693646525
- Dedicated scenario-specific anchors:
  - GEN-06 stale-PDS flow: family-name search `Smith` only. Keep this patient reserved for GEN-06, do not refresh PDS in other tests, and use it for the blocked `>24h` branch.
  - GEN-09 is currently skipped in automation: NHS `9690938533` and `9690938541` are not presently s-marked in PDS, so the blocked sensitive-trace branch cannot be validated until suitable data is restored.
  - GEN-13 to GEN-16 are currently tagged `@skip_requires_gp_provider_api_access` and skipped with reason `To be implemented once API access is exposed`.
  - Investigations in extended structured are currently split:
    - INV-01, INV-02, INV-03, INV-04, INV-05, INV-07 and INV-09 are tagged `@skip_requires_gp_provider_api_access`.
    - INV-06 is implemented through Patient GP Record UI (Investigations tab), not API response parsing.

## Skip Tag Meanings

Three skip tags are used across the feature files. Understand the distinction before attempting to unskip any scenario.

### `@skip_requires_gp_provider_api_access`

These scenarios cannot be satisfied by UI observation alone. The assertions are about the GP Connect API contract — the request the consumer sends, the response it receives, and that it correctly processes that response.

The GP Connect API calls are made **server-side** by the consumer backend (the consumer holds the mTLS certificates and ASID required to call the GP Provider). Browser-level interception (`page.route()`) cannot see these calls. The test framework must not construct or fire its own requests at the GP Provider — that would bypass the consumer entirely.

The correct approach when these tests are unskipped:

1. **Drive the UI** — Playwright triggers the clinical area request through the normal user flow, exactly as current tests do.
2. **Capture server-side traffic** — a network proxy (for example mitmproxy) sits between the consumer backend and the GP Provider Test system, or the consumer supplier exposes structured API call logs from their test environment. The raw outbound FHIR request and inbound FHIR Bundle response are captured per test run.
3. **Assert the captured request** — validate the outbound request contains the correct FHIR parameters (NHS number, correct clinical area parameter, correct part-parameter values, absence of parameters where required).
4. **Assert the captured response** — validate the FHIR Bundle conforms to the GP Connect v1.5 specification (resource types, required fields, cardinalities, clinical area content).
5. **Assert the UI** — validate the consumer application screen correctly represents what was in that FHIR Bundle, confirming it has processed the response successfully.

At every stage, log: the raw outbound FHIR request body, the raw inbound FHIR response body, and a timestamped video of the UI, all named against the scenario ID.

Prerequisite before any of these can be unskipped: an agreed mechanism with the consumer supplier and the NHS environment team to expose server-side GP Connect traffic for test observation.

### `@skip_supplier_not_implemented_out_of_scope`

The consumer supplier has not yet implemented the relevant clinical area (referrals, problems, consultations, allergies, immunisations) in their UI. Once the screens exist, these tests can be implemented using the same pure UI Playwright approach as current tests — no API-layer access is needed.

### `@skip_sensitive_pds_data_unavailable`

The required test patient (s-flagged on PDS) is not currently available in the test environment. Do not attempt to implement GEN-09 until a suitable patient is confirmed available.
  - GEN-17 (GP2GP transfer warning) uses NHS `9690938096` by demographics family-name search `Beston`, then `#ChoosePatient`, then `#view-gp-record` before asserting warning text.
  - PDS verification state branches to account for in future scenarios:
    - Never verified: UI shows `Verify patient via PDS` and message `The patient's details have not been PDS verified`.
    - Previously verified but stale: UI shows `Refresh patient data via PDS`.
- Source references:
  - `tests/conftest.py`
  - `supporting-documentation/1_5_structured_context.csv`

### Evidence-First Context (Agent Accuracy)

- To improve agent accuracy, keep `supporting-documentation/` rich and current with implementation-facing evidence.
- Prefer the original onboarding evidence set submitted for NHS Solutions Assurance (where available), including requirement notes, sample requests/responses, flow recordings, and scenario mappings.
- When evidence and current UI behavior differ, treat the live UI as source of truth for selectors/flow and record the discrepancy in `docs/ui-feature-map.md`.

## Files to Keep in Sync

When updating flow, selectors, or assertions, update these together where relevant:

- `pages/home_page.py`
- `pages/nms_episode_page.py`
- `pages/gp_record_page.py`
- `pages/structured_record_page.py`
- `tests/step_defs/access_record_screens.py` (step-composition helper)
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

## Shared GEN ID Mapping (Structured vs Extended)

The same GEN IDs appear in both Access Record Structured feature files because they represent shared
assurance requirements reused across two capability packs. Use this map when tracing overlap.

1. `@GPC-STR-TST-GEN-06`
  Structured file: tags `@general @pds`; scenario title includes "Access Control and Audit - PDS trace timeliness".
  Extended file: tags `@general`; scenario title "PDS trace timeliness".
  Difference: same requirement intent (PDS trace age gate), different tag granularity and shorter title in extended file.
2. `@GPC-STR-TST-GEN-07`
  Structured file: tags `@patient_demographics`; scenario title includes "Patient Demographics - primary".
  Extended file: tags `@general`; scenario title "Patient demographics primary".
  Difference: same demographics assurance intent, different category tags.
3. `@GPC-STR-TST-GEN-08`
  Structured file: tags `@patient_demographics @pds`; scenario title includes "PDS trace registered practice".
  Extended file: tags `@general`; scenario title "PDS trace registered practice".
  Difference: same registered-practice rule, richer tagging in structured file.
4. `@GPC-STR-TST-GEN-09`
  Structured file: tags `@patient_demographics @pds`; scenario title includes "PDS trace sensitive patient".
  Extended file: tags `@general`; scenario title "PDS trace sensitive".
  Difference: same sensitive/not-on-PDS blocking intent, tags simplified in extended file.

Interpretation note:

- Treat the GEN ID as the shared requirement identifier.
- Treat each feature file as a different capability-pack context where that requirement is re-stated.

Implementation guidance for later phases:

- Heavy reuse is expected when implementing overlapping GEN scenarios in `access_record_structured.feature` after `access_record_structured_extended.feature`.
- Prioritise reuse of page-object helpers and shared assertion utilities (for example: navigation, patient search, PDS gating, blocked/success state checks).
- Keep scenario-specific step files thin; avoid duplicating low-level UI interaction logic in each step definition module.
- Expect differences mainly in tag classification, scenario wording, and capability-specific request setup (for example meds/allergies-focused toggles in non-extended flows).
- When implementing a duplicated GEN ID in the second file, map it to existing helpers first, then add only minimal wrapper logic needed for the file-specific context.
