# Clinical Assurance Tests

This folder contains **clinical assurance BDD feature files** that verify GP Connect consumer applications correctly **display** clinical data retrieved from GP provider systems.

## Purpose

These tests are **UI display verification** — they validate that medication, observation, and investigation data from the GP record appears correctly on screen in the consumer application. They are not API conformance tests.

The focus is:

- Correct drug names, dosages, quantities, and dates are shown
- Notes (prescriber notes, patient notes) are displayed without truncation
- Special characters are rendered correctly
- Long text values are not truncated beyond the GP system's own limits
- Private/confidential items are excluded with an appropriate warning
- Data that cannot be displayed does not cause internal server errors

## Source

These tests are derived from two sources:

| Feature | Source |
|---------|--------|
| Medications | **GP Connect ARS Clinical Test Pack** (spreadsheet): `GP Connect ARS Clinical Test Pack using TPP data v1.8 1.xlsx` |
| Allergies | **Confluence — Allergy Test Cases**: [Allergy - Test cases](https://nhsd-confluence.digital.nhs.uk/spaces/DIM/pages/1373783539/Allergy+-+Test+cases) (NHS internal; exported page used as source) |

The spreadsheet contains manually-executed test evidence for medications; the Confluence page defines the allergy test cases including patient scenarios, expected field values, and edge cases. The feature files here express both sets of test cases in Gherkin so they can be automated.

Note: Neither source file is in source control — test data originates from GP provider systems but the feature files are supplier-agnostic.

## Test Data

| Patient | NHS Number | Purpose |
|---------|------------|---------|
| Louise Job | 9692136744 | Gold patient — Medications, Uncategorised, Investigations, Allergies |
| Gorsedd Gavin | 9437702055 | Additional tests (Update Record data) |
| Oliver Greenford | 5990275439 | Consent refused scenario |
| Quanah Hitchcox | 5459007634 | ListWarnings scenario |
| Derryl Hitchcott | 9465693839 | Investigations |

GP Practice: WEST FARM SURGERY (A86005)

## Feature Files

| Feature file | Scope |
|---|---|
| `access_record_structured_medications.feature` | Medications — Acute, Repeat, Prescribed Elsewhere, Discontinued + related Uncategorised/Investigations |
| `access_record_structured_allergies.feature` | Allergies — Active, Resolved, Adverse Reactions, Problems, Intolerances, Negation Records |

> **TODO:** Other areas of Access Record Structured (e.g. Immunisations, Consultations, Problems, Observations, Referrals, Documents) have not yet had their clinical test cases captured and documented. Feature files for these areas will be added once the corresponding test case documentation is available.

## Relationship to SCAL Technical Assurance Tests

The tests in `../SCAL_technical/` focus on the **technical SCAL assurance** — request conformance, response processing, API contract validation, and GP Connect specification compliance.

The tests in **this folder** focus on **clinical data accuracy** — given known test data in the GP provider, does the consumer UI show it correctly? They complement each other:

| Aspect | SCAL Technical | Clinical Assurance |
|--------|---------------|-------------------|
| Focus | API contract, request/response spec conformance | UI display correctness |
| Assertion target | FHIR request params, response structure | Visible on-screen text |
| Test data | Multiple providers (EMIS, TPP, Medicus) | Primarily gold patient (Louise Job) |
| Automation approach | UI + API observation | Pure UI verification |
