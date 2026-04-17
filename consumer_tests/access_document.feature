@access_document
Feature: Access Document
  As a GP Connect consumer
  I want to search for and retrieve patient documents from the GP provider system
  So that I can access document records for patient care

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Access-Document
  # Uses v1.5 test data (Coxwold Surgery, ODS: B82617)

  # --- General Tests ---

  @GPC-STR-TST-GEN-05 @audit
  Scenario: GPC-STR-TST-GEN-05 - Access Control and Audit
    Given I am at a point in the system where I have access to attempt a call to a GP Connect service
    When I make that attempt to access GP Connect
    Then an audit record is written to an appropriate audit log including when access is blocked, unsuccessful or successful
    And the audit record conforms to NHS Digital audit standards
    # Test data: 9690937286, 9690938533

  @GPC-STR-TST-GEN-06 @pds
  Scenario Outline: GPC-STR-TST-GEN-06 - PDS trace timeliness
    Given I have access to request data from GP Connect and the patient trace was <time> ago
    When I make that attempt to access GP Connect
    Then the GP Connect request message is <result>
    # Test data: 9690937286

    Examples:
      | time        | result  |
      | > 24 hours  | blocked |
      | < 24 hours  | sent    |

  @GPC-STR-TST-GEN-07 @demographics
  Scenario: GPC-STR-TST-GEN-07 - Patient demographics primary verification
    Given I have made a successful request to GP Connect for patient "9690937286"
    When I receive a valid response including a patient resource
    Then I verify the patient resource details for family name, given name, gender, date of birth and GP Practice Code match to those presented to the user from the local system
    And I alert the user to any mismatch between the local record demographics and those provided in the GP Connect response message

  @GPC-STR-TST-GEN-08 @pds
  Scenario: GPC-STR-TST-GEN-08 - PDS trace registered practice
    Given I have access to request data from GP Connect and the patient trace was within the last 24 hours
    When I make that attempt to access GP Connect
    Then the registered GP practice from the last PDS trace is used to identify the practice to submit the request to
    # Test data: 9690937286

  @GPC-STR-TST-GEN-09 @sensitive
  Scenario: GPC-STR-TST-GEN-09 - PDS trace no registered practice or S-flag
    Given I have access to request data from GP Connect but I cannot confirm the registered practice either because it is not on PDS or the patient has an S-flag
    When I attempt to access GP Connect
    Then the request to GP Connect is blocked and handled gracefully so the user is aware that access is not available for that patient at that time
    # Test data: 9690938533, 9690938541

  @GPC-STR-TST-GEN-10 @deceased
  Scenario: GPC-STR-TST-GEN-10 - Deceased patient
    Given I access a patient "9690938681" which is recorded as deceased on PDS or on the local system
    When I am at a point where I would normally be able to access GP Connect
    Then the system prevents access to GP Connect
    And handles the prevention gracefully so the user is aware that GP Connect is not available for this patient

  @GPC-STR-TST-GEN-11 @error_handling
  Scenario: GPC-STR-TST-GEN-11 - Patient Not Found error
    Given I have made a request to a GP Connect service for patient "9999999999"
    When I receive a patient not found error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  @GPC-STR-TST-GEN-12 @error_handling
  Scenario: GPC-STR-TST-GEN-12 - Patient Dissent to Share error
    Given I have made a request to a GP Connect service for patient "9690938576"
    When I receive a patient dissent to share error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  @GPC-STR-TST-GEN-13 @error_handling
  Scenario: GPC-STR-TST-GEN-13 - Invalid resource error
    Given I have made a request to a GP Connect service using an invalid resource for patient "9690937286"
    When I receive an invalid resource error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  @GPC-STR-TST-GEN-14 @error_handling
  Scenario: GPC-STR-TST-GEN-14 - Invalid NHS Number error
    Given I have made a request to a GP Connect service using an invalid NHS number
    When I receive an invalid NHS number error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution

  # --- Find Patient ---

  @GPC-DOC-TST-PAT-01 @find_patient
  Scenario: GPC-DOC-TST-PAT-01 - Find Patient request
    Given the user wishes to access documents for patient "9690937286"
    And provider system identifiers are not known
    When an access document request is triggered
    Then a Find Patient request is sent to obtain the patient identifier
    And the request uses a verified NHS Number
    And the request conforms to the Access Document Find Patient specification
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-PAT-02 @find_patient @deceased
  Scenario: GPC-DOC-TST-PAT-02 - Find Patient deceased error
    Given the consumer attempts to find patient "9690938681"
    And the provider patient record is recorded as deceased
    And the consumer sends a valid Find Patient request
    When the consumer receives the Find Patient response
    Then the resulting response is processed successfully by the consumer
    And the error details are communicated appropriately

  @GPC-DOC-TST-PAT-04 @find_patient @dissent
  Scenario: GPC-DOC-TST-PAT-04 - Find Patient dissent to share
    Given the consumer attempts to find patient "9690938576"
    And the provider patient record is recorded as dissent to share
    And the consumer sends a valid Find Patient request
    When the consumer receives the Find Patient response
    Then the resulting response with Operational Outcome NO_PATIENT_CONSENT and Error Code 403 is processed successfully by the consumer
    And the error details are communicated appropriately

  @GPC-DOC-TST-PAT-05 @find_patient @error_handling
  Scenario: GPC-DOC-TST-PAT-05 - Find Patient invalid request
    Given the consumer attempts to find patient "9690937286"
    And the consumer sends a request to the invalid parameter service
    When the consumer receives the Find Patient response
    Then the resulting response with Operational Outcome INVALID_PARAMETER and Error Code 422 is processed successfully by the consumer
    And the error details are communicated appropriately

  @GPC-DOC-TST-PAT-07 @find_patient @error_handling
  Scenario: GPC-DOC-TST-PAT-07 - Find Patient practice not enabled
    Given the consumer attempts to find patient "9658218873"
    And the consumer sends a valid request
    And the provider practice is not enabled for access document
    When the consumer receives the Find Patient response
    Then the resulting response with Operational Outcome ACCESS_DENIED and Error Code 403 is processed successfully by the consumer
    And the error details are communicated appropriately

  @GPC-DOC-TST-PAT-08 @find_patient @error_handling
  Scenario: GPC-DOC-TST-PAT-08 - Find Patient invalid NHS Number
    Given the consumer attempts to find a patient
    And the consumer sends a valid Find Patient request with an invalid NHS Number
    When the consumer receives the Find Patient response
    Then the resulting response with Operational Outcome INVALID_NHS_NUMBER and Error Code 400 is processed successfully by the consumer
    And the error details are communicated appropriately

  # --- Search Patient Documents ---

  @GPC-DOC-TST-LST-01 @search_documents
  Scenario: GPC-DOC-TST-LST-01 - List of all documents
    Given the user wishes to obtain a full patient documents list for patient "9690937286"
    And the system has a valid GP system patient identifier
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the request is constructed as per the specification with the mandatory headers and parameters
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-LST-02 @search_documents
  Scenario: GPC-DOC-TST-LST-02 - List documents from a given date
    Given the user wishes to obtain the patient documents list from a given date for patient "9690937286"
    And the system has a valid GP system patient identifier
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the request is constructed as per the specification with the mandatory fields
    And the request also contains a created parameter with a date prefixed by ge
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-LST-03 @search_documents
  Scenario: GPC-DOC-TST-LST-03 - List documents to a given date
    Given the user wishes to obtain the patient documents list up to a given date for patient "9690937286"
    And the system has a valid GP system patient identifier
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the request is constructed as per the specification with the mandatory fields
    And the request also contains a created parameter with a date prefixed by le
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-LST-04 @search_documents
  Scenario: GPC-DOC-TST-LST-04 - List documents for a date period
    Given the user wishes to obtain the patient documents list for a date range for patient "9690937286"
    And the system has a valid GP system patient identifier
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the request is constructed as per the specification with the mandatory fields
    And the request also contains a created parameter with a date prefixed by ge
    And the request also contains a created parameter with a date prefixed by le
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-LST-05 @search_documents
  Scenario: GPC-DOC-TST-LST-05 - List documents for author organisation
    Given the user wishes to obtain the patient documents list for an author organisation for patient "9690937286"
    And the system has a valid GP system patient identifier
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the request is constructed as per the specification with the mandatory fields
    And the request also contains an author parameter with a value of ORG1
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-LST-06 @search_documents
  Scenario: GPC-DOC-TST-LST-06 - List documents by description
    Given the user wishes to obtain the patient documents list with a given document description for patient "9690937286"
    And the system has a valid GP system patient identifier
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the request is constructed as per the specification with the mandatory fields
    And the request also contains a description parameter with a value of "Discharge Summary"
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-LST-07 @search_documents
  Scenario: GPC-DOC-TST-LST-07 - No documents available
    Given the user has found a valid patient "9690937294" who has no documents associated
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the request is constructed as per the specification
    And the resulting response is processed successfully by the consumer
    And the user is aware that there are no documents available where applicable

  @GPC-DOC-TST-LST-08 @search_documents
  Scenario: GPC-DOC-TST-LST-08 - Supported document reference elements
    Given I have sent a valid search documents request for patient "9690937286"
    When I receive a successful valid search documents response and resources
    Then I display or utilise all the key information to represent or process the document records commensurate with the original record meaning and my specific use case

  @GPC-DOC-TST-LST-09 @search_documents @error_handling
  Scenario: GPC-DOC-TST-LST-09 - Search documents invalid parameter error
    Given the user has found a valid patient "9690937286" who has documents associated
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents without the mandatory include parameters
    Then the resulting response with Operational Outcome INVALID_PARAMETER and Error Code 422 is processed successfully by the consumer

  @GPC-DOC-TST-LST-10 @search_documents @error_handling
  Scenario: GPC-DOC-TST-LST-10 - Search documents patient not found error
    Given the user has found a valid patient "9690937286" who has documents associated
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents with an invalid patient ID
    Then the resulting response with Operational Outcome PATIENT_NOT_FOUND and Error Code 404 is processed successfully by the consumer

  @GPC-DOC-TST-LST-11 @search_documents @error_handling
  Scenario: GPC-DOC-TST-LST-11 - Search documents no patient consent error
    Given the user has found a valid patient "9690938576" who has dissented to share records via GP Connect
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the resulting response with Operational Outcome NO_PATIENT_CONSENT and Error Code 403 is processed successfully by the consumer

  @GPC-DOC-TST-LST-12 @search_documents @error_handling
  Scenario: GPC-DOC-TST-LST-12 - Search documents access denied error
    Given the user has found a valid patient and the practice has dissented to share records via GP Connect
    And the consumer has successfully identified the endpoint for the Search Documents call
    When the user selects request to Search for Documents
    Then the resulting response with Operational Outcome ACCESS_DENIED and Error Code 403 is processed successfully by the consumer

  # --- Request Document ---

  @GPC-DOC-TST-BIN-01 @retrieve_document
  Scenario: GPC-DOC-TST-BIN-01 - Get document
    Given the user has found a valid patient "9690937286" who has documents associated
    And has successfully carried out a document search
    And successfully resolved the endpoint for the retrieve document call
    When the user selects request to retrieve a document
    Then the request is constructed as per the specification with the mandatory fields
    And the resulting response is processed successfully by the consumer

  @GPC-DOC-TST-BIN-02 @retrieve_document
  Scenario: GPC-DOC-TST-BIN-02 - Document file size warning
    Given the user wishes to retrieve a document previously found by searching documents
    And the file size is known and is likely to result in a slow response to retrieval
    When the user selects request to retrieve a document
    Then the user may be warned that the document may be slow to retrieve
    And the file size may be included in the warning where available

  @GPC-DOC-TST-BIN-03 @retrieve_document @error_handling
  Scenario: GPC-DOC-TST-BIN-03 - Retrieve document no record found
    Given the user has found a valid document for patient "9690937286"
    And the consumer has successfully identified the endpoint for the Retrieve Documents call
    And the record no longer exists at the practice or is too large
    When the user selects to retrieve a document and submits a non-existent document URL instead
    Then the resulting response with Operational Outcome NO_RECORD_FOUND and Error Code 404 is processed successfully by the consumer

  @GPC-DOC-TST-BIN-04 @retrieve_document @error_handling
  Scenario: GPC-DOC-TST-BIN-04 - Retrieve document access denied
    Given the user has found a valid document
    And the consumer has successfully identified the endpoint for the Retrieve Documents call
    And the practice has dissented to share records via GP Connect
    When the user selects to retrieve a document
    Then the resulting response with Operational Outcome ACCESS_DENIED and Error Code 403 is processed successfully by the consumer

  # --- Additional Core Tests ---

  @GPC-CORE-05-TEST @superseded
  Scenario: GPC-CORE-05-TEST - Superseded NHS Number
    Given I want to view a patient's record
    When I retrieve a patient's record from its registered GP practice including a PDS trace
    Then the consuming application should allow a GP Connect call to be made using the latest NHS number
    # Test data: superseded NHS number 9658220215
