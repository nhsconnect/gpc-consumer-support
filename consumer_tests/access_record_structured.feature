@access_record_structured
Feature: Access Record Structured - Medications and Allergies
  As a GP Connect consumer
  I want to access a patient's structured medication and allergy records
  So that I can view or import their clinical data from the registered GP practice

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Structured
  # Demonstrator: v0.7/v1.2 - Dr Legg's Surgery (ODS: A20047)
  # Structured record up to v1.2.7

  # ---------------------------------------------------------------------------
  # General Tests
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-GEN-02 @general
  Scenario: GPC-STR-TST-GEN-02 - Imported data - Exporting data to a third party
    Given I have imported GP Connect data
    And I support data sharing with other systems
    When I receive a request for patient record data for a patient I hold GP Connect data for
    Then I only include GP Connect data where the request is for Direct Care use only
    And I always include the resource identifiers received from GP Connect messages when exporting the data
    # SCAL: GPC-STR-GEN-02

  @GPC-STR-TST-GEN-05 @general @audit @skip_audit_logs_unavailable
  Scenario: GPC-STR-TST-GEN-05 - Access Control and Audit
    Given I am at a point in the system where I have access to attempt a call to a GP Connect service
    When I make that attempt to access GP Connect
    Then an audit record is written to an appropriate audit log including when access is blocked, unsuccessful or successful
    And the audit record conforms to NHS Digital audit standards
    # SCAL: GPC-IG10-01, GPC-IG10-02 | Test data: 9658218873, 9658220142, 9476718943

  @GPC-STR-TST-GEN-06 @general @pds
  Scenario: GPC-STR-TST-GEN-06 - Access Control and Audit - PDS trace timeliness
    Given I have access to request data from GP Connect and the patient trace was performed at a given time
    When I make that attempt to access GP Connect
    Then the GP Connect request message is blocked if the trace was more than 24 hours ago
    And the GP Connect request message is sent if the trace was less than 24 hours ago
    # SCAL: GPC-CORE01-01 | Test data: 9658218873

  @GPC-STR-TST-GEN-07 @patient_demographics
  Scenario: GPC-STR-TST-GEN-07 - Patient Demographics - primary
    Given I have made a successful request to GP Connect
    When I receive a valid response including a patient resource
    Then I verify the patient resource details for family name, given name, gender, date of birth and GP Practice Code match to those in the local system
    And I alert the user to any mismatch between the local record demographics and those provided in the GP Connect response message
    # SCAL: GPC-CORE02-02 | Test data: 9658218873

  @GPC-STR-TST-GEN-08 @patient_demographics @pds
  Scenario: GPC-STR-TST-GEN-08 - Patient Demographics - PDS trace registered practice
    Given I have access to request data from GP Connect and the patient trace was within the last 24 hours
    When I make that attempt to access GP Connect
    Then the registered GP practice from the last PDS trace is used to identify the practice to submit the request to
    # SCAL: GPC-CORE03-01, GPC-CORE03-02 | Test data: 9658218873

  @GPC-STR-TST-GEN-09 @patient_demographics @pds @skip_sensitive_pds_data_unavailable
  Scenario: GPC-STR-TST-GEN-09 - Patient Demographics - PDS trace sensitive patient
    Given I have access to request data from GP Connect but I cannot confirm the registered practice either because it is not on PDS or the patient has an s-flag
    When I attempt to access GP Connect
    Then the request to GP Connect is blocked and handled gracefully so the user is aware that access is not available for that patient at that time
    # SCAL: GPC-CORE03-03, GPC-CORE04-01 | Test data: 9658220142, 9658220150

  @GPC-STR-TST-GEN-10 @patient_demographics
  Scenario: GPC-STR-TST-GEN-10 - Patient Demographics - Deceased patient
    Given I access a patient which is recorded as deceased on PDS or on the local system
    When I am at a point where I would normally be able to access GP Connect
    Then the system prevents access to GP Connect
    And handles the prevention gracefully so the user is aware that GP Connect is not available for this patient
    # SCAL: GPC-CORE07-01 | Test data: 9658220290

  @GPC-STR-TST-GEN-11 @error_handling @skip_api_access_not_exposed
  Scenario: GPC-STR-TST-GEN-11 - Error Handling - Patient Not Found
    Given I have made a request to a GP Connect service
    When I receive a patient not found error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution
    # SCAL: GPC-CORE13-02 | Test data: 9999999999

  @GPC-STR-TST-GEN-12 @error_handling @skip_api_access_not_exposed
  Scenario: GPC-STR-TST-GEN-12 - Error Handling - Patient Dissent to Share
    Given I have made a request to a GP Connect service
    When I receive a patient dissent to share error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution
    # SCAL: GPC-CORE13-03 | Test data: 9658220169

  @GPC-STR-TST-GEN-13 @error_handling @skip_api_access_not_exposed
  Scenario: GPC-STR-TST-GEN-13 - Error Handling - Invalid resource
    Given I have made a request to a GP Connect service using an Invalid Resource
    When I receive an invalid resource error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution
    # SCAL: GPC-CORE13-04 | Test data: 9658218873

  @GPC-STR-TST-GEN-14 @error_handling @skip_api_access_not_exposed
  Scenario: GPC-STR-TST-GEN-14 - Error Handling - Invalid NHS Number
    Given I have made a request to a GP Connect service using an Invalid NHS Number
    When I receive an invalid NHS number error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution
    # SCAL: GPC-CORE13-05

  @GPC-STR-TST-GEN-15 @error_handling @allergies @skip_api_access_not_exposed
  Scenario: GPC-STR-TST-GEN-15 - Error Handling - Invalid parameter allergies
    Given I have made a request for allergies to a GP Connect service with invalid Allergies Parameters
    When I receive an invalid parameter error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution
    # SCAL: GPC-CORE13-ALL01 | Test data: 9658218873

  @GPC-STR-TST-GEN-16 @error_handling @medications @skip_api_access_not_exposed
  Scenario: GPC-STR-TST-GEN-16 - Error Handling - Invalid parameter medications
    Given I have made a request for medications to a GP Connect service with invalid Medications Parameters
    When I receive an invalid parameter error response
    Then I handle the response gracefully
    And I make available all the diagnostic details to appropriate people to enable fault resolution
    # SCAL: GPC-CORE13-MED01 | Test data: 9658218873

  Rule: Handling message warnings from GP Connect

    Background: Valid message sent to GP Connect
      Given I have sent a valid message to GP Connect

    @GPC-STR-TST-GEN-17 @warnings @gp2gp_transfer
    Scenario: GPC-STR-TST-GEN-17 - Warnings - Message warnings GP2GP transfer
      When I receive a response including a data in transit warning
      Then I make the user aware as appropriate
      # SCAL: GPC-CORE13-07, GPC-CORE13-06 | Test data: 9658219705

    @GPC-STR-TST-GEN-18 @warnings @allergies @skip_cededim_did_not_implement_so_out_of_scope
    Scenario: GPC-STR-TST-GEN-18 - Warnings - Message warnings Confidential allergy
      Given I have requested allergies are included
      When I receive a response including a confidential items warning for allergies
      Then I make the user aware and apply controls as appropriate
      # SCAL: GPC-CORE13-ALL02 | Test data: 9658219705

    @GPC-STR-TST-GEN-19 @warnings @medications
    Scenario: GPC-STR-TST-GEN-19 - Warnings - Message warnings Confidential medication
      Given I have requested medications are included
      When I receive a response including a confidential items warning for medications
      Then I make the user aware and apply controls as appropriate
      # SCAL: GPC-CORE13-MED02 | Test data: 9658218873

    @GPC-STR-TST-GEN-25 @warnings
    Scenario: GPC-STR-TST-GEN-25 - Warnings - Multiple message warnings
      Given I have included a request for medications data
      When I receive a response including a data in transit warning and a confidential data items warning for medications
      Then I make the user aware as appropriate and that the data in transit warning is shown as applicable to all data
      And the confidential data warning is shown to apply to medications data only
      # SCAL: GPC-CORE13-09 | Test data: 9658219705

  @GPC-STR-TST-GEN-20 @general @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: GPC-STR-TST-GEN-20 - Presenting patient data - Data Source
    Given I have received a valid message response
    When I present the data to the end user
    Then the user is aware that the data has come from the patient's registered GP record
    # SCAL: GPC-STR02-01 | Test data: 9658218873

  @GPC-STR-TST-GEN-24 @general
  Scenario: GPC-STR-TST-GEN-24 - Imported data - Storing identifiers
    Given I have received a successful valid response message
    When I import the GP Connect resource or data into the local system
    Then I always retain resource identifiers including but not limited to system and value
    # SCAL: GPC-STR-TST-GEN-24 | Test data: 9658218873

  @GPC-STR-TST-GEN-26 @warnings
  Scenario: GPC-STR-TST-GEN-26 - Warnings - Forwards compatibility
    Given I have sent a request for both medications and allergies
    When the provider processes the request and returns a success response with resources for one clinical area and a warning that the other is not recognised
    Then I recognise the warning in the response as appropriate to my use case
    And I utilise the successful response information
    And I handle gracefully the warning that the request for the other area has failed informing users appropriately
    # SCAL: GPC-STR-TST-GEN-26

  @GPC-STR-TST-GEN-27 @warnings
  Scenario: GPC-STR-TST-GEN-27 - Warnings - Backwards compatibility
    Given I have sent a valid request to a provider at a higher version than I support
    When I receive the response it includes additional information
    Then I ignore the additional information
    And I process the response successfully
    # SCAL: GPC-STR-TST-GEN-27

  # ---------------------------------------------------------------------------
  # Medication Tests
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-MED-02 @medications
  Scenario: GPC-STR-TST-MED-02 - Medication data elements
    Given I have received a successful valid medications message response
    When I display or use the medication information
    Then I display or utilise all the key information to represent or process the medication records commensurate with the original record meaning and my specific use case
    # SCAL: GPC-STR-MED02-01, GPC-STR-MED13-01, GPC-STR-MED13-(03-17), GPC-STR-MED14-02 | Test data: 9658218873

  @GPC-STR-TST-MED-07 @medications
  Scenario: GPC-STR-TST-MED-07 - No medication records
    Given I have received a successful valid medications message response
    And the response has a list with an empty reason
    And the response does not include medication resources
    When I display or use the medication information
    Then I display or utilise the list empty reason to inform the user that the patient has no medication records within the request parameters
    # SCAL: GPC-STR-MED15-01 | Test data: 9658218903

  Rule: Medication requests for a GP Connect enabled patient

    Background: Patient enabled for GP Connect medication access
      Given I am enabled to access GP Connect data for a given patient

    @GPC-STR-TST-MED-01 @medications
    Scenario: GPC-STR-TST-MED-01 - Request all medications
      Given I want to retrieve a full medication history
      When I make the medication request to GP Connect
      Then the request conforms to the GP Connect specification
      And includes the patient's NHS Number
      And the request has the includeMedication parameter
      And the request sets the includePrescriptionIssues part parameter to true
      And the request does NOT include the medicationSearchFromDate parameter
      And the resulting response is processed successfully by the Consumer
      # SCAL: GPC-STR-MED01-01, GPC-STR-MED01-02 | Test data: 9658218873

    @GPC-STR-TST-MED-03 @medications @date_filters
    Scenario: GPC-STR-TST-MED-03 - Request medication by date
      Given I want to retrieve medication details but I do not require a full medication history
      When I make the medication request to GP Connect
      Then the request conforms to the GP Connect specification
      And includes the patient's NHS Number
      And the request has the includeMedication parameter
      And the request sets the includePrescriptionIssues part parameter to true or false
      And the request includes the medicationSearchFromDate parameter
      And the medicationSearchFromDate is in the defined format
      And the medicationSearchFromDate is equal or less than the current date
      And the resulting response is processed successfully by the Consumer
      # SCAL: GPC-STR-MED04-01, GPC-STR-MED04-03 | Test data: 9658218873

    @GPC-STR-TST-MED-04 @medications
    Scenario: GPC-STR-TST-MED-04 - Request medication by user selected date future date rejected
      Given I am able to specify the date from which I want medications
      When I attempt to request medications by a future date
      Then I am prevented from submitting the request
      # SCAL: GPC-STR-MED04-02 | Test data: 9658218873

    @GPC-STR-TST-MED-05 @medications
    Scenario: GPC-STR-TST-MED-05 - Requesting medication issues
      Given my use case does or does not require medication issues to be included
      When I make the medication request to GP Connect
      Then the request conforms to the GP Connect specification
      And includes the patient's NHS Number
      And the request has the includeMedication parameter
      And the request sets the includePrescriptionIssues part parameter to the appropriate value
      And the resulting response is processed successfully by the Consumer
      # SCAL: GPC-STR-MED06-01 | Test data: 9658218873

    @GPC-STR-TST-MED-08 @medications
    Scenario: GPC-STR-TST-MED-08 - Request all medications v1.2.7
      Given I want to retrieve a full medication history
      When I make the medication request to GP Connect
      Then the request conforms to the GP Connect specification
      And includes the patient's NHS Number
      And the request has the includeMedication parameter
      And the request does NOT include the includePrescriptionIssues part parameter OR includes and sets it to true
      And the request does NOT include the medicationSearchFromDate parameter
      # SCAL: GPC-STR-TST-MED-08 | Test data: 9658218873

    @GPC-STR-TST-MED-09 @medications
    Scenario: GPC-STR-TST-MED-09 - Requesting medication issues v1.2.7
      Given my use case does or does not require medication issues to be included
      When I make the medication request to GP Connect
      Then the request conforms to the GP Connect specification
      And includes the patient's NHS Number
      And the request has the includeMedication parameter
      And the request sets the includePrescriptionIssues part parameter to true, false, or is absent
      # SCAL: GPC-STR-TST-MED-09 | Test data: 9658218873

  # ---------------------------------------------------------------------------
  # Allergy Tests
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-ALG-01 @allergies
  Scenario: GPC-STR-TST-ALG-01 - Request current allergies
      Given the response includes resolved allergies
    When the user selects to access current allergies from GP Connect
    Then the resulting request is populated with valid syntax using the includeAllergies parameter with part parameter includeResolvedAllergies set to false
    And the resulting response is processed successfully by the Consumer
    # SCAL: GPC-STR-ALL01-(01-02) | Test data: 9658218873

  @GPC-STR-TST-ALG-02 @allergies
  Scenario: GPC-STR-TST-ALG-02 - Request current and resolved allergies
      Given the response includes allergies which are not recognised by my system
    When the user selects to access all allergies from GP Connect
    Then the resulting request is populated with valid syntax using the includeAllergies parameter with part parameter includeResolvedAllergies set to true
    And the resulting response is processed successfully by the Consumer
    # SCAL: GPC-STR-ALL02-01 | Test data: 9658218873

  Rule: Handling allergy response data

    Background: Successful allergy response received
      Given I have received a successful valid allergies message response

    @GPC-STR-TST-ALG-03 @allergies
    Scenario: GPC-STR-TST-ALG-03 - Handling resolved allergies
      Given the response includes an empty active allergies list resource indicating that the patient record has no content recorded
      When I display or use the allergies information
      Then my system identifies the resolved allergies and handles them in a clinically safe manner such that they remain distinct from current allergies
      And where the resolved allergies are presented in the UI they are clearly and prominently labelled as ended, resolved or equivalent
      And ensures that the resolved allergies cannot be utilised by decision support where decision support is in use
      # SCAL: GPC-STR-ALL02-02 | Test data: 9658218873

    @GPC-STR-TST-ALG-04 @allergies @skip_cededim_did_not_implement_so_out_of_scope
    Scenario: GPC-STR-TST-ALG-04 - Allergy data elements
      Given the response includes a single code item which indicates that the clinician has recorded that the patient has no known allergies
      Then I display or utilise all the key information to represent or process the allergy records commensurate with the original record meaning and my specific use case
      # SCAL: GPC-STR-ALL04-(01-09) | Test data: 9658218873

    @GPC-STR-TST-ALG-05 @allergies
    Scenario: GPC-STR-TST-ALG-05 - Unrecognised allergies
      Given the response includes allergies which are not recognised by my system
      When I display or use the allergy information
      Then I display or utilise any SNOMED code or alternative code system coding as applicable to my use case
      And I display or utilise the allergy name as provided
      And I can handle any records which are sent as allergies but are not recognised as allergy codes by my system
      # SCAL: GPC-STR-TST-ALG-05

    @GPC-STR-TST-ALG-07 @allergies
    Scenario: GPC-STR-TST-ALG-07 - No data response
      Given the response includes an empty active allergies list resource indicating that the patient record has no content recorded
      When I display or use the allergies response
      Then I recognise this as a record with no active allergies recorded
      And I handle it appropriate to my use case and in such a way it is not confused with a clinical assertion of no known allergies
      # SCAL: GPC-STR-ALL06-01 | Test data: 9658218865

    @GPC-STR-TST-ALG-08 @allergies
    Scenario: GPC-STR-TST-ALG-08 - Clinically asserted no known allergies
      Given the response includes a single code item which indicates that the clinician has recorded that the patient has no known allergies
      When I display or use the allergies response
      Then I recognise this as a clinical assertion of no known allergies
      And I handle it appropriate to my use case and in such a way it is not confused with an empty list response
      # SCAL: GPC-STR-ALL06-01 | Test data: 9658218989
