"""Step definitions for Access Record HTML feature."""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/access_record_html.feature')

# ---------------------------------------------------------------------------
# Patient Tracing & Demographics
# ---------------------------------------------------------------------------


@given('I have traced a Patient as per the recommended means in the GPC API spec in the last 24 hours')
def given_traced_patient(gp_connect_context):
    gp_connect_context['traced'] = True


@given('I have NOT traced a Patient as per the recommended means in the GPC API spec in the last 24 hours')
def given_not_traced_patient(gp_connect_context):
    gp_connect_context['traced'] = False


@given("I have a Patient's NHS number")
def given_have_nhs_number(access_record_html_page, gp_connect_context):
    access_record_html_page.navigate('access-record-html')
    access_record_html_page.wait_for_load()
    access_record_html_page.search_patient('9658218873')
    gp_connect_context['nhs_number'] = '9658218873'


@given("I want to retrieve a Patient's record from its registered GP Practice")
def given_want_retrieve_record_from_gp(gp_connect_context):
    gp_connect_context['intent'] = 'retrieve_record'


@given("I want to view a patient's record and its demographics")
def given_want_view_record_demographics(access_record_html_page, gp_connect_context):
    access_record_html_page.navigate('access-record-html')
    access_record_html_page.wait_for_load()
    gp_connect_context['view_demographics'] = True


@given("I want to view a Patient's record")
def given_want_view_patient_record(access_record_html_page):
    access_record_html_page.navigate('access-record-html')
    access_record_html_page.wait_for_load()


@given("I try to retrieve a patient's record from its GP Practice")
def given_try_retrieve_from_gp_practice(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658218873')
    access_record_html_page.retrieve_record()
    gp_connect_context['record_retrieved'] = True


@given("I receive an API response with the patient's details")
def given_receive_api_response_patient_details(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@given("I receive an API response with patient's details")
def given_receive_api_response_patients_details(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@given("I compare the returned structured patient demographic data against the demographic data held in the consumer system")
def given_compare_demographics(access_record_html_page, gp_connect_context):
    gp_connect_context['demographics_compared'] = True


# ---------------------------------------------------------------------------
# Data Sharing
# ---------------------------------------------------------------------------


@given('that data sharing agreements are in place between my organisation and the GP Practice from which I want to retrieve a patient\'s record')
def given_data_sharing_in_place(access_record_html_page, gp_connect_context):
    access_record_html_page.navigate('access-record-html')
    access_record_html_page.wait_for_load()
    gp_connect_context['dsa_in_place'] = True


@given('that data sharing agreements are NOT in place between my organisation and the GP Practice from which I want to retrieve a patient\'s record')
def given_data_sharing_not_in_place(access_record_html_page, gp_connect_context):
    access_record_html_page.navigate('access-record-html')
    access_record_html_page.wait_for_load()
    gp_connect_context['dsa_in_place'] = False


@given("I try to retrieve patient's information from their registered GP Practice")
def given_try_retrieve_from_registered_gp(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658218873')
    access_record_html_page.retrieve_record()
    gp_connect_context['record_retrieved'] = True


@given('the data sharing agreements are checked by Spine Security Proxy')
def given_data_sharing_checked_by_ssp(access_record_html_page):
    status = access_record_html_page.get_dsa_status()
    assert status, "DSA status not returned from SSP"


# ---------------------------------------------------------------------------
# GP2GP Transfer
# ---------------------------------------------------------------------------


@given('that a patient has registered with a new GP Practice Y')
def given_patient_registered_new_gp(access_record_html_page, gp_connect_context):
    access_record_html_page.navigate('access-record-html')
    access_record_html_page.wait_for_load()
    gp_connect_context['gp2gp_transfer'] = True


@given('their patient record is being transferred from the previous GP Practice X to Y GP Practice')
def given_record_transferring(gp_connect_context):
    gp_connect_context['record_in_transit'] = True


@given('I access the Patient\'s record from Y GP Practice')
def given_access_from_new_gp(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658219691')
    access_record_html_page.retrieve_record()
    gp_connect_context['accessed_from_new_gp'] = True


@given('only details from the current GP record of the Y GP Practice are returned as old GP record of X is still in transit and not committed')
def given_only_current_record_returned(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


# ---------------------------------------------------------------------------
# Date Filters & Banners
# ---------------------------------------------------------------------------


@given('I have applied a date filter with a start date and an end date for a section in the API request')
def given_date_filter_start_end(access_record_html_page, gp_connect_context):
    access_record_html_page.apply_date_filter(date_from='2020-01-01', date_to='2023-12-31')
    gp_connect_context['date_filter'] = 'start_and_end'


@given('I have applied a date filter with a start date and no end date for a section in the API request')
def given_date_filter_start_only(access_record_html_page, gp_connect_context):
    access_record_html_page.apply_date_filter(date_from='2020-01-01')
    gp_connect_context['date_filter'] = 'start_only'


@given('I have not applied a date filter for a section in the API request')
def given_no_date_filter(gp_connect_context):
    gp_connect_context['date_filter'] = 'none'


@given('the API response has date banner for the given section')
def given_response_has_date_banner(access_record_html_page):
    assert access_record_html_page.date_banner_visible()


@given('the API response has section banner and subsection banner')
def given_response_has_section_subsection_banner(access_record_html_page):
    assert access_record_html_page.section_banner_visible()
    assert access_record_html_page.subsection_banner_visible()


@given('the API response has a section from which some data has been excluded')
def given_response_has_excluded_data(gp_connect_context):
    gp_connect_context['has_exclusions'] = True


@given('it has an exclusions banner')
def given_has_exclusions_banner(access_record_html_page):
    assert access_record_html_page.exclusion_banner_visible()


# ---------------------------------------------------------------------------
# API Request
# ---------------------------------------------------------------------------


@given('I have provided the required items in the header of the API Request')
def given_required_header_items(gp_connect_context):
    gp_connect_context['header_items_provided'] = True


@given('I have provided the required items of the API Request')
def given_required_api_items(gp_connect_context):
    gp_connect_context['api_items_provided'] = True


@given('I create a valid GPConnect API Request')
def given_valid_gpconnect_request(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658218873')
    gp_connect_context['valid_request'] = True


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I try to retrieve a patient's record from its registered GP practice")
def when_try_retrieve_record(access_record_html_page, gp_connect_context):
    if not gp_connect_context.get('record_retrieved'):
        access_record_html_page.navigate('access-record-html')
        access_record_html_page.wait_for_load()
        access_record_html_page.search_patient('9658218873')
        if gp_connect_context.get('traced'):
            access_record_html_page.retrieve_record()
        else:
            access_record_html_page.retrieve_record()


@when("I retrieve a patient's record from its registered GP practice")
def when_retrieve_record(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658218873')
    access_record_html_page.retrieve_record()
    gp_connect_context['record_retrieved'] = True


@when("I try to find the Patient's registered GP Practice using the patient's NHS number")
def when_find_registered_gp(access_record_html_page):
    access_record_html_page.retrieve_record()


@when("the differences exist in any of the following fields: Family Name, Given Name, Gender, Birth Date, GP Practice Code")
def when_differences_in_fields(access_record_html_page):
    assert access_record_html_page.demographics_alert_visible()


@when("I try to retrieve patient's information from their registered GP Practice")
def when_try_retrieve_info(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658218873')
    access_record_html_page.retrieve_record()
    gp_connect_context['record_retrieved'] = True


@when("I receive an exception in the API response that the data sharing agreement does not exist in SSP")
def when_receive_exception_no_dsa(access_record_html_page):
    error = access_record_html_page.get_displayed_error()
    assert error, "Expected a DSA error but none was displayed"


@when("I see a banner message in the response specifying patient record transfer from previous GP Practice not yet complete")
def when_see_transfer_banner(access_record_html_page):
    assert access_record_html_page.transfer_banner_visible()


@when("I display the received patient's details from the API response on my system")
def when_display_patient_details(access_record_html_page):
    access_record_html_page.wait_for_load()


@when("I use the GPC API to request a Patient's record from their registered GP Practice for any section")
def when_request_record_any_section(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658218873')
    access_record_html_page.retrieve_record()
    gp_connect_context['record_retrieved'] = True


@when('I create HTML views')
def when_create_html_views(access_record_html_page):
    access_record_html_page.wait_for_load()


@when("I try to retrieve a patient's record from their registered GP Practice")
def when_try_retrieve_record_from_registered(access_record_html_page, gp_connect_context):
    access_record_html_page.search_patient('9658218873')
    access_record_html_page.retrieve_record()
    gp_connect_context['record_retrieved'] = True


@when("I try to retrieve a patient's record from its GP Practice")
def when_try_retrieve_record_from_gp(access_record_html_page, gp_connect_context):
    if not gp_connect_context.get('record_retrieved'):
        access_record_html_page.retrieve_record()
        gp_connect_context['record_retrieved'] = True


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("I am able to retrieve the patient's record")
def then_able_to_retrieve(access_record_html_page, gp_connect_context):
    assert gp_connect_context.get('traced'), "Patient must be traced to retrieve record"
    assert '200' in access_record_html_page.get_response_status()


@then("I am NOT able to retrieve the patient's record")
def then_not_able_to_retrieve(access_record_html_page, gp_connect_context):
    assert not gp_connect_context.get('traced'), "Patient should not have been traced"
    error = access_record_html_page.get_displayed_error()
    assert error, "Expected an error when patient is not traced"


@then("I get the ODS code of the Patient's registered GP Practice in response")
def then_get_ods_code(access_record_html_page):
    ods_code = access_record_html_page.get_ods_code()
    assert ods_code, "ODS code was not returned in the response"


@then("I can use the ODS code of the registered GP Practice to request patient's information from the GP Practice")
def then_can_use_ods_code(access_record_html_page):
    ods_code = access_record_html_page.get_ods_code()
    assert len(ods_code) > 0


@then("I display the patient's details on my system as per the CUI guidance")
def then_display_per_cui(access_record_html_page):
    assert access_record_html_page.patient_banner_visible()
    assert access_record_html_page.get_banner_name()
    assert access_record_html_page.get_banner_nhs()
    assert access_record_html_page.get_banner_dob()
    assert access_record_html_page.get_banner_gender()


@then('the consumer system MUST show an alert or warning')
def then_show_alert_warning(access_record_html_page):
    assert access_record_html_page.demographics_alert_visible()


@then('provide details of which fields and values are different between the two systems')
def then_provide_diff_details(access_record_html_page):
    differences = access_record_html_page.get_demographics_differences()
    assert differences, "Expected demographic difference details to be displayed"


@then('the data sharing agreements are checked by Spine Security Proxy')
def then_data_sharing_checked(access_record_html_page):
    status = access_record_html_page.get_dsa_status()
    assert status, "DSA status not available"


@then('I can retrieve the Patient\'s record only if the data sharing agreement between my organisation and the given GP Practice is set up on Spine Security Proxy')
def then_can_retrieve_if_dsa(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()
    status = access_record_html_page.get_dsa_status()
    assert status


@then('I am able to handle this error gracefully on my system')
def then_handle_error_gracefully(access_record_html_page):
    error = access_record_html_page.get_displayed_error()
    assert error, "Expected an error message to be displayed"


@then('I display the banner as per the CUI guidance')
def then_display_banner_cui(access_record_html_page):
    assert access_record_html_page.transfer_banner_visible()
    text = access_record_html_page.get_transfer_banner_text()
    assert text, "Transfer banner text should not be empty"


@then("my system MUST present a patient banner above the HTML content returned from the GP Connect APIs in line with the CUI guidance")
def then_present_patient_banner(access_record_html_page):
    assert access_record_html_page.patient_banner_visible()
    assert access_record_html_page.get_banner_name()
    assert access_record_html_page.get_banner_nhs()
    assert access_record_html_page.get_banner_dob()
    assert access_record_html_page.get_banner_gender()
    assert access_record_html_page.get_banner_gp_practice()


@then('it applies to all the HTML views')
def then_applies_all_html_views(access_record_html_page):
    assert access_record_html_page.patient_banner_visible()
    assert access_record_html_page.get_section_count() > 0


@then('I display the section banner above the relevant section')
def then_display_section_banner(access_record_html_page):
    assert access_record_html_page.section_banner_visible()
    text = access_record_html_page.get_section_banner_text()
    assert text, "Section banner text should not be empty"


@then('I display the subsection banner above the relevant subsections with the expected styling as per the API spec')
def then_display_subsection_banner(access_record_html_page):
    assert access_record_html_page.subsection_banner_visible()
    text = access_record_html_page.get_subsection_banner_text()
    assert text, "Subsection banner text should not be empty"


@then('I can apply date filters to the following sections only: Administrative items, Clinical items, Encounters, Medications All Medication, Medications All Medication Issues, Observations, Problems and issues Major inactive, Problems and issues Other inactive, Referrals')
def then_apply_date_filters(access_record_html_page):
    filterable_sections = [
        'Administrative items', 'Clinical items', 'Encounters',
        'Medications All Medication', 'Medications All Medication Issues',
        'Observations', 'Problems and issues Major inactive',
        'Problems and issues Other inactive', 'Referrals',
    ]
    for section in filterable_sections:
        access_record_html_page.select_section(section)
        access_record_html_page.apply_date_filter(date_from='2020-01-01', date_to='2023-12-31')
        assert access_record_html_page.date_banner_visible(), f"Date banner not visible for {section}"


@then('I receive and display details for the relevant section for the applied date filter')
def then_display_filtered_details(access_record_html_page):
    content = access_record_html_page.get_xhtml_content()
    assert content, "Expected filtered content to be displayed"


@then('I display the date banner above the relevant section with start and end dates with the expected styling as per the API spec')
def then_display_date_banner_start_end(access_record_html_page):
    assert access_record_html_page.date_banner_visible()
    text = access_record_html_page.get_date_banner_text()
    assert text, "Date banner text should not be empty"


@then('I display the date banner above the relevant section with start date only displaying in the text "All data items from [Start Date]" with the expected styling as per the API spec')
def then_display_date_banner_start_only(access_record_html_page):
    assert access_record_html_page.date_banner_visible()
    text = access_record_html_page.get_date_banner_text()
    assert 'All data items from' in text


@then('I display the date banner above the relevant section that does not display any date range and its text reads as "Date filter not applied" with the expected styling as per the API spec')
def then_display_date_banner_no_filter(access_record_html_page):
    assert access_record_html_page.date_banner_visible()
    text = access_record_html_page.get_date_banner_text()
    assert 'Date filter not applied' in text


@then('I display another date banner with no dates whose text reads as "All relevant items"')
def then_display_all_relevant_items_banner(access_record_html_page):
    assert access_record_html_page.date_banner_visible()
    text = access_record_html_page.get_date_banner_text()
    assert 'All relevant items' in text


@then('I display the exclusion banner above the given section with the expected styling as per the API spec')
def then_display_exclusion_banner(access_record_html_page):
    assert access_record_html_page.exclusion_banner_visible()
    text = access_record_html_page.get_exclusion_banner_text()
    assert text, "Exclusion banner text should not be empty"


@then('in the header of the API request I must provide the following details: Ssp-TraceID, Ssp-From, Ssp-To, Ssp-InteractionID')
def then_provide_header_details(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('the API request payload MUST have a set of Parameters conforming to the gpconnect-carerecord-operation-1 profiled OperationDefinition')
def then_payload_conforms(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('include Parameter patientNHSNumber')
def then_include_nhs_number_param(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('include Parameter recordSection')
def then_include_record_section_param(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('the request payload MAY have the optional parameter timePeriod')
def then_optional_time_period(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('the API request payload MUST meet the following business rules: NHS number is in valid format, NHS number is verified, patient record is retrieved from nominated primary care provider, record section is from approved valueset, and time period rules are met')
def then_business_rules_met(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('the API response includes a 200 OK HTTP status code')
def then_response_200(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('the care record section as valid XHTML in line with the FHIR Narrative guidance')
def then_valid_xhtml(access_record_html_page):
    content = access_record_html_page.get_xhtml_content()
    assert content, "Expected XHTML content in the response"


@then('relevant GP Connect StructureDefinition profile details in the meta fields')
def then_structure_definition_meta(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('Patient, Practitioner and Organization details in a searchset Bundle')
def then_searchset_bundle(access_record_html_page):
    assert '200' in access_record_html_page.get_response_status()


@then('I am able to display the details successfully in relevant HTML views')
def then_display_in_html_views(access_record_html_page):
    content = access_record_html_page.get_xhtml_content()
    assert content, "Expected HTML content to be displayable"
    assert access_record_html_page.get_section_count() > 0
