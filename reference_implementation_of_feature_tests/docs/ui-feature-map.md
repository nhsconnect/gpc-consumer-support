# UI → Feature Map

Use this document to record how the consumer application UI maps to the access record structured
GP Connect BDD feature files.  This should drive the step
definitions and page-object selectors for that capability area.

## Access Record: Structured

**Feature files:** `access_record_structured.feature`, `access_record_structured_extended.feature`  
**Page objects:** `HomePage`, `NmsEpisodePage`, `GpRecordPage`, `StructuredRecordPage` (facade: `AccessRecordStructuredPage`)

### Common navigation path

```text
Home (pharmacy/home)
  └─ [nav link] click the NMS link displayed:

href="/pharmacy/new-medicine-service"
  └─ then click the Start New NMS button
    └─ navigate to pharmacy/nms-episode
      └─ search for the patient using family name, given name, date of birth, and postcode
        └─ click the first patient result button (`#ChoosePatient`)
          └─ if View GP Record (`#view-gp-record`) is disabled, check PDS verification state:
            └─ never verified: show text `The patient's details have not been PDS verified` and link `Verify patient via PDS`
            └─ previously verified but now stale: show link `Refresh patient data via PDS`
            └─ wait for the patient details route to refresh
              └─ click View GP Record (`#view-gp-record`)
                └─ clinical area toggles → Submit
```

### GEN-09 PDS Trace path (registered practice cannot be confirmed)

```text
Home (pharmacy/home)
  └─ click NMS link
    └─ click Start New NMS
      └─ on pharmacy/nms-episode click Add New Patient (`#add-new-patient`)
        └─ click NHS NUMBER SEARCH (`[id='patient-search=NHS NUMBER SEARCH']`)
          └─ enter NHS number + date of birth
            └─ click Search (`#submit`)
              └─ verify access is blocked when registered practice cannot be confirmed (including s-flag cases)
```

### GEN-06 stale PDS trace path (>24 hours old)

```text
Home (pharmacy/home)
  └─ click NMS link
    └─ click Start New NMS
      └─ on pharmacy/nms-episode search for reserved GEN-06 patient by family name `Smith`
        └─ click the first patient result button (`#ChoosePatient`)
          └─ verify View GP Record (`#view-gp-record`) is disabled
            └─ if `Refresh patient data via PDS` is displayed, treat it as the recovery path once the stale-PDS state needs clearing
```

### GEN-17 GP2GP transfer warning path

```text
Home (pharmacy/home)
  └─ click NMS link
    └─ click Start New NMS
      └─ search patient by demographics using family name `Beston` (NHS `9690938096`)
        └─ click the first patient result button (`#ChoosePatient`)
          └─ click View GP Record (`#view-gp-record`)
            └─ assert warning text is visible:
              └─ `Information not available`
              └─ `Patient record transfer from previous GP practice not yet complete; information recorded before`
```

### MED-02 path (valid medications response via UI)

```text
Home (pharmacy/home)
  └─ click NMS link
    └─ click Start New NMS
      └─ search patient by demographics (Skelly/Horace + DOB + postcode)
        └─ click first Choose Patient (`#ChoosePatient`)
          └─ click View GP Record (`#view-gp-record`)
            └─ if demographics confirmation overlay appears, click CONFIRM DETAILS
              └─ open Repeat Medications tab
                └─ assert medication range control is visible
                  └─ assert Repeat item count > 1
                    └─ extract top item medication text dynamically and highlight asserted text
```

### MED-07 path (empty acute medications via UI)

```text
Home (pharmacy/home)
  └─ click NMS link
    └─ click Start New NMS
      └─ search patient by demographics (Skelly/Horace + DOB + postcode)
        └─ click first Choose Patient (`#ChoosePatient`)
          └─ click View GP Record (`#view-gp-record`)
            └─ if demographics confirmation overlay appears, click CONFIRM DETAILS
              └─ open Acute Medications tab
                └─ assert exact two-line no-data guidance message
                  └─ highlight both asserted lines for evidence videos
```

### INV-06 path (supported investigations elements via UI)

```text
Home (pharmacy/home)
  └─ click NMS link
    └─ click Start New NMS
      └─ search patient by demographics (Skelly/Horace + DOB + postcode)
        └─ click first Choose Patient (`#ChoosePatient`)
          └─ click View GP Record (`#view-gp-record`)
            └─ if demographics confirmation overlay appears, click CONFIRM DETAILS
              └─ open Investigations tab
                └─ assert investigations list has more than one item
                  └─ click top investigation item
                    └─ highlight top-item asserted text for evidence videos
```

### Selectors

| Element | Selector | Notes |
| --- | --- | --- |
| Nav link | <!-- fill in --> | |
| Family name input | `#familyName` | **First field** on the form |
| Given name input | `#givenName` | Second field on the form |
| Date of birth input | `#dateOfBirth` | Format: `DD/MM/YYYY` |
| Postcode input | `#postcode` | |
| Search button | `#submit` | Submits demographic search on `pharmacy/nms-episode` |
| Add new patient button | `#add-new-patient` | Entry point for PDS trace NHS-number route |
| NHS number search mode | `[id='patient-search=NHS NUMBER SEARCH']` | Must be selected for GEN-09 |
| Choose patient button | `#ChoosePatient` | Click the first/top result where multiple patients are shown |
| View GP Record button | `#view-gp-record` | Required after selecting a patient to enter record view; may be disabled if PDS trace is stale |
| Verify patient via PDS link | role link with name `Verify patient via PDS` | Displayed for patients that have never been PDS verified |
| Not PDS verified message | text `The patient's details have not been PDS verified` | Companion state text for the never-verified branch |
| Refresh patient data via PDS link | role link with name `Refresh patient data via PDS` | Optional recovery path when the patient trace is older than 24 hours and View GP Record is disabled |
| Confirm details button | role button with name `CONFIRM DETAILS` | Displayed on Patient GP Record demographics confirmation overlay |
| Medications heading | role heading with name `Medications` | Use as GP record anchor after confirmation overlay |
| Acute Medications tab | role button with name `Acute Medications` | Used by MED-07 empty guidance assertion |
| Repeat Medications tab | role button with name `Repeat Medications` | Used by MED-02 valid medications assertion |
| Medication range filter | role button with name `Showing 15 months of medication data` (fallback `#select`) | Expected visible on medication tab content |
| Repeat medication items | role button with name containing `Most Recent Issue Date` | Repeat medication cards summary controls |
| Investigations tab | role button with name `Investigations` | Used by INV-06 supported-investigation UI validation |
| Investigation list rows | `tbody tr` (fallback visible button candidates in investigations content) | Assert item count > 1 for INV-06 |
| Acute empty message line 1 | text `No Issued Acute Medication data is recorded for this patient.` | MED-07 exact assertion line 1 |
| Acute empty message line 2 | text `There may be some unissued medication data available in the 'Not Issued' tab` | MED-07 exact assertion line 2 |
| NHS number input | `#nhsNumber` (fallbacks: `#nhs-number`, `input[name='nhsNumber']`) | Used by GEN-09 PDS trace route |
| Submit / retrieve button | <!-- fill in --> | |
| Medications toggle | <!-- fill in --> | |
| Allergies toggle | <!-- fill in --> | |
| Response / results panel | <!-- fill in --> | |
| Error display | <!-- fill in --> | |

### API calls triggered

| UI action | Endpoint | Method | Key params | Expected response |
| --- | --- | --- | --- | --- |
| Submit structured request | <!-- e.g. /aggregator/structured --> | POST | `nhsNumber`, clinical areas | 200 + FHIR Bundle |
| <!-- next --> | | | | |

### BDD scenario → UI step mapping

| Scenario tag | Given | When | Then |
| --- | --- | --- | --- |
| <!-- fill in --> | | | |

---

## Notes

- All GP Connect routes redirect to `/pharmacy/home` in this tenant unless the capability is explicitly enabled.
- Most patient searches for this workflow should be performed from `pharmacy/nms-episode` using family name, given name, date of birth, and postcode.
- The PDS patient-details call (`/aggregator/pds/patient-details`) requires `birthDate`, `givenName`, `familyName`, `gender`, `postCode` alongside `nhsNumber` to return HTTP 200 — NHS number alone returns 400.
- Patient banner selectors (`.patient-banner *`) are shared across HTML and Access Document pages but may not be present in all capability routes.
- Demographic mismatch: when PDS-returned details differ from locally-held data, the differing fields are highlighted in **red** in the patient demographics section.
- When a patient PDS trace is more than 24 hours old, `View GP Record` can be disabled. Some UI states also show `Refresh patient data via PDS` as the recovery path.
- If a patient has never been PDS verified, the UI can show `Verify patient via PDS` and the text `The patient's details have not been PDS verified` instead of `Refresh patient data via PDS`.
- GEN-06 now uses a dedicated stale-PDS family-name search anchor: `Smith`. Do not use this patient in other tests so the >24h stale trace state remains available for GEN-06.
- The current automated GEN-06 path covers the blocked `>24 hours old` branch using the reserved `Smith` patient; the `<24 hours sent` branch is not exercised by this dedicated stale-PDS flow.
- GEN-09 PDS trace fail scenarios currently use: NHS `9690938533` + DOB `09/09/2020`, and NHS `9690938541` + DOB `28/03/1960`.
- GEN-09 is currently skipped in automation because the supplied NHS numbers are not presently s-marked in PDS, so the blocked sensitive-trace path cannot be exercised with current data.
- GEN-13 through GEN-16 are currently tagged `@skip_requires_gp_provider_api_access` and intentionally skipped until API access is available.
- GEN-17 warning assertions should call the text-highlight helper so evidence videos clearly show the asserted warning content.
- MED-01, MED-03, MED-04 and MED-05 are currently tagged `@skip_requires_gp_provider_api_access` and intentionally skipped pending API access in this environment.
- MED-02 and MED-07 currently run through the UI GP Record medication tabs and store a `medications_ui_mode` context flag in step definitions to bypass API-only response checks.
- MED-02 assertions should dynamically extract top repeat-item medication text for highlighting (no hardcoded medicine names).
- MED-07 assertions should exactly match both acute no-data guidance lines and highlight both lines for evidence videos.
- INV-01, INV-02, INV-03, INV-04, INV-05, INV-07 and INV-09 are currently tagged `@skip_requires_gp_provider_api_access`.
- INV-06 is implemented as UI mode on the Investigations tab and stores an `investigations_ui_mode` context flag to avoid API-only response checks.
- INV-06 assertions should click the top investigation item and highlight a visible top-item text anchor (short title/headline) for evidence videos.
- Videos of UI flows are saved under `test-results/videos-manual/`.
