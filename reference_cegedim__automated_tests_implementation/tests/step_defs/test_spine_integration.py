"""Step definitions for Spine Integration feature."""
import uuid

from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/spine_integration.feature')

# Default test data
DEFAULT_ORG_CODE = "A20047"
DEFAULT_INTERACTION_ID = "urn:nhs:names:services:gpconnect:fhir:rest:read:metadata-1"

# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given('I am using the Spine Directory Services LDAP server')
def given_using_sds_ldap(spine_page, gp_connect_context):
    spine_page.navigate('spine-integration')
    spine_page.wait_for_load()
    gp_connect_context['sds_server'] = 'ldap'


@given('I am performing the ldapsearch to retrieve the ASID and the MHS Party Key')
def given_ldapsearch_asid_mhs(spine_page, gp_connect_context):
    gp_connect_context['lookup_type'] = 'asid_mhs'
    gp_connect_context['org_code'] = DEFAULT_ORG_CODE
    gp_connect_context['interaction_id'] = DEFAULT_INTERACTION_ID


@given('I am using the default Spine Directory Services LDAP server')
def given_using_default_sds_ldap(spine_page, gp_connect_context):
    spine_page.navigate('spine-integration')
    spine_page.wait_for_load()
    gp_connect_context['sds_server'] = 'default_ldap'


@given('I am performing the ldapsearch to retrieve the FHIR endpoint URL of the MHS')
def given_ldapsearch_fhir_endpoint(spine_page, gp_connect_context):
    gp_connect_context['lookup_type'] = 'fhir_endpoint'
    gp_connect_context['org_code'] = DEFAULT_ORG_CODE
    gp_connect_context['interaction_id'] = DEFAULT_INTERACTION_ID


@given('I am using the default server')
def given_using_default_server(spine_page, gp_connect_context):
    spine_page.navigate('spine-integration')
    spine_page.wait_for_load()
    gp_connect_context['server'] = 'default'


@given('I am performing a GP Connect interaction')
def given_performing_gp_connect_interaction(spine_page, gp_connect_context):
    gp_connect_context['interaction'] = 'gp_connect'
    gp_connect_context['interaction_id'] = DEFAULT_INTERACTION_ID


@given('I set the request content type to application/xml+fhir')
def given_content_type_xml(spine_page, gp_connect_context):
    spine_page.set_content_type('application/xml+fhir')
    gp_connect_context['content_type'] = 'application/xml+fhir'


@given('I set the Accept header to application/json+fhir')
def given_accept_json(spine_page, gp_connect_context):
    spine_page.set_accept_header('application/json+fhir')
    gp_connect_context['accept_header'] = 'application/json+fhir'


@given('I set the request content type to application/json+fhir')
def given_content_type_json(spine_page, gp_connect_context):
    spine_page.set_content_type('application/json+fhir')
    gp_connect_context['content_type'] = 'application/json+fhir'


@given('I do not send the Accept header')
def given_no_accept_header(spine_page, gp_connect_context):
    spine_page.set_accept_header('')
    gp_connect_context['accept_header'] = None


@given('I add the parameter _format with the value application/json+fhir')
def given_format_param_json(spine_page, gp_connect_context):
    spine_page.set_format_param('application/json+fhir')
    gp_connect_context['format_param'] = 'application/json+fhir'


@given('I author a GPConnect request for a patient who does not consent to their record being shared')
def given_author_request_no_consent(spine_page, gp_connect_context):
    gp_connect_context['patient_nhs_number'] = '9450056234'
    gp_connect_context['no_consent'] = True


@given('I author a GPConnect request for a patient')
def given_author_request_patient(spine_page, gp_connect_context):
    gp_connect_context['patient_nhs_number'] = '9658218873'
    gp_connect_context['no_consent'] = False


@given('I make a valid request')
def given_make_valid_request(spine_page, gp_connect_context):
    trace_id = str(uuid.uuid4())
    gp_connect_context['trace_id'] = trace_id
    ssp_from = gp_connect_context.get('my_asid', '200000000359')
    ssp_to = gp_connect_context.get('recipient_asid', '918999198993')
    interaction_id = gp_connect_context.get('interaction_id', DEFAULT_INTERACTION_ID)
    spine_page.set_ssp_headers(trace_id, ssp_from, ssp_to, interaction_id)
    spine_page.submit_request()
    gp_connect_context['response_status'] = spine_page.get_response_status()


@given('I am performing a GP Connect interaction', target_fixture='gp_connect_interaction')
def given_performing_interaction(spine_page, gp_connect_context):
    gp_connect_context['interaction'] = 'gp_connect'
    gp_connect_context['interaction_id'] = DEFAULT_INTERACTION_ID
    return gp_connect_context


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when('I request the ldapsearch operation')
def when_request_ldapsearch(spine_page, gp_connect_context):
    org_code = gp_connect_context.get('org_code', DEFAULT_ORG_CODE)
    interaction_id = gp_connect_context.get('interaction_id', DEFAULT_INTERACTION_ID)
    spine_page.perform_sds_lookup(org_code, interaction_id)


@when('I make a GPConnect request')
def when_make_gpconnect_request(spine_page, gp_connect_context):
    spine_page.submit_request()
    gp_connect_context['response_status'] = spine_page.get_response_status()
    gp_connect_context['response_body'] = spine_page.get_response_body()


@when('I make the GPConnect request')
def when_make_the_gpconnect_request(spine_page, gp_connect_context):
    spine_page.submit_request()
    gp_connect_context['response_status'] = spine_page.get_response_status()
    gp_connect_context['response_body'] = spine_page.get_response_body()


@when('I make a valid request')
def when_make_valid_request(spine_page, gp_connect_context):
    trace_id = str(uuid.uuid4())
    gp_connect_context['trace_id'] = trace_id
    ssp_from = gp_connect_context.get('my_asid', '200000000359')
    ssp_to = gp_connect_context.get('recipient_asid', '918999198993')
    interaction_id = gp_connect_context.get('interaction_id', DEFAULT_INTERACTION_ID)
    spine_page.set_ssp_headers(trace_id, ssp_from, ssp_to, interaction_id)
    spine_page.submit_request()
    gp_connect_context['response_status'] = spine_page.get_response_status()
    gp_connect_context['response_body'] = spine_page.get_response_body()


@when('I receive a successful response')
def when_receive_successful_response(spine_page, gp_connect_context):
    status = spine_page.get_response_status()
    gp_connect_context['response_status'] = status
    assert status.startswith('2'), f"Expected success status but got {status}"


@when('I receive an unsuccessful response')
def when_receive_unsuccessful_response(spine_page, gp_connect_context):
    status = spine_page.get_response_status()
    gp_connect_context['response_status'] = status
    assert not status.startswith('2'), f"Expected unsuccessful status but got {status}"


# ---------------------------------------------------------------------------
# Then steps - SDS
# ---------------------------------------------------------------------------


@then('I set Accredited System type as nhsAS, Organisation code as the GP Practice Organisation code and the InteractionID as a specific GP Connect Interaction ID')
def then_set_accredited_system(spine_page, gp_connect_context):
    org_code = gp_connect_context.get('org_code', DEFAULT_ORG_CODE)
    interaction_id = gp_connect_context.get('interaction_id', DEFAULT_INTERACTION_ID)
    spine_page.perform_sds_lookup(org_code, interaction_id)
    gp_connect_context['asid'] = spine_page.get_asid()
    gp_connect_context['mhs_party_key'] = spine_page.get_mhs_party_key()


@then('the LDAP response should contain the ASID and the MHS Party Key of the GP Practice Organisation Code')
def then_ldap_contains_asid_mhs(spine_page, gp_connect_context):
    asid = spine_page.get_asid()
    mhs_party_key = spine_page.get_mhs_party_key()
    assert asid, "ASID should not be empty"
    assert mhs_party_key, "MHS Party Key should not be empty"
    gp_connect_context['asid'] = asid
    gp_connect_context['mhs_party_key'] = mhs_party_key


@then('I set Message Handling System type as nhsMHS, provide the MHS Party Key and the Interaction ID')
def then_set_mhs_type(spine_page, gp_connect_context):
    org_code = gp_connect_context.get('org_code', DEFAULT_ORG_CODE)
    interaction_id = gp_connect_context.get('interaction_id', DEFAULT_INTERACTION_ID)
    spine_page.perform_sds_lookup(org_code, interaction_id)
    gp_connect_context['fhir_endpoint'] = spine_page.get_fhir_endpoint()


@then('the LDAP response should contain the FHIR endpoint URL of the MHS in the nhsMhsEndPoint')
def then_ldap_contains_fhir_endpoint(spine_page, gp_connect_context):
    endpoint = spine_page.get_fhir_endpoint()
    assert endpoint, "FHIR endpoint URL should not be empty"
    assert endpoint.startswith('http'), f"Expected HTTP endpoint but got: {endpoint}"
    gp_connect_context['fhir_endpoint'] = endpoint


# ---------------------------------------------------------------------------
# Then steps - Security
# ---------------------------------------------------------------------------


@then('I use a valid client certificate')
def then_valid_client_cert(spine_page, gp_connect_context):
    gp_connect_context['client_cert'] = True
    status = spine_page.get_response_status()
    assert status != '403', "Request should not be rejected with a valid client certificate"


@then('the response status code should indicate success')
def then_status_success(spine_page, gp_connect_context):
    status = spine_page.get_response_status()
    assert status.startswith('2'), f"Expected success status but got {status}"
    gp_connect_context['response_status'] = status


@then('I use a valid SSLCipherSuite with AESGCM and AES256 ciphers')
def then_valid_ssl_cipher(spine_page, gp_connect_context):
    gp_connect_context['ssl_cipher'] = 'AESGCM+AES256'
    status = spine_page.get_response_status()
    assert status != '403', "Request should not be rejected with a valid SSL cipher suite"


# ---------------------------------------------------------------------------
# Then steps - Content Type
# ---------------------------------------------------------------------------


@then('the response body should be FHIR JSON')
def then_response_fhir_json(spine_page):
    assert spine_page.response_is_fhir_json(), "Response body should be valid FHIR JSON"


# ---------------------------------------------------------------------------
# Then steps - Error Handling
# ---------------------------------------------------------------------------


@then('the response status code should be 403')
def then_status_403(spine_page, gp_connect_context):
    status = spine_page.get_response_status()
    assert status == '403', f"Expected status 403 but got {status}"
    gp_connect_context['response_status'] = status


@then('the Error Code should be NO_PATIENT_CONSENT')
def then_error_no_consent(spine_page):
    error = spine_page.get_displayed_error()
    assert 'NO_PATIENT_CONSENT' in error, f"Expected NO_PATIENT_CONSENT error but got: {error}"


@then('I will display an appropriate error response')
def then_display_error(spine_page):
    error = spine_page.get_displayed_error()
    assert error, "An error response should be displayed"


@then('I will add the interaction to the audit trail')
def then_add_to_audit(spine_page, gp_connect_context):
    audit_log = spine_page.get_audit_log()
    assert audit_log, "Audit log should not be empty"
    gp_connect_context['audit_log'] = audit_log


# ---------------------------------------------------------------------------
# Then steps - Audit
# ---------------------------------------------------------------------------


@then('I shall add to the systems audit trail the interaction header data items including Ssp-TraceID, Ssp-From, Ssp-To, Ssp-InteractionID')
def then_audit_headers(spine_page, gp_connect_context):
    audit_log = spine_page.get_audit_log()
    assert 'Ssp-TraceID' in audit_log, "Audit log should contain Ssp-TraceID"
    assert 'Ssp-From' in audit_log, "Audit log should contain Ssp-From"
    assert 'Ssp-To' in audit_log, "Audit log should contain Ssp-To"
    assert 'Ssp-InteractionID' in audit_log, "Audit log should contain Ssp-InteractionID"
    gp_connect_context['audit_log'] = audit_log


@then('I shall add to the systems audit trail the JWT data items including User ID, Name, Role, Organisation, authority identity, date and time, event details')
def then_audit_jwt(spine_page, gp_connect_context):
    audit_log = spine_page.get_audit_log()
    for item in ['User ID', 'Name', 'Role', 'Organisation']:
        assert item in audit_log, f"Audit log should contain {item}"
    gp_connect_context['audit_log'] = audit_log


# ---------------------------------------------------------------------------
# Then steps - JWT
# ---------------------------------------------------------------------------


@then('I include a JWT Header, Payload and Signature each separated by dots')
def then_jwt_structure(spine_page):
    assert spine_page.jwt_panel_visible(), "JWT panel should be visible"
    header = spine_page.get_jwt_header()
    payload = spine_page.get_jwt_payload()
    assert header, "JWT header should not be empty"
    assert payload, "JWT payload should not be empty"


@then('I include the alg header parameter with value none')
def then_jwt_alg_none(spine_page):
    header = spine_page.get_jwt_header()
    assert '"alg"' in header and '"none"' in header, \
        f"JWT header should contain alg=none, got: {header}"


@then('I include the typ header parameter with value JWT')
def then_jwt_typ(spine_page):
    header = spine_page.get_jwt_header()
    assert '"typ"' in header and '"JWT"' in header, \
        f"JWT header should contain typ=JWT, got: {header}"


@then('I have set the JWT payload creation time iat to now')
def then_jwt_iat(spine_page):
    payload = spine_page.get_jwt_payload()
    assert '"iat"' in payload, f"JWT payload should contain iat claim, got: {payload}"


@then('I have set the JWT payload expiry time exp to 300 seconds after creation time')
def then_jwt_exp(spine_page):
    payload = spine_page.get_jwt_payload()
    assert '"exp"' in payload, f"JWT payload should contain exp claim, got: {payload}"


@then('I set the JWT payload reason_for_request to directcare')
def then_jwt_reason(spine_page):
    payload = spine_page.get_jwt_payload()
    assert '"reason_for_request"' in payload and 'directcare' in payload, \
        f"JWT payload should contain reason_for_request=directcare, got: {payload}"


@then('I have set the JWT payload requesting_device claim value with business identifiers')
def then_jwt_device(spine_page):
    payload = spine_page.get_jwt_payload()
    assert '"requesting_device"' in payload, \
        f"JWT payload should contain requesting_device claim, got: {payload}"


@then('I have set the JWT payload requesting_organization claim value with organisation details')
def then_jwt_org(spine_page):
    payload = spine_page.get_jwt_payload()
    assert '"requesting_organization"' in payload, \
        f"JWT payload should contain requesting_organization claim, got: {payload}"


@then('I have set the JWT payload requesting_practitioner claim value with practitioner details including SDS User ID')
def then_jwt_practitioner_with_sds(spine_page):
    payload = spine_page.get_jwt_payload()
    assert '"requesting_practitioner"' in payload, \
        f"JWT payload should contain requesting_practitioner claim, got: {payload}"
    assert 'sds' in payload.lower() or 'SDS' in payload or 'userId' in payload, \
        f"Practitioner claim should include SDS User ID, got: {payload}"


@then('I have set the JWT payload requesting_practitioner claim value with practitioner details without smartcard')
def then_jwt_practitioner_no_smartcard(spine_page):
    payload = spine_page.get_jwt_payload()
    assert '"requesting_practitioner"' in payload, \
        f"JWT payload should contain requesting_practitioner claim, got: {payload}"


# ---------------------------------------------------------------------------
# Then steps - HTTP Headers
# ---------------------------------------------------------------------------


@then('I set the transfer-encoding header to chunked')
def then_transfer_encoding(spine_page, gp_connect_context):
    gp_connect_context['transfer_encoding'] = 'chunked'


@then('I set the Accept-encoding header to gzip')
def then_accept_encoding(spine_page, gp_connect_context):
    gp_connect_context['accept_encoding'] = 'gzip'


@then('I set the Ssp-TraceID to a TraceID that uniquely identifies this request')
def then_ssp_trace_id(spine_page, gp_connect_context):
    trace_id = str(uuid.uuid4())
    gp_connect_context['trace_id'] = trace_id
    ssp_from = gp_connect_context.get('my_asid', '200000000359')
    ssp_to = gp_connect_context.get('recipient_asid', '918999198993')
    interaction_id = gp_connect_context.get('interaction_id', DEFAULT_INTERACTION_ID)
    spine_page.set_ssp_headers(trace_id, ssp_from, ssp_to, interaction_id)


@then('I set the Ssp-From to my ASID')
def then_ssp_from(spine_page, gp_connect_context):
    asid = gp_connect_context.get('my_asid', '200000000359')
    gp_connect_context['ssp_from'] = asid


@then("I set the Ssp-To to the recipient's ASID")
def then_ssp_to(spine_page, gp_connect_context):
    recipient_asid = gp_connect_context.get('recipient_asid', '918999198993')
    gp_connect_context['ssp_to'] = recipient_asid


@then('I set the Ssp-InteractionID to the correct value for the interaction')
def then_ssp_interaction_id(spine_page, gp_connect_context):
    interaction_id = gp_connect_context.get('interaction_id', DEFAULT_INTERACTION_ID)
    gp_connect_context['ssp_interaction_id'] = interaction_id
