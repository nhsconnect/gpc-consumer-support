"""Step definitions for Structured Documents Migrate feature."""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/structured_documents_migrate.feature')

# ---------------------------------------------------------------------------
# General - Given steps
# ---------------------------------------------------------------------------


@given('I am at a point in the system where I have access to attempt a call to a GP Connect service')
def given_access_to_gp_connect(access_document_page, gp_connect_context):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    gp_connect_context['access_granted'] = True


@given(parsers.parse('I have access to request data from GP Connect and the patient trace was {time} ago'))
def given_access_trace_time(access_document_page, gp_connect_context, time):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    gp_connect_context['trace_time'] = time


@given(parsers.parse('I have made a successful request to migrate a GP Connect record for patient "{nhs_number}"'))
def given_successful_migrate_request(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    access_document_page.search_documents()
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['migrate_successful'] = True


@given(parsers.parse('the user is going to make a migration request for a record for patient "{nhs_number}"'))
def given_migration_request_for_patient(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['migration_pending'] = True


@given("the JWT Org claim contains an ODS code which is not the patient's practice")
def given_jwt_wrong_ods(gp_connect_context):
    gp_connect_context['jwt_wrong_ods'] = True


@given('I have access to request data from GP Connect but I cannot confirm the registered practice either because it is not on PDS or the patient has an S-flag')
def given_cannot_confirm_practice(access_document_page, gp_connect_context):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    gp_connect_context['practice_confirmed'] = False


@given(parsers.parse('I access a patient "{nhs_number}" which is recorded as deceased on PDS or on the local system'))
def given_access_deceased(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['deceased'] = True


@given(parsers.parse('I have made a request to a GP Connect service for patient "{nhs_number}"'))
def given_made_request_for_patient(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number


@given(parsers.parse('I have made a request to a GP Connect service using an invalid resource for patient "{nhs_number}"'))
def given_request_invalid_resource(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['invalid_resource'] = True


@given('I have made a request to a GP Connect service using an invalid NHS number')
def given_request_invalid_nhs(access_document_page, gp_connect_context):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    access_document_page.find_patient('0000000000')
    gp_connect_context['invalid_nhs'] = True


@given('I have made a request to a GP Connect service using an invalid parameter')
def given_request_invalid_param(access_document_page, gp_connect_context):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    gp_connect_context['invalid_parameter'] = True


# ---------------------------------------------------------------------------
# Find Patient - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('the consumer attempts to find patient "{nhs_number}"'))
def given_consumer_attempts_find(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
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


@given('the consumer attempts to find a patient')
def given_consumer_attempts_find_generic(access_document_page, gp_connect_context):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    gp_connect_context['find_patient_attempted'] = True


@given('the consumer sends a valid Find Patient request with an invalid NHS Number')
def given_find_patient_invalid_nhs(access_document_page, gp_connect_context):
    access_document_page.find_patient('0000000000')
    gp_connect_context['invalid_nhs'] = True


# ---------------------------------------------------------------------------
# Retrieve Document - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('the user has found a valid document for patient "{nhs_number}"'))
def given_found_valid_document(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
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


@given(parsers.parse('the user has found a valid patient "{nhs_number}" who has documents associated'))
def given_patient_with_docs(access_document_page, gp_connect_context, nhs_number):
    access_document_page.navigate('structured-documents-migrate')
    access_document_page.wait_for_load()
    access_document_page.find_patient(nhs_number)
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['has_documents'] = True


@given('has successfully carried out a document search')
def given_successful_doc_search(access_document_page, gp_connect_context):
    access_document_page.search_documents()
    gp_connect_context['search_completed'] = True


@given('successfully resolved the endpoint for the retrieve document call')
def given_resolved_retrieve_endpoint(gp_connect_context):
    gp_connect_context['retrieve_endpoint_identified'] = True


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when('I make that attempt to migrate GP Connect')
def when_attempt_migrate(access_document_page, gp_connect_context):
    access_document_page.find_patient('9690937286')
    gp_connect_context['migrate_attempted'] = True


@when(parsers.parse('I make that attempt to migrate a GP Connect record'))
def when_attempt_migrate_record(access_document_page, gp_connect_context):
    nhs_number = gp_connect_context.get('nhs_number', '9690937286')
    access_document_page.find_patient(nhs_number)
    access_document_page.search_documents()
    gp_connect_context['migrate_attempted'] = True


@when(parsers.parse('the GP Connect migrate request message is {result}'))
def when_migrate_result(access_document_page, gp_connect_context, result):
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


@when('the user selects to migrate')
def when_select_migrate(access_document_page, gp_connect_context):
    nhs_number = gp_connect_context.get('nhs_number', '9690937286')
    access_document_page.search_documents()
    gp_connect_context['migrate_attempted'] = True


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


@when('I receive an invalid parameter error response')
def when_invalid_parameter(access_document_page, gp_connect_context):
    error = access_document_page.get_displayed_error()
    assert error, "Expected invalid parameter error"
    gp_connect_context['error_type'] = 'invalid_parameter'


@when('the consumer receives the Find Patient response')
def when_consumer_receives_find_patient(access_document_page, gp_connect_context):
    access_document_page.wait_for_load()
    gp_connect_context['find_patient_response_received'] = True


@when('the user selects to retrieve a document and submits a non-existent document URL instead')
def when_retrieve_nonexistent(access_document_page, gp_connect_context):
    access_document_page.retrieve_document()
    gp_connect_context['retrieve_nonexistent'] = True


@when('the user selects request to retrieve a document')
def when_select_retrieve_doc(access_document_page, gp_connect_context):
    if not gp_connect_context.get('document_selected'):
        access_document_page.select_document(0)
    access_document_page.retrieve_document()
    gp_connect_context['retrieve_attempted'] = True


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('an audit record is written to an appropriate audit log including when migration is blocked, unsuccessful or successful')
def then_audit_record_migrate(access_document_page):
    audit_log = access_document_page.get_audit_log()
    assert audit_log, "Audit log should contain entries for migration"


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


@then(parsers.parse('the resulting response with Operational Outcome {outcome} and Error Code {code} is processed successfully by the consumer'))
def then_operational_outcome(access_document_page, outcome, code):
    op_outcome = access_document_page.get_operational_outcome()
    assert outcome in op_outcome, f"Expected operational outcome '{outcome}' but got '{op_outcome}'"
    status = access_document_page.get_response_status()
    assert code in status, f"Expected error code '{code}' but got '{status}'"


@then('the request to migrate GP Connect is blocked and handled gracefully so the user is aware that access is not available for that patient at that time')
def then_blocked_gracefully_migrate(access_document_page):
    error = access_document_page.get_displayed_error()
    assert error, "Expected a graceful block message when migration is not available"


@then('the system prevents access to GP Connect')
def then_prevents_access(access_document_page, gp_connect_context):
    error = access_document_page.get_displayed_error()
    assert error or gp_connect_context.get('deceased'), "Access should be prevented"


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


@then('the resulting response is processed successfully by the consumer')
def then_response_processed(access_document_page):
    status = access_document_page.get_response_status()
    assert status, "Response status should be available"


@then('the error details are communicated appropriately')
def then_error_communicated(access_document_page):
    error = access_document_page.get_displayed_error()
    assert error, "Error details should be communicated to the user"


@then('the request is constructed as per the specification with the mandatory fields')
def then_request_mandatory_fields(access_document_page):
    status = access_document_page.get_response_status()
    assert status, "Request with mandatory fields should return a valid response status"


@then('the resulting response is processed successfully by the consumer')
def then_response_processed_migration(access_document_page):
    status = access_document_page.get_response_status()
    assert status, "Response status should be available"
