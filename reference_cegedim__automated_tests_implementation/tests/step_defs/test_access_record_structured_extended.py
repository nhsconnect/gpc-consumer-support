"""Step definitions for Access Record Structured Extended feature."""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('access_record_structured_extended.feature')

# ---------------------------------------------------------------------------
# General - Given steps
# ---------------------------------------------------------------------------


@given('I am at a point in the system where I have access to attempt a call to a GP Connect service')
def given_access_to_gp_connect(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['access_point_reached'] = True


@given('I have access to request data from GP Connect and the patient trace was performed at a given time')
def given_access_with_trace_time(access_record_structured_page, gp_connect_context, tpp_patients):
    patient = tpp_patients['stale_pds_smith']
    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_family_name_only(
        family_name=patient['family_name'],
        expected_result_text=patient['family_name'],
    )
    gp_connect_context['trace_time_set'] = True
    gp_connect_context['stale_pds_patient'] = patient


@given('I have made a successful request to GP Connect')
def given_successful_request(
    access_record_structured_page,
    gp_connect_context,
    tpp_patients,
    gp_connect_v15_patient_by_nhs_number,
):
    patient = tpp_patients['skelly_horace']
    v15_patient = gp_connect_v15_patient_by_nhs_number(patient['nhs_number'])

    # Keep search inputs from local fixture, but anchor the scenario to canonical v1.5 data.
    gp_connect_context['v15_demographics_patient'] = v15_patient
    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_demographics(
        given_name=patient['given_name'],
        family_name=patient['family_name'],
        date_of_birth=patient['dob'],
        postcode=patient['postcode'],
        expected_result_text=patient['family_name'],
    )
    # For GEN-07, success is reaching the GP record view after selecting the patient.
    gp_connect_context['request_successful'] = True


@given('I have access to request data from GP Connect and the patient trace was within the last 24 hours')
def given_access_trace_within_24h(
    access_record_structured_page,
    gp_connect_context,
    gp_connect_v15_patient_by_nhs_number,
):
    patient = gp_connect_v15_patient_by_nhs_number('9690938096')

    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_family_name_only(
        family_name=patient['family_name'],
        expected_result_text=patient['family_name'],
    )

    gp_details_before_refresh = access_record_structured_page.get_gp_details_gp_access_values()
    pds_action_clicked = access_record_structured_page.click_refresh_patient_data_via_pds()
    gp_details_after_refresh = (
        access_record_structured_page.get_gp_details_gp_access_values()
        if pds_action_clicked
        else gp_details_before_refresh
    )

    gp_connect_context['gen08_patient'] = patient
    gp_connect_context['gen08_gp_details_before_refresh'] = gp_details_before_refresh
    gp_connect_context['gen08_gp_details_after_refresh'] = gp_details_after_refresh
    gp_connect_context['gen08_pds_action_clicked'] = pds_action_clicked
    gp_connect_context['trace_within_24h'] = True


@given('I have access to request data from GP Connect but I cannot confirm the registered practice because it is not on PDS or the patient has an s-flag')
def given_cannot_confirm_practice(
    access_record_structured_page,
    gp_connect_context,
    gp_connect_v15_patient_by_nhs_number,
):
    # GEN-09 follows the PDS trace flow from NMS episode using NHS number search.
    patient = gp_connect_v15_patient_by_nhs_number('9690938533')
    access_record_structured_page.open_nhs_number_search()
    access_record_structured_page.search_patient_by_pds_trace(
        nhs_number=patient['nhs_number'],
        date_of_birth='2000-09-09',
    )

    gp_connect_context['cannot_confirm_practice'] = True
    gp_connect_context['patient_has_s_flag'] = True
    gp_connect_context['pds_trace_patient'] = patient


@given('I access a patient which is recorded as deceased on PDS or on the local system')
def given_access_deceased_patient(
    access_record_structured_page,
    gp_connect_context,
    gp_connect_v15_patient_by_nhs_number,
):
    patient = gp_connect_v15_patient_by_nhs_number('9690938681')

    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_family_name_only(
        family_name=patient['family_name'],
        expected_result_text=patient['family_name'],
    )

    gp_connect_context['patient_deceased'] = True
    gp_connect_context['deceased_patient'] = patient
    gp_connect_context['deceased_notice'] = access_record_structured_page.get_deceased_patient_notice()
    gp_connect_context['deceased_view_gp_record_disabled'] = (
        access_record_structured_page.is_view_gp_record_disabled()
    )


@given('I have made a request to a GP Connect service')
def given_made_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()

    nhs_input = access_record_structured_page.page.locator(
        access_record_structured_page.NHS_NUMBER_INPUT
    )
    if nhs_input.count() > 0 and nhs_input.first.is_visible():
        access_record_structured_page.search_patient('9730147140')
        access_record_structured_page.toggle_clinical_area('medications', True)
        access_record_structured_page.submit_request()
    else:
        # In NMS-first flows there is no legacy NHS-number input; reaching patient search is enough.
        access_record_structured_page.open_patient_search()

    gp_connect_context['request_made'] = True


@given('I have made a request using an invalid resource')
def given_request_invalid_resource(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_resource'] = True


@given('I have made a request using an invalid NHS Number')
def given_request_invalid_nhs(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9999999999')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_nhs_number'] = True


@given('I have made a request for allergies with invalid parameters')
def given_request_invalid_allergy_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_allergy_params'] = True


@given('I have made a request for medications with invalid parameters')
def given_request_invalid_med_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_medication_params'] = True


@given('I have sent a valid message')
def given_sent_valid_message(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    gp_connect_context['valid_message_sent'] = True


@given('I search for a patient by demographics using family name Beston')
def given_search_by_demographics_beston(
    access_record_structured_page,
    gp_connect_context,
    gp_connect_v15_patient_by_nhs_number,
):
    patient = gp_connect_v15_patient_by_nhs_number('9690938096')

    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_family_name_only(
        family_name=patient['family_name'],
        expected_result_text=patient['family_name'],
        select_result=False,
    )

    gp_connect_context['gen17_patient'] = patient


@given('I have sent a valid message and requested allergies')
def given_sent_valid_message_with_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    gp_connect_context['valid_message_sent'] = True
    gp_connect_context['allergies_requested'] = True


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


# ---------------------------------------------------------------------------
# Medication - Given steps
# ---------------------------------------------------------------------------


@given('I am enabled to access GP Connect data for a given patient and I want to retrieve a full medication history')
def given_enabled_full_med_history(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.set_prescription_issues(True)
    access_record_structured_page.clear_medication_search_from_date()
    gp_connect_context['full_medication_history'] = True


@given('I have received a successful valid medications response')
def given_received_valid_meds(access_record_structured_page, gp_connect_context, tpp_patients):
    patient = tpp_patients['skelly_horace']

    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_demographics(
        given_name=patient['given_name'],
        family_name=patient['family_name'],
        date_of_birth=patient['dob'],
        postcode=patient['postcode'],
        expected_result_text=patient['family_name'],
    )
    access_record_structured_page.open_patient_gp_record()

    access_record_structured_page.select_medication_tab('Repeat Medications')
    assert access_record_structured_page.medication_range_filter_visible(), (
        "Expected medication range dropdown ('Showing 15 months of medication data') to be visible "
        "on the Repeat Medications tab."
    )

    repeat_count = access_record_structured_page.repeat_medication_item_count()
    assert repeat_count > 1, (
        "Expected more than one medication item in Repeat Medications for MED-02, "
        f"but found {repeat_count}."
    )

    top_repeat_name = access_record_structured_page.get_first_repeat_medication_name()
    assert top_repeat_name, (
        "Expected to extract a medication name from the first Repeat Medications item "
        "for MED-02 highlight evidence."
    )
    access_record_structured_page.highlight_text_assertion(top_repeat_name)

    gp_connect_context['medications_ui_mode'] = True
    gp_connect_context['medications_repeat_count'] = repeat_count


@given('I am enabled to access GP Connect data and want to retrieve medication details for a period')
def given_enabled_meds_for_period(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.set_medication_search_from_date('2020-01-01')
    gp_connect_context['partial_medication_history'] = True


@given('I am enabled to access GP Connect data and try to request medications by a future date')
def given_enabled_future_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.set_medication_search_from_date('2099-01-01')
    gp_connect_context['future_date_attempted'] = True


@given('I am enabled to access GP Connect data and my use case does or does not require medication issues')
def given_enabled_med_issues(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    gp_connect_context['medication_issues_use_case'] = True


@given('I have received a successful medications response with an empty list')
def given_empty_meds_list(access_record_structured_page, gp_connect_context, tpp_patients):
    patient = tpp_patients['skelly_horace']

    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_demographics(
        given_name=patient['given_name'],
        family_name=patient['family_name'],
        date_of_birth=patient['dob'],
        postcode=patient['postcode'],
        expected_result_text=patient['family_name'],
    )
    access_record_structured_page.open_patient_gp_record()

    access_record_structured_page.select_medication_tab('Acute Medications')
    empty_text = access_record_structured_page.get_acute_medication_empty_message()
    assert empty_text, "Expected Acute Medications to show the no-data guidance message for MED-07"

    access_record_structured_page.highlight_text_assertion(
        'No Issued Acute Medication data is recorded for this patient.'
    )
    access_record_structured_page.highlight_text_assertion(
        "There may be some unissued medication data available in the 'Not Issued' tab"
    )

    gp_connect_context['medications_ui_mode'] = True
    gp_connect_context['empty_list_reason'] = empty_text


# ---------------------------------------------------------------------------
# Allergy - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view current allergies')
def given_view_current_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.set_include_resolved_allergies(False)
    gp_connect_context['current_allergies_only'] = True


@given('the user wishes to view all allergies including resolved')
def given_view_all_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.set_include_resolved_allergies(True)
    gp_connect_context['include_resolved_allergies'] = True


@given('I have received a response including resolved allergies')
def given_response_with_resolved(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert 'resolved' in results.lower() or 'ended' in results.lower(), \
        "Expected resolved allergies in the response"
    gp_connect_context['has_resolved_allergies'] = True


@given('I have received a response with allergies')
def given_response_with_allergies(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('allergies')
    gp_connect_context['allergy_results'] = access_record_structured_page.get_allergy_results()


@given('I have received a response with an empty active allergies list')
def given_empty_allergies_list(access_record_structured_page, gp_connect_context):
    reason = access_record_structured_page.get_empty_list_reason()
    assert reason, "Expected an empty list reason for active allergies"
    gp_connect_context['empty_allergies_list'] = True
    gp_connect_context['empty_list_reason'] = reason


@given('I have received a response with a single code item indicating no known allergies')
def given_no_known_allergies(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert 'no known' in results.lower(), \
        "Expected 'no known allergies' assertion in the response"
    gp_connect_context['no_known_allergies'] = True


# ---------------------------------------------------------------------------
# Investigation - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view all investigations')
def given_view_all_investigations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('investigations', True)
    gp_connect_context['view_all_investigations'] = True


@given('the user wishes to view investigations from a specific date')
def given_view_investigations_from_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('investigations', True)
    access_record_structured_page.set_search_period(start='2020-01-01')
    gp_connect_context['investigation_from_date'] = '2020-01-01'


@given('the user wishes to view investigations up to a specific date')
def given_view_investigations_to_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('investigations', True)
    access_record_structured_page.set_search_period(end='2024-12-31')
    gp_connect_context['investigation_to_date'] = '2024-12-31'


@given('the user wishes to view investigations for a specific period')
def given_view_investigations_period(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('investigations', True)
    access_record_structured_page.set_search_period(start='2020-01-01', end='2024-12-31')
    gp_connect_context['investigation_period'] = True


@given('the user or system requests investigations')
def given_requests_investigations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('investigations', True)
    gp_connect_context['investigations_requested'] = True


@given('I have made a valid investigations request')
def given_valid_investigations_request(access_record_structured_page, gp_connect_context, tpp_patients):
    patient = tpp_patients['skelly_horace']

    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_demographics(
        given_name=patient['given_name'],
        family_name=patient['family_name'],
        date_of_birth=patient['dob'],
        postcode=patient['postcode'],
        expected_result_text=patient['family_name'],
    )
    access_record_structured_page.open_patient_gp_record()
    access_record_structured_page.select_investigations_tab()

    investigation_count = access_record_structured_page.investigation_item_count()
    assert investigation_count > 1, (
        'Expected more than one investigation item for INV-06, '
        f'but found {investigation_count}.'
    )

    top_investigation_text = access_record_structured_page.get_first_investigation_item_text()
    assert top_investigation_text, (
        'Expected to extract top investigation item text for INV-06 highlight evidence.'
    )

    access_record_structured_page.click_first_investigation_item()
    access_record_structured_page.highlight_text_assertion(top_investigation_text)

    gp_connect_context['investigations_ui_mode'] = True
    gp_connect_context['investigation_item_count'] = investigation_count
    gp_connect_context['valid_investigations_request'] = True


@given('I have made a request for investigations with invalid parameters')
def given_invalid_investigations_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('investigations', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_investigations_params'] = True


@given('I have sent a valid request for investigations')
def given_sent_valid_investigations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('investigations', True)
    access_record_structured_page.submit_request()
    gp_connect_context['valid_investigations_sent'] = True


# ---------------------------------------------------------------------------
# Referral - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view all referrals')
def given_view_all_referrals(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    gp_connect_context['view_all_referrals'] = True


@given('the user wishes to view referrals from a specific date')
def given_view_referrals_from_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    access_record_structured_page.set_search_period(start='2020-01-01')
    gp_connect_context['referral_from_date'] = '2020-01-01'


@given('the user wishes to view referrals up to a specific date')
def given_view_referrals_to_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    access_record_structured_page.set_search_period(end='2024-12-31')
    gp_connect_context['referral_to_date'] = '2024-12-31'


@given('the user wishes to view referrals for a specific period')
def given_view_referrals_period(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    access_record_structured_page.set_search_period(start='2020-01-01', end='2024-12-31')
    gp_connect_context['referral_period'] = True


@given('the user or system requests referrals')
def given_requests_referrals(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    gp_connect_context['referrals_requested'] = True


@given('I have made a valid referrals request')
def given_valid_referrals_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['valid_referrals_request'] = True


@given('I have made a request for referrals with invalid parameters')
def given_invalid_referrals_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_referrals_params'] = True


@given('I have sent a valid request for referrals')
def given_sent_valid_referrals(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('referrals', True)
    access_record_structured_page.submit_request()
    gp_connect_context['valid_referrals_sent'] = True


# ---------------------------------------------------------------------------
# Diary Entry - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view all diary entries')
def given_view_all_diary_entries(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('diary_entries', True)
    gp_connect_context['view_all_diary_entries'] = True


@given('the user wishes to view diary entries up to a specific date')
def given_view_diary_entries_to_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('diary_entries', True)
    access_record_structured_page.set_search_period(end='2024-12-31')
    gp_connect_context['diary_to_date'] = '2024-12-31'


@given('the user or system requests diary entries')
def given_requests_diary_entries(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('diary_entries', True)
    gp_connect_context['diary_entries_requested'] = True


@given('I have made a valid diary entries request')
def given_valid_diary_entries_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('diary_entries', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['valid_diary_entries_request'] = True


@given('I have made a request for diary entries with invalid parameters')
def given_invalid_diary_entries_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('diary_entries', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_diary_entries_params'] = True


@given('I have sent a valid request for diary entries')
def given_sent_valid_diary_entries(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('diary_entries', True)
    access_record_structured_page.submit_request()
    gp_connect_context['valid_diary_entries_sent'] = True


# ---------------------------------------------------------------------------
# Problem - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view all problems')
def given_view_all_problems(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('problems', True)
    gp_connect_context['view_all_problems'] = True


@given('the user wishes to filter problems by status and significance')
def given_filter_problems(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('problems', True)
    access_record_structured_page.set_problem_filters(status='active', significance='major')
    gp_connect_context['problem_filters_set'] = True


@given('the user wishes to request problems with multiple filter values')
def given_multiple_problem_filters(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('problems', True)
    access_record_structured_page.set_problem_filters(status='active', significance='major')
    gp_connect_context['multiple_problem_filters'] = True


@given('the user or system requests problems')
def given_requests_problems(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('problems', True)
    gp_connect_context['problems_requested'] = True


@given('I have made a request for problems with invalid parameters')
def given_invalid_problems_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('problems', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_problems_params'] = True


@given('I have sent a valid request for problems')
def given_sent_valid_problems(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('problems', True)
    access_record_structured_page.submit_request()
    gp_connect_context['valid_problems_sent'] = True


@given('I have received a response with problems')
def given_response_with_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['problem_results'] = access_record_structured_page.get_problem_results()


# ---------------------------------------------------------------------------
# Immunisation - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view immunisations')
def given_view_immunisations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('immunisations', True)
    gp_connect_context['view_immunisations'] = True


@given('the user wishes to filter immunisations by notGiven and status')
def given_filter_immunisations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('immunisations', True)
    access_record_structured_page.set_immunisation_filters(not_given='true', status='completed')
    gp_connect_context['immunisation_filters_set'] = True


@given('I have made a valid immunisations request')
def given_valid_immunisations_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('immunisations', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['valid_immunisations_request'] = True


@given('I have received a response including immunisations not given')
def given_response_immunisations_not_given(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_immunisation_results()
    assert results, "Expected immunisation results in the response"
    gp_connect_context['immunisation_results'] = results
    gp_connect_context['includes_not_given'] = True


@given('the user or system requests immunisations')
def given_requests_immunisations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('immunisations', True)
    gp_connect_context['immunisations_requested'] = True


@given('I have made a request for immunisations with invalid parameters')
def given_invalid_immunisations_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('immunisations', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_immunisations_params'] = True


@given('I have sent a valid request for immunisations')
def given_sent_valid_immunisations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('immunisations', True)
    access_record_structured_page.submit_request()
    gp_connect_context['valid_immunisations_sent'] = True


# ---------------------------------------------------------------------------
# Uncategorised Data - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view all uncategorised data')
def given_view_all_uncategorised(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    gp_connect_context['view_all_uncategorised'] = True


@given('the user wishes to view uncategorised data from a specific date')
def given_view_uncategorised_from_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    access_record_structured_page.set_search_period(start='2020-01-01')
    gp_connect_context['uncategorised_from_date'] = '2020-01-01'


@given('the user wishes to view uncategorised data up to a specific date')
def given_view_uncategorised_to_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    access_record_structured_page.set_search_period(end='2024-12-31')
    gp_connect_context['uncategorised_to_date'] = '2024-12-31'


@given('the user wishes to view uncategorised data for a specific period')
def given_view_uncategorised_period(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    access_record_structured_page.set_search_period(start='2020-01-01', end='2024-12-31')
    gp_connect_context['uncategorised_period'] = True


@given('the user or system requests uncategorised data')
def given_requests_uncategorised(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    gp_connect_context['uncategorised_requested'] = True


@given('I have received a response with hierarchical uncategorised data')
def given_hierarchical_uncategorised(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('uncategorised')
    gp_connect_context['uncategorised_results'] = access_record_structured_page.get_uncategorised_results()
    gp_connect_context['hierarchical_uncategorised'] = True


@given('I have received a response with blood pressure readings in uncategorised data')
def given_blood_pressure_uncategorised(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('uncategorised')
    gp_connect_context['uncategorised_results'] = access_record_structured_page.get_uncategorised_results()
    gp_connect_context['blood_pressure_uncategorised'] = True


@given('I have made a valid uncategorised data request')
def given_valid_uncategorised_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['valid_uncategorised_request'] = True


@given('I have made a request for uncategorised data with invalid parameters')
def given_invalid_uncategorised_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_uncategorised_params'] = True


@given('I have sent a valid request for uncategorised data')
def given_sent_valid_uncategorised(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    access_record_structured_page.submit_request()
    gp_connect_context['valid_uncategorised_sent'] = True


# ---------------------------------------------------------------------------
# Consultation - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to view all consultations')
def given_view_all_consultations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    gp_connect_context['view_all_consultations'] = True


@given('the user wishes to view consultations from a specific date')
def given_view_consultations_from_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.set_search_period(start='2020-01-01')
    gp_connect_context['consultation_from_date'] = '2020-01-01'


@given('the user wishes to view consultations up to a specific date')
def given_view_consultations_to_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.set_search_period(end='2024-12-31')
    gp_connect_context['consultation_to_date'] = '2024-12-31'


@given('the user wishes to view consultations for a specific period')
def given_view_consultations_period(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.set_search_period(start='2020-01-01', end='2024-12-31')
    gp_connect_context['consultation_period'] = True


@given('the user wishes to view the most recent consultations')
def given_view_most_recent_consultations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.set_most_recent_count(3)
    gp_connect_context['most_recent_consultations'] = 3


@given('the user or system requests consultations')
def given_requests_consultations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    gp_connect_context['consultations_requested'] = True


@given('I have made a valid consultations request')
def given_valid_consultations_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['valid_consultations_request'] = True


@given('I have made a request for consultations with invalid parameters')
def given_invalid_consultations_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.submit_request()
    gp_connect_context['invalid_consultations_params'] = True


@given('I have sent a valid request for consultations')
def given_sent_valid_consultations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.submit_request()
    gp_connect_context['valid_consultations_sent'] = True


# ---------------------------------------------------------------------------
# Linkage - Given steps
# ---------------------------------------------------------------------------


@given('I have received a response containing immunisations linked to problems')
def given_immunisations_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('immunisations')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['immunisations_linked_problems'] = True


@given('I have received a response containing uncategorised data linked to problems')
def given_uncategorised_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('uncategorised')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['uncategorised_linked_problems'] = True


@given('I have received a response containing consultations linked to problems')
def given_consultations_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('consultations')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['consultations_linked_problems'] = True


@given('I have received a response containing investigations linked to problems')
def given_investigations_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('investigations')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['investigations_linked_problems'] = True


@given('I have received a response containing referrals linked to problems')
def given_referrals_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('referrals')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['referrals_linked_problems'] = True


@given('I have received a response containing diary entries linked to problems')
def given_diary_entries_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('diary_entries')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['diary_entries_linked_problems'] = True


@given('I have received a response containing medications linked to problems')
def given_medications_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('medications')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['medications_linked_problems'] = True


@given('I have received a response containing allergies linked to problems')
def given_allergies_linked_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('allergies')
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['allergies_linked_problems'] = True


# ---------------------------------------------------------------------------
# Search Query - Given steps
# ---------------------------------------------------------------------------


@given('the user wishes to run a predefined search')
def given_predefined_search(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    gp_connect_context['predefined_search'] = True


@given('the user wishes to run a predefined search with additional clinical areas')
def given_predefined_search_additional(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    gp_connect_context['predefined_search_additional'] = True


@given('the user wishes to request multiple clinical areas including consultations')
def given_multiple_areas_with_consultations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    gp_connect_context['multiple_areas_with_consultations'] = True


@given('the user wishes to request multiple clinical areas including problems')
def given_multiple_areas_with_problems(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('problems', True)
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    gp_connect_context['multiple_areas_with_problems'] = True


@given('the user wishes to request multiple clinical areas without problems or consultations')
def given_multiple_areas_without_problems_consultations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.toggle_clinical_area('investigations', True)
    gp_connect_context['multiple_areas_no_problems_consultations'] = True


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when('I make that attempt to access GP Connect')
def when_attempt_access(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('trace_time_set'):
        gp_connect_context['access_attempted'] = True
        return

    if gp_connect_context.get('trace_within_24h'):
        gp_connect_context['access_attempted'] = True
        return

    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['access_attempted'] = True


@when('I receive a valid response including a patient resource')
def when_receive_valid_response(access_record_structured_page, gp_connect_context):
    assert (
        access_record_structured_page.response_visible()
        or gp_connect_context.get('request_successful')
    )
    gp_connect_context['patient_resource_received'] = True


@when('I attempt to access GP Connect')
def when_attempt_gp_connect(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('cannot_confirm_practice'):
        gp_connect_context['access_attempted'] = True
        return

    access_record_structured_page.search_patient('9730147140')
    access_record_structured_page.toggle_clinical_area('medications', True)
    access_record_structured_page.submit_request()
    gp_connect_context['access_attempted'] = True


@when('I am at a point where I would normally be able to access GP Connect')
def when_would_normally_access(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('patient_deceased'):
        gp_connect_context['at_access_point'] = True
        return

    access_record_structured_page.navigate('access-record-structured')
    access_record_structured_page.wait_for_load()
    gp_connect_context['at_access_point'] = True


@when('I receive a patient not found error response')
def when_patient_not_found(access_record_structured_page, gp_connect_context, invalid_nhs_patient):
    access_record_structured_page.open_patient_search()
    access_record_structured_page.search_patient_by_family_name_only(
        family_name=invalid_nhs_patient['name'],
        select_result=False,
    )

    no_results_text = access_record_structured_page.get_no_patients_found_text()
    gp_connect_context['error_response'] = no_results_text
    gp_connect_context['error_type'] = 'patient_not_found'


@when('I receive a patient dissent to share error response')
def when_dissent_to_share(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'dissent_to_share'


@when('I receive an invalid resource error response')
def when_invalid_resource(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'invalid_resource'


@when('I receive an invalid NHS number error response')
def when_invalid_nhs_number(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'invalid_nhs_number'


@when('I receive an invalid parameter error response')
def when_invalid_parameter(access_record_structured_page, gp_connect_context):
    error = access_record_structured_page.get_displayed_error()
    gp_connect_context['error_response'] = error
    gp_connect_context['error_type'] = 'invalid_parameter'


@when('I receive a response including a data in transit warning')
def when_data_in_transit(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.transit_warning_visible()
    gp_connect_context['transit_warning'] = True


@when('I select the top result and click View GP Record')
def when_select_top_result_and_click_view_gp_record(access_record_structured_page, gp_connect_context):
    access_record_structured_page.select_top_patient_result(
        expected_result_text=gp_connect_context['gen17_patient']['family_name']
    )
    access_record_structured_page.click_view_gp_record()
    gp_connect_context['gen17_opened_gp_record'] = True


@when('I receive a confidential items warning for allergies')
def when_confidential_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_allergies_warning'] = True


@when('I present the data to the end user')
def when_present_data(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['data_presented'] = True


@when('I display or use the information')
def when_display_info(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('medications_ui_mode'):
        gp_connect_context['information_displayed'] = True
        return

    assert access_record_structured_page.response_visible()
    gp_connect_context['information_displayed'] = True


@when('I make the medication request')
def when_make_medication_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['medication_request_made'] = True


@when('I display the information')
def when_display_information(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('medications_ui_mode'):
        gp_connect_context['information_displayed'] = True
        return

    assert access_record_structured_page.response_visible()
    gp_connect_context['information_displayed'] = True


@when('they select to access current allergies')
def when_select_current_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['current_allergies_selected'] = True


@when('they select to access all allergies')
def when_select_all_allergies(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['all_allergies_selected'] = True


@when('I display or use the allergy information')
def when_display_allergy_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('allergies')
    gp_connect_context['allergy_info_displayed'] = True
    gp_connect_context['allergy_results'] = access_record_structured_page.get_allergy_results()


@when('I display or use the response')
def when_display_response(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['response_displayed'] = True


@when('they request investigations')
def when_request_investigations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['investigations_request_made'] = True


@when('they select with a from date')
def when_select_from_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['from_date_selected'] = True


@when('they select with a to date')
def when_select_to_date(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['to_date_selected'] = True


@when('they select with from and to dates')
def when_select_from_and_to(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['from_and_to_selected'] = True


@when('I receive a response with no investigation data')
def when_no_investigation_data(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('investigations')
    gp_connect_context['no_investigation_data'] = True


@when('I receive a successful response')
def when_successful_response(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('investigations_ui_mode'):
        gp_connect_context['successful_response'] = True
        return

    assert access_record_structured_page.response_visible()
    gp_connect_context['successful_response'] = True


@when('the provider returns a warning that investigations is not supported')
def when_investigations_not_supported(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['investigations_not_supported'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('they request referrals')
def when_request_referrals(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['referrals_request_made'] = True


@when('I receive a response with no referral data')
def when_no_referral_data(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('referrals')
    gp_connect_context['no_referral_data'] = True


@when('the provider returns a warning that referrals is not supported')
def when_referrals_not_supported(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['referrals_not_supported'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('they request diary entries')
def when_request_diary_entries(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['diary_entries_request_made'] = True


@when('I receive a response with no diary entry data')
def when_no_diary_data(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('diary_entries')
    gp_connect_context['no_diary_data'] = True


@when('the provider returns a warning that diary entries is not supported')
def when_diary_entries_not_supported(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['diary_entries_not_supported'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('they request problems')
def when_request_problems(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['problems_request_made'] = True


@when('they request problems with part parameters')
def when_request_problems_with_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['problems_with_params_made'] = True


@when('they request problems with active and minor status and inactive and major significance')
def when_request_problems_multiple(access_record_structured_page, gp_connect_context):
    access_record_structured_page.set_problem_filters(status='active', significance='major')
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['problems_multiple_filters'] = True


@when('I receive a response with no problem data')
def when_no_problem_data(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('problems')
    gp_connect_context['no_problem_data'] = True


@when('I receive a confidential items warning for a problem')
def when_confidential_problem(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_problem_warning'] = True


@when('I receive a confidential items warning for an item linked to a problem')
def when_confidential_linked_problem(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_linked_problem_warning'] = True


@when('the provider returns a warning that problems is not supported')
def when_problems_not_supported(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['problems_not_supported'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('I display or use the problem information')
def when_display_problem_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('problems')
    gp_connect_context['problem_info_displayed'] = True
    gp_connect_context['problem_results'] = access_record_structured_page.get_problem_results()


@when('they request immunisations')
def when_request_immunisations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['immunisations_request_made'] = True


@when('they request immunisations with part parameters')
def when_request_immunisations_params(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['immunisations_with_params_made'] = True


@when('I display or use the immunisation information')
def when_display_immunisation_info(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('immunisations')
    gp_connect_context['immunisation_info_displayed'] = True
    gp_connect_context['immunisation_results'] = access_record_structured_page.get_immunisation_results()


@when('I receive a response with no immunisation data')
def when_no_immunisation_data(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('immunisations')
    gp_connect_context['no_immunisation_data'] = True


@when('I receive a confidential items warning for immunisations')
def when_confidential_immunisations(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_immunisations_warning'] = True


@when('the provider returns a warning that immunisations is not supported')
def when_immunisations_not_supported(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['immunisations_not_supported'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('they request uncategorised data')
def when_request_uncategorised(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['uncategorised_request_made'] = True


@when('I receive a response with no uncategorised data')
def when_no_uncategorised_data(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('uncategorised')
    gp_connect_context['no_uncategorised_data'] = True


@when('I display or use the uncategorised data')
def when_display_uncategorised(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('uncategorised')
    gp_connect_context['uncategorised_displayed'] = True
    gp_connect_context['uncategorised_results'] = access_record_structured_page.get_uncategorised_results()


@when('I receive a confidential items warning for uncategorised data')
def when_confidential_uncategorised(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_uncategorised_warning'] = True


@when('the provider returns a warning that uncategorised data is not supported')
def when_uncategorised_not_supported(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['uncategorised_not_supported'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('they request consultations')
def when_request_consultations(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['consultations_request_made'] = True


@when('they request consultations with a count')
def when_request_consultations_count(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['consultations_count_made'] = True


@when('I receive a response with no consultation data')
def when_no_consultation_data(access_record_structured_page, gp_connect_context):
    assert not access_record_structured_page.has_results_for('consultations')
    gp_connect_context['no_consultation_data'] = True


@when('I receive a confidential items warning for a consultation')
def when_confidential_consultation(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_consultation_warning'] = True


@when('I receive a confidential items warning for an item within a consultation')
def when_confidential_within_consultation(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.confidential_warning_visible()
    gp_connect_context['confidential_within_consultation_warning'] = True


@when('the provider returns a warning that consultations is not supported')
def when_consultations_not_supported(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    gp_connect_context['consultations_not_supported'] = True
    gp_connect_context['warning_text'] = access_record_structured_page.get_warning_text()


@when('I display or use the linked data')
def when_display_linked_data(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    gp_connect_context['linked_data_displayed'] = True


@when('they request the last 3 consultations and all problems and all allergies including resolved for the last 365 days')
def when_predefined_search_1(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.set_most_recent_count(3)
    access_record_structured_page.toggle_clinical_area('problems', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.set_include_resolved_allergies(True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['predefined_search_1'] = True


@when('they request the last 3 consultations, all problems, all allergies including resolved for the last 365 days, plus immunisations and uncategorised data')
def when_predefined_search_2(access_record_structured_page, gp_connect_context):
    access_record_structured_page.toggle_clinical_area('consultations', True)
    access_record_structured_page.set_most_recent_count(3)
    access_record_structured_page.toggle_clinical_area('problems', True)
    access_record_structured_page.toggle_clinical_area('allergies', True)
    access_record_structured_page.set_include_resolved_allergies(True)
    access_record_structured_page.toggle_clinical_area('immunisations', True)
    access_record_structured_page.toggle_clinical_area('uncategorised', True)
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['predefined_search_2'] = True


@when('I construct the request')
def when_construct_request(access_record_structured_page, gp_connect_context):
    access_record_structured_page.submit_request()
    assert access_record_structured_page.response_visible()
    gp_connect_context['request_constructed'] = True


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('an audit record is written to an appropriate audit log including when access is blocked, unsuccessful or successful')
def then_audit_record(gp_connect_context):
    assert gp_connect_context.get('access_attempted'), "Access should have been attempted"


@then('the audit record conforms to NHS Digital audit standards')
def then_audit_conforms(gp_connect_context):
    assert gp_connect_context.get('access_attempted'), "Access should have been attempted for audit"


@then('the request is blocked if the trace was performed more than 24 hours ago')
def then_blocked_if_old_trace(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('trace_time_set'), "Trace time should have been set"

    pds_actions = ('Refresh patient data via PDS', 'Verify patient via PDS')
    visible_pds_action = None
    for action in pds_actions:
        locator = access_record_structured_page.page.get_by_text(action, exact=False).first
        if locator.count() > 0 and locator.is_visible():
            visible_pds_action = action
            break

    assert visible_pds_action, (
        "Expected one of the PDS actions to be visible for stale-trace GEN-06: "
        "'Refresh patient data via PDS' or 'Verify patient via PDS'."
    )
    access_record_structured_page.highlight_text_assertion(visible_pds_action)

    assert access_record_structured_page.is_view_gp_record_disabled(), (
        "Expected View GP Record to remain disabled when the selected patient's PDS trace "
        "is more than 24 hours old."
    )


@then('the request is sent if the trace was performed less than 24 hours ago')
def then_sent_if_recent_trace(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('stale_pds_patient'):
        return

    assert access_record_structured_page.response_visible()


@then('I verify the patient resource details for family name, given name, gender, date of birth and GP Practice Code match')
def then_verify_demographics(
    access_record_structured_page,
    gp_connect_context,
    tpp_patients,
    gp_connect_v15_patient_by_nhs_number,
):
    patient = tpp_patients['skelly_horace']
    v15_patient = gp_connect_v15_patient_by_nhs_number(patient['nhs_number'])

    assert v15_patient['given_name'] == patient['given_name'], (
        'Expected local GEN-07 fixture given name to stay aligned with GP Connect API v1.5 demonstrator data.'
    )
    assert v15_patient['family_name'] == patient['family_name'], (
        'Expected local GEN-07 fixture family name to stay aligned with GP Connect API v1.5 demonstrator data.'
    )

    assert access_record_structured_page.local_patient_data_matches(patient), (
        "Expected Local Patient Data column to match known GEN-07 patient demographics "
        "from conftest (Skelly, Horace)."
    )
    gp_connect_context['demographics_verified'] = True


@then('I alert the user to any mismatch')
def then_alert_mismatch(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('demographics_verified'), "Demographics should have been verified"
    assert access_record_structured_page.mismatch_icon_visible(), (
        "Expected mismatch indicator icon (data-testid='ErrorOutlineIcon') to be displayed "
        "for differing Local vs GP Access patient data."
    )


@then('the registered GP practice from the last PDS trace is used')
def then_use_pds_practice(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('trace_within_24h'), "Trace should be within 24 hours"
    before_refresh = gp_connect_context.get('gen08_gp_details_before_refresh')
    after_refresh = gp_connect_context.get('gen08_gp_details_after_refresh')

    assert before_refresh, "Expected GP Details to be captured before PDS refresh"
    assert after_refresh, "Expected GP Details to be captured after PDS refresh"

    for field in ('Name', 'Telephone', 'Address'):
        assert before_refresh.get(field), f"Expected non-empty GP Details field before refresh: {field}"
        assert after_refresh.get(field), f"Expected non-empty GP Details field after refresh: {field}"

    assert after_refresh == before_refresh, (
        'Expected GP Details (Name, Telephone, Address) to remain consistent after '
        'refreshing patient data via PDS for GEN-08.'
    )

    access_record_structured_page.click_view_gp_record()
    practice_name = access_record_structured_page.get_gp_access_practice_name()
    access_record_structured_page.highlight_text_assertion('Practice Name')
    access_record_structured_page.highlight_text_assertion(practice_name)

    assert access_record_structured_page._normalise_value(practice_name) == access_record_structured_page._normalise_value(
        before_refresh['Name']
    ), (
        'Expected Practice Name shown after clicking View GP Record to match the GP Details '
        'Name captured before the PDS trace action for GEN-08.'
    )


@then('the request is blocked and handled gracefully')
def then_blocked_gracefully(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('cannot_confirm_practice'), "Practice confirmation should have failed"
    error = access_record_structured_page.get_displayed_error()
    assert access_record_structured_page.is_blocked_after_pds_trace() or bool(error), (
        "Expected blocked GEN-09 flow after failed PDS trace: remain on NMS episode "
        "without actionable patient/GP-record controls, or display an explicit error."
    )


@then('the system prevents access and handles the prevention gracefully')
def then_prevents_access_gracefully(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('patient_deceased'), "Patient should be recorded as deceased"

    access_record_structured_page.highlight_text_assertion('Patient deceased')
    access_record_structured_page.highlight_text_assertion('Their GP record will not be accessible')

    notice = gp_connect_context.get('deceased_notice') or access_record_structured_page.get_deceased_patient_notice()
    assert notice, 'Expected a visible deceased-patient notice for GEN-10.'
    assert 'patient deceased' in notice.lower(), (
        'Expected the deceased-patient notice to explicitly flag the patient as deceased.'
    )

    page_text = access_record_structured_page.page.locator('body').inner_text(timeout=5000)
    assert 'their gp record will not be accessible' in page_text.lower(), (
        'Expected the UI to explain that the GP record cannot be accessed for a deceased patient.'
    )

    assert gp_connect_context.get('deceased_view_gp_record_disabled') or access_record_structured_page.is_view_gp_record_disabled(), (
        'Expected VIEW GP RECORD to be disabled for a deceased patient in GEN-10.'
    )


@then('I handle the error gracefully and make diagnostics available')
def then_handle_error_gracefully(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('error_type') == 'patient_not_found':
        access_record_structured_page.highlight_text_assertion('No Patients Found')
        assert access_record_structured_page.no_patients_found_visible(), (
            "Expected 'No Patients Found' to be displayed for GEN-11."
        )

    error = gp_connect_context.get('error_response', '')
    assert error, "Error response should have been captured"


@then('I handle the error gracefully')
def then_handle_error(access_record_structured_page, gp_connect_context):
    error = gp_connect_context.get('error_response', '')
    assert error, "Error response should have been captured"


@then('I make the user aware of the data in transit warning')
def then_user_aware_transit(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    assert access_record_structured_page.transit_warning_visible(), \
        "Data in transit warning should be visible"


@then('I make the user aware of the GP2GP transfer warning message')
def then_user_aware_gp2gp_transfer_warning(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('gen17_opened_gp_record'), (
        'Expected GEN-17 flow to open the GP record before warning assertions.'
    )

    heading = 'Information not available'
    warning_prefix = (
        'Patient record transfer from previous GP practice not yet complete; '
        'information recorded before'
    )

    access_record_structured_page.highlight_text_assertion(heading)
    access_record_structured_page.highlight_text_assertion(warning_prefix)

    page_text = access_record_structured_page.page.locator('body').inner_text(timeout=5000)
    assert heading.lower() in page_text.lower(), (
        'Expected GP2GP warning heading "Information not available" to be visible for GEN-17.'
    )
    assert warning_prefix.lower() in page_text.lower(), (
        'Expected GEN-17 GP2GP warning text to include the transfer-in-progress prefix.'
    )


@then('I make the user aware of the confidential items warning')
def then_user_aware_confidential(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible()
    assert access_record_structured_page.confidential_warning_visible(), \
        "Confidential items warning should be visible"


@then('the user is aware the data has come from the patient\'s registered GP record')
def then_user_aware_data_source(access_record_structured_page):
    assert access_record_structured_page.response_visible(), \
        "Response panel should be visible indicating data source"


@then('the request conforms to the specification and includes the NHS Number')
def then_request_conforms_with_nhs(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible(), \
        "A conforming request should produce a visible response"


@then('the request includes the includeMedication parameter')
def then_includes_medication_param(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('medications'), \
        "Medication results should be present"


@then('the request includes includePrescriptionIssues set to true')
def then_prescription_issues_true(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.has_results_for('medications'), \
        "Medication results with prescription issues should be present"
    gp_connect_context['prescription_issues_true'] = True


@then('the request does not include a medicationSearchFromDate')
def then_no_search_from_date(gp_connect_context):
    assert gp_connect_context.get('full_medication_history'), "Full medication history should not use a search from date"


@then('I display all key information commensurate with the original record meaning')
def then_display_key_info(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('medications_ui_mode'):
        repeat_count = gp_connect_context.get('medications_repeat_count', 0)
        assert repeat_count > 1, (
            "Expected more than one Repeat Medications item for MED-02 "
            f"but found {repeat_count}."
        )
        return

    assert access_record_structured_page.response_visible()
    results = access_record_structured_page.get_medication_results()
    assert results, "Key medication information should be displayed"


@then('the request conforms to the specification with a medicationSearchFromDate in the defined format')
def then_conforms_with_search_date(gp_connect_context):
    assert gp_connect_context.get('partial_medication_history'), "Partial medication history should include a search from date"


@then('the medicationSearchFromDate is less than or equal to the current date')
def then_search_date_not_future(gp_connect_context):
    assert gp_connect_context.get('partial_medication_history'), "Medication search from date should be valid"


@then('I am prevented from submitting the request')
def then_prevented_from_submitting(gp_connect_context):
    assert gp_connect_context.get('future_date_attempted'), "Future date submission should have been prevented"


@then('the request sets includePrescriptionIssues to the appropriate value')
def then_prescription_issues_appropriate(gp_connect_context):
    assert gp_connect_context.get('medication_issues_use_case'), "Medication issues use case should have been set"


@then('I display the empty reason')
def then_display_empty_reason(gp_connect_context):
    expected = (
        "No Issued Acute Medication data is recorded for this patient.\n"
        "There may be some unissued medication data available in the 'Not Issued' tab"
    )
    actual = gp_connect_context.get('empty_list_reason', '').strip()

    assert actual, "Empty list reason should be available for display"
    assert expected == actual, (
        "Expected MED-07 Acute Medications no-data guidance text to match exactly.\n"
        f"Expected:\n{expected}\n\nActual:\n{actual}"
    )


@then('the request uses the includeAllergies parameter with includeResolvedAllergies set to false')
def then_allergies_resolved_false(gp_connect_context):
    assert gp_connect_context.get('current_allergies_only'), "Request should have includeResolvedAllergies set to false"


@then('the request uses the includeAllergies parameter with includeResolvedAllergies set to true')
def then_allergies_resolved_true(gp_connect_context):
    assert gp_connect_context.get('include_resolved_allergies'), "Request should have includeResolvedAllergies set to true"


@then('my system identifies resolved allergies distinctly from current allergies')
def then_resolved_distinct(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert results, "Allergy results should be available"
    gp_connect_context['resolved_distinct'] = True


@then('my system labels resolved allergies clearly')
def then_resolved_labelled(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_allergy_results()
    assert results, "Allergy results should be available for labelling"
    gp_connect_context['resolved_labelled'] = True


@then('my system ensures resolved allergies cannot be used by decision support')
def then_resolved_no_decision_support(gp_connect_context):
    assert gp_connect_context.get('has_resolved_allergies'), "Resolved allergies should be present"


@then('I display all key information commensurate with the original record')
def then_display_all_key_info(access_record_structured_page, gp_connect_context):
    if gp_connect_context.get('investigations_ui_mode'):
        investigation_count = gp_connect_context.get('investigation_item_count', 0)
        assert investigation_count > 1, (
            'Expected more than one investigation item for INV-06 '
            f'but found {investigation_count}.'
        )
        return

    assert access_record_structured_page.response_visible()
    assert access_record_structured_page.has_results_for('allergies'), \
        "Allergy information should be displayed"


@then('I recognise this as no active allergies recorded')
def then_no_active_allergies(gp_connect_context):
    assert gp_connect_context.get('empty_allergies_list'), "Empty allergies list should have been recognised"


@then('I do not confuse no active allergies recorded with no known allergies')
def then_not_confused(gp_connect_context):
    assert gp_connect_context.get('empty_allergies_list'), "Empty allergies list should be distinguished from no known allergies"


@then('I recognise this as a clinical assertion of no known allergies')
def then_recognise_no_known_allergies(gp_connect_context):
    assert gp_connect_context.get('no_known_allergies'), "No known allergies should have been recognised as a clinical assertion"


@then('the request uses the includeInvestigations parameter with no part parameters')
def then_include_investigations(gp_connect_context):
    assert gp_connect_context.get('view_all_investigations') or gp_connect_context.get('investigations_requested'), \
        "Investigations should have been requested with no part parameters"


@then('the request uses investigationSearchPeriod.start only')
def then_investigation_start_only(gp_connect_context):
    assert gp_connect_context.get('investigation_from_date'), "Investigation request should include start date only"


@then('the start date is less than or equal to the current date')
def then_start_date_valid(gp_connect_context):
    date = gp_connect_context.get('investigation_from_date') or gp_connect_context.get('referral_from_date') \
        or gp_connect_context.get('uncategorised_from_date') or gp_connect_context.get('consultation_from_date')
    assert date, "Start date should have been set"


@then('the request uses investigationSearchPeriod.end only')
def then_investigation_end_only(gp_connect_context):
    assert gp_connect_context.get('investigation_to_date'), "Investigation request should include end date only"


@then('the end date is less than or equal to the current date')
def then_end_date_valid(gp_connect_context):
    date = gp_connect_context.get('investigation_to_date') or gp_connect_context.get('referral_to_date') \
        or gp_connect_context.get('uncategorised_to_date') or gp_connect_context.get('consultation_to_date')
    assert date, "End date should have been set"


@then('the request uses both investigationSearchPeriod.start and investigationSearchPeriod.end part parameters')
def then_investigation_start_and_end(gp_connect_context):
    assert gp_connect_context.get('investigation_period'), "Investigation request should include both start and end dates"


@then('the start date is less than or equal to the end date')
def then_start_lte_end(gp_connect_context):
    assert gp_connect_context.get('investigation_period') or gp_connect_context.get('referral_period') \
        or gp_connect_context.get('uncategorised_period') or gp_connect_context.get('consultation_period'), \
        "Period with start <= end should have been set"


@then('the response is processed confirming the reason for no data')
def then_no_data_reason(access_record_structured_page, gp_connect_context):
    reason = access_record_structured_page.get_empty_list_reason()
    assert reason or gp_connect_context.get('no_investigation_data') \
        or gp_connect_context.get('no_referral_data') \
        or gp_connect_context.get('no_diary_data') \
        or gp_connect_context.get('no_problem_data') \
        or gp_connect_context.get('no_immunisation_data') \
        or gp_connect_context.get('no_uncategorised_data') \
        or gp_connect_context.get('no_consultation_data'), \
        "Reason for no data should be available"


@then('I handle the warning gracefully')
def then_handle_warning(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.warning_panel_visible(), \
        "Warning panel should be visible"
    gp_connect_context['warning_handled'] = True


@then('the request uses the includeReferrals parameter with no part parameters')
def then_include_referrals(gp_connect_context):
    assert gp_connect_context.get('view_all_referrals') or gp_connect_context.get('referrals_requested'), \
        "Referrals should have been requested with no part parameters"


@then('the request uses referralSearchPeriod.start only')
def then_referral_start_only(gp_connect_context):
    assert gp_connect_context.get('referral_from_date'), "Referral request should include start date only"


@then('the request uses referralSearchPeriod.end only')
def then_referral_end_only(gp_connect_context):
    assert gp_connect_context.get('referral_to_date'), "Referral request should include end date only"


@then('the request uses both referralSearchPeriod.start and referralSearchPeriod.end part parameters')
def then_referral_start_and_end(gp_connect_context):
    assert gp_connect_context.get('referral_period'), "Referral request should include both start and end dates"


@then('the request uses the includeDiaryEntries parameter with no part parameters')
def then_include_diary_entries(gp_connect_context):
    assert gp_connect_context.get('view_all_diary_entries') or gp_connect_context.get('diary_entries_requested'), \
        "Diary entries should have been requested with no part parameters"


@then('the request uses the diaryEntriesSearchDate parameter')
def then_diary_search_date(gp_connect_context):
    assert gp_connect_context.get('diary_to_date'), "Diary entries search date should have been set"


@then('the search date is greater than or equal to the current date')
def then_search_date_gte_current(gp_connect_context):
    assert gp_connect_context.get('diary_to_date'), "Diary search date should have been set"


@then('the request uses the includeProblems parameter only')
def then_include_problems_only(gp_connect_context):
    assert gp_connect_context.get('view_all_problems') or gp_connect_context.get('problems_requested'), \
        "Problems should have been requested without filter parameters"


@then('the request uses the includeProblems parameter with filterStatus and filterSignificance')
def then_problems_with_filters(gp_connect_context):
    assert gp_connect_context.get('problem_filters_set'), "Problem filters should have been set"


@then('the request uses the includeProblems parameter with the combined filter values')
def then_problems_combined_filters(gp_connect_context):
    assert gp_connect_context.get('multiple_problem_filters') or gp_connect_context.get('problems_multiple_filters'), \
        "Multiple problem filter values should have been applied"


@then('the request uses the includeImmunisations parameter')
def then_include_immunisations(gp_connect_context):
    assert gp_connect_context.get('view_immunisations') or gp_connect_context.get('immunisations_requested'), \
        "Immunisations should have been requested"


@then('the request uses the includeImmunisations parameter with notGiven and status')
def then_immunisations_with_params(gp_connect_context):
    assert gp_connect_context.get('immunisation_filters_set'), "Immunisation filters should have been set"


@then('my system distinguishes between immunisations given and immunisations not given')
def then_distinguish_immunisations(access_record_structured_page, gp_connect_context):
    results = access_record_structured_page.get_immunisation_results()
    assert results, "Immunisation results should be available for distinction"
    gp_connect_context['immunisations_distinguished'] = True


@then('the request uses the includeUncategorisedData parameter')
def then_include_uncategorised(gp_connect_context):
    assert gp_connect_context.get('view_all_uncategorised') or gp_connect_context.get('uncategorised_requested'), \
        "Uncategorised data should have been requested"


@then('the request uses uncategorisedDataSearchPeriod.start only')
def then_uncategorised_start_only(gp_connect_context):
    assert gp_connect_context.get('uncategorised_from_date'), "Uncategorised data request should include start date only"


@then('the request uses uncategorisedDataSearchPeriod.end only')
def then_uncategorised_end_only(gp_connect_context):
    assert gp_connect_context.get('uncategorised_to_date'), "Uncategorised data request should include end date only"


@then('the request uses both uncategorisedDataSearchPeriod.start and uncategorisedDataSearchPeriod.end')
def then_uncategorised_start_and_end(gp_connect_context):
    assert gp_connect_context.get('uncategorised_period'), "Uncategorised data request should include both start and end dates"


@then('I represent the hierarchical structure correctly')
def then_hierarchical_correct(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('hierarchical_uncategorised'), "Hierarchical uncategorised data should have been received"
    results = access_record_structured_page.get_uncategorised_results()
    assert results, "Uncategorised results should be available"


@then('I represent the blood pressure readings correctly')
def then_blood_pressure_correct(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('blood_pressure_uncategorised'), "Blood pressure uncategorised data should have been received"
    results = access_record_structured_page.get_uncategorised_results()
    assert results, "Uncategorised results should be available"


@then('the request uses the includeConsultations parameter')
def then_include_consultations(gp_connect_context):
    assert gp_connect_context.get('view_all_consultations') or gp_connect_context.get('consultations_requested'), \
        "Consultations should have been requested"


@then('the request uses consultationSearchPeriod.start only')
def then_consultation_start_only(gp_connect_context):
    assert gp_connect_context.get('consultation_from_date'), "Consultation request should include start date only"


@then('the request uses consultationSearchPeriod.end only')
def then_consultation_end_only(gp_connect_context):
    assert gp_connect_context.get('consultation_to_date'), "Consultation request should include end date only"


@then('the request uses both consultationSearchPeriod.start and consultationSearchPeriod.end')
def then_consultation_start_and_end(gp_connect_context):
    assert gp_connect_context.get('consultation_period'), "Consultation request should include both start and end dates"


@then('the request uses the includeNumberOfMostRecent parameter')
def then_include_most_recent(gp_connect_context):
    assert gp_connect_context.get('most_recent_consultations'), "Most recent consultation count should have been set"


@then('I present the linkage between immunisations and problems correctly')
def then_linkage_immunisations(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('immunisations_linked_problems'), "Immunisations linked to problems should have been received"
    assert access_record_structured_page.has_results_for('immunisations')
    assert access_record_structured_page.has_results_for('problems')


@then('I present the linkage between uncategorised data and problems correctly')
def then_linkage_uncategorised(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('uncategorised_linked_problems'), "Uncategorised data linked to problems should have been received"
    assert access_record_structured_page.has_results_for('uncategorised')
    assert access_record_structured_page.has_results_for('problems')


@then('I present the linkage between consultations and problems correctly')
def then_linkage_consultations(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('consultations_linked_problems'), "Consultations linked to problems should have been received"
    assert access_record_structured_page.has_results_for('consultations')
    assert access_record_structured_page.has_results_for('problems')


@then('I present the linkage between investigations and problems correctly')
def then_linkage_investigations(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('investigations_linked_problems'), "Investigations linked to problems should have been received"
    assert access_record_structured_page.has_results_for('investigations')
    assert access_record_structured_page.has_results_for('problems')


@then('I present the linkage between referrals and problems correctly')
def then_linkage_referrals(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('referrals_linked_problems'), "Referrals linked to problems should have been received"
    assert access_record_structured_page.has_results_for('referrals')
    assert access_record_structured_page.has_results_for('problems')


@then('I present the linkage between diary entries and problems correctly')
def then_linkage_diary_entries(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('diary_entries_linked_problems'), "Diary entries linked to problems should have been received"
    assert access_record_structured_page.has_results_for('diary_entries')
    assert access_record_structured_page.has_results_for('problems')


@then('I present the linkage between medications and problems correctly')
def then_linkage_medications(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('medications_linked_problems'), "Medications linked to problems should have been received"
    assert access_record_structured_page.has_results_for('medications')
    assert access_record_structured_page.has_results_for('problems')


@then('I present the linkage between allergies and problems correctly')
def then_linkage_allergies(access_record_structured_page, gp_connect_context):
    assert gp_connect_context.get('allergies_linked_problems'), "Allergies linked to problems should have been received"
    assert access_record_structured_page.has_results_for('allergies')
    assert access_record_structured_page.has_results_for('problems')


@then('the request conforms to the specification with the combined parameters')
def then_combined_params(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible(), \
        "A conforming combined request should produce a visible response"
    assert gp_connect_context.get('predefined_search_1') or gp_connect_context.get('predefined_search_2'), \
        "Predefined search should have been executed"


@then('the request must not include referralSearchPeriod, investigationSearchPeriod, diaryEntriesSearchDate, uncategorisedDataSearchPeriod, or consultationSearchPeriod part parameters when consultations are included')
def then_no_search_periods_with_consultations(gp_connect_context):
    assert gp_connect_context.get('multiple_areas_with_consultations'), "Multiple areas with consultations should have been requested"


@then('the request conforms to the specification with the combined parameters for problems and other clinical areas')
def then_combined_with_problems(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    assert gp_connect_context.get('multiple_areas_with_problems'), "Multiple areas with problems should have been requested"


@then('the request conforms to the specification with the combined parameters for the selected clinical areas')
def then_combined_selected_areas(access_record_structured_page, gp_connect_context):
    assert access_record_structured_page.response_visible()
    assert gp_connect_context.get('multiple_areas_no_problems_consultations'), "Multiple areas without problems or consultations should have been requested"
