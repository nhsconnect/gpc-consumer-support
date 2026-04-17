"""Page object for Send Document interactions.

Covers both Consultation Summary and Online Consultation message flows,
including MESH/ITK3 message construction, payload verification,
error handling, and document amendment workflows.
"""
from pages.base_page import BasePage


class SendDocumentPage(BasePage):
    """Page object for GP Connect Send Document capability."""

    # ------------------------------------------------------------------
    # Selectors
    # ------------------------------------------------------------------
    PATIENT_NHS_INPUT = "#send-doc-nhs-number"
    SEARCH_PATIENT_BTN = "#send-doc-search-btn"

    # Consultation recording
    CONSULTATION_PANEL = ".consultation-panel"
    RECORD_CONSULTATION_BTN = "#record-consultation-btn"
    CONFIDENTIAL_CHECKBOX = "#confidential-checkbox"
    PRACTITIONER_SELECT = "#practitioner-select"
    ORGANISATION_SELECT = "#organisation-select"
    SAVE_CONSULTATION_BTN = "#save-consultation-btn"

    # Send controls
    TRIGGER_SEND_BTN = "#trigger-send-btn"
    SEND_STATUS = ".send-status"
    MESSAGE_LOG = ".message-log"

    # Payload inspection
    PAYLOAD_PANEL = ".payload-panel"
    COMPOSITION_SECTION = ".composition-section"
    BINARY_RESOURCES = ".binary-resource"
    RELATED_PERSON_RESOURCE = ".related-person-resource"
    ITK_DEVICE_RESOURCE = ".itk-device-resource"
    OPTIONAL_RESOURCE = ".optional-resource"

    # Amendment
    AMEND_BTN = "#amend-consultation-btn"
    DELETE_BTN = "#delete-consultation-btn"
    VERSION_DISPLAY = ".version-number"
    REPLACEMENT_ID = ".replacement-id"

    # Documents
    ADD_DOCUMENT_BTN = "#add-document-btn"
    DOCUMENT_FILE_INPUT = "#document-file-input"
    DOCUMENT_LIST = ".document-list"

    # Errors & acknowledgements
    ERROR_DISPLAY = ".error-display"
    ACK_STATUS = ".ack-status"
    NOTIFICATION_PANEL = ".notification-panel"

    # ------------------------------------------------------------------
    # Patient search
    # ------------------------------------------------------------------

    def search_patient(self, nhs_number: str) -> None:
        self.fill(self.PATIENT_NHS_INPUT, nhs_number)
        self.click(self.SEARCH_PATIENT_BTN)
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Consultation recording
    # ------------------------------------------------------------------

    def record_consultation(self) -> None:
        self.click(self.RECORD_CONSULTATION_BTN)
        self.wait_for_load()

    def set_confidential(self, confidential: bool) -> None:
        is_checked = self.page.is_checked(self.CONFIDENTIAL_CHECKBOX)
        if confidential != is_checked:
            self.click(self.CONFIDENTIAL_CHECKBOX)

    def select_practitioner(self, practitioner_id: str) -> None:
        self.select_option(self.PRACTITIONER_SELECT, practitioner_id)

    def select_organisation(self, org_id: str) -> None:
        self.select_option(self.ORGANISATION_SELECT, org_id)

    def save_consultation(self) -> None:
        self.click(self.SAVE_CONSULTATION_BTN)
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Send document
    # ------------------------------------------------------------------

    def trigger_send(self) -> None:
        self.click(self.TRIGGER_SEND_BTN)
        self.wait_for_load()

    def get_send_status(self) -> str:
        return self.get_text(self.SEND_STATUS).strip()

    def send_was_successful(self) -> bool:
        status = self.get_send_status().lower()
        return "success" in status or "sent" in status

    # ------------------------------------------------------------------
    # Payload verification
    # ------------------------------------------------------------------

    def get_composition_sections(self) -> list:
        elements = self.page.query_selector_all(self.COMPOSITION_SECTION)
        return [el.text_content() for el in elements]

    def get_binary_resource_count(self) -> int:
        return len(self.page.query_selector_all(self.BINARY_RESOURCES))

    def get_related_person_text(self) -> str:
        return self.get_text(self.RELATED_PERSON_RESOURCE).strip()

    def get_itk_device_text(self) -> str:
        return self.get_text(self.ITK_DEVICE_RESOURCE).strip()

    def get_optional_resource_text(self) -> str:
        return self.get_text(self.OPTIONAL_RESOURCE).strip()

    def payload_visible(self) -> bool:
        return self.is_visible(self.PAYLOAD_PANEL)

    # ------------------------------------------------------------------
    # Amendment / replacement
    # ------------------------------------------------------------------

    def amend_consultation(self) -> None:
        self.click(self.AMEND_BTN)
        self.wait_for_load()

    def delete_consultation(self) -> None:
        self.click(self.DELETE_BTN)
        self.wait_for_load()

    def get_version_number(self) -> str:
        return self.get_text(self.VERSION_DISPLAY).strip()

    def get_replacement_id(self) -> str:
        return self.get_text(self.REPLACEMENT_ID).strip()

    # ------------------------------------------------------------------
    # Additional documents
    # ------------------------------------------------------------------

    def add_document(self, file_path: str) -> None:
        self.page.set_input_files(self.DOCUMENT_FILE_INPUT, file_path)
        self.click(self.ADD_DOCUMENT_BTN)
        self.wait_for_load()

    def get_document_count(self) -> int:
        return len(self.page.query_selector_all(f"{self.DOCUMENT_LIST} .document-item"))

    # ------------------------------------------------------------------
    # Errors & acknowledgements
    # ------------------------------------------------------------------

    def get_displayed_error(self) -> str:
        if self.is_visible(self.ERROR_DISPLAY):
            return self.get_text(self.ERROR_DISPLAY).strip()
        return self.get_error_message()

    def get_ack_status(self) -> str:
        return self.get_text(self.ACK_STATUS).strip()

    def notification_visible(self) -> bool:
        return self.is_visible(self.NOTIFICATION_PANEL)

    def get_notification_text(self) -> str:
        return self.get_text(self.NOTIFICATION_PANEL).strip()

    # ------------------------------------------------------------------
    # Message log
    # ------------------------------------------------------------------

    def get_message_log(self) -> str:
        return self.get_text(self.MESSAGE_LOG).strip()

    def message_conforms_to_mesh_itk3(self) -> bool:
        log = self.get_message_log().lower()
        return "mesh" in log and "itk3" in log
