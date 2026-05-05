# AGENTS.md — Cegedim Reference Implementation Context

This file acts as a guide to coding agents for how to build step definitions for the feature files stored at the top level consumer_tests directory, it also stores durable context for coding agents working in this folder.

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

### Mandatory Visual Evidence Rule

- For any assertion against visible UI text, always call the highlight helper on the exact asserted text so evidence videos clearly show what was validated.
- Apply this to both positive content assertions and empty-state/error-message assertions.
- Do not finish implementation until highlighted assertion evidence is present in the executed scenario video.
- Verify UI flow and selectors with `playwright-cli` before editing page objects or step definitions.
- Do not guess selectors; confirm behavior in the live UI first.
- Prefer minimal edits and avoid reformatting unrelated code.
- Keep scenario-to-step mapping clear and traceable.
- Model page objects by real application screens, not by feature file. Use dedicated classes for pages such as home, demographics search, patient search results, and GP record views.
- Keep UI interaction logic in screen-specific page object classes. Step-definition composition helpers belong in `tests/step_defs/`, not `pages/`.
- Create a top-level execution folder for each run under `test-results/` named `test-suite-execution-YYYYMMDD-HHMMSS`.
- Store all artefacts for that run inside its execution folder (for example `report.html`, `results.json`, and `videos-manual/`).
- Name scenario-level artefacts (for example videos) using the scenario test ID plus timestamp (for example `@GPC-STR-TST-GEN-09+YYYYMMDD-HHMMSS`) so evidence is easy to review.
- Each time a new test is added or an existing test is changed, rerun the relevant previously passing tests (or a broader regression subset) before finishing work to catch regressions early.
- Store video evidence for each executed test scenario under the current run folder at `test-results/test-suite-execution-*/videos-manual/` and keep these recordings available for review.
- For assertions that validate visible UI text, use the page highlight helper so the asserted text is visibly emphasised in the recorded video evidence (double-click + temporary highlight).
- For INV-06 UI validation, click the top investigation item and highlight a visible top-item text anchor rather than trying to match a full multi-line row payload.
- Do not use broad exception swallowing (for example `try: ... except Exception: pass`) to make tests pass. If UI state can vary, assert explicit accepted alternatives and fail with a clear reason when none are present.

## Test Data Notes

- Primary provider patient anchors currently used:
  - EMIS: 9730147140
  - TPP: 9692136744
  - Medicus: 9693646525
- Dedicated scenario-specific anchors:
  - GEN-06 stale-PDS flow: family-name search `Smith` only. Keep this patient reserved for GEN-06 and do not refresh PDS in other tests.
  - GEN-06 automation currently covers the blocked `>24h` stale-PDS branch with the reserved `Smith` patient.
  - GEN-09 is currently skipped in automation: NHS `9690938533` and `9690938541` are not presently s-marked in PDS, so the blocked sensitive-trace branch cannot be validated until suitable data is restored.
  - GEN-13 to GEN-16 are currently tagged `@skip_api_access_not_exposed` and skipped with reason `To be implemented once API access is exposed`.
  - Investigations in extended structured are currently split:
    - INV-01, INV-02, INV-03, INV-04, INV-05, INV-07 and INV-09 are tagged `@skip_api_access_not_exposed`.
    - INV-06 is implemented through Patient GP Record UI (Investigations tab), not API response parsing.
  - GEN-17 (GP2GP transfer warning) uses NHS `9690938096` by demographics family-name search `Beston`, then `#ChoosePatient`, then `#view-gp-record` before asserting warning text.
  - PDS verification state branches to account for in future scenarios:
    - Never verified: UI shows `Verify patient via PDS` and message `The patient's details have not been PDS verified`.
    - Previously verified but stale: UI shows `Refresh patient data via PDS`.
- Source references:
  - `tests/conftest.py`
  - `supporting-documentation/1_5_structured_context.csv`

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
