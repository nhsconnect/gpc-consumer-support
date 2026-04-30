# GP Connect Consumer Support

GP Connect consumer assurance test scripts and supporting documentation.

## Repository Structure

```text
├── consumer_tests/                                    # BDD feature files (Gherkin)
│   ├── foundations.feature
│   ├── spine_integration.feature
│   ├── access_record_html.feature
│   ├── access_record_structured.feature
│   ├── access_record_structured_extended.feature
│   ├── access_document.feature
│   ├── send_document_consultation_summary.feature
│   ├── send_document_online_consultation.feature
│   └── structured_documents_migrate.feature
│
├── reference_cegedim__automated_tests_implementation/ # Reference implementation (Cegedim)
│   └── ...                                            # See its own README for details
│
├── test_data_files/                                   # Test data (FHIR JSON bundles)
└── images/                                            # Documentation images
```

## consumer_tests

The `consumer_tests/` folder contains the **supplier-agnostic BDD feature files** that define the GP Connect consumer assurance test scenarios in Gherkin syntax. These are the tests that every consumer supplier must pass.

Each feature file maps to a GP Connect capability:

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

## Reference Implementation

The `reference_cegedim__automated_tests_implementation/` folder contains a **working reference implementation** that shows how the feature files in `consumer_tests/` can be automated using Python, pytest-bdd, and Playwright against the Cegedim Pharmacy Services pre-production environment.

Suppliers should use this as a guide to build their own test automation that executes the same BDD scenarios against their own consumer application. See the [reference implementation README](reference_cegedim__automated_tests_implementation/README.md) for setup and usage details.

For agent-specific implementation context and guardrails, see [AGENTS.md](reference_cegedim__automated_tests_implementation/AGENTS.md).

## Test Data

Three provider systems are configured with test patients:

| Provider | Primary Patient | NHS Number | Notes |
|----------|----------------|------------|-------|
| EMIS | Ms Janine Liston | 9730147140 | Do not amend, main AR:S test patient |
| TPP | Miss Louise Job | 9692136744 | Do not amend, main AR:S test patient |
| Medicus | Mr James Baggs | 9693646525 | ODS: N82090 |