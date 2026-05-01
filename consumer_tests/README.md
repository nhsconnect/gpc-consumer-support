# GP Connect Consumer Assurance Tests — Access Record: Structured

This folder contains the **BDD feature files** (Gherkin) that define the GP Connect consumer assurance test scenarios for the **Access Record: Structured** capability.

Every consumer supplier must implement and pass these tests to gather the assurance evidence required. The scenarios are supplier-agnostic — they describe _what_ must be tested, not _how_ to automate it.

## Feature Files

| Feature file | Capability |
| --- | --- |
| `access_record_structured.feature` | Access Record Structured — Medications & Allergies |
| `access_record_structured_extended.feature` | Access Record Structured — Problems, Immunisations, Consultations |

## How to Use

1. Use a BDD test framework in your language of choice (e.g. pytest-bdd, Cucumber, SpecFlow).
2. Point your framework at this folder as the feature file source.
3. Implement step definitions that drive your consumer application.
4. See the reference implementation folder for a worked example using Python + pytest-bdd + Playwright.
   The current example in this repository is under `../reference_cegedim__automated_tests_implementation/`.
