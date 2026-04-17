@structured_documents_migrate
Feature: Access Record - Structured Documents Migrate
  As a GP Connect consumer
  I want to migrate structured records and documents from a GP provider system
  So that patient records can be migrated between systems

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Access-Record:-Structured-Documents-Migrate
  # Uses v1.5 test data (Coxwold Surgery, ODS: B82617)

  # --- General Tests ---

  @GPC-MIG-TST-GEN-05 @audit
  Scenario: GPC-MIG-TST-GEN-05 - Access Control and Audit
    Given I am at a point in the system where I have access to attempt a call to a GP Connect service
    When I make that attempt to migrate GP Connect
    Then an audit record is written to an appropriate audit log including when migration is blocked, unsuccessful or successful
    And the audit record conforms to NHS Digital audit standards
    # Test data: 9690937286, 9690938681, 9674964738 (Business S Flag)

  @GPC-MIG-TST-GEN-06 @pds
  Scenario Outline: GPC-MIG-TST-GEN-06 - PDS trace timeliness for migration
    Given I have access to request data from GP Connect and the patient trace was <time> ago
    When I make that attempt to migrate a GP Connect record
    Then the GP Connect migrate request message is <result>
    # Test data: 9690937286

    Examples:
      | time        | result  |
      | > 24 hours  | blocked |
      | < 24 hours  | sent    |

  @GPC-MIG-TST-GEN-07 @demographics
  Scenario: GPC-MIG-TST-GEN-07 - Patient demographics primary verification for migration
    Given I have made a successful request to migrate a GP Connect record for patient "9690937286"
    When I receive a valid response including a patient resource
    Then I verify the patient resource details for family name, given name, gender, date of birth and GP Practice Code match to those presented to the user from the local system
    And I alert the user to any mismatch between the local record demographics and those provided in the GP Connect response message

  @GPC-MIG-TST-GEN-08 @authorisation
  Scenario: GPC-MIG-TST-GEN-08 - JWT claim does not match patient ODS code
    Given the user is going to make a migration request for a record for patient "9690937286"
    And the JWT Org claim contains an ODS code which is not the patient's practice
    When the user selects to migrate
    Then the resulting response with Operational Outcome NOT_AUTHORISED and Error Code 403 is processed successfully by the consumer

  @GPC-MIG-TST-GEN-09 @sensitive
  Scenario: GPC-MIG-TST-GEN-09 - PDS trace sensitive patient
    Given I have access to request data from GP Connect but I cannot confirm the registered practice either because it is not on PDS or the patient has an S-flag
    Then the request to migrate GP Connect is blocked and handled gracefully so the user is aware that access is not available for that patient at that time
    # Test data: 9690938533, 9690938541

  @GPC-MIG-TST-GEN-10 @deceased
  Scenario: GPC-MIG-TST-GEN-10 - Deceased patient
    Given I access a patient "9690938681" which is recorded as deceased on PDS or on the local system
    When I am at a point where I would normally be able to access GP Connect
    Then the system prevents access to GP Connect
    And handles the prevention gracefully so the user is aware that GP Connect is not available for this patient

  @GPC-MIG-TST-GEN-11 @error_handling
  Scenario: GPC-MIG-TST-GEN-11 - Patient Not Found error
    Given I have made a request to a GP Connect service for patient "9999999999"
    When I receive a patient not found error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  @GPC-MIG-TST-GEN-12 @error_handling
  Scenario: GPC-MIG-TST-GEN-12 - Patient Dissent to Share error
    Given I have made a request to a GP Connect service for patient "9690938576"
    When I receive a patient dissent to share error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  @GPC-MIG-TST-GEN-13 @error_handling
  Scenario: GPC-MIG-TST-GEN-13 - Invalid resource error
    Given I have made a request to a GP Connect service using an invalid resource for patient "9690937286"
    When I receive an invalid resource error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  @GPC-MIG-TST-GEN-14 @error_handling
  Scenario: GPC-MIG-TST-GEN-14 - Invalid NHS Number error
    Given I have made a request to a GP Connect service using an invalid NHS number
    When I receive an invalid NHS number error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  @GPC-MIG-TST-GEN-15 @error_handling
  Scenario: GPC-MIG-TST-GEN-15 - Invalid Parameter error
    Given I have made a request to a GP Connect service using an invalid parameter
    When I receive an invalid parameter error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  # --- Find Patient ---

  @GPC-DOC-TST-PAT-02 @find_patient @deceased
  Scenario: GPC-DOC-TST-PAT-02 - Find Patient deceased error for migration
    Given the consumer attempts to find patient "9690938681"
    And the provider patient record is recorded as deceased
    And the consumer sends a valid Find Patient request
    When the consumer receives the Find Patient response
    Then the resulting response is processed successfully by the consumer
    And the error details are communicated appropriately

  @GPC-DOC-TST-PAT-04 @find_patient @dissent
  Scenario: GPC-DOC-TST-PAT-04 - Find Patient dissent to share for migration
    Given the consumer attempts to find patient "9690938576"
    And the provider patient record is recorded as dissent to share
    And the consumer sends a valid Find Patient request
    When the consumer receives the Find Patient response
    Then the resulting response with Operational Outcome NO_PATIENT_CONSENT and Error Code 403 is processed successfully by the consumer
    And the error details are communicated appropriately

  @GPC-DOC-TST-PAT-05 @find_patient @error_handling
  Scenario: GPC-DOC-TST-PAT-05 - Find Patient invalid request for migration
    Given the consumer attempts to find patient "9690937286"
    And the consumer sends a request to the invalid parameter service
    When the consumer receives the Find Patient response
    Then the resulting response with Operational Outcome INVALID_PARAMETER and Error Code 422 is processed successfully by the consumer
    And the error details are communicated appropriately

  @GPC-DOC-TST-PAT-08 @find_patient @error_handling
  Scenario: GPC-DOC-TST-PAT-08 - Find Patient invalid NHS Number for migration
    Given the consumer attempts to find a patient
    And the consumer sends a valid Find Patient request with an invalid NHS Number
    When the consumer receives the Find Patient response
    Then the resulting response with Operational Outcome INVALID_NHS_NUMBER and Error Code 400 is processed successfully by the consumer
    And the error details are communicated appropriately

  # --- Request Document ---

  @GPC-DOC-TST-BIN-03 @retrieve_document @error_handling
  Scenario: GPC-DOC-TST-BIN-03 - Retrieve document no record found for migration
    Given the user has found a valid document for patient "9690937286"
    And the consumer has successfully identified the endpoint for the Retrieve Documents call
    And the record no longer exists at the practice or is too large
    When the user selects to retrieve a document and submits a non-existent document URL instead
    Then the resulting response with Operational Outcome NO_RECORD_FOUND and Error Code 404 is processed successfully by the consumer

  # --- Migration Specific Document Tests ---

  Rule: Migration Document Retrieval

    Background: Patient with documents found and endpoint resolved
      Given the user has found a valid patient "9690937286" who has documents associated
      And has successfully carried out a document search
      And successfully resolved the endpoint for the retrieve document call

    @GPC-DOC-TST-MIG-01 @retrieve_document
    Scenario: GPC-DOC-TST-MIG-01 - Get document for migration
      When the user selects request to retrieve a document
      Then the request is constructed as per the specification with the mandatory fields
      And the resulting response is processed successfully by the consumer

    @GPC-DOC-TST-MIG-02 @retrieve_document @sensitive
    Scenario: GPC-DOC-TST-MIG-02 - Get document including sensitive data
      When the user selects request to retrieve a document
      Then the request is constructed as per the specification with the mandatory fields
      And the resulting response is processed successfully by the consumer

    @GPC-DOC-TST-MIG-03 @retrieve_document @sensitive
    Scenario: GPC-DOC-TST-MIG-03 - Get document excluding sensitive data
      When the user selects request to retrieve a document
      Then the request is constructed as per the specification with the mandatory fields
      And the resulting response is processed successfully by the consumer
