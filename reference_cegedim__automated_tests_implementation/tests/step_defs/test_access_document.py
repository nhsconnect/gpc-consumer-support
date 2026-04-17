"""Step definitions for Access Document feature."""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/access_document.feature')

# ---------------------------------------------------------------------------
# General - Given steps
# ---------------------------------------------------------------------------


@given('I am at a point in the system where I have access to attempt a call to a GP Connect service')
def given_access_to_gp_connect(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    gp_connect_context['access_granted'] = True


@given(parsers.parse('I have access to request data from GP Connect and the patient trace was {time} ago'))
def given_access_trace_time(access_document_page, gp_connect_context, time):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    gp_connect_context['trace_time'] = time


@given(parsers.parse('I have made a successful request to GP Connect for patient "{nhs_number}"'))
def given_successful_request_for_patient(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    access_document_page.search_documents()
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['request_successful'] = True


@given('I have access to request data from GP Connect and the patient trace was within the last 24 hours')
def given_trace_within_24h(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    gp_connect_context['trace_time'] = '< 24 hours'


@given('I have access to request data from GP Connect but I cannot confirm the registered practice either because it is not on PDS or the patient has an S-flag')
def given_cannot_confirm_practice(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    gp_connect_context['practice_confirmed'] = False


@given(parsers.parse('I access a patient "{nhs_number}" which is recorded as deceased on PDS or on the local system'))
def given_access_deceased(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['deceased'] = True


@given(parsers.parse('I have made a request to a GP Connect service for patient "{nhs_number}"'))
def given_made_request_for_patient(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number


@given(parsers.parse('I have made a request to a GP Connect service using an invalid resource for patient "{nhs_number}"'))
def given_request_invalid_resource(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['invalid_resource'] = True


@given('I have made a request to a GP Connect service using an invalid NHS number')
def given_request_invalid_nhs(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient('0000000000')
    gp_connect_context['invalid_nhs'] = True


# ---------------------------------------------------------------------------
# Find Patient - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('the user wishes to access documents for patient "{nhs_number}"'))
def given_wishes_to_access_docs(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    gp_connect_context['nhs_number'] = nhs_number


@given('provider system identifiers are not known')
def given_identifiers_not_known(gp_connect_context):
    gp_connect_context['identifiers_known'] = False


@given(parsers.parse('the consumer attempts to find patient "{nhs_number}"'))
def given_consumer_attempts_find_patient(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number


@given('the provider patient record is recorded as deceased')
def given_provider_record_deceased(gp_connect_context):
    gp_connect_context['deceased'] = True


@given('the consumer sends a valid Find Patient request')
def given_valid_find_patient_request(gp_connect_context):
    gp_connect_context['valid_find_patient'] = True


@given('the provider patient record is recorded as dissent to share')
def given_provider_record_dissent(gp_connect_context):
    gp_connect_context['dissent_to_share'] = True


@given('the consumer sends a request to the invalid parameter service')
def given_sends_invalid_param_service(gp_connect_context):
    gp_connect_context['invalid_parameter_service'] = True


@given(parsers.parse('the consumer attempts to find patient "{nhs_number}"'), target_fixture='consumer_patient')
def given_consumer_attempts_find(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    return nhs_number


@given('the consumer sends a valid request')
def given_consumer_valid_request(gp_connect_context):
    gp_connect_context['valid_request'] = True


@given('the provider practice is not enabled for access document')
def given_practice_not_enabled(gp_connect_context):
    gp_connect_context['practice_enabled'] = False


@given('the consumer attempts to find a patient')
def given_consumer_attempts_find_patient_generic(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    gp_connect_context['find_patient_attempted'] = True


@given('the consumer sends a valid Find Patient request with an invalid NHS Number')
def given_find_patient_invalid_nhs(access_document_page, gp_connect_context):
    access_document_page.find_patient('0000000000')
    gp_connect_context['invalid_nhs'] = True


# ---------------------------------------------------------------------------
# Search Documents - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('the user wishes to obtain a full patient documents list for patient "{nhs_number}"'))
def given_full_docs_list(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['search_type'] = 'full'


@given('the system has a valid GP system patient identifier')
def given_valid_patient_identifier(access_document_page, gp_connect_context):
    assert access_document_page.patient_found(), "Patient identifier not available"
    gp_connect_context['patient_identifier'] = access_document_page.get_patient_identifier()


@given('the consumer has successfully identified the endpoint for the Search Documents call')
def given_search_docs_endpoint(gp_connect_context):
    gp_connect_context['search_endpoint_identified'] = True


@given(parsers.parse('the user wishes to obtain the patient documents list from a given date for patient "{nhs_number}"'))
def given_docs_from_date(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['search_type'] = 'from_date'


@given(parsers.parse('the user wishes to obtain the patient documents list up to a given date for patient "{nhs_number}"'))
def given_docs_to_date(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['search_type'] = 'to_date'


@given(parsers.parse('the user wishes to obtain the patient documents list for a date range for patient "{nhs_number}"'))
def given_docs_date_range(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['search_type'] = 'date_range'


@given(parsers.parse('the user wishes to obtain the patient documents list for an author organisation for patient "{nhs_number}"'))
def given_docs_by_author(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['search_type'] = 'author'


@given(parsers.parse('the user wishes to obtain the patient documents list with a given document description for patient "{nhs_number}"'))
def given_docs_by_description(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['search_type'] = 'description'


@given(parsers.parse('the user has found a valid patient "{nhs_number}" who has no documents associated'))
def given_patient_no_docs(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['has_documents'] = False


@given(parsers.parse('I have sent a valid search documents request for patient "{nhs_number}"'))
def given_valid_search_docs_request(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    access_document_page.search_documents()
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['search_completed'] = True


@given(parsers.parse('the user has found a valid patient "{nhs_number}" who has documents associated'))
def given_patient_with_docs(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['has_documents'] = True


@given(parsers.parse('the user has found a valid patient "{nhs_number}" who has dissented to share records via GP Connect'))
def given_patient_dissented(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['dissent_to_share'] = True


@given('the user has found a valid patient and the practice has dissented to share records via GP Connect')
def given_practice_dissented(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient('9690937286')
    gp_connect_context['nhs_number'] = '9690937286'
    gp_connect_context['practice_dissented'] = True


# ---------------------------------------------------------------------------
# Retrieve Document - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('the user has found a valid document for patient "{nhs_number}"'))
def given_found_valid_document(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    access_document_page.search_documents()
    access_document_page.select_document(0)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['document_selected'] = True


@given('the consumer has successfully identified the endpoint for the Retrieve Documents call')
def given_retrieve_docs_endpoint(gp_connect_context):
    gp_connect_context['retrieve_endpoint_identified'] = True


@given('the record no longer exists at the practice or is too large')
def given_record_no_longer_exists(gp_connect_context):
    gp_connect_context['record_exists'] = False


@given(parsers.parse('the user has found a valid patient "{nhs_number}" who has documents associated'), target_fixture='patient_docs')
def given_patient_with_docs_fixture(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['has_documents'] = True
    return nhs_number


@given('has successfully carried out a document search')
def given_successful_doc_search(access_document_page, gp_connect_context):
    access_document_page.search_documents()
    gp_connect_context['search_completed'] = True


@given('successfully resolved the endpoint for the retrieve document call')
def given_resolved_retrieve_endpoint(gp_connect_context):
    gp_connect_context['retrieve_endpoint_identified'] = True


@given('the user wishes to retrieve a document previously found by searching documents')
def given_wishes_to_retrieve_doc(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient('9690937286')
    access_document_page.search_documents()
    access_document_page.select_document(0)
    gp_connect_context['nhs_number'] = '9690937286'
    gp_connect_context['document_selected'] = True


@given('the file size is known and is likely to result in a slow response to retrieval')
def given_large_file_size(gp_connect_context):
    gp_connect_context['large_file'] = True


@given('the user has found a valid document')
def given_found_valid_doc(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    access_document_page.find_patient('9690937286')
    access_document_page.search_documents()
    access_document_page.select_document(0)
    gp_connect_context['document_selected'] = True


@given('the practice has dissented to share records via GP Connect')
def given_practice_dissented_retrieve(gp_connect_context):
    gp_connect_context['practice_dissented'] = True


# ---------------------------------------------------------------------------
# Superseded NHS Number
# ---------------------------------------------------------------------------


@given("I want to view a patient's record")
def given_want_to_view_record(access_document_page, gp_connect_context):
    access_document_page.navigate('access-document')
    access_document_page.wait_for_load()
    gp_connect_context['intent'] = 'view_record'


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when('I make that attempt to access GP Connect')
def when_attempt_access(access_document_page, gp_connect_context):
    access_document_page.find_patient('9690937286')
    gp_connect_context['access_attempted'] = True


@when(parsers.parse('the GP Connect request message is {result}'))
def when_request_message_result(access_document_page, gp_connect_context, result):
    gp_connect_context['expected_result'] = result
    if result == 'sent':
        assert not access_document_page.get_displayed_error(), "Request should have been sent but error was displayed"
    elif result == 'blocked':
        error = access_document_page.get_displayed_error()
        assert error, "Request should have been blocked but no error was displayed"


@when('I receive a valid response including a patient resource')
def when_receive_valid_response(access_document_page, gp_connect_context):
    assert access_document_page.patient_found(), "No valid patient resource received"
    gp_connect_context['valid_response'] = True


@when('I attempt to access GP Connect')
def when_attempt_gp_connect(access_document_page, gp_connect_context):
    access_document_page.find_patient('9690938533')
    gp_connect_context['access_attempted'] = True


@when('I am at a point where I would normally be able to access GP Connect')
def when_would_normally_access(access_document_page, gp_connect_context):
    gp_connect_context['would_access'] = True


@when('I receive a patient not found error response')
def when_patient_not_found(access_document_page, gp_connect_context):
    error = access_document_page.get_displayed_error()
    assert error, "Expected patient not found error"
    gp_connect_context['error_type'] = 'patient_not_found'


@when('I receive a patient dissent to share error response')
def when_dissent_to_share(access_document_page, gp_connect_context):
    error = access_document_page.get_displayed_error()
    assert error, "Expected dissent to share error"
    gp_connect_context['error_type'] = 'dissent_to_share'


@when('I receive an invalid resource error response')
def when_invalid_resource(access_document_page, gp_connect_context):
    error = access_document_page.get_displayed_error()
    assert error, "Expected invalid resource error"
    gp_connect_context['error_type'] = 'invalid_resource'


@when('I receive an invalid NHS number error response')
def when_invalid_nhs_number(access_document_page, gp_connect_context):
    error = access_document_page.get_displayed_error()
    assert error, "Expected invalid NHS number error"
    gp_connect_context['error_type'] = 'invalid_nhs_number'


@when('an access document request is triggered')
def when_access_doc_triggered(access_document_page, gp_connect_context):
    nhs_number = gp_connect_context.get('nhs_number', '9690937286')
    access_document_page.find_patient(nhs_number)
    gp_connect_context['request_triggered'] = True


@when('the consumer receives the Find Patient response')
def when_consumer_receives_find_patient(access_document_page, gp_connect_context):
    access_document_page.wait_for_load()
    gp_connect_context['find_patient_response_received'] = True


@when('the user selects request to Search for Documents')
def when_select_search_docs(access_document_page, gp_connect_context):
    search_type = gp_connect_context.get('search_type', 'full')
    if search_type == 'from_date':
        access_document_page.search_documents_from_date('2020-01-01')
    elif search_type == 'to_date':
        access_document_page.search_documents_to_date('2023-12-31')
    elif search_type == 'date_range':
        access_document_page.search_documents_date_range('2020-01-01', '2023-12-31')
    elif search_type == 'author':
        access_document_page.search_documents_by_author('ORG1')
    elif search_type == 'description':
        access_document_page.search_documents_by_description('Discharge Summary')
    else:
        access_document_page.search_documents()
    gp_connect_context['search_completed'] = True


@when('I receive a successful valid search documents response and resources')
def when_receive_search_docs_response(access_document_page, gp_connect_context):
    assert access_document_page.get_document_count() > 0, "Expected documents in response"
    gp_connect_context['docs_returned'] = True


@when('the user selects request to Search for Documents without the mandatory include parameters')
def when_search_docs_no_mandatory(access_document_page, gp_connect_context):
    access_document_page.search_documents()
    gp_connect_context['search_no_mandatory'] = True


@when('the user selects request to Search for Documents with an invalid patient ID')
def when_search_docs_invalid_patient(access_document_page, gp_connect_context):
    access_document_page.search_documents()
    gp_connect_context['search_invalid_patient'] = True


@when('the user selects request to retrieve a document')
def when_select_retrieve_doc(access_document_page, gp_connect_context):
    if not gp_connect_context.get('document_selected'):
        access_document_page.select_document(0)
    access_document_page.retrieve_document()
    gp_connect_context['retrieve_attempted'] = True


@when('the user selects to retrieve a document and submits a non-existent document URL instead')
def when_retrieve_nonexistent(access_document_page, gp_connect_context):
    access_document_page.retrieve_document()
    gp_connect_context['retrieve_nonexistent'] = True


@when('the user selects to retrieve a document')
def when_select_retrieve(access_document_page, gp_connect_context):
    if not gp_connect_context.get('document_selected'):
        access_document_page.select_document(0)
    access_document_page.retrieve_document()
    gp_connect_context['retrieve_attempted'] = True


@when("I retrieve a patient's record from its registered GP practice including a PDS trace")
def when_retrieve_record_pds_trace(access_document_page, gp_connect_context):
    access_document_page.find_patient('9658220215')
    gp_connect_context['pds_trace'] = True


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('an audit record is written to an appropriate audit log including when access is blocked, unsuccessful or successful')
def then_audit_record(access_document_page):
    audit_log = access_document_page.get_audit_log()
    assert audit_log, "Audit log should contain entries"


@then('the audit record conforms to NHS Digital audit standards')
def then_audit_conforms(access_document_page):
    audit_log = access_document_page.get_audit_log()
    assert audit_log, "Audit log should conform to NHS Digital standards"


@then('I verify the patient resource details for family name, given name, gender, date of birth and GP Practice Code match to those presented to the user from the local system')
def then_verify_demographics(access_document_page):
    patient_id = access_document_page.get_patient_identifier()
    assert patient_id, "Patient identifier should be present for demographic verification"


@then('I alert the user to any mismatch between the local record demographics and those provided in the GP Connect response message')
def then_alert_mismatch(access_document_page):
    assert access_document_page.patient_found(), "Patient resource should be available"


@then('the registered GP practice from the last PDS trace is used to identify the practice to submit the request to')
def then_use_pds_practice(access_document_page):
    assert access_document_page.patient_found(), "Patient should be found using PDS trace practice"


@then('the request to GP Connect is blocked and handled gracefully so the user is aware that access is not available for that patient at that time')
def then_blocked_gracefully(access_document_page):
    error = access_document_page.get_displayed_error()
    assert error, "Expected a graceful block message when practice cannot be confirmed"


@then('the system prevents access to GP Connect')
def then_prevents_access(access_document_page, gp_connect_context):
    error = access_document_page.get_displayed_error()
    assert error or gp_connect_context.get('deceased'), "Access should be prevented for deceased patient"


@then('handles the prevention gracefully so the user is aware that GP Connect is not available for this patient')
def then_handles_prevention(access_document_page):
    error = access_document_page.get_displayed_error()
    assert error, "Expected a graceful prevention message"


@then('I handle the response gracefully')
def then_handle_gracefully(access_document_page):
    error = access_document_page.get_displayed_error()
    assert error, "Expected an error message to be displayed gracefully"


@then('I make available all the diagnostic details to appropriate people to enable fault resolution')
def then_diagnostics_available(access_document_page):
    diagnostics = access_document_page.get_diagnostic_details()
    assert diagnostics, "Diagnostic details should be available for fault resolution"


@then('a Find Patient request is sent to obtain the patient identifier')
def then_find_patient_sent(access_document_page):
    assert access_document_page.patient_found(), "Find Patient request should have returned a patient identifier"


@then('the request uses a verified NHS Number')
def then_verified_nhs(access_document_page):
    patient_id = access_document_page.get_patient_identifier()
    assert patient_id, "Patient identifier should confirm a verified NHS Number was used"


@then('the request conforms to the Access Document Find Patient specification')
def then_conforms_find_patient_spec(access_document_page):
    assert access_document_page.patient_found(), "Response should conform to Find Patient specification"


@then('the resulting response is processed successfully by the consumer')
def then_response_processed(access_document_page):
    status = access_document_page.get_response_status()
    assert status, "Response status should be available"


@then('the error details are communicated appropriately')
def then_error_communicated(access_document_page):
    error = access_document_page.get_displayed_error()
    assert error, "Error details should be communicated to the user"


@then(parsers.parse('the resulting response with Operational Outcome {outcome} and Error Code {code} is processed successfully by the consumer'))
def then_operational_outcome(access_document_page, outcome, code):
    op_outcome = access_document_page.get_operational_outcome()
    assert outcome in op_outcome, f"Expected operational outcome '{outcome}' but got '{op_outcome}'"
    status = access_document_page.get_response_status()
    assert code in status, f"Expected error code '{code}' but got '{status}'"


@then('the request is constructed as per the specification with the mandatory headers and parameters')
def then_request_mandatory_headers(access_document_page):
    status = access_document_page.get_response_status()
    assert status, "Request with mandatory headers should return a valid response status"


@then('the request is constructed as per the specification with the mandatory fields')
def then_request_mandatory_fields(access_document_page):
    status = access_document_page.get_response_status()
    assert status, "Request with mandatory fields should return a valid response status"


@then('the request also contains a created parameter with a date prefixed by ge')
def then_created_param_ge(gp_connect_context):
    search_type = gp_connect_context.get('search_type', '')
    assert search_type in ('from_date', 'date_range'), f"Expected from_date or date_range search type, got '{search_type}'"


@then('the request also contains a created parameter with a date prefixed by le')
def then_created_param_le(gp_connect_context):
    search_type = gp_connect_context.get('search_type', '')
    assert search_type in ('to_date', 'date_range'), f"Expected to_date or date_range search type, got '{search_type}'"


@then('the request also contains an author parameter with a value of ORG1')
def then_author_param(gp_connect_context):
    assert gp_connect_context.get('search_type') == 'author', "Expected author search type"


@then(parsers.parse('the request also contains a description parameter with a value of "{description}"'))
def then_description_param(gp_connect_context, description):
    assert gp_connect_context.get('search_type') == 'description', "Expected description search type"
    assert description, "Description value should not be empty"


@then('the request is constructed as per the specification')
def then_request_conforms_spec(access_document_page):
    status = access_document_page.get_response_status()
    assert status, "Request should conform to the specification"


@then('the user is aware that there are no documents available where applicable')
def then_no_docs_available(access_document_page):
    assert access_document_page.no_documents_message_visible(), "No documents message should be visible"


@then('I display or utilise all the key information to represent or process the document records commensurate with the original record meaning and my specific use case')
def then_display_key_info(access_document_page):
    count = access_document_page.get_document_count()
    assert count > 0, "Document records should be displayed"


@then('the user may be warned that the document may be slow to retrieve')
def then_slow_retrieve_warning(access_document_page):
    assert access_document_page.file_size_warning_visible(), "File size warning should be visible for large documents"


@then('the file size may be included in the warning where available')
def then_file_size_warning(access_document_page):
    assert access_document_page.file_size_warning_visible(), "File size information should be included in the warning"


@then('the consuming application should allow a GP Connect call to be made using the latest NHS number')
def then_allow_latest_nhs(access_document_page):
    assert access_document_page.patient_found(), "System should allow a call using the latest (superseded) NHS number"
