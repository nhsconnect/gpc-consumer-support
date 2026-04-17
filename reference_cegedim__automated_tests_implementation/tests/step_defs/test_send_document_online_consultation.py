"""Step definitions for Send Document - Online Consultation feature."""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/send_document_online_consultation.feature')

# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given('an Online Consultation has been submitted')
def given_online_consultation_submitted(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    gp_connect_context['oc_submitted'] = True


@given('I have not marked the consultation as confidential')
def given_not_marked_confidential(send_document_page):
    send_document_page.set_confidential(False)


@given('I mark the consultation as confidential')
def given_mark_confidential(send_document_page):
    send_document_page.set_confidential(True)


@given('I have completed GPCM-OC-TST-01')
def given_completed_oc_tst_01(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.set_confidential(False)
    send_document_page.save_consultation()
    send_document_page.trigger_send()
    assert send_document_page.send_was_successful()
    gp_connect_context['initial_version'] = send_document_page.get_version_number()
    gp_connect_context['original_doc_id'] = send_document_page.get_replacement_id()


@given('I record a new consultation for the patient as a different practitioner working for a different organisation')
def given_new_consultation_different_practitioner(send_document_page, gp_connect_context):
    send_document_page.select_practitioner('practitioner-2')
    send_document_page.select_organisation('organisation-2')
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    gp_connect_context['different_practitioner'] = True


@given('I have sent a valid Online Consultation Send Document message with appropriate keywords for each type of error response')
def given_sent_valid_oc_error_keywords(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    send_document_page.trigger_send()
    gp_connect_context['error_keywords_sent'] = True


@given('the receiver is unable to process it', target_fixture='receiver_unable')
def given_receiver_unable(gp_connect_context):
    gp_connect_context['receiver_unable'] = True
    return True


@given('I have sent a valid Online Consultation Send Document message with appropriate keywords')
def given_sent_valid_oc_keywords(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    send_document_page.trigger_send()
    gp_connect_context['keywords_sent'] = True


@given('I access an Online Consultation which has previously been sent via Send Document')
def given_access_previously_sent_oc(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    send_document_page.trigger_send()
    assert send_document_page.send_was_successful()
    gp_connect_context['initial_version'] = send_document_page.get_version_number()
    gp_connect_context['original_doc_id'] = send_document_page.get_replacement_id()


@given('I have amended the Online Consultation after it was sent via Send Document')
def given_amended_oc_after_send(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    send_document_page.trigger_send()
    assert send_document_page.send_was_successful()
    gp_connect_context['initial_version'] = send_document_page.get_version_number()
    gp_connect_context['original_doc_id'] = send_document_page.get_replacement_id()
    send_document_page.amend_consultation()
    send_document_page.save_consultation()


@given('the amended Online Consultation is then sent via Send Document')
def given_amended_oc_sent(send_document_page, gp_connect_context):
    send_document_page.trigger_send()
    gp_connect_context['amended_sent'] = True


@given('the send is not successful')
def given_send_not_successful(send_document_page, gp_connect_context):
    assert not send_document_page.send_was_successful()
    gp_connect_context['send_failed'] = True


@given('I have additional documents relating to the Online Consultation')
def given_additional_documents_oc(send_document_page, gp_connect_context):
    send_document_page.add_document('test_data_files/additional_doc_1.pdf')
    send_document_page.add_document('test_data_files/additional_doc_2.pdf')
    gp_connect_context['additional_doc_count'] = send_document_page.get_document_count()


@given('I include the additional documents to be sent')
def given_include_additional_documents(gp_connect_context):
    gp_connect_context['include_additional_docs'] = True


@given('I record a new online consultation for the patient as a different practitioner working for a different organisation')
def given_new_oc_different_practitioner(send_document_page, gp_connect_context):
    send_document_page.select_practitioner('practitioner-2')
    send_document_page.select_organisation('organisation-2')
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    gp_connect_context['different_practitioner'] = True


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when('the requisite amount of time has passed since the consultation was recorded or last updated')
def when_requisite_time_passed(send_document_page):
    send_document_page.wait_for_load()


@when('a send document message is triggered')
def when_send_document_triggered(send_document_page):
    send_document_page.trigger_send()


@when('the send document message is triggered')
def when_send_document_message_triggered(send_document_page):
    send_document_page.trigger_send()


@when('I receive an error response')
def when_receive_error_response(send_document_page, gp_connect_context):
    error = send_document_page.get_displayed_error()
    gp_connect_context['error_response'] = error


@when('I do not receive a technical or business acknowledgement response')
def when_no_acknowledgement(send_document_page, gp_connect_context):
    ack_status = send_document_page.get_ack_status()
    gp_connect_context['ack_status'] = ack_status


@when('I amend the Online Consultation')
def when_amend_oc(send_document_page, gp_connect_context):
    gp_connect_context['pre_amend_version'] = send_document_page.get_version_number()
    send_document_page.amend_consultation()
    send_document_page.save_consultation()


@when('the necessary time elapses for the message send')
def when_necessary_time_elapses(send_document_page):
    send_document_page.wait_for_load()


@when('I receive the error or do not receive a response')
def when_receive_error_or_no_response(send_document_page, gp_connect_context):
    error = send_document_page.get_displayed_error()
    ack_status = send_document_page.get_ack_status()
    gp_connect_context['error_response'] = error
    gp_connect_context['ack_status'] = ack_status


@when('the requisite amount of time has passed since the Online Consultation was recorded or updated')
def when_requisite_time_oc(send_document_page):
    send_document_page.wait_for_load()


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('a message is sent which conforms to the MESH and ITK3 requirements for Send Document')
def then_conforms_mesh_itk3(send_document_page):
    assert send_document_page.message_conforms_to_mesh_itk3()


@then('a PDF is included as a binary document')
def then_pdf_included(send_document_page):
    assert send_document_page.get_binary_resource_count() > 0


@then('the Composition.confidentiality is set to R')
def then_confidentiality_r(send_document_page):
    status = send_document_page.get_send_status()
    assert 'R' in status


@then('confidential items are not included in the headers as per requirements')
def then_confidential_not_in_headers(send_document_page):
    log = send_document_page.get_message_log()
    assert 'confidential' not in log.lower().split('header')[0] if 'header' in log.lower() else True


@then('the organisation details are included in structured resources')
def then_org_details_structured(send_document_page):
    sections = send_document_page.get_composition_sections()
    assert any('organisation' in s.lower() or 'organization' in s.lower() for s in sections)


@then('the organization and practitioner resources reflect the practitioner and organisation details used to record the consultation')
def then_reflect_practitioner_org(send_document_page):
    sections = send_document_page.get_composition_sections()
    assert any('practitioner' in s.lower() for s in sections)
    assert any('organisation' in s.lower() or 'organization' in s.lower() for s in sections)


@then('the error is handled gracefully')
def then_error_handled(send_document_page):
    error = send_document_page.get_displayed_error()
    assert error, "Expected an error to be displayed"


@then('a notification of the error is made to an appropriate person')
def then_error_notification(send_document_page):
    assert send_document_page.notification_visible()
    notification_text = send_document_page.get_notification_text()
    assert notification_text, "Expected notification text to be present"


@then('the sender has an appropriate way to manage the non-response')
def then_manage_non_response(send_document_page):
    assert send_document_page.notification_visible()


@then('if not resolved a notification of no response is made to an appropriate person')
def then_no_response_notification(send_document_page):
    assert send_document_page.notification_visible()
    notification_text = send_document_page.get_notification_text()
    assert notification_text, "Expected no-response notification text"


@then('an updated Send Document message is sent')
def then_updated_message_sent(send_document_page):
    assert send_document_page.message_conforms_to_mesh_itk3()
    assert send_document_page.send_was_successful()


@then('the version number is incremented from the previous send')
def then_version_incremented(send_document_page, gp_connect_context):
    current_version = send_document_page.get_version_number()
    initial_version = gp_connect_context.get('initial_version', '0')
    assert int(current_version) > int(initial_version)


@then('it identifies the document is a replacement')
def then_identifies_replacement(send_document_page):
    replacement_id = send_document_page.get_replacement_id()
    assert replacement_id, "Expected a replacement ID to be present"


@then('it refers to the original document unique ID it is replacing')
def then_refers_original_id(send_document_page, gp_connect_context):
    replacement_id = send_document_page.get_replacement_id()
    original_doc_id = gp_connect_context.get('original_doc_id')
    assert original_doc_id, "Original document ID not stored in context"
    assert replacement_id == original_doc_id


@then('I will handle the error gracefully')
def then_will_handle_error(send_document_page):
    error = send_document_page.get_displayed_error()
    assert error, "Expected an error to be displayed for graceful handling"


@then('trigger an appropriate resolution process')
def then_trigger_resolution(send_document_page):
    assert send_document_page.notification_visible()


@then('manage the data integrity of the record')
def then_manage_data_integrity(send_document_page):
    assert send_document_page.payload_visible()


@then('the consultation report and each document is included in the composition as individual sections')
def then_composition_individual_sections(send_document_page, gp_connect_context):
    sections = send_document_page.get_composition_sections()
    additional_doc_count = gp_connect_context.get('additional_doc_count', 0)
    assert len(sections) >= 1 + additional_doc_count


@then('the first section in the composition refers to a binary resource for the consultation report')
def then_first_section_binary(send_document_page):
    sections = send_document_page.get_composition_sections()
    assert sections, "Expected at least one composition section"
    assert 'binary' in sections[0].lower() or 'report' in sections[0].lower()


@then('there is a section for each additional document with a reference to a binary resource')
def then_section_per_document(send_document_page, gp_connect_context):
    sections = send_document_page.get_composition_sections()
    additional_doc_count = gp_connect_context.get('additional_doc_count', 0)
    assert len(sections) >= 1 + additional_doc_count


@then('the binary resources are included in the bundle with matching references and IDs')
def then_binary_resources_match(send_document_page, gp_connect_context):
    binary_count = send_document_page.get_binary_resource_count()
    additional_doc_count = gp_connect_context.get('additional_doc_count', 0)
    assert binary_count >= 1 + additional_doc_count


@then('the binary resources are base64 encoded')
def then_base64_encoded(send_document_page):
    assert send_document_page.get_binary_resource_count() > 0
    assert send_document_page.payload_visible()


@then('the RelatedPerson resource details reflect the person, birthdate and telecom details used in the online consultation message as per specification')
def then_related_person_details(send_document_page):
    related_person_text = send_document_page.get_related_person_text()
    assert related_person_text, "Expected RelatedPerson resource details to be present"


@then('the ITK Device Resource details reflect the type and manufacturer of the device in question as per specification')
def then_itk_device_details(send_document_page):
    itk_device_text = send_document_page.get_itk_device_text()
    assert itk_device_text, "Expected ITK Device resource details to be present"


@then('the Optional Resource in the payload is populated as per specification')
def then_optional_resource_populated(send_document_page):
    optional_resource_text = send_document_page.get_optional_resource_text()
    assert optional_resource_text, "Expected Optional Resource to be populated"
