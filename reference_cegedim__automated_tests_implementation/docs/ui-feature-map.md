# UI → Feature Map

Use this document to record how the Cegedim Pharmacy Services UI maps to the access record structured
GP Connect BDD feature files.  This should drive the step
definitions and page-object selectors for that capability area.

## Access Record: Structured

**Feature files:** `access_record_structured.feature`, `access_record_structured_extended.feature`  
**Page object:** `AccessRecordStructuredPage`

### Navigation path

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
- Videos of UI flows are saved under `test-results/videos-manual/`.
