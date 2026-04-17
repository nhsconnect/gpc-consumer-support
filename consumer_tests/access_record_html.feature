@access_record_html
Feature: Access Record HTML
  As a GP Connect consumer
  I want to access a patient's HTML care record
  So that I can view their clinical information from the registered GP practice

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-HTML
  # Demonstrator: v0.7/v1.2 - Dr Legg's Surgery (ODS: A20047)

  @GPC-ARHTML-01-TEST @patient_demographics
  Scenario: GPC-ARHTML-01 - Patient tracing - Success Scenario
    Given I have traced a Patient as per the recommended means in the GPC API spec in the last 24 hours
    When I try to retrieve a patient's record from its registered GP practice
    Then I am able to retrieve the patient's record
    # SCAL: GPC-ARHTML-01 | Test data: 9658218873

  @GPC-ARHTML-02-TEST @patient_demographics
  Scenario: GPC-ARHTML-02 - Patient tracing - Exception Scenario
    Given I have NOT traced a Patient as per the recommended means in the GPC API spec in the last 24 hours
    When I try to retrieve a patient's record from its registered GP practice
    Then I am NOT able to retrieve the patient's record
    # SCAL: GPC-ARHTML-02 | Test data: 9658218873

  @GPC-ARHTML-03-TEST @patient_demographics
  Scenario: GPC-ARHTML-03 - GP Organisation identification
    Given I have a Patient's NHS number
    And I want to retrieve a Patient's record from its registered GP Practice
    When I try to find the Patient's registered GP Practice using the patient's NHS number
    Then I get the ODS code of the Patient's registered GP Practice in response
    And I can use the ODS code of the registered GP Practice to request patient's information from the GP Practice
    # SCAL: GPC-ARHTML-03 | Test data: 9658218873

  @GPC-ARHTML-04-TEST @patient_demographics
  Scenario: GPC-ARHTML-04 - Minimum Patient Demographics
    Given I want to view a patient's record and its demographics
    When I retrieve a patient's record from its registered GP practice
    Then I display the patient's details on my system as per the CUI guidance
    # SCAL: GPC-ARHTML-04 | Test data: 9658218873

  @GPC-ARHTML-05-TEST @patient_demographics
  Scenario: GPC-ARHTML-05 - Demographic cross checking - details do not match
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with the patient's details
    And I compare the returned structured patient demographic data against the demographic data held in the consumer system
    When the differences exist in any of the following fields: Family Name, Given Name, Gender, Birth Date, GP Practice Code
    Then the consumer system MUST show an alert or warning
    And provide details of which fields and values are different between the two systems
    # SCAL: GPC-ARHTML-05 | Test data: 9658218873

  @GPC-ARHTML-06-TEST @data_sharing
  Scenario: GPC-ARHTML-06 - Data Sharing - Success Scenario
    Given that data sharing agreements are in place between my organisation and the GP Practice from which I want to retrieve a patient's record
    When I try to retrieve patient's information from their registered GP Practice
    Then the data sharing agreements are checked by Spine Security Proxy
    And I can retrieve the Patient's record only if the data sharing agreement between my organisation and the given GP Practice is set up on Spine Security Proxy
    # SCAL: GPC-ARHTML-06 | Test data: 9658218873

  @GPC-ARHTML-07-TEST @data_sharing @error_handling
  Scenario: GPC-ARHTML-07 - Data Sharing - Exception Scenario
    Given that data sharing agreements are NOT in place between my organisation and the GP Practice from which I want to retrieve a patient's record
    And I try to retrieve patient's information from their registered GP Practice
    And the data sharing agreements are checked by Spine Security Proxy
    When I receive an exception in the API response that the data sharing agreement does not exist in SSP
    Then I am able to handle this error gracefully on my system
    # SCAL: GPC-ARHTML-07 | Test data: 9658218873

  @GPC-ARHTML-08-TEST @gp2gp_transfer
  Scenario: GPC-ARHTML-08 - Get an in-transit Patient record
    Given that a patient has registered with a new GP Practice Y
    And their patient record is being transferred from the previous GP Practice X to Y GP Practice
    And I access the Patient's record from Y GP Practice
    And only details from the current GP record of the Y GP Practice are returned as old GP record of X is still in transit and not committed
    When I see a banner message in the response specifying patient record transfer from previous GP Practice not yet complete
    Then I display the banner as per the CUI guidance
    # SCAL: GPC-ARHTML-08 | Test data: 9658219691

  @GPC-ARHTML-09-TEST @ui_display
  Scenario: GPC-ARHTML-09 - Patient banner
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with the patient's details
    When I display the received patient's details from the API response on my system
    Then my system MUST present a patient banner above the HTML content returned from the GP Connect APIs in line with the CUI guidance
    And it applies to all the HTML views
    # SCAL: GPC-ARHTML-09 | Test data: 9658218873

  @GPC-ARHTML-10-TEST @ui_display
  Scenario: GPC-ARHTML-10 - Content banner - display section banner and subsection banner
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with patient's details
    And the API response has section banner and subsection banner
    When I create HTML views
    Then I display the section banner above the relevant section
    And I display the subsection banner above the relevant subsections with the expected styling as per the API spec
    # SCAL: GPC-ARHTML-10 | Test data: 9658218873

  @GPC-ARHTML-11-TEST @date_filters
  Scenario: GPC-ARHTML-11 - Sections with date filters
    Given I want to view a Patient's record
    When I use the GPC API to request a Patient's record from their registered GP Practice for any section
    Then I can apply date filters to the following sections only: Administrative items, Clinical items, Encounters, Medications All Medication, Medications All Medication Issues, Observations, Problems and issues Major inactive, Problems and issues Other inactive, Referrals
    And I receive and display details for the relevant section for the applied date filter
    # SCAL: GPC-ARHTML-11 | Test data: 9658218873

  @GPC-ARHTML-12-TEST @date_filters @ui_display
  Scenario: GPC-ARHTML-12 - Date banner - display date banner with start date and end date
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I have applied a date filter with a start date and an end date for a section in the API request
    And I receive an API response with patient's details
    And the API response has date banner for the given section
    When I create HTML views
    Then I display the date banner above the relevant section with start and end dates with the expected styling as per the API spec
    # SCAL: GPC-ARHTML-12 | Test data: 9658218873

  @GPC-ARHTML-13-TEST @date_filters @ui_display
  Scenario: GPC-ARHTML-13 - Date banner - display date banner with start date and no end date
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I have applied a date filter with a start date and no end date for a section in the API request
    And I receive an API response with patient's details
    And the API response has date banner for the given section
    When I create HTML views
    Then I display the date banner above the relevant section with start date only displaying in the text "All data items from [Start Date]" with the expected styling as per the API spec
    # SCAL: GPC-ARHTML-13 | Test data: 9658218873

  @GPC-ARHTML-14-TEST @date_filters @ui_display
  Scenario: GPC-ARHTML-14 - Date banner - display date banner with no start date and an end date
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I have not applied a date filter for a section in the API request
    And I receive an API response with patient's details
    And the API response has date banner for the given section
    When I create HTML views
    Then I display the date banner above the relevant section that does not display any date range and its text reads as "Date filter not applied" with the expected styling as per the API spec
    And I display another date banner with no dates whose text reads as "All relevant items"
    # SCAL: GPC-ARHTML-14 | Test data: 9658218873

  @GPC-ARHTML-15-TEST @date_filters @ui_display
  Scenario: GPC-ARHTML-15 - Date banner - display date banner with no date ranges applied
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with patient's details
    And the API response has a section from which some data has been excluded
    And it has an exclusions banner
    When I create HTML views
    Then I display the exclusion banner above the given section with the expected styling as per the API spec
    # SCAL: GPC-ARHTML-15 | Test data: 9658218873

  @GPC-ARHTML-16-TEST @ui_display
  Scenario: GPC-ARHTML-16 - Exclusions banner
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with patient's details
    And the API response has a section from which some data has been excluded
    And it has an exclusions banner
    When I create HTML views
    Then I display the exclusion banner above the given section with the expected styling as per the API spec
    # SCAL: GPC-ARHTML-16 | Test data: 9658219705

  @GPC-ARHTML-17-TEST @http_headers
  Scenario: GPC-ARHTML-17 - Http Header Pre-requisites
    Given I want to view a Patient's record
    When I try to retrieve a patient's record from their registered GP Practice
    Then in the header of the API request I must provide the following details: Ssp-TraceID, Ssp-From, Ssp-To, Ssp-InteractionID
    # SCAL: GPC-ARHTML-17 | Test data: 9658218873

  @GPC-ARHTML-18-TEST @api_request
  Scenario: GPC-ARHTML-18 - Get Care Record API Request items
    Given I want to view a Patient's record
    And I have provided the required items in the header of the API Request
    When I try to retrieve a patient's record from its GP Practice
    Then the API request payload MUST have a set of Parameters conforming to the gpconnect-carerecord-operation-1 profiled OperationDefinition
    And include Parameter patientNHSNumber
    And include Parameter recordSection
    And the request payload MAY have the optional parameter timePeriod
    # SCAL: GPC-ARHTML-18 | Test data: 9658218873

  @GPC-ARHTML-19-TEST @api_request
  Scenario: GPC-ARHTML-19 - Get Care Record API Request - Business Rules
    Given I want to view a Patient's record
    And I have provided the required items of the API Request
    When I try to retrieve a patient's record from its GP Practice
    Then the API request payload MUST meet the following business rules: NHS number is in valid format, NHS number is verified, patient record is retrieved from nominated primary care provider, record section is from approved valueset, and time period rules are met
    # SCAL: GPC-ARHTML-19 | Test data: 9658218873

  @GPC-ARHTML-20-TEST @api_response
  Scenario: GPC-ARHTML-20 - Success Scenario
    Given I want to view a Patient's record
    And I create a valid GPConnect API Request
    When I try to retrieve a patient's record from its GP Practice
    Then the API response includes a 200 OK HTTP status code
    And the care record section as valid XHTML in line with the FHIR Narrative guidance
    And relevant GP Connect StructureDefinition profile details in the meta fields
    And Patient, Practitioner and Organization details in a searchset Bundle
    And I am able to display the details successfully in relevant HTML views
    # SCAL: GPC-ARHTML-20 | Test data: 9658218873

  @GPC-ARHTML-21-TEST @error_handling
  Scenario: GPC-ARHTML-21 - Exception Scenario
    Given I want to view a Patient's record
    And I create a GPC API Request that does not meet one or more business rules
    When I try to retrieve a patient's record from its GP Practice
    Then the API response must return an OperationOutcome resource that provides additional detail
    And error codes are as per the Development Guidance Error Handling
    # SCAL: GPC-ARHTML-21 | Test data: 9658218873

  @GPC-ARHTML-22-TEST @ui_display
  Scenario: GPC-ARHTML-22 - CSS IDs and Classes
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with patient's details
    When I display the html from the API response on my system
    Then I must apply CSS IDs and Classes as per the GPConnect API spec
    # SCAL: GPC-ARHTML-22 | Test data: 9658218873

  @GPC-ARHTML-23-TEST @ui_display
  Scenario: GPC-ARHTML-23 - HTML Views with a single table
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with patient's details
    When I create HTML views with a single table or section
    Then I am able to apply the structure: Section title, GP transfer banner, Content banner, Date banner, Exclusion banner, Table
    And the following views have a single section: Encounters, Clinical items, Referrals, Observations, Immunisations, Administrative items, Emergency Codes
    # SCAL: GPC-ARHTML-23 | Test data: 9658218873

  @GPC-ARHTML-24-TEST @ui_display
  Scenario: GPC-ARHTML-24 - HTML Views with multiple tables
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I receive an API response with patient's details
    When I create HTML views with multiple tables or sections
    Then I am able to apply the structure: Section title, GP transfer banner, Content banner, Subsection with title and banners, Table
    And the following views have multiple sections: Summary, problems and issues, allergies and adverse reactions, medications
    # SCAL: GPC-ARHTML-24 | Test data: 9658218873

  @GPC-ARHTML-25-TEST @ui_display
  Scenario: GPC-ARHTML-25 - Section and subsection title
    Given I have retrieved a patient's record from their GP Practice using GPConnect
    When I display the patient's details in HTML View
    Then any section title is inside an "h1" tag
    And subsection titles are inside an "h2" tag
    # SCAL: GPC-ARHTML-25 | Test data: 9658218873

  @GPC-ARHTML-26-TEST @ui_display
  Scenario: GPC-ARHTML-26 - Display all content supplied by the provider
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    When I receive an API response with patient's details
    Then I must display all the content provided by the GP Practice in the API response
    # SCAL: GPC-ARHTML-26 | Test data: 9658218873

  @GPC-ARHTML-27-TEST @ui_display
  Scenario: GPC-ARHTML-27 - Common User Interface Guidance
    Given I have retrieved a patient's record from its GP Practice using GPConnect
    When I display the API response in HTML View
    Then I am able to follow Common User Interface (CUI) guidance documents
    # SCAL: GPC-ARHTML-27 | Test data: 9658218873

  @GPC-ARHTML-28-TEST @ui_display
  Scenario: GPC-ARHTML-28 - Minimum Display Resolution
    Given I have retrieved a patient's record from its GP Practice using GPConnect
    When I display the API response on a laptop or display computer
    Then the computer is capable of operating at a minimum display resolution of 1024 x 768
    And has a keyboard and pointing device
    # SCAL: GPC-ARHTML-28 | Test data: 9658218873

  @GPC-ARHTML-29-TEST @summary
  Scenario: GPC-ARHTML-29 - Get Summary
    Given I want to view a summary of patient's clinical information
    And I retrieve a patient's summary information from their registered GP Practice using GPConnect
    When I am able to view the following in the API response: Last 3 Encounters, Active Problems and Issues, Major Inactive Problems and Issues, Current Allergies and Adverse Reactions, Acute Medication Last 12 Months, Current Repeat Medications
    Then I am able to display them on my system as per the HTML guidance for the resources
    # SCAL: GPC-ARHTML-29 | Test data: 9658218873

  @GPC-ARHTML-30-TEST @encounters @date_filters
  Scenario: GPC-ARHTML-30 - Get Encounters - with date filter
    Given I want to view encounters from patient's clinical information
    And I do pass a date filter for encounters
    When I retrieve a patient's encounter section from its GP Practice using GPConnect API
    Then I receive all the relevant encounters that fall within the date filter applied
    And the API response has a populated table with columns: Date descending, Title, Details
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-30 | Test data: 9658218873

  @GPC-ARHTML-30-1-TEST @encounters
  Scenario: GPC-ARHTML-30/1 - Get Encounters - without date filter
    Given I want to view encounters from patient's clinical information
    And I do NOT pass a date filter for encounters
    When I retrieve a patient's encounter section from its GP Practice using GPConnect API
    Then I receive all the relevant encounters in the API response
    And the API response has a populated table with columns: Date descending, Title, Details
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-30 | Test data: 9658218873

  @GPC-ARHTML-31-TEST @clinical_items @date_filters
  Scenario: GPC-ARHTML-31 - Get Clinical Items - with date filter
    Given I want to view clinical items from patient's record
    And I do pass a date filter for the clinical items
    When I retrieve a patient's clinical items section from their GP Practice using GPConnect API
    Then I receive all the relevant clinical items that fall within the date filter applied
    And the API response has a populated table with columns: Date descending, Entry, Details
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-31 | Test data: 9658218873

  @GPC-ARHTML-31-1-TEST @clinical_items
  Scenario: GPC-ARHTML-31/1 - Get Clinical Items - without date filter
    Given I want to view clinical items from patient's record
    And I do NOT pass a date filter for the clinical items
    When I retrieve a patient's clinical items section from their GP Practice using GPConnect API
    Then I receive all the relevant clinical items in the API response
    And the API response has a populated table with columns: Date descending, Entry, Details
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-31 | Test data: 9658218873

  Rule: Problems and Issues
    Background:
      Given I want to view problems and issues from patient's record

    @GPC-ARHTML-32-1-TEST @problems @date_filters
    Scenario: GPC-ARHTML-32/1 - Get Problems and Issues - with date filter
      And I do pass a date filter for the problems and issues
      When I retrieve a patient's problems and issues section from their GP Practice using GPConnect
      Then I receive all the relevant problems and issues that fall within the date filter applied
      And the API response has Active Problems and Issues section with columns: Start Date, End Date descending, Entry, Significance, Details
      And the API response has Inactive Problems and Issues section with columns: Start Date, End Date descending, Entry, Significance, Details
      # SCAL: GPC-ARHTML-32/1 | Test data: 9658218873

    @GPC-ARHTML-32-2-TEST @problems
    Scenario: GPC-ARHTML-32/2 - Get Problems and Issues - without date filter
      And I do NOT pass a date filter for the problems and issues
      When I retrieve a patient's problems and issues section from their GP Practice using GPConnect
      Then I receive all the relevant problems and issues in the API response
      And the API response has Active Problems and Issues section with columns: Start Date, End Date descending, Entry, Significance, Details
      And the API response has Inactive Problems and Issues section with columns: Start Date, End Date descending, Entry, Significance, Details
      # SCAL: GPC-ARHTML-32/2 | Test data: 9658218873

    @GPC-ARHTML-37-TEST @problems
    Scenario: GPC-ARHTML-37 - Get Problems and Issues - changes to sections and subsections v0.7.2
      And I do pass a date filter for the problems and issues
      When I retrieve a patient's problems and issues section from their GP Practice using GPConnect
      Then the API response has Active Problems and Issues, Major Inactive Problems and Issues, Other Inactive Problems and Issues sections
      And each section has a populated table with columns: Date descending, Entry, Significance, Details
      # SCAL: GPC-ARHTML-37 | Test data: 9658218873

  @GPC-ARHTML-33-TEST @allergies
  Scenario: GPC-ARHTML-33 - Get Allergies and Adverse Reactions
    Given I want to view allergies and adverse reactions of a patient from their patient record
    When I retrieve a patient's allergies and adverse reactions section from its GP Practice using GPConnect API
    Then I receive all the current and historic allergies and adverse reactions
    And the API response has Current Allergies and Adverse Reactions section with columns: Start Date descending, Details
    And the API response has Historical Allergies and Adverse Reactions section with columns: Start Date, End Date descending, Details
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-33 | Test data: 9658218873

  @GPC-ARHTML-34-TEST @medications
  Scenario: GPC-ARHTML-34 - Get Medications
    Given I want to view medications of a patient from their patient record
    When I retrieve a patient's medications section from its GP Practice using GPConnect
    Then I receive all patient's medications details in the API response
    And the API response has sections: Acute Medication Last 12 Months, Current Repeat Medication, Discontinued Repeat Medication, All Medication, All Medication Issues
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-34 | Test data: 9658218873

  @GPC-ARHTML-35-1-TEST @referrals @date_filters
  Scenario: GPC-ARHTML-35/1 - Get Referrals - with date filter
    Given I want to view referrals from the patient's record
    And I do pass a date filter for the referrals
    When I retrieve a patient's referrals section from its GP Practice using GPConnect API
    Then I receive all the relevant referrals that fall within the date filter applied
    And the API response has a populated table with columns: Date descending, From, To, Priority, Details
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-35/1 | Test data: 9658218873

  @GPC-ARHTML-35-2-TEST @referrals
  Scenario: GPC-ARHTML-35/2 - Get Referrals - without date filter
    Given I want to view referrals from the patient's record
    And I do NOT pass a date filter for the referrals
    When I retrieve a patient's referrals section from its GP Practice using GPConnect API
    Then I receive all the relevant referrals in the API response
    And the API response has a populated table with columns: Date descending, From, To, Priority, Details
    And I am able to display them as per the HTML guidance
    # SCAL: GPC-ARHTML-35/2 | Test data: 9658218873

  Rule: Observations
    Background:
      Given I want to view observations for a Patient from their patient record

    @GPC-ARHTML-36-1-TEST @observations @date_filters
    Scenario: GPC-ARHTML-36/1 - Get Observations - with date filter
      And I do pass a date filter for the observations
      When I retrieve a patient's observations section from its GP Practice using GPConnect API
      Then I receive all the relevant observations that fall within the date filter applied
      And the API response has a populated table with columns: Date descending, Entry, Value, Details
      And I am able to display them as per the HTML guidance
      # SCAL: GPC-ARHTML-36/1 | Test data: 9658218873

    @GPC-ARHTML-36-2-TEST @observations
    Scenario: GPC-ARHTML-36/2 - Get Observations - without date filter
      And I do NOT pass a date filter for the observations
      When I retrieve a patient's observations section from its GP Practice using GPConnect API
      Then I receive all the relevant observations in the API response
      And the API response has a populated table with columns: Date descending, Entry, Value, Details
      And I am able to display them as per the HTML guidance
      # SCAL: GPC-ARHTML-36/2 | Test data: 9658218873

    @GPC-ARHTML-40-TEST @observations
    Scenario: GPC-ARHTML-40 - Get Observations - Display value and range v0.7.2
      And I do pass a date filter for the observations
      When I retrieve a patient's observations section from its GP Practice using GPConnect API
      Then the API response has a populated table with columns: Date descending, Entry, Value with unit, Range with unit where available, Details
      And I am able to display them as per the HTML guidance
      # SCAL: GPC-ARHTML-40 | Test data: 9658218873

  @GPC-ARHTML-38-TEST @gp2gp_transfer
  Scenario: GPC-ARHTML-38 - Get an in-transit Patient record - Display changed patient banner message v0.7.2
    Given that a patient has registered with a new GP Practice Y
    And their patient record is being transferred from the previous GP Practice X to Y GP Practice
    And I access the Patient's record from Y GP Practice
    When I see a banner message in the response specifying patient record transfer from previous GP practice not yet complete and information recorded before a date may be missing
    Then I display the banner as per the CUI guidance
    # SCAL: GPC-ARHTML-38 | Test data: 9658218873

  @GPC-ARHTML-39-TEST @date_filters @ui_display
  Scenario: GPC-ARHTML-39 - Date banner - banner text has word All removed v0.7.2
    Given I want to view a Patient's record
    And I try to retrieve a patient's record from its GP Practice
    And I have applied a date filter with a start date and no end date for a section in the API request
    And I receive an API response with patient's details
    And the API response has date banner for the given section
    When I create HTML views
    Then I display the date banner above the relevant section with start date only displaying in the text "Data items from [Start Date]" with the expected styling as per the API spec
    # SCAL: GPC-ARHTML-39 | Test data: 9658218873

  @GPC-ARHTML-41-TEST @summary
  Scenario: GPC-ARHTML-41 - Get Summary with Emergency codes
    Given I want to view a summary of patient's clinical information
    And I retrieve a patient's summary information from their registered GP Practice using GPConnect
    When I am able to view the following in the API response: Emergency codes, Last 3 Encounters, Active Problems and Issues, Major Inactive Problems and Issues, Current Allergies and Adverse Reactions, Acute Medication Last 12 Months, Current Repeat Medications
    Then I am able to display them on my system as per the HTML guidance for the resources
    # SCAL: GPC-ARHTML-29 | Test data: 9658218873

  @GPC-CORE-01-TEST @patient_demographics
  Scenario: GPC-CORE-01 - Deceased Patient
    Given I want to view a deceased patient's record
    When I retrieve a patient's record from its registered GP practice including a PDS trace
    Then the consuming application should not allow a GPC call to be made
    # SCAL: GPC-CORE-07 | Test data: 9658220290

  @GPC-CORE-05-TEST @patient_demographics
  Scenario: GPC-CORE-05 - Superseded NHS Number
    Given I want to view a patient's record
    When I retrieve a patient's record from its registered GP practice including a PDS trace
    Then the consuming application should allow a GPC call to be made using the latest NHS number
    # SCAL: GPC-CORE-5 | Test data: superseded NHS number 9658220215

  @GPC-STR-TST-GEN-10-HTML @patient_demographics
  Scenario: GPC-STR-TST-GEN-10 - Patient Demographics Deceased patient for HTML
    Given I access a patient which is recorded as deceased on PDS or on the local system
    When I am at a point where I would normally be able to access GP Connect
    Then the system prevents access to GP Connect
    And handles the prevention gracefully so the user is aware that GP Connect is not available for this patient
    # SCAL: GPC-CORE07-01 | Test data: 9658220290
