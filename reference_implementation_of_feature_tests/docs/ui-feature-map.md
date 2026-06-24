# UI → Feature Map (Template)

This document records how **your** consumer application UI maps to the GP Connect BDD feature files in `assurance_tests/`. It should drive the step definitions and page-object selectors for each capability area.

> **This is a template.** When building your own test implementation, create a copy of this file in your project and populate it with the real navigation paths, selectors, and API calls for your consumer application. Use `playwright-cli` to discover the actual UI structure before filling this in.

---

## How to Use This Document

This file serves as **persistent memory between AI coding sessions**. When an AI agent (Copilot, Claude, etc.) uses `playwright-cli` to discover your consumer's UI structure, it should record what it learns here so that future sessions don't have to rediscover the same flows, selectors, and quirks from scratch.

### Purpose

- A durable record of **discovered UI navigation paths, selectors, and behaviours** that persists across agent sessions.
- Reduces repeated exploration — the AI reads this file at the start of a session to recall what was previously confirmed.
- Drives the page objects and step definitions by providing verified selector/flow knowledge.

### Source of Truth

**The live application is always the source of truth — not this file.** This document is a cache of observations that will drift over time as the consumer UI changes. When the AI detects that a recorded flow no longer works (selectors missing, navigation changed, new screens added), it should:

1. Use `playwright-cli` to rediscover the current UI state.
2. Update this file with the corrected paths and selectors.
3. Update the corresponding page objects and step definitions.

Treat discrepancies as a signal to re-explore, not as a bug in the application.

### What to Record

1. For each clinical area (medications, allergies, investigations, etc.), document the **navigation path** from login to the screen where assertions are made.
2. Record the **selectors** for each interactive element — confirmed via `playwright-cli`.
3. Map the **BDD scenarios** to the UI steps required to reach and assert the expected state.
4. Note any **API calls** triggered by UI actions, if observable.
5. Record **quirks and gotchas** (loading states, conditional overlays, timing issues) that affect test reliability.

---

## Access Record: Structured

**Feature files:** `access_record_structured.feature`, `access_record_structured_extended.feature`
**Page objects:** *(list your page object classes here)*

### Common Navigation Path

Document the path from login to the structured record clinical area. Every consumer will be different. Example structure:

```text
Login page
  └─ Authenticate (your auth mechanism)
    └─ Home / landing screen
      └─ Patient search (your search mechanism — demographics, NHS number, etc.)
        └─ Select patient from results
          └─ [If applicable] PDS verification / refresh step
            └─ View GP Record / clinical summary
              └─ Select clinical area (medications, allergies, etc.)
```

### PDS Verification Path (if applicable)

Some consumers require PDS verification before the GP record can be viewed. Document the specific flow if your consumer has one:

```text
After selecting a patient:
  └─ [If PDS not verified] Show verification prompt
    └─ Trigger PDS trace
      └─ On success → enable GP record access
  └─ [If PDS stale] Show refresh prompt
    └─ Trigger PDS refresh
      └─ On success → enable GP record access
```

> **Note:** Not all consumers expose PDS verification as a user-facing step. Some handle it automatically in the backend. Document what your consumer actually does.

### Patient Search Path (NHS Number Trace)

If your consumer supports searching by NHS number (required for some GEN scenarios):

```text
Navigate to patient search
  └─ Switch to NHS number search mode (if applicable)
    └─ Enter NHS number + date of birth
      └─ Submit search
        └─ Handle result (patient found / not found / access blocked)
```

### Medications Path

```text
Navigate to patient's GP record
  └─ Open medications area
    └─ [Tab/section for medication type: Acute, Repeat, etc.]
      └─ Assert expected medication data is visible
```

### Allergies Path

```text
Navigate to patient's GP record
  └─ Open allergies area
    └─ Assert expected allergy data is visible (clinical status, category, reactions, etc.)
```

### Investigations Path

```text
Navigate to patient's GP record
  └─ Open investigations area
    └─ Assert investigation items are listed
      └─ Click an investigation to expand details (if applicable)
```

---

### Selectors

Record the actual selectors discovered via `playwright-cli` for your consumer:

| Element | Selector | Notes |
| --- | --- | --- |
| Login username field | *(e.g. `#username`)* | |
| Login password field | *(e.g. `#password`)* | |
| Login submit button | *(e.g. `#login-submit`)* | |
| Patient search input | *(your selector)* | |
| Search submit button | *(your selector)* | |
| Patient result row / button | *(your selector)* | Click to select a patient |
| View GP Record button | *(your selector)* | May be absent or named differently in your consumer |
| PDS verification prompt | *(your selector, if applicable)* | |
| Medications tab/section | *(your selector)* | |
| Allergies tab/section | *(your selector)* | |
| Investigations tab/section | *(your selector)* | |
| Clinical data display area | *(your selector)* | Where structured record content renders |
| Error / warning display | *(your selector)* | |

---

### API Calls Triggered (if observable)

If your test framework can observe the GP Connect API calls (via proxy, logs, or network capture):

| UI Action | Endpoint | Method | Key Params | Expected Response |
| --- | --- | --- | --- | --- |
| Request structured record | *(your consumer's backend endpoint)* | POST | `nhsNumber`, clinical area params | 200 + FHIR Bundle |
| PDS trace | *(your consumer's PDS endpoint, if applicable)* | GET/POST | NHS number, demographics | 200 + patient details |

---

### BDD Scenario → UI Step Mapping

Map each scenario tag to the UI actions required:

| Scenario Tag | Given (setup) | When (action) | Then (assertion) |
| --- | --- | --- | --- |
| `@GPC-STR-TST-MED-02` | Search patient, navigate to GP record | Open repeat medications | Assert medication items visible, highlight top item text |
| `@GPC-STR-TST-MED-07` | Search patient, navigate to GP record | Open acute medications | Assert empty-state guidance message visible |
| `@GPC-STR-TST-GEN-06` | Search patient with stale PDS trace | Attempt to view GP record | Assert access is blocked, refresh prompt shown |
| *(add your scenarios)* | | | |

---

## Notes

- Keep this document updated as your consumer UI changes — selectors drift over time.
- Use `playwright-cli` to verify selectors before each implementation session.
- Record any consumer-specific quirks (e.g. confirmation overlays, loading states, conditional UI elements) that affect test reliability.
- For assertions against visible UI text, always call your highlight helper so evidence videos clearly show what was validated.
- Videos and test artefacts should be saved under `test-results/` with timestamped folder names.
