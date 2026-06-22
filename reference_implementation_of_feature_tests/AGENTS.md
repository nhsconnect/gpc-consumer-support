# AGENTS.md — Reference Implementation Context

This file provides context for coding agents building step definitions for the GP Connect consumer assurance feature files in `assurance_tests/`. It documents the patterns, guardrails, and durable context from this specific reference implementation.

> **CRITICAL: This folder (`reference_implementation_of_feature_tests/`) is a read-only reference.**
> Do NOT modify any files in this folder. It exists as a worked example for a specific consumer application. When building a new implementation for a different consumer, create your own project folder and use this as a guide.

## Consumer-Specific vs Universal Concepts

This reference implementation was built against one specific consumer application. Many of the page objects, navigation flows, and helper patterns you see here are **specific to that consumer or its class of system** and will not exist in yours. Do not copy them blindly.

**Concepts that are specific to this consumer or its class:**

- `nms_episode_page.py` — NMS (New Medicine Service) is a pharmacy-specific workflow. If the target consumer is not a pharmacy system, there is no NMS screen. You will not need this page object at all. Your patient search entry point will be completely different.
- PDS 24-hour refresh gate — this consumer requires PDS verification to be refreshed within 24 hours before the GP record can be viewed. Other consumers may handle PDS verification differently, automatically, or not expose it as a user-facing step.
- Login flow and session management — entirely application-specific.
- Navigation path from patient search → GP record → clinical area tabs — specific to this consumer's screen structure.

**Concepts that are universal across all GP Connect consumers:**

- The feature files in `assurance_tests/` — every consumer must satisfy the same Gherkin scenarios.
- The GP Connect FHIR API contract — `$gpc.getstructuredrecord` with the same parameters.
- The test assertions specified in the tests — drug names, dosages, allergy details, dates must appear on screen or in the logs produced.
- The evidence model — video capture, highlighting asserted text, artefact naming.

**When building a new implementation:** expect to replace the entire page object layer and most step definition wiring. Your consumer will have its own screens, its own navigation, and potentially concepts that do not exist in this reference at all. Ask the test engineer about the target consumer's UI structure before writing any page objects.

## Scope

- The feature files that must be automated are in:
  - `assurance_tests/SCAL_technical/` (SCAL technical assurance)
  - `assurance_tests/clinical/` (clinical data display assurance)
- This reference implementation covers a subset — primarily the SCAL technical structured record features.
- Keep supporting code and docs aligned to the target feature files.

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

### Do Not Modify the Reference Implementation

- The `reference_implementation_of_feature_tests/` folder is a **read-only reference**. Never edit, delete, or add files in this folder.
- When building a new test implementation for a different consumer, create a separate project folder (e.g. `my_consumer_tests/`) and use the reference as a guide.
- The reference implementation's page objects, step definitions, and helpers are specific to one consumer — they are not a starting template to be forked in-place.

### Ask the Test Engineer — Do Not Guess

- Before writing any page objects or navigation code, **ask the test engineer** about the target consumer application's UI structure, screens, login flow, and patient search mechanism.
- Do not assume the target consumer has the same screens, navigation, or workflows as the reference implementation.
- If you are uncertain about any aspect of the consumer's behaviour — a selector, a navigation step, a clinical area's availability, how PDS works in this system — **stop and ask** rather than guessing.
- Use `playwright-cli` to verify real UI behaviour, but ask the test engineer first to understand what you are looking at.

### Require API Observability — Do Not Work Around It

- A large proportion of SCAL technical tests require access to the **actual GP Connect API requests and responses** exchanged between the consumer backend and the GP provider. These are tagged `@skip_requires_gp_provider_api_access` in the feature files.
- If API observability (proxy logs, structured API call logs, or equivalent) has not been set up, **do not attempt to implement these tests**. Do not try to satisfy API-contract assertions through UI observation alone — it is not possible.
- Ask the test engineer whether API observability is available. If not, flag it as a blocker and focus on the UI-only tests that can proceed without it.
- When API observability is available, the test framework must still **drive the UI** to trigger the API calls (the consumer is the system under test). Never construct or fire FHIR requests directly at the GP Provider — that bypasses the consumer entirely.
- For each API-observed test, log: the raw outbound FHIR request body, the raw inbound FHIR response body, and a timestamped video of the UI, all named against the scenario ID.

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

The consumer supplier has not yet, or does not want to implement the relevant clinical area (referrals, problems, consultations, allergies, immunisations) in their consumer application. Once the screens exist, these tests can be implemented using the same pure UI Playwright approach as current tests — no API-layer access is needed.

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

- To improve agent accuracy, keep `supporting-documentation/` rich and current with implementation-facing evidence. If this is empty or not fleshed out then warn the user driving the AI Agent of this limitation.
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
- SCAL technical assurance feature sources: `../assurance_tests/SCAL_technical/`
- Clinical assurance feature sources: `../assurance_tests/clinical/`
- UI selector and navigation map: `docs/ui-feature-map.md`

## Clinical Assurance Tests — Key Context

The `../assurance_tests/clinical/` folder contains a separate set of feature files focused on **UI display verification** of clinical data. These are fundamentally different from the SCAL technical tests:

- **Purpose**: Verify the consumer UI correctly displays medication/allergy/observation data from the GP record.
- **Assertion target**: Visible on-screen text (drug names, dosages, dates, notes, prescribers) — NOT API request/response conformance.
- **Source**: Derived from the NHS clinical testing team's spreadsheet-based manual test pack (`GP Connect ARS Clinical Test Pack using TPP data v1.8`).
- **Test data**: Primarily the TPP gold patient Louise Job (9692136744) at WEST FARM SURGERY (A86005).
- **Automation approach**: Pure UI — Playwright navigates to the medication/clinical area and asserts the expected data values are visible.
- **No API-layer observation needed**: Unlike `@skip_requires_gp_provider_api_access` scenarios, these tests only need to see what appears on screen.

When implementing step definitions for clinical assurance tests, the `Then` steps should assert visible text on the page matches the expected field values from the data table.

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
