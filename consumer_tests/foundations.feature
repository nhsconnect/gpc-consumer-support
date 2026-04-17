@foundations
Feature: Foundations
  As a GP Connect consumer
  I want to perform foundational FHIR operations
  So that I can retrieve capability statements, find and read patients, practitioners, organisations, and locations

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Foundations
  # Uses v0.7/v1.2 test data (Dr Legg's Surgery, ODS: A20047)

  # --- Capability Statement ---

  @GPC-FOU-CAP-01-1 @capability_statement
  Scenario: GPC-FOU-CAP-01/1 - Get the FHIR capability statement
    Given I perform the GP Connect interaction to get the FHIR capability statement
    When I make the GET request
    Then I shall handle the returned resources to accurately reflect what is held in the provider system

  # --- Find a Patient ---

  @GPC-FOU-FPA-01-1 @find_patient
  Scenario: GPC-FOU-FPA-01/1 - Find a patient with a single record
    Given I search for a patient using NHS number "9658218865" where there is a single record associated with this NHS number in the GP system
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system

  @GPC-FOU-FPA-01-2 @find_patient
  Scenario: GPC-FOU-FPA-01/2 - Find a patient with multiple records
    Given I search for a patient using an NHS number where there are multiple records associated with this NHS number in the GP system
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system

  @GPC-FOU-FPA-01-3 @find_patient
  Scenario: GPC-FOU-FPA-01/3 - Find a patient with no corresponding record
    Given I search for a patient using NHS number "9324926233" where there is no corresponding record in the GP system
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system
    And my system reflects a successful interaction

  @GPC-FOU-FPA-01-4 @find_patient @sensitive
  Scenario: GPC-FOU-FPA-01/4 - Find a patient flagged as sensitive in GP system
    Given I am using the default server
    And I search for a patient using NHS number "9658220150" who is flagged as sensitive in the GP system record
    When I make the GET request
    Then the consumer system must display the messages returned from the Provider which specify that the Patient is Not Found

  @GPC-FOU-FPA-01-5 @find_patient @sensitive
  Scenario: GPC-FOU-FPA-01/5 - Find a patient flagged as sensitive on PDS
    Given I am using the default server
    When I make a request to search for a patient using NHS number "9658220142" who is flagged as sensitive on their PDS record
    Then the consumer system must not perform the search for this patient

  @GPC-FOU-FPA-01-6 @find_patient @deceased
  Scenario: GPC-FOU-FPA-01/6 - Find a patient marked as deceased
    Given I search for a patient using NHS number "9658220290" who is marked as deceased in the GP system
    When I make the GET request
    Then I shall handle the empty bundle of returned resources to accurately reflect what is held in the provider system
    And reflect a successful interaction

  @GPC-FOU-FPA-01-7 @find_patient @inactive
  Scenario: GPC-FOU-FPA-01/7 - Find a patient marked as inactive
    Given I search for a patient using NHS number "9658219748" who is marked as inactive in the GP system
    When I make the GET request
    Then I shall handle the empty bundle of returned resources to accurately reflect what is held in the provider system
    And reflect a successful interaction

  @GPC-FOU-FPA-01-8 @find_patient @error_handling
  Scenario: GPC-FOU-FPA-01/8 - Find a patient with an invalid NHS number
    Given I search for a patient with an invalid NHS number "9999999991"
    When I make the GET request
    Then the error returned is captured and displayed appropriately to the caller

  # --- Read a Patient ---

  @GPC-FOU-RPA-01-1 @read_patient
  Scenario: GPC-FOU-RPA-01/1 - Read a patient request conforms to specification
    Given I have resolved the logical patient identifier for NHS number "9658218865"
    And I request the details for this patient from the provider system
    When I make the GET request
    Then the request is formed as described in the specification

  @GPC-FOU-RPA-01-2 @read_patient @error_handling
  Scenario: GPC-FOU-RPA-01/2 - Read a patient not found on server
    Given I request the details for a patient using NHS number "9324926233" whose details cannot be found on the server
    When I make the GET request
    Then the error returned is captured and displayed appropriately to the caller

  @GPC-FOU-RPA-01-3 @read_patient
  Scenario: GPC-FOU-RPA-01/3 - Read a patient and verify data elements
    Given I have resolved the logical patient identifier for NHS number "9658218865"
    And I request the details for this patient from the provider system
    When I make the GET request
    Then the system can receive and read the data elements from the returned data as described in the specification and display them correctly

  # --- Register a Patient ---

  Rule: Register a previously registered patient

    @GPC-FOU-REG-01-2 @register_patient
    Scenario: GPC-FOU-REG-01/2 - Register a previously registered patient
      Given I want to book an appointment for a patient at an extended hours hub or federated practice
      And the patient has previously been registered at that hub or practice
      And I have searched for a suitable slot at that hub or practice and selected it
      When I confirm the booking
      Then a temporary patient registration is not created in the provider system at the chosen practice
      And the appointment is booked correctly
      And I can retrieve and read the details of the appointment when they are returned to me

  Rule: Register a new patient at a hub or federated practice

    Background: Patient not previously registered and slot selected
      Given I want to book an appointment for a patient at an extended hours hub or federated practice
      And the patient has not previously been registered at that hub or practice
      And I have searched for a suitable slot at that hub or practice and selected it

    @GPC-FOU-REG-01-1 @register_patient
    Scenario: GPC-FOU-REG-01/1 - Register a new patient and book appointment
      When I confirm the booking
      Then the request is formatted as described in the specification
      And a temporary patient registration is created in the provider system at the chosen practice
      And the appointment is booked correctly
      And I can retrieve and read the details of the appointment and of the temporary registration when they are returned to me

    @GPC-FOU-REG-01-3 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/3 - Register a patient with blank registration details
      And the registration details section of the request is blank
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-4 @register_patient
    Scenario: GPC-FOU-REG-01/4 - Register a patient with optional fields
      And I have included optional fields address and telecom in my request
      When I confirm the booking
      Then the temporary patient registration is created correctly including the optional fields

    @GPC-FOU-REG-01-5 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/5 - Register a patient with blank NHS Number
      And the NHS Number in the request is blank
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-6 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/6 - Register a patient with blank date of birth
      And the date of birth in the request is blank
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-7 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/7 - Register a patient with duplicate phone number Use values
      And I have provided two or more phone numbers both with the same value in the Use element
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-8 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/8 - Register a patient with duplicate address Use values
      And I have provided two or more addresses both with the same value in the Use element
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-9 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/9 - Register a patient with address Use not temp
      And I have provided an address where the value of the Use element is not temp
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-10 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/10 - Register a patient with phone Use not temp
      And I have provided a phone number where the value of the Use element is not temp
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-11 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/11 - Register a patient with demographics mismatch
      And I have provided an NHS number for a patient where the demographic details supplied do not match those on PDS
      When I confirm the booking
      Then I shall display an appropriate error message

    @GPC-FOU-REG-01-12 @register_patient @error_handling
    Scenario: GPC-FOU-REG-01/12 - Register a patient with inactive NHS number status
      And I have provided an NHS number with a status that is not an active status in the GP system
      When I confirm the booking
      Then I shall display an appropriate error message

  # --- Find a Practitioner ---

  @GPC-FOU-FPR-01-1 @find_practitioner
  Scenario: GPC-FOU-FPR-01/1 - Find a practitioner with multiple records
    Given I have resolved a SDS User Id for "practitioner3"
    And I request the details for this practitioner from the provider system
    And there are multiple practitioner records found for this SDS User Id
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system

  @GPC-FOU-FPR-01-2 @find_practitioner
  Scenario: GPC-FOU-FPR-01/2 - Find a practitioner with a single record
    Given I have resolved a SDS User Id for "practitioner2"
    And I request the details for this practitioner from the provider system
    And there is a single practitioner record found for this SDS User Id
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system

  @GPC-FOU-FPR-01-3 @find_practitioner
  Scenario: GPC-FOU-FPR-01/3 - Find a practitioner with no records
    Given I have resolved a SDS User Id for "practitioner4"
    And I request the details for this practitioner from the provider system
    And there are no practitioner records found for this SDS User Id
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system with no matching records
    And my system reflects a successful interaction

  @GPC-FOU-FPR-01-4 @find_practitioner @error_handling
  Scenario: GPC-FOU-FPR-01/4 - Find a practitioner with invalid SDS User Id
    Given I have resolved a SDS User Id that is invalid
    And I request the details for this practitioner from the provider system
    When I make the GET request
    Then the error returned is captured and displayed appropriately to the caller

  # --- Read a Practitioner ---

  @GPC-FOU-RPR-01-1 @read_practitioner
  Scenario: GPC-FOU-RPR-01/1 - Read a practitioner request conforms to specification
    Given I have a logical identifier for "practitioner2"
    And I request the details for this practitioner
    When I make the GET request
    Then the request is formed as described in the specification

  @GPC-FOU-RPR-01-2 @read_practitioner
  Scenario: GPC-FOU-RPR-01/2 - Read a practitioner and verify data elements
    Given I have a logical identifier for "practitioner2"
    And I request the details for this practitioner
    When I make the GET request
    Then the system can receive and read the data elements from the returned data as described in the specification and display them correctly

  @GPC-FOU-RPR-01-3 @read_practitioner @error_handling
  Scenario: GPC-FOU-RPR-01/3 - Read a practitioner not found on server
    Given I have a logical identifier for a practitioner that does not exist on the server
    And I request the details for this practitioner
    When I make the GET request
    Then the error returned is captured and displayed appropriately to the caller

  # --- Find an Organisation ---

  @GPC-FOU-FOR-01-1 @find_organisation
  Scenario: GPC-FOU-FOR-01/1 - Find an organisation with multiple records
    Given I have resolved an organisation ODS code
    And I request the details for this organisation from the provider system
    And there are multiple organisation records found for this ODS code
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system

  @GPC-FOU-FOR-01-2 @find_organisation
  Scenario: GPC-FOU-FOR-01/2 - Find an organisation with a single record
    Given I have resolved an organisation ODS code "ORG2"
    And I request the details for this organisation from the provider system
    And there is one organisation record found for this ODS code
    When I make the GET request
    Then I shall handle the bundle of returned resources to accurately reflect what is held in the provider system

  @GPC-FOU-FOR-01-3 @find_organisation
  Scenario: GPC-FOU-FOR-01/3 - Find an organisation with no records
    Given I have resolved an organisation ODS code "unknownORG"
    And I request the details for this organisation from the provider system
    And there are no organisation records found for this ODS code
    When I make the GET request
    Then I shall handle the empty bundle of returned resources to accurately reflect what is held in the provider system
    And reflect a successful interaction

  @GPC-FOU-FOR-01-4 @find_organisation @error_handling
  Scenario: GPC-FOU-FOR-01/4 - Find an organisation with invalid ODS code
    Given I request the details for an organisation with an invalid ODS code
    When I make the GET request
    Then the error returned is captured and displayed appropriately to the caller

  # --- Read an Organisation ---

  @GPC-FOU-ROR-01-1 @read_organisation
  Scenario: GPC-FOU-ROR-01/1 - Read an organisation request conforms to specification
    Given I have a logical identifier for organisation "ORG1"
    And I request the details for this organisation
    When I make the GET request
    Then the request is formed as described in the specification

  @GPC-FOU-ROR-01-2 @read_organisation
  Scenario: GPC-FOU-ROR-01/2 - Read an organisation and verify data elements
    Given I have a logical identifier for organisation "ORG1"
    And I request the details for this organisation
    When I make the GET request
    Then the system can receive and read the data elements from the returned data as described in the specification and display them correctly

  @GPC-FOU-ROR-01-3 @read_organisation @error_handling
  Scenario: GPC-FOU-ROR-01/3 - Read an organisation not found on server
    Given I have a logical identifier for an organisation that does not exist on the system
    And I request the details for this organisation
    When I make the GET request
    Then the error returned is captured and displayed appropriately to the caller

  # --- Read a Location ---

  @GPC-FOU-RLO-01-1 @read_location
  Scenario: GPC-FOU-RLO-01/1 - Read a location request conforms to specification
    Given I have an identifier for "Location 1"
    And I request the details for this location
    When I make the GET request
    Then the request is formed as described in the specification

  @GPC-FOU-RLO-01-2 @read_location
  Scenario: GPC-FOU-RLO-01/2 - Read a location and verify data elements
    Given I have an identifier for "Location 1"
    And I request the details for this location
    When I make the GET request
    Then the system can receive and read the data elements from the returned data as described in the specification and display them correctly

  @GPC-FOU-RLO-01-3 @read_location @error_handling
  Scenario: GPC-FOU-RLO-01/3 - Read a location not found on server
    Given I have an identifier for a location that cannot be found on the server
    And I request the details for this location
    When I make the GET request
    Then the error returned is captured and displayed appropriately to the caller
