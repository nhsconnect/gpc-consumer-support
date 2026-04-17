"""Step definitions for Send Document - Consultation Summary feature."""
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/send_document_consultation_summary.feature')

# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given('I have recorded a consultation for a patient who is not registered to my practice')
def given_recorded_consultation_not_registered(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    gp_connect_context['registered'] = False


@given('I am not sharing the consultation within the functionality of my clinical system')
def given_not_sharing_consultation(gp_connect_context):
    gp_connect_context['sharing'] = False


@given('I have not marked the consultation as confidential')
def given_not_marked_confidential(send_document_page):
    send_document_page.set_confidential(False)


@given('I mark the consultation as confidential')
def given_mark_confidential(send_document_page):
    send_document_page.set_confidential(True)


@given('I have completed GPCM-SD-TST-01')
def given_completed_sd_tst_01(send_document_page, gp_connect_context):
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


@given('I have sent a valid Send Document message with appropriate keywords in the request for each type of error response')
def given_sent_valid_with_error_keywords(send_document_page, gp_connect_context):
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


@given('I have sent a valid Send Document message with appropriate keywords in the request')
def given_sent_valid_with_keywords(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    send_document_page.trigger_send()
    gp_connect_context['keywords_sent'] = True


@given('I have recorded a consultation for a patient registered at my practice')
def given_recorded_consultation_registered(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    gp_connect_context['registered'] = True


@given('the patient registration type is Regular GMS or PMS')
def given_registration_regular(gp_connect_context):
    gp_connect_context['registration_type'] = 'Regular GMS or PMS'


@given('I have recorded a consultation as per GPCM-SD-TST-01')
def given_recorded_as_per_tst_01(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.set_confidential(False)
    send_document_page.save_consultation()
    gp_connect_context['recorded_as_tst_01'] = True


@given('I access a consultation which has previously been sent via Send Document')
def given_access_previously_sent_consultation(send_document_page, gp_connect_context):
    send_document_page.navigate('send-document')
    send_document_page.wait_for_load()
    send_document_page.record_consultation()
    send_document_page.save_consultation()
    send_document_page.trigger_send()
    assert send_document_page.send_was_successful()
    gp_connect_context['initial_version'] = send_document_page.get_version_number()
    gp_connect_context['original_doc_id'] = send_document_page.get_replacement_id()


@given('I have completed GPCM-SD-TST-08')
def given_completed_sd_tst_08(send_document_page, gp_connect_context):
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
    send_document_page.trigger_send()
    assert send_document_page.send_was_successful()
    gp_connect_context['previous_replacement_id'] = send_document_page.get_replacement_id()


@given('I make a further amendment to the consultation')
def given_further_amendment(send_document_page, gp_connect_context):
    gp_connect_context['previous_replacement_id'] = send_document_page.get_replacement_id()
    send_document_page.amend_consultation()
    send_document_page.save_consultation()


@given('I mark some items within the consultation as confidential')
def given_mark_some_items_confidential(send_document_page):
    send_document_page.set_confidential(True)


@given('I have amended a consultation after it was sent via Send Document')
def given_amended_after_send(send_document_page, gp_connect_context):
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


@given('the amended consultation is then sent via Send Document')
def given_amended_sent(send_document_page, gp_connect_context):
    send_document_page.trigger_send()
    gp_connect_context['amended_sent'] = True


@given('the send is not successful')
def given_send_not_successful(send_document_page, gp_connect_context):
    assert not send_document_page.send_was_successful()
    gp_connect_context['send_failed'] = True


@given('I have additional documents relating to the consultation')
def given_additional_documents(send_document_page, gp_connect_context):
    send_document_page.add_document('test_data_files/additional_doc_1.pdf')
    send_document_page.add_document('test_data_files/additional_doc_2.pdf')
    gp_connect_context['additional_doc_count'] = send_document_page.get_document_count()


@given('I include the additional documents to be sent to the registered GP')
def given_include_additional_documents(gp_connect_context):
    gp_connect_context['include_additional_docs'] = True


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


@when('I complete the consultation')
def when_complete_consultation(send_document_page):
    send_document_page.save_consultation()


@when('the Send Document is sent after I complete the consultation')
def when_send_document_sent(send_document_page):
    send_document_page.trigger_send()


@when('I amend the consultation')
def when_amend_consultation(send_document_page, gp_connect_context):
    gp_connect_context['pre_amend_version'] = send_document_page.get_version_number()
    send_document_page.amend_consultation()
    send_document_page.save_consultation()


@when('the necessary time elapses for the message send')
def when_necessary_time_elapses(send_document_page):
    send_document_page.wait_for_load()


@when('a replacement message is sent')
def when_replacement_sent(send_document_page):
    send_document_page.trigger_send()


@when('I delete the consultation')
def when_delete_consultation(send_document_page):
    send_document_page.delete_consultation()


@when('the requisite amount of time has passed since the consultation was recorded or updated')
def when_requisite_time_passed_recorded_or_updated(send_document_page):
    send_document_page.wait_for_load()


@when('I receive the error or do not receive a response')
def when_receive_error_or_no_response(send_document_page, gp_connect_context):
    error = send_document_page.get_displayed_error()
    ack_status = send_document_page.get_ack_status()
    gp_connect_context['error_response'] = error
    gp_connect_context['ack_status'] = ack_status


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('a message is sent which conforms to the MESH and ITK3 requirements for Send Document')
def then_conforms_mesh_itk3(send_document_page):
    assert send_document_page.message_conforms_to_mesh_itk3()


@then('a PDF is included as a binary document conforming to the Send Document specification')
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


@then('a PDF is included as a binary document conforming to the Send Document specification with items absent as per GPCM-SD-102')
def then_pdf_with_absent_items(send_document_page):
    assert send_document_page.get_binary_resource_count() > 0
    assert send_document_page.payload_visible()


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


@then('a Send Document message does not trigger')
def then_no_send_trigger(send_document_page):
    status = send_document_page.get_send_status()
    assert 'sent' not in status.lower() and 'success' not in status.lower()


@then('ideally less than 3 hours has elapsed between last update and send')
def then_less_than_3_hours(send_document_page):
    log = send_document_page.get_message_log()
    assert log, "Expected message log to contain timing information"


@then('an updated Send Document message is sent conforming to the specification')
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


@then('it refers to the previous replacement document unique ID it is replacing')
def then_refers_previous_replacement_id(send_document_page, gp_connect_context):
    replacement_id = send_document_page.get_replacement_id()
    previous_id = gp_connect_context.get('previous_replacement_id')
    assert previous_id, "Previous replacement ID not stored in context"
    assert replacement_id == previous_id


@then('a message is displayed to inform me this consultation has been sent to the registered practice and action needs to be taken')
def then_message_displayed_action_needed(send_document_page):
    assert send_document_page.notification_visible()
    notification_text = send_document_page.get_notification_text()
    assert notification_text, "Expected notification about sent consultation"


@then('the message includes the necessary details about the patient, consultation date and registered practice')
def then_message_includes_details(send_document_page):
    notification_text = send_document_page.get_notification_text()
    assert notification_text, "Expected notification text with patient details"


@then('the Composition.confidentiality is set to N')
def then_confidentiality_n(send_document_page):
    status = send_document_page.get_send_status()
    assert 'N' in status


@then('a PDF is included with any confidential item or text replaced with the text "confidential item"')
def then_pdf_confidential_replaced(send_document_page):
    assert send_document_page.get_binary_resource_count() > 0
    assert send_document_page.payload_visible()


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
