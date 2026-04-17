"""Step definitions for Foundations feature."""
from pytest_bdd import scenarios, given, when, then, parsers

from pages.foundations_page import FoundationsPage

scenarios('../features/foundations.feature')

# ---------------------------------------------------------------------------
# Capability Statement - Given steps
# ---------------------------------------------------------------------------


@given('I perform the GP Connect interaction to get the FHIR capability statement')
def given_get_capability_statement(foundations_page, gp_connect_context):
    response = foundations_page.get_capability_statement()
    gp_connect_context['capability_statement'] = response


# ---------------------------------------------------------------------------
# Find Patient - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('I search for a patient using NHS number "{nhs_number}" where there is a single record associated with this NHS number in the GP system'))
def given_search_patient_single(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    foundations_page.search_patient(nhs_number)
    gp_connect_context['patient_results_count'] = foundations_page.get_patient_results_count()


@given('I search for a patient using an NHS number where there are multiple records associated with this NHS number in the GP system')
def given_search_patient_multiple(foundations_page, gp_connect_context):
    nhs_number = gp_connect_context.get('nhs_number', '9999999998')
    foundations_page.search_patient(nhs_number)
    gp_connect_context['patient_results_count'] = foundations_page.get_patient_results_count()


@given(parsers.parse('I search for a patient using NHS number "{nhs_number}" where there is no corresponding record in the GP system'))
def given_search_patient_no_record(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    foundations_page.search_patient(nhs_number)
    gp_connect_context['patient_results_count'] = foundations_page.get_patient_results_count()


@given('I am using the default server')
def given_using_default_server(foundations_page, gp_connect_context):
    gp_connect_context['server'] = 'default'
    foundations_page.navigate('foundations')


@given(parsers.parse('I search for a patient using NHS number "{nhs_number}" who is flagged as sensitive in the GP system record'))
def given_search_sensitive_gp(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['patient_flag'] = 'sensitive'
    foundations_page.search_patient(nhs_number)


@given(parsers.parse('I search for a patient using NHS number "{nhs_number}" who is marked as deceased in the GP system'))
def given_search_deceased(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['patient_flag'] = 'deceased'
    foundations_page.search_patient(nhs_number)


@given(parsers.parse('I search for a patient using NHS number "{nhs_number}" who is marked as inactive in the GP system'))
def given_search_inactive(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['patient_flag'] = 'inactive'
    foundations_page.search_patient(nhs_number)


@given(parsers.parse('I search for a patient with an invalid NHS number "{nhs_number}"'))
def given_search_invalid_nhs(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['invalid_nhs'] = True
    foundations_page.search_patient(nhs_number)


# ---------------------------------------------------------------------------
# Read Patient - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('I have resolved the logical patient identifier for NHS number "{nhs_number}"'))
def given_resolved_patient_id(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    foundations_page.search_patient(nhs_number)
    gp_connect_context['patient_logical_id'] = nhs_number


@given('I request the details for this patient from the provider system')
def given_request_patient_details(foundations_page, gp_connect_context):
    logical_id = gp_connect_context.get('patient_logical_id', '')
    foundations_page.read_patient(logical_id)
    foundations_page.wait_for_load()


@given(parsers.parse('I request the details for a patient using NHS number "{nhs_number}" whose details cannot be found on the server'))
def given_request_patient_not_found(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    foundations_page.search_patient(nhs_number)
    gp_connect_context['expected_error'] = 'not found'


# ---------------------------------------------------------------------------
# Register Patient - Given steps
# ---------------------------------------------------------------------------


@given('I want to book an appointment for a patient at an extended hours hub or federated practice')
def given_want_to_book_appointment(foundations_page, gp_connect_context):
    gp_connect_context['booking_intent'] = True
    foundations_page.navigate('foundations')
    foundations_page.wait_for_load()


@given('the patient has not previously been registered at that hub or practice')
def given_patient_not_registered(foundations_page, gp_connect_context):
    gp_connect_context['patient_registered'] = False
    foundations_page.open_register_patient()


@given('I have searched for a suitable slot at that hub or practice and selected it')
def given_searched_for_slot(foundations_page, gp_connect_context):
    foundations_page.select_slot(0)
    gp_connect_context['slot_selected'] = True


@given('the patient has previously been registered at that hub or practice')
def given_patient_previously_registered(gp_connect_context):
    gp_connect_context['patient_registered'] = True


@given('the registration details section of the request is blank')
def given_registration_details_blank(foundations_page, gp_connect_context):
    gp_connect_context['registration_blank'] = True
    foundations_page.open_register_patient()
    foundations_page.clear_registration_field('nhs_number')
    foundations_page.clear_registration_field('dob')


@given('I have included optional fields address and telecom in my request')
def given_optional_fields_included(foundations_page, gp_connect_context):
    gp_connect_context['optional_fields'] = True
    nhs = gp_connect_context.get('nhs_number', '')
    dob = gp_connect_context.get('dob', '2000-01-01')
    address = gp_connect_context.get('address', '1 Test Street, London, W1A 1AA')
    telecom = gp_connect_context.get('telecom', '07700900000')
    foundations_page.fill_registration(nhs, dob, address=address, telecom=telecom)


@given('the NHS Number in the request is blank')
def given_nhs_number_blank(foundations_page, gp_connect_context):
    gp_connect_context['nhs_number_blank'] = True
    foundations_page.open_register_patient()
    foundations_page.clear_registration_field('nhs_number')


@given('the date of birth in the request is blank')
def given_dob_blank(foundations_page, gp_connect_context):
    gp_connect_context['dob_blank'] = True
    foundations_page.open_register_patient()
    foundations_page.clear_registration_field('dob')


@given('I have provided two or more phone numbers both with the same value in the Use element')
def given_duplicate_phone_use(gp_connect_context):
    gp_connect_context['duplicate_phone_use'] = True


@given('I have provided two or more addresses both with the same value in the Use element')
def given_duplicate_address_use(gp_connect_context):
    gp_connect_context['duplicate_address_use'] = True


@given('I have provided an address where the value of the Use element is not temp')
def given_address_use_not_temp(gp_connect_context):
    gp_connect_context['address_use_not_temp'] = True


@given('I have provided a phone number where the value of the Use element is not temp')
def given_phone_use_not_temp(gp_connect_context):
    gp_connect_context['phone_use_not_temp'] = True


@given('I have provided an NHS number for a patient where the demographic details supplied do not match those on PDS')
def given_demographics_mismatch(gp_connect_context):
    gp_connect_context['demographics_mismatch'] = True


@given('I have provided an NHS number with a status that is not an active status in the GP system')
def given_nhs_number_inactive_status(gp_connect_context):
    gp_connect_context['nhs_inactive_status'] = True


# ---------------------------------------------------------------------------
# Find Practitioner - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('I have resolved a SDS User Id for "{practitioner}"'))
def given_resolved_sds_user_id(practitioner, foundations_page, gp_connect_context):
    gp_connect_context['practitioner'] = practitioner
    gp_connect_context['sds_user_id'] = practitioner
    foundations_page.search_practitioner(practitioner)


@given('I request the details for this practitioner from the provider system')
def given_request_practitioner_details(foundations_page, gp_connect_context):
    sds_id = gp_connect_context.get('sds_user_id', '')
    foundations_page.search_practitioner(sds_id)
    gp_connect_context['practitioner_results_count'] = foundations_page.get_practitioner_results_count()


@given('there are multiple practitioner records found for this SDS User Id')
def given_multiple_practitioner_records(foundations_page, gp_connect_context):
    count = foundations_page.get_practitioner_results_count()
    gp_connect_context['practitioner_results_count'] = count
    assert count > 1, f"Expected multiple practitioner records, got {count}"


@given('there is a single practitioner record found for this SDS User Id')
def given_single_practitioner_record(foundations_page, gp_connect_context):
    count = foundations_page.get_practitioner_results_count()
    gp_connect_context['practitioner_results_count'] = count
    assert count == 1, f"Expected single practitioner record, got {count}"


@given('there are no practitioner records found for this SDS User Id')
def given_no_practitioner_records(foundations_page, gp_connect_context):
    count = foundations_page.get_practitioner_results_count()
    gp_connect_context['practitioner_results_count'] = count
    assert count == 0, f"Expected no practitioner records, got {count}"


@given('I have resolved a SDS User Id that is invalid')
def given_invalid_sds_user_id(foundations_page, gp_connect_context):
    gp_connect_context['sds_user_id'] = 'INVALID_SDS_ID'
    foundations_page.search_practitioner('INVALID_SDS_ID')


# ---------------------------------------------------------------------------
# Read Practitioner - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('I have a logical identifier for "{practitioner}"'))
def given_logical_id_practitioner(practitioner, gp_connect_context):
    gp_connect_context['practitioner'] = practitioner
    gp_connect_context['practitioner_logical_id'] = practitioner


@given('I request the details for this practitioner')
def given_request_practitioner(foundations_page, gp_connect_context):
    logical_id = gp_connect_context.get('practitioner_logical_id', '')
    foundations_page.read_practitioner(logical_id)
    foundations_page.wait_for_load()


@given('I have a logical identifier for a practitioner that does not exist on the server')
def given_practitioner_not_on_server(foundations_page, gp_connect_context):
    gp_connect_context['practitioner_logical_id'] = 'NON_EXISTENT_PRACTITIONER'
    foundations_page.read_practitioner('NON_EXISTENT_PRACTITIONER')
    foundations_page.wait_for_load()


# ---------------------------------------------------------------------------
# Find Organisation - Given steps
# ---------------------------------------------------------------------------


@given('I have resolved an organisation ODS code')
def given_resolved_ods_code(foundations_page, gp_connect_context):
    ods_code = gp_connect_context.get('ods_code', 'A20047')
    gp_connect_context['ods_code'] = ods_code
    foundations_page.search_organisation(ods_code)


@given('I request the details for this organisation from the provider system')
def given_request_org_details_from_provider(foundations_page, gp_connect_context):
    ods_code = gp_connect_context.get('ods_code', '')
    foundations_page.search_organisation(ods_code)
    gp_connect_context['organisation_results_count'] = foundations_page.get_organisation_results_count()


@given('there are multiple organisation records found for this ODS code')
def given_multiple_org_records(foundations_page, gp_connect_context):
    count = foundations_page.get_organisation_results_count()
    gp_connect_context['organisation_results_count'] = count
    assert count > 1, f"Expected multiple organisation records, got {count}"


@given(parsers.parse('I have resolved an organisation ODS code "{ods_code}"'))
def given_resolved_specific_ods(ods_code, foundations_page, gp_connect_context):
    gp_connect_context['ods_code'] = ods_code
    foundations_page.search_organisation(ods_code)


@given('there is one organisation record found for this ODS code')
def given_single_org_record(foundations_page, gp_connect_context):
    count = foundations_page.get_organisation_results_count()
    gp_connect_context['organisation_results_count'] = count
    assert count == 1, f"Expected single organisation record, got {count}"


@given('there are no organisation records found for this ODS code')
def given_no_org_records(foundations_page, gp_connect_context):
    count = foundations_page.get_organisation_results_count()
    gp_connect_context['organisation_results_count'] = count
    assert count == 0, f"Expected no organisation records, got {count}"


@given('I request the details for an organisation with an invalid ODS code')
def given_request_invalid_ods(foundations_page, gp_connect_context):
    gp_connect_context['ods_code'] = 'INVALID_ODS'
    foundations_page.search_organisation('INVALID_ODS')


# ---------------------------------------------------------------------------
# Read Organisation - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('I have a logical identifier for organisation "{org}"'))
def given_logical_id_org(org, gp_connect_context):
    gp_connect_context['organisation'] = org
    gp_connect_context['organisation_logical_id'] = org


@given('I request the details for this organisation')
def given_request_org_details(foundations_page, gp_connect_context):
    logical_id = gp_connect_context.get('organisation_logical_id', '')
    foundations_page.read_organisation(logical_id)
    foundations_page.wait_for_load()


@given('I have a logical identifier for an organisation that does not exist on the system')
def given_org_not_on_system(foundations_page, gp_connect_context):
    gp_connect_context['organisation_logical_id'] = 'NON_EXISTENT_ORG'
    foundations_page.read_organisation('NON_EXISTENT_ORG')
    foundations_page.wait_for_load()


# ---------------------------------------------------------------------------
# Read Location - Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('I have an identifier for "{location}"'))
def given_have_location_id(location, gp_connect_context):
    gp_connect_context['location'] = location
    gp_connect_context['location_id'] = location


@given('I request the details for this location')
def given_request_location_details(foundations_page, gp_connect_context):
    location_id = gp_connect_context.get('location_id', '')
    foundations_page.read_location(location_id)
    foundations_page.wait_for_load()


@given('I have an identifier for a location that cannot be found on the server')
def given_location_not_found(foundations_page, gp_connect_context):
    gp_connect_context['location_id'] = 'NON_EXISTENT_LOCATION'
    foundations_page.read_location('NON_EXISTENT_LOCATION')
    foundations_page.wait_for_load()


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when('I make the GET request')
def when_make_get_request(foundations_page, gp_connect_context):
    foundations_page.wait_for_load()
    gp_connect_context['request_made'] = True


@when(parsers.parse('I make a request to search for a patient using NHS number "{nhs_number}" who is flagged as sensitive on their PDS record'))
def when_search_sensitive_pds(nhs_number, foundations_page, gp_connect_context):
    gp_connect_context['nhs_number'] = nhs_number
    gp_connect_context['patient_flag'] = 'sensitive_pds'
    foundations_page.search_patient(nhs_number)


@when('I confirm the booking')
def when_confirm_booking(foundations_page, gp_connect_context):
    foundations_page.confirm_booking()
    gp_connect_context['booking_confirmed'] = True


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('I shall handle the returned resources to accurately reflect what is held in the provider system')
def then_handle_returned_resources(foundations_page):
    assert foundations_page.patient_detail_visible(), "Patient detail panel should be visible"


@then('I shall handle the bundle of returned resources to accurately reflect what is held in the provider system')
def then_handle_bundle(foundations_page):
    count = foundations_page.get_patient_results_count()
    assert count >= 1, f"Expected at least one result in the bundle, got {count}"


@then('my system reflects a successful interaction')
def then_successful_interaction(foundations_page):
    error = foundations_page.get_displayed_error()
    assert not error, f"Expected no error but got: {error}"


@then('the consumer system must display the messages returned from the Provider which specify that the Patient is Not Found')
def then_display_patient_not_found(foundations_page):
    error = foundations_page.get_displayed_error()
    assert 'not found' in error.lower() or 'no patient' in error.lower(), \
        f"Expected 'not found' message but got: {error}"


@then('the consumer system must not perform the search for this patient')
def then_must_not_search(foundations_page, gp_connect_context):
    assert gp_connect_context.get('invalid_nhs'), "Expected invalid NHS number flag to be set"
    error = foundations_page.get_displayed_error()
    assert error, "Expected an error to be displayed for invalid search"


@then('I shall handle the empty bundle of returned resources to accurately reflect what is held in the provider system')
def then_handle_empty_bundle(foundations_page):
    count = foundations_page.get_patient_results_count()
    assert count == 0, f"Expected empty bundle (0 results), got {count}"


@then('reflect a successful interaction')
def then_reflect_success(foundations_page):
    error = foundations_page.get_displayed_error()
    assert not error, f"Expected no error but got: {error}"


@then('the error returned is captured and displayed appropriately to the caller')
def then_error_captured(foundations_page):
    error = foundations_page.get_displayed_error()
    assert error, "Expected an error message to be displayed"


@then('the request is formed as described in the specification')
def then_request_conforms_spec(foundations_page):
    error = foundations_page.get_displayed_error()
    assert not error, f"Request should conform to spec but got error: {error}"


@then('the system can receive and read the data elements from the returned data as described in the specification and display them correctly')
def then_read_data_elements(foundations_page):
    assert foundations_page.patient_detail_visible(), "Patient details should be displayed"
    assert foundations_page.get_patient_name(), "Patient name should be present"
    assert foundations_page.get_patient_dob(), "Patient DOB should be present"
    assert foundations_page.get_patient_gender(), "Patient gender should be present"
    assert foundations_page.get_patient_nhs_number(), "Patient NHS number should be present"


@then('the request is formatted as described in the specification')
def then_request_formatted(foundations_page):
    error = foundations_page.get_displayed_error()
    assert not error, f"Request should be formatted per spec but got error: {error}"


@then('a temporary patient registration is created in the provider system at the chosen practice')
def then_temp_registration_created(foundations_page):
    success = foundations_page.get_success_message()
    assert success, "Expected a success message confirming temporary registration"


@then('the appointment is booked correctly')
def then_appointment_booked(foundations_page, gp_connect_context):
    assert gp_connect_context.get('booking_confirmed'), "Booking should have been confirmed"
    error = foundations_page.get_displayed_error()
    assert not error, f"Expected no error after booking but got: {error}"


@then('I can retrieve and read the details of the appointment and of the temporary registration when they are returned to me')
def then_retrieve_appointment_details(foundations_page):
    assert foundations_page.patient_detail_visible(), "Appointment and registration details should be visible"


@then('a temporary patient registration is not created in the provider system at the chosen practice')
def then_no_temp_registration(foundations_page):
    error = foundations_page.get_displayed_error()
    assert error, "Expected an error indicating registration was not created"


@then('I can retrieve and read the details of the appointment when they are returned to me')
def then_retrieve_appointment(foundations_page):
    assert foundations_page.patient_detail_visible(), "Appointment details should be visible"


@then('I shall display an appropriate error message')
def then_display_error(foundations_page):
    error = foundations_page.get_displayed_error()
    assert error, "Expected an error message to be displayed"


@then('the temporary patient registration is created correctly including the optional fields')
def then_temp_registration_with_optional(foundations_page):
    success = foundations_page.get_success_message()
    assert success, "Expected a success message confirming registration with optional fields"


@then('I shall handle the bundle of returned resources to accurately reflect what is held in the provider system with no matching records')
def then_handle_empty_bundle_no_match(foundations_page):
    count = foundations_page.get_patient_results_count()
    assert count == 0, f"Expected no matching records (0 results), got {count}"
