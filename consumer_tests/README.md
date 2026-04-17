# GP Connect Consumer Assurance Tests

This folder contains the **BDD feature files** (Gherkin) that define the GP Connect consumer assurance test scenarios.

Every consumer supplier must implement and pass these tests to gather the assurance evidence required. The scenarios are supplier-agnostic — they describe _what_ must be tested, not _how_ to automate it.

## Feature Files

| Feature file | Capability |
|---|---|
| `foundations.feature` | Find/Read Patient, Practitioner, Organisation, Location |
| `spine_integration.feature` | SDS lookup, JWT generation, SSP routing, HTTP headers |
| `access_record_html.feature` | Access Record HTML |
| `access_record_structured.feature` | Access Record Structured — Medications & Allergies |
| `access_record_structured_extended.feature` | Access Record Structured — Problems, Immunisations, Consultations |
| `access_document.feature` | Access Document |
| `send_document_consultation_summary.feature` | Send Document — Consultation Summary |
| `send_document_online_consultation.feature` | Send Document — Online Consultation |
| `structured_documents_migrate.feature` | Structured to Documents Migration |

## How to Use

1. Use a BDD test framework in your language of choice (e.g. pytest-bdd, Cucumber, SpecFlow).
2. Point your framework at this folder as the feature file source.
3. Implement step definitions that drive your consumer application.
4. See [`reference_cegedim__automated_tests_implementation/`](../reference_cegedim__automated_tests_implementation/) for a worked example using Python + pytest-bdd + Playwright.
