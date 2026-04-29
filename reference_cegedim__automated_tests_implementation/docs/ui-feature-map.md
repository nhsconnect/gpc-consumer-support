# UI → Feature Map

Use this document to record how the Cegedim Pharmacy Services UI maps to the access record structured
GP Connect BDD feature files.  This should drive the step
definitions and page-object selectors for that capability area.

## Access Record: Structured

**Feature files:** `access_record_structured.feature`, `access_record_structured_extended.feature`  
**Page object:** `AccessRecordStructuredPage`

### Navigation path

```
Home (pharmacy/home)
  └─ [nav link] click the NMS link displayed:

href="/pharmacy/new-medicine-service"
        └─ then click the Start New NMS button and do a patient search → clinical area toggles → Submit
```

### Selectors

| Element | Selector | Notes |
|---|---|---|
| Nav link | <!-- fill in --> | |
| NHS number input | <!-- fill in --> | |
| Submit / retrieve button | <!-- fill in --> | |
| Medications toggle | <!-- fill in --> | |
| Allergies toggle | <!-- fill in --> | |
| Response / results panel | <!-- fill in --> | |
| Error display | <!-- fill in --> | |

### API calls triggered

| UI action | Endpoint | Method | Key params | Expected response |
|---|---|---|---|---|
| Submit structured request | <!-- e.g. /aggregator/structured --> | POST | `nhsNumber`, clinical areas | 200 + FHIR Bundle |
| <!-- next --> | | | | |

### BDD scenario → UI step mapping

| Scenario tag | Given | When | Then |
|---|---|---|---|
| <!-- fill in --> | | | |

---

## Notes

- All GP Connect routes redirect to `/pharmacy/home` in this tenant unless the capability is explicitly enabled.
- The PDS patient-details call (`/aggregator/pds/patient-details`) requires `birthDate`, `givenName`, `familyName`, `gender`, `postCode` alongside `nhsNumber` to return HTTP 200 — NHS number alone returns 400.
- Patient banner selectors (`.patient-banner *`) are shared across HTML and Access Document pages but may not be present in all capability routes.
- Videos of UI flows are saved under `test-results/videos-manual/`.
