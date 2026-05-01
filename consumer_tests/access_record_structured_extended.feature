@access_record_structured_extended
Feature: Access Record Structured - Full Record (Extended)
  As a GP Connect consumer
  I want to access a patient's full structured clinical record
  So that I can view or import all clinical areas from the registered GP practice

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Access-Record-Structured-(extended)
  # Demonstrator: v1.5 - Coxwold Surgery (ODS: B82617)
  # Extended Structured up to v1.5.0

  # ---------------------------------------------------------------------------
  # GENERAL TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-GEN-05 @general @skip_audit_logs_unavailable
  Scenario: Access Control and Audit
    Given I am at a point in the system where I have access to attempt a call to a GP Connect service
    When I make that attempt to access GP Connect
    Then an audit record is written to an appropriate audit log including when access is blocked, unsuccessful or successful
    And the audit record conforms to NHS Digital audit standards
    # SCAL: GPC-STR-TST-GEN-05 | Test data: 9690937286, 9690938533

  @GPC-STR-TST-GEN-06 @general
  Scenario: PDS trace timeliness
    Given I have access to request data from GP Connect and the patient trace was performed at a given time
    When I make that attempt to access GP Connect
    Then the request is blocked if the trace was performed more than 24 hours ago
    And the request is sent if the trace was performed less than 24 hours ago
    # SCAL: GPC-STR-TST-GEN-06 | Test data: 9690937286

  @GPC-STR-TST-GEN-07 @general
  Scenario: Patient demographics primary
    Given I have made a successful request to GP Connect
    When I receive a valid response including a patient resource
    Then I verify the patient resource details for family name, given name, gender, date of birth and GP Practice Code match
    And I alert the user to any mismatch
    # SCAL: GPC-STR-TST-GEN-07 | Test data: 9690937286

  @GPC-STR-TST-GEN-08 @general
  Scenario: PDS trace registered practice
    Given I have access to request data from GP Connect and the patient trace was within the last 24 hours
    When I make that attempt to access GP Connect
    Then the registered GP practice from the last PDS trace is used
    # SCAL: GPC-STR-TST-GEN-08 | Test data: 9690937286

  # TEMPORARY: GEN-09 is skipped in automation because NHS 9690938533 and 9690938541 are
  # currently not s-marked in PDS, so this sensitive-trace blocked-path cannot be exercised.
  @GPC-STR-TST-GEN-09 @general @skip_sensitive_pds_data_unavailable
  Scenario: PDS trace sensitive
    Given I have access to request data from GP Connect but I cannot confirm the registered practice because it is not on PDS or the patient has an s-flag
    When I attempt to access GP Connect
    Then the request is blocked and handled gracefully
    # SCAL: GPC-STR-TST-GEN-09 | Test data: 9690938533, 9690938541

  @GPC-STR-TST-GEN-10 @general
  Scenario: Deceased patient
    Given I access a patient which is recorded as deceased on PDS or on the local system
    When I am at a point where I would normally be able to access GP Connect
    Then the system prevents access and handles the prevention gracefully
    # SCAL: GPC-STR-TST-GEN-10 | Test data: 9690938681

  @GPC-STR-TST-GEN-11 @general @skip_api_access_not_exposed
  Scenario: Patient Not Found
    Given I have made a request to a GP Connect service
    When I receive a patient not found error response
    Then I handle the error gracefully and make diagnostics available
    # SCAL: GPC-STR-TST-GEN-11 | Test data: 9999999999

  @GPC-STR-TST-GEN-12 @general @skip_api_access_not_exposed
  Scenario: Patient Dissent to Share
    Given I have made a request to a GP Connect service
    When I receive a patient dissent to share error response
    Then I handle the error gracefully and make diagnostics available
    # SCAL: GPC-STR-TST-GEN-12 | Test data: 9690938576

  @GPC-STR-TST-GEN-13 @general @skip_api_access_not_exposed
  Scenario: Invalid resource
    Given I have made a request using an invalid resource
    When I receive an invalid resource error response
    Then I handle the error gracefully and make diagnostics available
    # SCAL: GPC-STR-TST-GEN-13 | Test data: 9690937286

  @GPC-STR-TST-GEN-14 @general @skip_api_access_not_exposed
  Scenario: Invalid NHS Number
    Given I have made a request using an invalid NHS Number
    When I receive an invalid NHS number error response
    Then I handle the error gracefully and make diagnostics available
    # SCAL: GPC-STR-TST-GEN-14 | Test data: N/A

  @GPC-STR-TST-GEN-15 @general @skip_api_access_not_exposed
  Scenario: Invalid parameter allergies
    Given I have made a request for allergies with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-GEN-15 | Test data: 9690937286

  @GPC-STR-TST-GEN-16 @general @skip_api_access_not_exposed
  Scenario: Invalid parameter medications
    Given I have made a request for medications with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-GEN-16 | Test data: 9690937286

  @GPC-STR-TST-GEN-17 @general
  Scenario: GP2GP transfer warning
    Given I search for a patient by demographics using family name Beston
    When I select the top result and click View GP Record
    Then I make the user aware of the GP2GP transfer warning message
    # SCAL: GPC-STR-TST-GEN-17 | Test data: 9690938096

  @GPC-STR-TST-GEN-18 @general @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Confidential allergy warning
    Given I have sent a valid message and requested allergies
    When I receive a confidential items warning for allergies
    Then I make the user aware of the confidential items warning
    # SCAL: GPC-STR-TST-GEN-18 | Test data: 9690938118

  @GPC-STR-TST-GEN-20 @general @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Data Source
    Given I have received a valid message response
    When I present the data to the end user
    Then the user is aware the data has come from the patient's registered GP record
    # SCAL: GPC-STR-TST-GEN-20 | Test data: 9690937286

  # ---------------------------------------------------------------------------
  # MEDICATION TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-MED-01 @medications @skip_api_access_not_exposed
  Scenario: Request all medications
    Given I am enabled to access GP Connect data for a given patient and I want to retrieve a full medication history
    When I make the medication request
    Then the request conforms to the specification and includes the NHS Number
    And the request includes the includeMedication parameter
    And the request includes includePrescriptionIssues set to true
    And the request does not include a medicationSearchFromDate
    # SCAL: GPC-STR-TST-MED-01 | Test data: 9690937286

  @GPC-STR-TST-MED-02 @medications
  Scenario: Medication data elements
    Given I have received a successful valid medications response
    When I display or use the information
    Then I display all key information commensurate with the original record meaning
    # SCAL: GPC-STR-TST-MED-02 | Test data: 9690937286

  @GPC-STR-TST-MED-03 @medications @skip_api_access_not_exposed
  Scenario: Request medication by date
    Given I am enabled to access GP Connect data and want to retrieve medication details for a period
    When I make the medication request
    Then the request conforms to the specification with a medicationSearchFromDate in the defined format
    And the medicationSearchFromDate is less than or equal to the current date
    # SCAL: GPC-STR-TST-MED-03 | Test data: 9690937286

  @GPC-STR-TST-MED-04 @medications @skip_api_access_not_exposed
  Scenario: Request medication by future date rejected
    Given I am enabled to access GP Connect data and try to request medications by a future date
    Then I am prevented from submitting the request
    # SCAL: GPC-STR-TST-MED-04 | Test data: 9690937286

  @GPC-STR-TST-MED-05 @medications @skip_api_access_not_exposed
  Scenario: Requesting medication issues
    Given I am enabled to access GP Connect data and my use case does or does not require medication issues
    When I make the medication request
    Then the request sets includePrescriptionIssues to the appropriate value
    # SCAL: GPC-STR-TST-MED-05 | Test data: 9690937286

  @GPC-STR-TST-MED-07 @medications
  Scenario: No medication records
    Given I have received a successful medications response with an empty list
    When I display the information
    Then I display the empty reason
    # SCAL: GPC-STR-TST-MED-07 | Test data: 9690937308

  # ---------------------------------------------------------------------------
  # ALLERGY TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-ALG-01 @allergies
  Scenario: Request current allergies
    Given the user wishes to view current allergies
    When they select to access current allergies
    Then the request uses the includeAllergies parameter with includeResolvedAllergies set to false
    # SCAL: GPC-STR-TST-ALG-01 | Test data: 9690937308

  @GPC-STR-TST-ALG-02 @allergies
  Scenario: Request current and resolved allergies
    Given the user wishes to view all allergies including resolved
    When they select to access all allergies
    Then the request uses the includeAllergies parameter with includeResolvedAllergies set to true
    # SCAL: GPC-STR-TST-ALG-02 | Test data: 9690937308

  @GPC-STR-TST-ALG-03 @allergies
  Scenario: Handling resolved allergies
    Given I have received a response including resolved allergies
    When I display or use the allergy information
    Then my system identifies resolved allergies distinctly from current allergies
    And my system labels resolved allergies clearly
    And my system ensures resolved allergies cannot be used by decision support
    # SCAL: GPC-STR-TST-ALG-03 | Test data: 9690937308

  @GPC-STR-TST-ALG-04 @allergies @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Allergy data elements
    Given I have received a response with allergies
    When I display or use the allergy information
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-ALG-04 | Test data: 9690937308

  @GPC-STR-TST-ALG-07 @allergies
  Scenario: No data response
    Given I have received a response with an empty active allergies list
    When I display or use the response
    Then I recognise this as no active allergies recorded
    And I do not confuse no active allergies recorded with no known allergies
    # SCAL: GPC-STR-TST-ALG-07 | Test data: 9690937308

  @GPC-STR-TST-ALG-08 @allergies
  Scenario: Clinically asserted no known allergies
    Given I have received a response with a single code item indicating no known allergies
    When I display or use the response
    Then I recognise this as a clinical assertion of no known allergies
    # SCAL: GPC-STR-TST-ALG-08 | Test data: 9690937375

  # ---------------------------------------------------------------------------
  # INVESTIGATION TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-INV-01 @investigations
  Scenario: All investigations
    Given the user wishes to view all investigations
    When they request investigations
    Then the request uses the includeInvestigations parameter with no part parameters
    # SCAL: GPC-STR-TST-INV-01 | Test data: 9690937294

  @GPC-STR-TST-INV-02 @investigations
  Scenario: Investigations from a specified date
    Given the user wishes to view investigations from a specific date
    When they select with a from date
    Then the request uses investigationSearchPeriod.start only
    And the start date is less than or equal to the current date
    # SCAL: GPC-STR-TST-INV-02 | Test data: 9690937294

  @GPC-STR-TST-INV-03 @investigations
  Scenario: Investigations to a specified date
    Given the user wishes to view investigations up to a specific date
    When they select with a to date
    Then the request uses investigationSearchPeriod.end only
    And the end date is less than or equal to the current date
    # SCAL: GPC-STR-TST-INV-03 | Test data: 9690937286

  @GPC-STR-TST-INV-04 @investigations
  Scenario: Investigations in a date range
    Given the user wishes to view investigations for a specific period
    When they select with from and to dates
    Then the request uses both investigationSearchPeriod.start and investigationSearchPeriod.end part parameters
    And the end date is less than or equal to the current date
    And the start date is less than or equal to the end date
    # SCAL: GPC-STR-TST-INV-04 | Test data: 9690937286

  @GPC-STR-TST-INV-05 @investigations
  Scenario: No investigations available
    Given the user or system requests investigations
    When I receive a response with no investigation data
    Then the response is processed confirming the reason for no data
    # SCAL: GPC-STR-TST-INV-05 | Test data: 9690937308

  @GPC-STR-TST-INV-06 @investigations
  Scenario: Supported investigations elements
    Given I have made a valid investigations request
    When I receive a successful response
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-INV-06 | Test data: 9690937286

  @GPC-STR-TST-INV-07 @investigations
  Scenario: Invalid parameter investigations
    Given I have made a request for investigations with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-INV-07 | Test data: 9690937294

  @GPC-STR-TST-INV-09 @investigations
  Scenario: Forwards compatibility investigations
    Given I have sent a valid request for investigations
    When the provider returns a warning that investigations is not supported
    Then I handle the warning gracefully
    # SCAL: GPC-STR-TST-INV-09 | Test data: 9658218873

  # ---------------------------------------------------------------------------
  # REFERRAL TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-REF-01 @referrals @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: All referrals
    Given the user wishes to view all referrals
    When they request referrals
    Then the request uses the includeReferrals parameter with no part parameters
    # SCAL: GPC-STR-TST-REF-01 | Test data: 9690937294

  @GPC-STR-TST-REF-02 @referrals @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Referrals from a specified date
    Given the user wishes to view referrals from a specific date
    When they select with a from date
    Then the request uses referralSearchPeriod.start only
    And the start date is less than or equal to the current date
    # SCAL: GPC-STR-TST-REF-02 | Test data: 9690937286

  @GPC-STR-TST-REF-03 @referrals @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Referrals to a specified date
    Given the user wishes to view referrals up to a specific date
    When they select with a to date
    Then the request uses referralSearchPeriod.end only
    And the end date is less than or equal to the current date
    # SCAL: GPC-STR-TST-REF-03 | Test data: 9690937286

  @GPC-STR-TST-REF-04 @referrals @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Referrals in a date range
    Given the user wishes to view referrals for a specific period
    When they select with from and to dates
    Then the request uses both referralSearchPeriod.start and referralSearchPeriod.end part parameters
    And the end date is less than or equal to the current date
    And the start date is less than or equal to the end date
    # SCAL: GPC-STR-TST-REF-04 | Test data: 9690937286

  @GPC-STR-TST-REF-05 @referrals @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: No referrals available
    Given the user or system requests referrals
    When I receive a response with no referral data
    Then the response is processed confirming the reason for no data
    # SCAL: GPC-STR-TST-REF-05 | Test data: 9690937308

  @GPC-STR-TST-REF-06 @referrals @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Supported referrals elements
    Given I have made a valid referrals request
    When I receive a successful response
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-REF-06 | Test data: 9690937294

  @GPC-STR-TST-REF-07 @referrals @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Invalid parameter referrals
    Given I have made a request for referrals with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-REF-07 | Test data: 9690937294

  @GPC-STR-TST-REF-09 @referrals
  Scenario: Forwards compatibility referrals
    Given I have sent a valid request for referrals
    When the provider returns a warning that referrals is not supported
    Then I handle the warning gracefully
    # SCAL: GPC-STR-TST-REF-09 | Test data: 9658218873

  # ---------------------------------------------------------------------------
  # DIARY ENTRY TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-DIA-01 @diary_entries @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: All diary entries
    Given the user wishes to view all diary entries
    When they request diary entries
    Then the request uses the includeDiaryEntries parameter with no part parameters
    # SCAL: GPC-STR-TST-DIA-01 | Test data: 9690937294

  @GPC-STR-TST-DIA-02 @diary_entries @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Diary entries to a specified date
    Given the user wishes to view diary entries up to a specific date
    When they select with a to date
    Then the request uses the diaryEntriesSearchDate parameter
    And the search date is greater than or equal to the current date
    # SCAL: GPC-STR-TST-DIA-02 | Test data: 9690937286

  @GPC-STR-TST-DIA-03 @diary_entries @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: No diary entries available
    Given the user or system requests diary entries
    When I receive a response with no diary entry data
    Then the response is processed confirming the reason for no data
    # SCAL: GPC-STR-TST-DIA-03 | Test data: 9690937308

  @GPC-STR-TST-DIA-04 @diary_entries @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Supported diary entry elements
    Given I have made a valid diary entries request
    When I receive a successful response
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-DIA-04 | Test data: 9690937286

  @GPC-STR-TST-DIA-05 @diary_entries @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Invalid parameter diary entries
    Given I have made a request for diary entries with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-DIA-05 | Test data: 9690937294

  @GPC-STR-TST-DIA-07 @diary_entries
  Scenario: Forwards compatibility diary entries
    Given I have sent a valid request for diary entries
    When the provider returns a warning that diary entries is not supported
    Then I handle the warning gracefully
    # SCAL: GPC-STR-TST-DIA-07 | Test data: 9658218873

  # ---------------------------------------------------------------------------
  # PROBLEM TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-PRB-01 @problems @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Request all problems
    Given the user wishes to view all problems
    When they request problems
    Then the request uses the includeProblems parameter only
    # SCAL: GPC-STR-TST-PRB-01 | Test data: 9690937286

  @GPC-STR-TST-PRB-02 @problems @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Request with part parameters
    Given the user wishes to filter problems by status and significance
    When they request problems with part parameters
    Then the request uses the includeProblems parameter with filterStatus and filterSignificance
    # SCAL: GPC-STR-TST-PRB-02 | Test data: 9690937286

  @GPC-STR-TST-PRB-03 @problems @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Request with multiple parameters
    Given the user wishes to request problems with multiple filter values
    When they request problems with active and minor status and inactive and major significance
    Then the request uses the includeProblems parameter with the combined filter values
    # SCAL: GPC-STR-TST-PRB-03 | Test data: 9690937286

  @GPC-STR-TST-PRB-04 @problems @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: No problems available
    Given the user or system requests problems
    When I receive a response with no problem data
    Then the response is processed confirming the reason for no data
    # SCAL: GPC-STR-TST-PRB-04 | Test data: 9690937308

  @GPC-STR-TST-PRB-05 @problems @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Invalid parameter problems
    Given I have made a request for problems with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-PRB-05 | Test data: 9690937286

  Rule: Problem Confidentiality and Compatibility

    Background: Valid problems request sent
      Given I have sent a valid request for problems

    @GPC-STR-TST-PRB-06 @problems
    Scenario: Confidential problem item warning
      When I receive a confidential items warning for a problem
      Then I make the user aware of the confidential items warning
      # SCAL: GPC-STR-TST-PRB-06 | Test data: No Data

    @GPC-STR-TST-PRB-07 @problems
    Scenario: Confidential item linked to a problem warning
      When I receive a confidential items warning for an item linked to a problem
      Then I make the user aware of the confidential items warning
      # SCAL: GPC-STR-TST-PRB-07 | Test data: No Data

    @GPC-STR-TST-PRB-08 @problems
    Scenario: Forwards compatibility problems
      When the provider returns a warning that problems is not supported
      Then I handle the warning gracefully
      # SCAL: GPC-STR-TST-PRB-08 | Test data: 9658218873

  @GPC-STR-TST-PRB-09 @problems @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Problem header data elements
    Given I have received a response with problems
    When I display or use the problem information
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-PRB-09 | Test data: N/A

  # ---------------------------------------------------------------------------
  # IMMUNISATION TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-IMM-01 @immunisations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Request immunisations
    Given the user wishes to view immunisations
    When they request immunisations
    Then the request uses the includeImmunisations parameter
    # SCAL: GPC-STR-TST-IMM-01 | Test data: 9690938207

  @GPC-STR-TST-IMM-02 @immunisations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Request immunisations with part parameters
    Given the user wishes to filter immunisations by notGiven and status
    When they request immunisations with part parameters
    Then the request uses the includeImmunisations parameter with notGiven and status
    # SCAL: GPC-STR-TST-IMM-02 | Test data: 9690938207

  @GPC-STR-TST-IMM-03 @immunisations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Supported immunisation data elements
    Given I have made a valid immunisations request
    When I receive a successful response
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-IMM-03 | Test data: 9690938207

  @GPC-STR-TST-IMM-04 @immunisations
  Scenario: Presenting immunisations not given
    Given I have received a response including immunisations not given
    When I display or use the immunisation information
    Then my system distinguishes between immunisations given and immunisations not given
    # SCAL: GPC-STR-TST-IMM-04 | Test data: 9690938207

  @GPC-STR-TST-IMM-05 @immunisations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: No immunisations available
    Given the user or system requests immunisations
    When I receive a response with no immunisation data
    Then the response is processed confirming the reason for no data
    # SCAL: GPC-STR-TST-IMM-05 | Test data: 9658218903

  @GPC-STR-TST-IMM-06 @immunisations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Invalid parameter immunisations
    Given I have made a request for immunisations with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-IMM-06 | Test data: 9690938207

  @GPC-STR-TST-IMM-07 @immunisations
  Scenario: Confidential immunisations item warning
    Given I have sent a valid request for immunisations
    When I receive a confidential items warning for immunisations
    Then I make the user aware of the confidential items warning
    # SCAL: GPC-STR-TST-IMM-07 | Test data: No Data

  @GPC-STR-TST-IMM-08 @immunisations
  Scenario: Forwards compatibility immunisations
    Given I have sent a valid request for immunisations
    When the provider returns a warning that immunisations is not supported
    Then I handle the warning gracefully
    # SCAL: GPC-STR-TST-IMM-08 | Test data: 9658218873

  # ---------------------------------------------------------------------------
  # UNCATEGORISED DATA TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-UNC-01 @uncategorised_data
  Scenario: Request all uncategorised data
    Given the user wishes to view all uncategorised data
    When they request uncategorised data
    Then the request uses the includeUncategorisedData parameter
    # SCAL: GPC-STR-TST-UNC-01 | Test data: 9690937286, 9690937294

  @GPC-STR-TST-UNC-02 @uncategorised_data
  Scenario: Uncategorised data from a specified date
    Given the user wishes to view uncategorised data from a specific date
    When they select with a from date
    Then the request uses uncategorisedDataSearchPeriod.start only
    And the start date is less than or equal to the current date
    # SCAL: GPC-STR-TST-UNC-02 | Test data: 9690937286

  @GPC-STR-TST-UNC-03 @uncategorised_data
  Scenario: Uncategorised data up to a specified date
    Given the user wishes to view uncategorised data up to a specific date
    When they select with a to date
    Then the request uses uncategorisedDataSearchPeriod.end only
    And the end date is less than or equal to the current date
    # SCAL: GPC-STR-TST-UNC-03 | Test data: 9690937286

  @GPC-STR-TST-UNC-04 @uncategorised_data
  Scenario: Uncategorised data for a date range
    Given the user wishes to view uncategorised data for a specific period
    When they select with from and to dates
    Then the request uses both uncategorisedDataSearchPeriod.start and uncategorisedDataSearchPeriod.end
    And the end date is less than or equal to the current date
    And the start date is less than or equal to the end date
    # SCAL: GPC-STR-TST-UNC-04 | Test data: 9690937286

  @GPC-STR-TST-UNC-05 @uncategorised_data
  Scenario: No uncategorised data available
    Given the user or system requests uncategorised data
    When I receive a response with no uncategorised data
    Then the response is processed confirming the reason for no data
    # SCAL: GPC-STR-TST-UNC-05 | Test data: 9690937286

  @GPC-STR-TST-UNC-06 @uncategorised_data
  Scenario: Representing hierarchical records
    Given I have received a response with hierarchical uncategorised data
    When I display or use the uncategorised data
    Then I represent the hierarchical structure correctly
    # SCAL: GPC-STR-TST-UNC-06 | Test data: No Data

  @GPC-STR-TST-UNC-07 @uncategorised_data
  Scenario: Representing blood pressure readings
    Given I have received a response with blood pressure readings in uncategorised data
    When I display or use the uncategorised data
    Then I represent the blood pressure readings correctly
    # SCAL: GPC-STR-TST-UNC-07 | Test data: No Data

  @GPC-STR-TST-UNC-08 @uncategorised_data
  Scenario: Supported uncategorised data elements
    Given I have made a valid uncategorised data request
    When I receive a successful response
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-UNC-08 | Test data: 9690937286

  @GPC-STR-TST-UNC-09 @uncategorised_data
  Scenario: Invalid parameter uncategorised data
    Given I have made a request for uncategorised data with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-UNC-09 | Test data: 9690937286

  @GPC-STR-TST-UNC-10 @uncategorised_data
  Scenario: Confidential uncategorised data item warning
    Given I have sent a valid request for uncategorised data
    When I receive a confidential items warning for uncategorised data
    Then I make the user aware of the confidential items warning
    # SCAL: GPC-STR-TST-UNC-10 | Test data: No Data

  @GPC-STR-TST-UNC-11 @uncategorised_data
  Scenario: Forwards compatibility uncategorised data
    Given I have sent a valid request for uncategorised data
    When the provider returns a warning that uncategorised data is not supported
    Then I handle the warning gracefully
    # SCAL: GPC-STR-TST-UNC-11 | Test data: 9658218873

  # ---------------------------------------------------------------------------
  # CONSULTATION TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-ENC-01 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Request all consultations
    Given the user wishes to view all consultations
    When they request consultations
    Then the request uses the includeConsultations parameter
    # SCAL: GPC-STR-TST-ENC-01 | Test data: 9690937286

  @GPC-STR-TST-ENC-02 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Consultations from a specified date
    Given the user wishes to view consultations from a specific date
    When they select with a from date
    Then the request uses consultationSearchPeriod.start only
    And the start date is less than or equal to the current date
    # SCAL: GPC-STR-TST-ENC-02 | Test data: 9690937286

  @GPC-STR-TST-ENC-03 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Consultations up to a specified date
    Given the user wishes to view consultations up to a specific date
    When they select with a to date
    Then the request uses consultationSearchPeriod.end only
    And the end date is less than or equal to the current date
    # SCAL: GPC-STR-TST-ENC-03 | Test data: 9690937286

  @GPC-STR-TST-ENC-04 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Consultations for a date range
    Given the user wishes to view consultations for a specific period
    When they select with from and to dates
    Then the request uses both consultationSearchPeriod.start and consultationSearchPeriod.end
    And the end date is less than or equal to the current date
    And the start date is less than or equal to the end date
    # SCAL: GPC-STR-TST-ENC-04 | Test data: 9690937286

  @GPC-STR-TST-ENC-05 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Consultations by most recent
    Given the user wishes to view the most recent consultations
    When they request consultations with a count
    Then the request uses the includeNumberOfMostRecent parameter
    # SCAL: GPC-STR-TST-ENC-05 | Test data: 9690937286

  @GPC-STR-TST-ENC-06 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: No consultations available
    Given the user or system requests consultations
    When I receive a response with no consultation data
    Then the response is processed confirming the reason for no data
    # SCAL: GPC-STR-TST-ENC-06 | Test data: 9690937308

  @GPC-STR-TST-ENC-07 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Supported consultations elements
    Given I have made a valid consultations request
    When I receive a successful response
    Then I display all key information commensurate with the original record
    # SCAL: GPC-STR-TST-ENC-07 | Test data: 9690937286

  @GPC-STR-TST-ENC-08 @consultations @skip_cededim_did_not_implement_so_out_of_scope
  Scenario: Invalid parameter consultations
    Given I have made a request for consultations with invalid parameters
    When I receive an invalid parameter error response
    Then I handle the error gracefully
    # SCAL: GPC-STR-TST-ENC-08 | Test data: 9690937286

  Rule: Consultation Confidentiality and Compatibility

    Background: Valid consultations request sent
      Given I have sent a valid request for consultations

    @GPC-STR-TST-ENC-09 @consultations
    Scenario: Confidential consultation warning
      When I receive a confidential items warning for a consultation
      Then I make the user aware of the confidential items warning
      # SCAL: GPC-STR-TST-ENC-09 | Test data: No Data

    @GPC-STR-TST-ENC-10 @consultations
    Scenario: Confidential item within a consultation warning
      When I receive a confidential items warning for an item within a consultation
      Then I make the user aware of the confidential items warning
      # SCAL: GPC-STR-TST-ENC-10 | Test data: No Data

    @GPC-STR-TST-ENC-11 @consultations
    Scenario: Forwards compatibility consultations
      When the provider returns a warning that consultations is not supported
      Then I handle the warning gracefully
      # SCAL: GPC-STR-TST-ENC-11 | Test data: 9658218873

  # ---------------------------------------------------------------------------
  # LINKAGE TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-LNK01 @linkages
  Scenario: Immunisations linked to problems
    Given I have received a response containing immunisations linked to problems
    When I display or use the linked data
    Then I present the linkage between immunisations and problems correctly
    # SCAL: GPC-STR-TST-LNK01 | Test data: 9690937286

  @GPC-STR-TST-LNK02 @linkages
  Scenario: Uncategorised data linked to problems
    Given I have received a response containing uncategorised data linked to problems
    When I display or use the linked data
    Then I present the linkage between uncategorised data and problems correctly
    # SCAL: GPC-STR-TST-LNK02 | Test data: 9690937286

  @GPC-STR-TST-LNK03 @linkages
  Scenario: Consultations linked to problems
    Given I have received a response containing consultations linked to problems
    When I display or use the linked data
    Then I present the linkage between consultations and problems correctly
    # SCAL: GPC-STR-TST-LNK03 | Test data: 9690937286

  @GPC-STR-TST-LNK04 @linkages
  Scenario: Investigations linked to problems
    Given I have received a response containing investigations linked to problems
    When I display or use the linked data
    Then I present the linkage between investigations and problems correctly
    # SCAL: GPC-STR-TST-LNK04 | Test data: 9690937286

  @GPC-STR-TST-LNK05 @linkages
  Scenario: Referrals linked to problems
    Given I have received a response containing referrals linked to problems
    When I display or use the linked data
    Then I present the linkage between referrals and problems correctly
    # SCAL: GPC-STR-TST-LNK05 | Test data: 9690937286

  @GPC-STR-TST-LNK06 @linkages
  Scenario: Diary entries linked to problems
    Given I have received a response containing diary entries linked to problems
    When I display or use the linked data
    Then I present the linkage between diary entries and problems correctly
    # SCAL: GPC-STR-TST-LNK06 | Test data: 9690937286

  @GPC-STR-TST-LNK07 @linkages
  Scenario: Medications linked to problems
    Given I have received a response containing medications linked to problems
    When I display or use the linked data
    Then I present the linkage between medications and problems correctly
    # SCAL: GPC-STR-TST-LNK07 | Test data: 9690937286

  @GPC-STR-TST-LNK08 @linkages
  Scenario: Allergies linked to problems
    Given I have received a response containing allergies linked to problems
    When I display or use the linked data
    Then I present the linkage between allergies and problems correctly
    # SCAL: GPC-STR-TST-LNK08 | Test data: 9690937286

  # ---------------------------------------------------------------------------
  # SEARCH QUERY TESTS
  # ---------------------------------------------------------------------------

  @GPC-STR-TST-SRC01-01 @search_queries
  Scenario: Predefined search query 1
    Given the user wishes to run a predefined search
    When they request the last 3 consultations and all problems and all allergies including resolved for the last 365 days
    Then the request conforms to the specification with the combined parameters
    # SCAL: GPC-STR-TST-SRC01-01 | Test data: 9690937286

  @GPC-STR-TST-SRC01-02 @search_queries
  Scenario: Predefined search query 2
    Given the user wishes to run a predefined search with additional clinical areas
    When they request the last 3 consultations, all problems, all allergies including resolved for the last 365 days, plus immunisations and uncategorised data
    Then the request conforms to the specification with the combined parameters
    # SCAL: GPC-STR-TST-SRC01-02 | Test data: 9690937286

  @GPC-STR-TST-SRC02-01 @search_queries
  Scenario: Multiple parameter search including consultations
    Given the user wishes to request multiple clinical areas including consultations
    When I construct the request
    Then the request must not include referralSearchPeriod, investigationSearchPeriod, diaryEntriesSearchDate, uncategorisedDataSearchPeriod, or consultationSearchPeriod part parameters when consultations are included
    # SCAL: GPC-STR-TST-SRC02-01 | Test data: 9690937286

  @GPC-STR-TST-SRC02-02 @search_queries
  Scenario: Multiple parameter search including problems
    Given the user wishes to request multiple clinical areas including problems
    When I construct the request
    Then the request conforms to the specification with the combined parameters for problems and other clinical areas
    # SCAL: GPC-STR-TST-SRC02-02 | Test data: 9690937286

  @GPC-STR-TST-SRC02-03 @search_queries
  Scenario: Multiple clinical area search without problems or consultations
    Given the user wishes to request multiple clinical areas without problems or consultations
    When I construct the request
    Then the request conforms to the specification with the combined parameters for the selected clinical areas
    # SCAL: GPC-STR-TST-SRC02-03 | Test data: 9690937286
