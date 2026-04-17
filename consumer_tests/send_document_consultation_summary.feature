@send_document_consultation_summary
Feature: Send Document - Consultation Summary
  As a GP Connect consumer
  I want to send consultation summary documents to the registered GP practice
  So that the patient's registered practice receives the consultation record

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Send-Document
  # Uses MESH and ITK3 requirements for Send Document

  @GPCM-SD-TST-01
  Scenario: GPCM-SD-TST-01 - Standard Test
    Given I have recorded a consultation for a patient who is not registered to my practice
    And I am not sharing the consultation within the functionality of my clinical system
    And I have not marked the consultation as confidential
    When the requisite amount of time has passed since the consultation was recorded or last updated
    And a send document message is triggered
    Then a message is sent which conforms to the MESH and ITK3 requirements for Send Document
    And a PDF is included as a binary document conforming to the Send Document specification
    # Test data: NHS_NO 9691375087 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-SD-TST-02
  Scenario: GPCM-SD-TST-02 - Confidential Consultation
    Given I have recorded a consultation for a patient who is not registered to my practice
    And I am not sharing the consultation within the functionality of my clinical system
    And I mark the consultation as confidential
    When the requisite amount of time has passed since the consultation was recorded or last updated
    And a send document message is triggered
    Then a message is sent which conforms to the MESH and ITK3 requirements for Send Document
    And the Composition.confidentiality is set to R
    And confidential items are not included in the headers as per requirements
    And the organisation details are included in structured resources
    And a PDF is included as a binary document conforming to the Send Document specification with items absent as per GPCM-SD-102
    # Test data: NHS_NO 9691375095 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-SD-TST-03
  Scenario: GPCM-SD-TST-03 - Practitioner and sender details
    Given I have recorded a consultation for a patient who is not registered to my practice
    And the consultation has been sent successfully via Send Document
    And I record a new consultation for the patient as a different practitioner working for a different organisation
    When the send document message is triggered
    Then the organization and practitioner resources reflect the practitioner and organisation details used to record the consultation
    # Test data: NHS_NO 9691375109 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-SD-TST-04 @error_handling
  Scenario: GPCM-SD-TST-04 - Handling errors from the receiver
    Given I have sent a valid Send Document message with appropriate keywords in the request for each type of error response
    But the receiver is unable to process it
    When I receive an error response
    Then the error is handled gracefully
    And a notification of the error is made to an appropriate person
    # Test data: NHS_NO 9691375117 | Keyword: See ITK Test Harness Triggers

  @GPCM-SD-TST-05 @error_handling
  Scenario: GPCM-SD-TST-05 - Handling no response
    Given I have sent a valid Send Document message with appropriate keywords in the request
    But the receiver is unable to process it
    When I do not receive a technical or business acknowledgement response
    Then the sender has an appropriate way to manage the non-response
    And if not resolved a notification of no response is made to an appropriate person
    # Test data: NHS_NO 9691375125 | Keyword: Set //Practitioner/name/given/@value to noresponse

  @GPCM-SD-TST-06
  Scenario: GPCM-SD-TST-06 - Registered patient message not sent
    Given I have recorded a consultation for a patient registered at my practice
    And the patient registration type is Regular GMS or PMS
    When I complete the consultation
    Then a Send Document message does not trigger
    # Test data: NHS_NO 9691375133

  @GPCM-SD-TST-07
  Scenario: GPCM-SD-TST-07 - Timeliness of message
    Given I have recorded a consultation for a patient who is not registered to my practice
    And I am not sharing the consultation within the functionality of my clinical system
    And I have not marked the consultation as confidential
    When the Send Document is sent after I complete the consultation
    Then ideally less than 3 hours has elapsed between last update and send
    # No specific test data

  @GPCM-SD-TST-08
  Scenario: GPCM-SD-TST-08 - Amend a consultation after sending
    Given I access a consultation which has previously been sent via Send Document
    When I amend the consultation
    And the necessary time elapses for the message send
    Then an updated Send Document message is sent conforming to the specification
    And the version number is incremented from the previous send
    And it identifies the document is a replacement
    And it refers to the original document unique ID it is replacing
    # Test data: NHS_NO 9691375141 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-SD-TST-09
  Scenario: GPCM-SD-TST-09 - Third send of document
    Given a consultation has previously been sent via Send Document
    And the consultation was subsequently amended and re-sent as a replacement
    And I make a further amendment to the consultation
    When a replacement message is sent
    Then an updated Send Document message is sent conforming to the specification
    And the version number is incremented from the previous send
    And it identifies the document is a replacement
    And it refers to the previous replacement document unique ID it is replacing
    # Test data: NHS_NO 9691375141 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-SD-TST-10
  Scenario: GPCM-SD-TST-10 - Deleted consultation
    Given I access a consultation which has previously been sent via Send Document
    When I delete the consultation
    Then a message is displayed to inform me this consultation has been sent to the registered practice and action needs to be taken
    And the message includes the necessary details about the patient, consultation date and registered practice
    # Test data: NHS_NO 9691375141

  @GPCM-SD-TST-11
  Scenario: GPCM-SD-TST-11 - Consultation with individual items marked as confidential
    Given I have recorded a consultation for a patient who is not registered to my practice
    And I am not sharing the consultation within the functionality of my clinical system
    And I mark some items within the consultation as confidential
    When the requisite amount of time has passed since the consultation was recorded or last updated
    And a send document message is triggered
    Then a message is sent which conforms to the MESH and ITK3 requirements for Send Document
    And the Composition.confidentiality is set to N
    And confidential items are not included in the headers as per requirements
    And the organisation details are included in structured resources
    And a PDF is included with any confidential item or text replaced with the text "confidential item"
    # Test data: NHS_NO 9691375141 | Keyword: Set //Practitioner/name/given/@value to IB001

  @GPCM-SD-TST-12 @error_handling
  Scenario: GPCM-SD-TST-12 - Receiver reports amended document cannot be processed
    Given I have amended a consultation after it was sent via Send Document
    And the amended consultation is then sent via Send Document
    And the send is not successful
    When I receive the error or do not receive a response
    Then I will handle the error gracefully
    And trigger an appropriate resolution process
    And manage the data integrity of the record
    # Test data: NHS_NO 9691375141 | Keyword: Set //Practitioner/name/given/@value to 30003

  @GPCM-SD-TST-13
  Scenario: GPCM-SD-TST-13 - Additional documents sent
    Given I have additional documents relating to the consultation
    And I include the additional documents to be sent to the registered GP
    When the requisite amount of time has passed since the consultation was recorded or updated
    And a send document message is triggered
    Then a message is sent which conforms to the MESH and ITK3 requirements for Send Document
    And the consultation report and each document is included in the composition as individual sections
    And the first section in the composition refers to a binary resource for the consultation report
    And there is a section for each additional document with a reference to a binary resource
    And the binary resources are included in the bundle with matching references and IDs
    And the binary resources are base64 encoded
    # Test data: NHS_NO 9691375176 | Keyword: Set //Practitioner/name/given/@value to IB001
