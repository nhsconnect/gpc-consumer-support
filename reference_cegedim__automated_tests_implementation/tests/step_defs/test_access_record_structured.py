"""Step definitions for Access Record Structured feature."""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/access_record_structured.feature')

# ---------------------------------------------------------------------------
# General - Given steps
# ---------------------------------------------------------------------------


@given('I have imported GP Connect data')
def given_imported_gp_connect_data(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    access_record_structured_page.import_data()
    gp_connect_context['data_imported'] = True


@given('I support data sharing with other systems')
def given_support_data_sharing(gp_connect_context):
    gp_connect_context['data_sharing_enabled'] = True


@given('I am at a point in the system where I have access to attempt a call to a GP Connect service')
def given_access_to_gp_connect_service(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['access_point_reached'] = True


@given('I have access to request data from GP Connect and the patient trace was performed at a given time')
def given_access_with_trace_time(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['trace_time_set'] = True


@given('I have made a successful request to GP Connect')
def given_successful_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['request_successful'] = True


@given('I have access to request data from GP Connect and the patient trace was within the last 24 hours')
def given_access_trace_within_24h(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['trace_within_24h'] = True


@given('I have access to request data from GP Connect but I cannot confirm the registered practice either because it is not on PDS or the patient has an s-flag')
def given_cannot_confirm_practice(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['cannot_confirm_practice'] = True
    gp_connect_context['patient_has_s_flag'] = True


@given('I access a patient which is recorded as deceased on PDS or on the local system')
def given_access_deceased_patient(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['patient_deceased'] = True


@given('I have made a request to a GP Connect service')
def given_made_request_to_service(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['request_made'] = True


@given('I have made a request to a GP Connect service using an Invalid Resource')
def given_request_invalid_resource(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_resource'] = True


@given('I have made a request to a GP Connect service using an Invalid NHS Number')
def given_request_invalid_nhs_number(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9999999999')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_nhs_number'] = True


@given('I have made a request for allergies to a GP Connect service with invalid Allergies Parameters')
def given_request_invalid_allergy_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_allergy_params'] = True


@given('I have made a request for medications to a GP Connect service with invalid Medications Parameters')
def given_request_invalid_medication_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_medication_params'] = True


@given('I have sent a valid message to GP Connect')
def given_sent_valid_message(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    gp_connect_context['valid_message_sent'] = True


@given('I have requested allergies are included')
def given_requested_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('allergies', True)
    gp_connect_context['allergies_requested'] = True


@given('I have requested medications are included')
def given_requested_medications(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('medications', True)
    gp_connect_context['medications_requested'] = True


@given('I have received a valid message response')
def given_received_valid_response(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['valid_response_received'] = True


@given('I have received a successful valid response message')
def given_received_successful_response(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['successful_response'] = True


@given('I have included a request for medications data')
def given_included_medications_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('medications', True)
    gp_connect_context['medications_requested'] = True


@given('I have sent a request for both medications and allergies')
def given_sent_request_meds_and_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.submit_request()
    gp_connect_context['meds_and_allergies_requested'] = True


@given('I have sent a valid request to a provider at a higher version than I support')
def given_sent_request_higher_version(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['higher_version_request'] = True


# ---------------------------------------------------------------------------
# Medication - Given steps
# ---------------------------------------------------------------------------


@given('I am enabled to access GP Connect data for a given patient')
def given_enabled_access_gp_connect(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    gp_connect_context['patient_enabled'] = True


@given('I want to retrieve a full medication history')
def given_want_full_medication_history(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.set_prescription_issues(True)
    access_record_structured_page.clear_medication_search_from_date()
    gp_connect_context['full_medication_history'] = True


@given('I have received a successful valid medications message response')
def given_received_valid_medications_response(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.set_prescription_issues(True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['medications_response'] = access_record_structured_page.get_medication_results()


@given('I want to retrieve medication details but I do not require a full medication history')
def given_want_medication_details_not_full(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.set_medication_search_from_date('2020-01-01')
    gp_connect_context['partial_medication_history'] = True


@given('I am able to specify the date from which I want medications')
def given_able_to_specify_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('medications', True)
    gp_connect_context['date_specification_enabled'] = True


@given('my use case does or does not require medication issues to be included')
def given_use_case_medication_issues(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('medications', True)
    gp_connect_context['medication_issues_use_case'] = True


@given('the response has a list with an empty reason')
def given_response_empty_reason(access_record_structured_page, gp_connect_context):
    reason = access_record_structured_page.get_empty_list_reason()
    assert reason, "Expected an empty list reason in the response"
    gp_connect_context['empty_list_reason'] = reason


@given('the response does not include medication resources')
def given_no_medication_resources(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('medications')
    gp_connect_context['no_medication_resources'] = True


# ---------------------------------------------------------------------------
# Allergy - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view or import all current allergies or the system is set to only view or import all current allergies')
def given_view_current_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.set_include_resolved_allergies(False)
    gp_connect_context['current_allergies_only'] = True


@given('the user wishes to view or import all allergies including resolved allergies or the system is set to do so')
def given_view_all_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.set_include_resolved_allergies(True)
    gp_connect_context['include_resolved_allergies'] = True


@given('I have received a successful valid allergies message response')
def given_received_valid_allergies_response(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.set_include_resolved_allergies(True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['allergies_response'] = access_record_structured_page.get_allergy_results()


@given('the response includes resolved allergies')
def given_response_includes_resolved(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert 'resolved' in results.lower() or 'ended' in results.lower(), \
        "Expected resolved allergies in the response"
    gp_connect_context['has_resolved_allergies'] = True


@given('the response includes allergies which are not recognised by my system')
def given_unrecognised_allergies(gp_connect_context):
    gp_connect_context['unrecognised_allergies'] = True


@given('the response includes an empty active allergies list resource indicating that the patient record has no content recorded')
def given_empty_active_allergies_list(access_record_structured_page, gp_connect_context):
    reason = access_record_structured_page.get_empty_list_reason()
    assert reason, "Expected an empty list reason for active allergies"
    gp_connect_context['empty_allergies_list'] = True
    gp_connect_context['empty_list_reason'] = reason


@given('the response includes a single code item which indicates that the clinician has recorded that the patient has no known allergies')
def given_no_known_allergies_assertion(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert 'no known' in results.lower(), \
        "Expected 'no known allergies' assertion in the response"
    gp_connect_context['no_known_allergies'] = True


# ---------------------------------------------------------------------------
# General - When steps
# ---------------------------------------------------------------------------


@when('I receive a request for patient record data for a patient I hold GP Connect data for')
def when_receive_request_for_patient_data(access_record_structured_page, gp_connect_context):
    gp_connect_context['data_request_received'] = True


@when('I make that attempt to access GP Connect')
def when_attempt_access_gp_connect(access_record_structured_page, gp_connect_context):
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['access_attempted'] = True


@when('I receive a valid response including a patient resource')
def when_receive_valid_response_patient(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['patient_resource_received'] = True


@when('I attempt to access GP Connect')
def when_attempt_gp_connect(access_record_structured_page, gp_connect_context):
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['access_attempted'] = True


@when('I am at a point where I would normally be able to access GP Connect')
def when_would_normally_access(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['at_access_point'] = True


@when('I receive a patient not found error response')
def when_receive_patient_not_found(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'patient_not_found'


@when('I receive a patient dissent to share error response')
def when_receive_dissent_to_share(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'dissent_to_share'


@when('I receive an invalid resource error response')
def when_receive_invalid_resource(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'invalid_resource'


@when('I receive an invalid NHS number error response')
def when_receive_invalid_nhs_number(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'invalid_nhs_number'


@when('I receive an invalid parameter error response')
def when_receive_invalid_parameter(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'invalid_parameter'


@when('I receive a response including a data in transit warning')
def when_receive_data_in_transit(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.transit_warning_visible()
    gp_connect_context['transit_warning'] = True


@when('I receive a response including a confidential items warning for allergies')
def when_receive_confidential_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_allergies_warning'] = True


@when('I receive a response including a confidential items warning for medications')
def when_receive_confidential_medications(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_medications_warning'] = True


@when('I present the data to the end user')
def when_present_data(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['data_presented'] = True


@when('I import the GP Connect resource or data into the local system')
def when_import_data(access_record_structured_page, gp_connect_context):
    access_record_structured_page.import_data()
    gp_connect_context['data_imported'] = True


@when('I receive a response including a data in transit warning and a confidential data items warning for medications')
def when_receive_transit_and_confidential(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.transit_warning_visible()
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['transit_warning'] = True
    gp_connect_context['confidential_medications_warning'] = True


@when('the provider processes the request and returns a success response with resources for one clinical area and a warning that the other is not recognised')
def when_provider_returns_partial_success(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['partial_success'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('I receive the response it includes additional information')
def when_response_includes_additional_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['additional_info_received'] = True


# ---------------------------------------------------------------------------
# Medication - When steps
# ---------------------------------------------------------------------------


@when('I make the medication request to GP Connect')
def when_make_medication_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['medication_request_made'] = True


@when('I display or use the medication information')
def when_display_medication_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('medications')
    gp_connect_context['medication_info_displayed'] = True
    gp_connect_context['medication_results'] = access_record_structured_page.get_medication_results()


@when('I attempt to request medications by a future date')
def when_request_future_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.set_medication_search_from_date('2099-01-01')
    gp_connect_context['future_date_attempted'] = True


# ---------------------------------------------------------------------------
# Allergy - When steps
# ---------------------------------------------------------------------------


@when('the user selects to access current allergies from GP Connect')
def when_select_current_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['current_allergies_selected'] = True


@when('the user selects to access all allergies from GP Connect')
def when_select_all_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['all_allergies_selected'] = True


@when('I display or use the allergies information')
def when_display_allergies_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('allergies')
    gp_connect_context['allergies_info_displayed'] = True
    gp_connect_context['allergy_results'] = access_record_structured_page.get_allergy_results()


@when('I display or use the allergy information')
def when_display_allergy_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('allergies')
    gp_connect_context['allergy_info_displayed'] = True
    gp_connect_context['allergy_results'] = access_record_structured_page.get_allergy_results()


@when('I display or use the allergies response')
def when_display_allergies_response(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['allergies_response_displayed'] = True


# ---------------------------------------------------------------------------
# General - Then steps
# ---------------------------------------------------------------------------


@then('I only include GP Connect data where the request is for Direct Care use only')
def then_direct_care_only(gp_connect_context):
    assert gp_connect_context.get('data_imported'), "Data should have been imported"
    assert gp_connect_context.get('data_sharing_enabled'), "Data sharing should be enabled"


@then('I always include the resource identifiers received from GP Connect messages when exporting the data')
def then_include_resource_identifiers(access_record_structured_page):
    identifiers = access_record_structured_page.get_resource_identifiers()
    assert identifiers, "Resource identifiers should be present in exported data"


@then('an audit record is written to an appropriate audit log including when access is blocked, unsuccessful or successful')
def then_audit_record_written(gp_connect_context):
    assert gp_connect_context.get('access_attempted'), "Access should have been attempted"


@then('the audit record conforms to NHS Digital audit standards')
def then_audit_conforms(gp_connect_context):
    assert gp_connect_context.get('access_attempted'), "Access should have been attempted for audit"


@then('the GP Connect request message is blocked if the trace was more than 24 hours ago')
def then_blocked_if_old_trace(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('trace_time_set'), "Trace time should have been set"


@then('the GP Connect request message is sent if the trace was less than 24 hours ago')
def then_sent_if_recent_trace(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()


@then('I verify the patient resource details for family name, given name, gender, date of birth and GP Practice Code match to those in the local system')
def then_verify_demographics(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['demographics_verified'] = True


@then('I alert the user to any mismatch between the local record demographics and those provided in the GP Connect response message')
def then_alert_mismatch(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('demographics_verified'), "Demographics should have been verified"


@then('the registered GP practice from the last PDS trace is used to identify the practice to submit the request to')
def then_use_pds_trace_practice(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('trace_within_24h'), "Trace should be within 24 hours"
    assert access_record_structured_page.response_visible()


@then('the request to GP Connect is blocked and handled gracefully so the user is aware that access is not available for that patient at that time')
def then_blocked_gracefully(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('cannot_confirm_practice'), "Practice confirmation should have failed"
    error = access_record_structured_page.get_displayed_error()
    assert error, "An error message should be displayed to the user"


@then('the system prevents access to GP Connect')
def then_prevents_access(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('patient_deceased'), "Patient should be recorded as deceased"


@then('handles the prevention gracefully so the user is aware that GP Connect is not available for this patient')
def then_handles_prevention_gracefully(access_record_structured_page):
    error = access_record_structured_page.get_displayed_error()
    assert error, "A graceful error message should be displayed"


@then('I handle the response gracefully')
def then_handle_gracefully(access_record_structured_page, gp_connect_context):
    error = gp_connect_context.get('error_response', '')
    assert error, "Error response should have been captured"


@then('I make available all the diagnostic details to appropriate people to enable fault resolution')
def then_make_diagnostics_available(gp_connect_context):
    assert gp_connect_context.get('error_response'), "Error response details should be available"


@then('I make the user aware as appropriate')
def then_make_user_aware(access_record_structured_page):
    assert access_record_structured_page.warning_panel_visible(), \
        "Warning panel should be visible to the user"


@then('I make the user aware and apply controls as appropriate')
def then_make_user_aware_apply_controls(access_record_structured_page):
    assert access_record_structured_page.warning_panel_visible(), \
        "Warning panel should be visible to the user"
    assert access_record_structured_page.confidential_warning_visible(), \
        "Confidential warning should be visible"


@then('the user is aware that the data has come from the patient\'s registered GP record')
def then_user_aware_data_source(access_record_structured_page):
    assert access_record_structured_page.response_visible(), \
        "Response panel should be visible indicating data source"


@then('I always retain resource identifiers including but not limited to system and value')
def then_retain_identifiers(access_record_structured_page):
    identifiers = access_record_structured_page.get_resource_identifiers()
    assert identifiers, "Resource identifiers should be retained after import"


@then('I make the user aware as appropriate and that the data in transit warning is shown as applicable to all data')
def then_transit_warning_all_data(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    assert access_record_structured_page.transit_warning_visible(), \
        "Data in transit warning should be visible and apply to all data"


@then('the confidential data warning is shown to apply to medications data only')
def then_confidential_meds_only(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.confidential_warning_visible(), \
        "Confidential warning should be visible for medications"
    warning_text = access_record_structured_page.get_warning_text()
    gp_connect_context['confidential_warning_text'] = warning_text


@then('I recognise the warning in the response as appropriate to my use case')
def then_recognise_warning(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['warning_recognised'] = True


@then('I utilise the successful response information')
def then_utilise_success(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    has_meds = access_record_structured_page.has_results_for('medications')
    has_allergies = access_record_structured_page.has_results_for('allergies')
    assert has_meds or has_allergies, \
        "At least one clinical area should have returned results"


@then('I handle gracefully the warning that the request for the other area has failed informing users appropriately')
def then_handle_partial_failure(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    warning_text = access_record_structured_page.get_warning_text()
    assert warning_text, "Warning text should describe the partial failure"


@then('I ignore the additional information')
def then_ignore_additional_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['additional_info_ignored'] = True


@then('I process the response successfully')
def then_process_successfully(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()


# ---------------------------------------------------------------------------
# Medication - Then steps
# ---------------------------------------------------------------------------


@then('the request conforms to the GP Connect specification')
def then_request_conforms(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible(), \
        "A conforming request should produce a visible response"
    gp_connect_context['request_conforms'] = True


@then("includes the patient's NHS Number")
def then_includes_nhs_number(gp_connect_context):
    assert gp_connect_context.get('patient_enabled'), \
        "Patient NHS number should have been included in the request"


@then('the request has the includeMedication parameter')
def then_has_include_medication(access_record_structured_page):
    assert access_record_structured_page.has_results_for('medications'), \
        "Medication results should be present indicating the includeMedication parameter was set"


@then('the request sets the includePrescriptionIssues part parameter to true')
def then_prescription_issues_true(gp_connect_context):
    assert gp_connect_context.get('full_medication_history'), \
        "Prescription issues should be set to true for full medication history"


@then('the request does NOT include the medicationSearchFromDate parameter')
def then_no_search_from_date(gp_connect_context):
    assert gp_connect_context.get('full_medication_history'), \
        "medicationSearchFromDate should not be included for full history requests"


@then('the resulting response is processed successfully by the Consumer')
def then_response_processed(access_record_structured_page):
    assert access_record_structured_page.response_visible(), \
        "Response should be visible indicating successful processing"


@then('I display or utilise all the key information to represent or process the medication records commensurate with the original record meaning and my specific use case')
def then_display_medication_records(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_medication_results()
    assert results, "Medication results should contain key information"
    gp_connect_context['medication_records_displayed'] = True


@then('the request sets the includePrescriptionIssues part parameter to true or false')
def then_prescription_issues_true_or_false(gp_connect_context):
    assert gp_connect_context.get('partial_medication_history'), \
        "Prescription issues parameter should be set for partial medication history"


@then('the request includes the medicationSearchFromDate parameter')
def then_includes_search_from_date(gp_connect_context):
    assert gp_connect_context.get('partial_medication_history'), \
        "medicationSearchFromDate should be included for partial history requests"


@then('the medicationSearchFromDate is in the defined format')
def then_search_from_date_format(gp_connect_context):
    assert gp_connect_context.get('partial_medication_history'), \
        "Date format should be valid for medication search"


@then('the medicationSearchFromDate is equal or less than the current date')
def then_search_from_date_not_future(gp_connect_context):
    assert gp_connect_context.get('partial_medication_history'), \
        "medicationSearchFromDate should not be in the future"


@then('I am prevented from submitting the request')
def then_prevented_from_submitting(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('future_date_attempted'), \
        "A future date should have been attempted"
    error = access_record_structured_page.get_displayed_error()
    assert error, "An error should prevent submission with a future date"


@then('the request sets the includePrescriptionIssues part parameter to the appropriate value')
def then_prescription_issues_appropriate(gp_connect_context):
    assert gp_connect_context.get('medication_issues_use_case'), \
        "Prescription issues should be set appropriately for the use case"


@then('I display or utilise the list empty reason to inform the user that the patient has no medication records within the request parameters')
def then_display_empty_reason(access_record_structured_page, gp_connect_context):
    reason = access_record_structured_page.get_empty_list_reason()
    assert reason, "Empty list reason should be displayed to the user"
    assert gp_connect_context.get('empty_list_reason'), "Empty list reason should have been captured"


@then('the request does NOT include the includePrescriptionIssues part parameter OR includes and sets it to true')
def then_prescription_issues_absent_or_true(gp_connect_context):
    assert gp_connect_context.get('full_medication_history'), \
        "Prescription issues should be absent or true for full history v1.2.7"


@then('the request sets the includePrescriptionIssues part parameter to true, false, or is absent')
def then_prescription_issues_any(gp_connect_context):
    assert gp_connect_context.get('medication_issues_use_case'), \
        "Prescription issues parameter should be valid for the use case"


# ---------------------------------------------------------------------------
# Allergy - Then steps
# ---------------------------------------------------------------------------


@then('the resulting request is populated with valid syntax using the includeAllergies parameter with part parameter includeResolvedAllergies set to false')
def then_include_allergies_resolved_false(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('current_allergies_only'), \
        "Request should have includeResolvedAllergies set to false"
    assert access_record_structured_page.has_results_for('allergies'), \
        "Allergy results should be present"


@then('the resulting request is populated with valid syntax using the includeAllergies parameter with part parameter includeResolvedAllergies set to true')
def then_include_allergies_resolved_true(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('include_resolved_allergies'), \
        "Request should have includeResolvedAllergies set to true"
    assert access_record_structured_page.has_results_for('allergies'), \
        "Allergy results should be present"


@then('my system identifies the resolved allergies and handles them in a clinically safe manner such that they remain distinct from current allergies')
def then_resolved_allergies_distinct(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('has_resolved_allergies'), \
        "Resolved allergies should have been identified"
    results = access_record_structured_page.get_allergy_results()
    assert results, "Allergy results should be present for clinical review"


@then('where the resolved allergies are presented in the UI they are clearly and prominently labelled as ended, resolved or equivalent')
def then_resolved_allergies_labelled(access_record_structured_page):
    results = access_record_structured_page.get_allergy_results()
    assert 'resolved' in results.lower() or 'ended' in results.lower(), \
        "Resolved allergies should be labelled as resolved or ended"


@then('ensures that the resolved allergies cannot be utilised by decision support where decision support is in use')
def then_resolved_no_decision_support(gp_connect_context):
    assert gp_connect_context.get('has_resolved_allergies'), \
        "Resolved allergies should be excluded from decision support"


@then('I display or utilise all the key information to represent or process the allergy records commensurate with the original record meaning and my specific use case')
def then_display_allergy_records(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert results, "Allergy results should contain key information"
    gp_connect_context['allergy_records_displayed'] = True


@then('I display or utilise any SNOMED code or alternative code system coding as applicable to my use case')
def then_display_snomed_codes(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert results, "Allergy results should include code information"


@then('I display or utilise the allergy name as provided')
def then_display_allergy_name(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert results, "Allergy name should be displayed as provided"


@then('I can handle any records which are sent as allergies but are not recognised as allergy codes by my system')
def then_handle_unrecognised_allergies(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('unrecognised_allergies'), \
        "Unrecognised allergies should have been flagged"
    results = access_record_structured_page.get_allergy_results()
    assert results, "Unrecognised allergy records should still be handled"


@then('I recognise this as a record with no active allergies recorded')
def then_no_active_allergies(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('empty_allergies_list'), \
        "Empty allergies list should have been identified"
    reason = access_record_structured_page.get_empty_list_reason()
    assert reason, "Empty list reason should be displayed"


@then('I handle it appropriate to my use case and in such a way it is not confused with a clinical assertion of no known allergies')
def then_handle_no_active_allergies(gp_connect_context):
    assert gp_connect_context.get('empty_allergies_list'), \
        "Empty list should not be confused with no known allergies assertion"
    assert not gp_connect_context.get('no_known_allergies'), \
        "Should not be treated as a no known allergies assertion"


@then('I recognise this as a clinical assertion of no known allergies')
def then_recognise_no_known_allergies(gp_connect_context):
    assert gp_connect_context.get('no_known_allergies'), \
        "Should be recognised as a clinical assertion of no known allergies"


@then('I handle it appropriate to my use case and in such a way it is not confused with an empty list response')
def then_handle_no_known_allergies(gp_connect_context):
    assert gp_connect_context.get('no_known_allergies'), \
        "No known allergies assertion should not be confused with empty list"
    assert not gp_connect_context.get('empty_allergies_list'), \
        "Should not be treated as an empty list response"
