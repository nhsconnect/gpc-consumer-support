@send_document_online_consultation
Feature: Send Document - Online Consultation
  As a GP Connect consumer
  I want to send online consultation documents to the registered GP practice
  So that the patient's registered practice receives the online consultation record

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Send-Document---'Online-Consultations'
  # Uses MESH and ITK3 requirements for Send Document

  @GPCM-OC-TST-01
  Scenario: GPCM-OC-TST-01 - Standard Test
    Given an Online Consultation has been submitted
    And I have not marked the consultation as confidential
    When the requisite amount of time has passed since the consultation was recorded or last updated
    And a send document message is triggered
    Then a message is sent which conforms to the MESH and ITK3 requirements for Send Document
    And a PDF is included as a binary document
    # Test data: NHS_NO 9691375087 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-OC-TST-02
  Scenario: GPCM-OC-TST-02 - Confidential Consultation
    Given an Online Consultation has been submitted
    And I mark the consultation as confidential
    When the requisite amount of time has passed since the consultation was recorded or last updated
    And a send document message is triggered
    Then a message is sent which conforms to the MESH and ITK3 requirements for Send Document
    And the Composition.confidentiality is set to R
    And confidential items are not included in the headers as per requirements
    And the organisation details are included in structured resources
    # Test data: NHS_NO 9691375095 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-OC-TST-03
  Scenario: GPCM-OC-TST-03 - Practitioner and sender details
    Given an Online Consultation has been submitted and sent successfully via Send Document
    And I record a new online consultation for the patient as a different practitioner working for a different organisation
    When the send document message is triggered
    Then the organization and practitioner resources reflect the practitioner and organisation details used to record the consultation
    # Test data: NHS_NO 9691375109 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-OC-TST-04 @error_handling
  Scenario: GPCM-OC-TST-04 - Handling errors from the receiver
    Given I have sent a valid Online Consultation Send Document message with appropriate keywords for each type of error response
    But the receiver is unable to process it
    When I receive an error response
    Then the error is handled gracefully
    And a notification of the error is made to an appropriate person
    # Test data: NHS_NO 9691375117 | Keyword: See ITK Test Harness Triggers

  @GPCM-OC-TST-05 @error_handling
  Scenario: GPCM-OC-TST-05 - Handling no response
    Given I have sent a valid Online Consultation Send Document message with appropriate keywords
    But the receiver is unable to process it
    When I do not receive a technical or business acknowledgement response
    Then the sender has an appropriate way to manage the non-response
    And if not resolved a notification of no response is made to an appropriate person
    # Test data: NHS_NO 9691375125 | Keyword: Set //Practitioner/name/given/@value to noresponse

  @GPCM-OC-TST-08
  Scenario: GPCM-OC-TST-08 - Amend a consultation after sending
    Given I access an Online Consultation which has previously been sent via Send Document
    When I amend the Online Consultation
    And the necessary time elapses for the message send
    Then an updated Send Document message is sent
    And the version number is incremented from the previous send
    And it identifies the document is a replacement
    And it refers to the original document unique ID it is replacing
    # Test data: NHS_NO 9691375141 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-OC-TST-12 @error_handling
  Scenario: GPCM-OC-TST-12 - Receiver reports amended document cannot be processed
    Given I have amended the Online Consultation after it was sent via Send Document
    And the amended Online Consultation is then sent via Send Document
    And the send is not successful
    When I receive the error or do not receive a response
    Then I will handle the error gracefully
    And trigger an appropriate resolution process
    And manage the data integrity of the record
    # Test data: NHS_NO 9691375141 | Keyword: Set //Practitioner/name/given/@value to 30003

  @GPCM-OC-TST-13
  Scenario: GPCM-OC-TST-13 - Additional documents sent
    Given I have additional documents relating to the Online Consultation
    And I include the additional documents to be sent
    When the requisite amount of time has passed since the Online Consultation was recorded or updated
    And a send document message is triggered
    Then a message is sent which conforms to the MESH and ITK3 requirements for Send Document
    And the consultation report and each document is included in the composition as individual sections
    And the first section in the composition refers to a binary resource for the consultation report
    And there is a section for each additional document with a reference to a binary resource
    And the binary resources are included in the bundle with matching references and IDs
    And the binary resources are base64 encoded
    # Test data: NHS_NO 9691375176 | Keyword: Set //Practitioner/name/given/@value to IB001

  # --- Payload Verification Tests ---
  # These scenarios all require a prior Online Consultation to have been sent successfully

  Rule: Verify payload resources after a successful Online Consultation send

    Background: An Online Consultation has been sent successfully
      Given an Online Consultation has been submitted and sent successfully via Send Document
      And I record a new online consultation for the patient as a different practitioner working for a different organisation

    @GPCM-OC-TST-14
    Scenario: GPCM-OC-TST-14 - Payload Related Person Resource
      When the send document message is triggered
      Then the RelatedPerson resource details reflect the person, birthdate and telecom details used in the online consultation message as per specification
      # Test data: NHS_NO 9691375109 | Keyword: Set //Practitioner/name/given/@value to IB001

    @GPCM-OC-TST-15
    Scenario: GPCM-OC-TST-15 - Payload ITK Device Resource
      When the send document message is triggered
      Then the ITK Device Resource details reflect the type and manufacturer of the device in question as per specification
      # Test data: NHS_NO 9691375109 | Keyword: Set //Practitioner/name/given/@value to IB001

    @GPCM-OC-TST-16
    Scenario: GPCM-OC-TST-16 - Payload Optional Resource that is being implemented
      When the send document message is triggered
      Then the Optional Resource in the payload is populated as per specification
      # Test data: NHS_NO 9691375109 | Keyword: Set //Practitioner/name/given/@value to IB001
