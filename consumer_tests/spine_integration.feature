@spine_integration
Feature: Spine Integration
  As a GP Connect consumer
  I want to integrate with the Spine infrastructure
  So that I can securely communicate with GP provider systems

  # Source: https://github.com/nhsconnect/gpc-consumer-support/wiki/Consumer-Test-Scripts-Spine-Integration
  # Spine Integration Consumer Tests for all of the latest versions of the capabilities

  # --- SDS / LDAP Tests ---

  Rule: Spine Directory Service lookups

    @GPC-SPN-TST-01 @sds
    Scenario: GPC-SPN-TST-01 - Retrieve ASID for a patient's GP Provider Organisation
      Given I am using the Spine Directory Services LDAP server
      And I am performing the ldapsearch to retrieve the ASID and the MHS Party Key
      When I request the ldapsearch operation
      Then I set Accredited System type as nhsAS, Organisation code as the GP Practice Organisation code and the InteractionID as a specific GP Connect Interaction ID
      And the LDAP response should contain the ASID and the MHS Party Key of the GP Practice Organisation Code
      # SCAL: GPC-SSP03-02 | Test data: 9658218873

    @GPC-SPN-TST-02 @sds
    Scenario: GPC-SPN-TST-02 - Retrieve FHIR endpoint URL of the MHS for the ASID record
      Given I am using the default Spine Directory Services LDAP server
      And I am performing the ldapsearch to retrieve the FHIR endpoint URL of the MHS
      When I request the ldapsearch operation
      Then I set Message Handling System type as nhsMHS, provide the MHS Party Key and the Interaction ID
      And the LDAP response should contain the FHIR endpoint URL of the MHS in the nhsMhsEndPoint
      # SCAL: GPC-SSP03-03 | Test data: 9658218873

  # --- JWT Tests ---

  Rule: JWT construction for GP Connect interactions

    @GPC-SPN-TST-10 @jwt
    Scenario: GPC-SPN-TST-10 - JWT is valid - practitioner has smartcard
      Given I am performing a GP Connect interaction
      When I make the GPConnect request
      Then I include a JWT Header, Payload and Signature each separated by dots
      And I include the alg header parameter with value none
      And I include the typ header parameter with value JWT
      And I have set the JWT payload creation time iat to now
      And I have set the JWT payload expiry time exp to 300 seconds after creation time
      And I set the JWT payload reason_for_request to directcare
      And I have set the JWT payload requesting_device claim value with business identifiers
      And I have set the JWT payload requesting_organization claim value with organisation details
      And I have set the JWT payload requesting_practitioner claim value with practitioner details including SDS User ID
      # SCAL: GPC-SSP10-01 | Test data: 9658218873

    @GPC-SPN-TST-11 @jwt
    Scenario: GPC-SPN-TST-11 - JWT is valid - practitioner not a smartcard login
      Given I am performing a GP Connect interaction
      When I make the GPConnect request
      Then I include a JWT Header, Payload and Signature each separated by dots
      And I include the alg header parameter with value none
      And I include the typ header parameter with value JWT
      And I have set the JWT payload creation time iat to now
      And I have set the JWT payload expiry time exp to 300 seconds after creation time
      And I set the JWT payload reason_for_request to directcare
      And I have set the JWT payload requesting_device claim value with business identifiers
      And I have set the JWT payload requesting_organization claim value with organisation details
      And I have set the JWT payload requesting_practitioner claim value with practitioner details without smartcard
      # SCAL: GPC-SSP10-01 | Test data: 9658218873

  # --- Server Interaction Tests ---

  Rule: GP Connect interactions via the default server

    Background: Connected to default server for GP Connect interaction
      Given I am using the default server
      And I am performing a GP Connect interaction

    @GPC-SPN-TST-03 @security
    Scenario: GPC-SPN-TST-03 - Retrieve a patient record using valid security certificate and TLS
      When I make a GPConnect request
      Then I use a valid client certificate
      And the response status code should indicate success
      # SCAL: GPC-SSP04-02, GPC-SSP04-03, GPC-SSP04-04 | Test data: 9658218873

    @GPC-SPN-TST-04 @security
    Scenario: GPC-SPN-TST-04 - Retrieve a patient record using a valid SSLCipherSuite
      When I make a GPConnect request
      Then I use a valid SSLCipherSuite with AESGCM and AES256 ciphers
      And the response status code should indicate success
      # SCAL: GPC-SSP04-05 | Test data: 9658218873

    @GPC-SPN-TST-05 @content_type
    Scenario: GPC-SPN-TST-05 - FHIR content type test - Accept JSON request XML
      And I set the request content type to application/xml+fhir
      And I set the Accept header to application/json+fhir
      When I make the GPConnect request
      Then the response status code should indicate success
      And the response body should be FHIR JSON
      # SCAL: GPC-SSP06-03 | Test data: 9658218873

    @GPC-SPN-TST-06 @content_type
    Scenario: GPC-SPN-TST-06 - FHIR content type test - format parameter JSON request JSON
      And I set the request content type to application/json+fhir
      And I do not send the Accept header
      And I add the parameter _format with the value application/json+fhir
      When I make the GPConnect request
      Then the response status code should indicate success
      And the response body should be FHIR JSON
      # SCAL: GPC-SSP06-04 | Test data: 9658218873

    @GPC-SPN-TST-07 @error_handling
    Scenario: GPC-SPN-TST-07 - Receive and handle a SPINE operation outcome resource
      And I author a GPConnect request for a patient who does not consent to their record being shared
      When I make a valid request
      Then the response status code should be 403
      And the Error Code should be NO_PATIENT_CONSENT
      And I will display an appropriate error response
      And I will add the interaction to the audit trail
      # SCAL: GPC-SSP07-01 | Test data: 9450056234

    @GPC-SPN-TST-08 @audit
    Scenario: GPC-SPN-TST-08 - Write to audit trail successful interaction
      And I author a GPConnect request for a patient
      And I make a valid request
      When I receive a successful response
      Then I shall add to the systems audit trail the interaction header data items including Ssp-TraceID, Ssp-From, Ssp-To, Ssp-InteractionID
      And I shall add to the systems audit trail the JWT data items including User ID, Name, Role, Organisation, authority identity, date and time, event details
      # SCAL: GPC-SSP08-01 | Test data: 9658218873

    @GPC-SPN-TST-09 @audit
    Scenario: GPC-SPN-TST-09 - Write to audit trail unsuccessful interaction
      And I author a GPConnect request for a patient
      And I make a valid request
      When I receive an unsuccessful response
      Then I shall add to the systems audit trail the interaction header data items including Ssp-TraceID, Ssp-From, Ssp-To, Ssp-InteractionID
      And I shall add to the systems audit trail the JWT data items including User ID, Name, Role, Organisation, authority identity, date and time, event details
      # SCAL: GPC-SSP08-01 | Test data: 9658218873

    @GPC-SPN-TST-12 @http_headers
    Scenario: GPC-SPN-TST-12 - Use transfer encoding and compression headers
      When I make the GPConnect request
      Then I set the transfer-encoding header to chunked
      And I set the Accept-encoding header to gzip
      And the response status code should indicate success
      # SCAL: GPC-SSP04-07 | Test data: 9658218873

    @GPC-SPN-TST-13 @http_headers
    Scenario: GPC-SPN-TST-13 - Use spine headers
      When I make the GPConnect request
      Then I set the Ssp-TraceID to a TraceID that uniquely identifies this request
      And I set the Ssp-From to my ASID
      And I set the Ssp-To to the recipient's ASID
      And I set the Ssp-InteractionID to the correct value for the interaction
      And the response status code should indicate success
      # SCAL: GPC-SSP05-09 | Test data: 9658218873
