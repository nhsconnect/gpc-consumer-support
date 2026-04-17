"""Page object for Access Document interactions.

Covers: Find Patient, Search Documents, Retrieve Document,
date/author/description filters, error handling, and
superseded NHS number handling.
"""
from pages.base_page import BasePage


class AccessDocumentPage(BasePage):
    """Page object for GP Connect Access Document capability."""

    # ------------------------------------------------------------------
    # Selectors
    # ------------------------------------------------------------------

    # Find Patient
    NHS_NUMBER_INPUT = "#doc-nhs-number"
    FIND_PATIENT_BTN = "#doc-find-patient-btn"
    PATIENT_ID_DISPLAY = ".patient-identifier"

    # Search Documents
    SEARCH_DOCS_BTN = "#search-documents-btn"
    DATE_FROM_INPUT = "#doc-date-from"
    DATE_TO_INPUT = "#doc-date-to"
    AUTHOR_INPUT = "#doc-author"
    DESCRIPTION_INPUT = "#doc-description"
    INCLUDE_PARAMS = ".include-params"
    DOCUMENT_LIST = ".document-list"
    DOCUMENT_ROW = ".document-row"
    NO_DOCS_MESSAGE = ".no-documents-message"

    # Retrieve Document
    RETRIEVE_DOC_BTN = "#retrieve-document-btn"
    DOCUMENT_VIEWER = ".document-viewer"
    DOCUMENT_CONTENT = ".document-content"
    FILE_SIZE_WARNING = ".file-size-warning"

    # Error / status
    ERROR_DISPLAY = ".error-display"
    RESPONSE_STATUS = ".response-status"
    OPERATIONAL_OUTCOME = ".operational-outcome"
    DIAGNOSTIC_DETAILS = ".diagnostic-details"
    AUDIT_LOG = ".audit-log"

    # ------------------------------------------------------------------
    # Find Patient
    # ------------------------------------------------------------------

    def find_patient(self, nhs_number: str) -> None:
        self.fill(self.NHS_NUMBER_INPUT, nhs_number)
        self.click(self.FIND_PATIENT_BTN)
        self.wait_for_load()

    def get_patient_identifier(self) -> str:
        return self.get_text(self.PATIENT_ID_DISPLAY).strip()

    def patient_found(self) -> bool:
        return self.is_visible(self.PATIENT_ID_DISPLAY)

    # ------------------------------------------------------------------
    # Search Documents
    # ------------------------------------------------------------------

    def search_documents(self) -> None:
        self.click(self.SEARCH_DOCS_BTN)
        self.wait_for_load()

    def search_documents_from_date(self, date_from: str) -> None:
        self.fill(self.DATE_FROM_INPUT, date_from)
        self.search_documents()

    def search_documents_to_date(self, date_to: str) -> None:
        self.fill(self.DATE_TO_INPUT, date_to)
        self.search_documents()

    def search_documents_date_range(self, date_from: str, date_to: str) -> None:
        self.fill(self.DATE_FROM_INPUT, date_from)
        self.fill(self.DATE_TO_INPUT, date_to)
        self.search_documents()

    def search_documents_by_author(self, author: str) -> None:
        self.fill(self.AUTHOR_INPUT, author)
        self.search_documents()

    def search_documents_by_description(self, description: str) -> None:
        self.fill(self.DESCRIPTION_INPUT, description)
        self.search_documents()

    def get_document_count(self) -> int:
        return len(self.page.query_selector_all(self.DOCUMENT_ROW))

    def no_documents_message_visible(self) -> bool:
        return self.is_visible(self.NO_DOCS_MESSAGE)

    # ------------------------------------------------------------------
    # Retrieve Document
    # ------------------------------------------------------------------

    def select_document(self, index: int = 0) -> None:
        rows = self.page.query_selector_all(self.DOCUMENT_ROW)
        if rows and index < len(rows):
            rows[index].click()

    def retrieve_document(self) -> None:
        self.click(self.RETRIEVE_DOC_BTN)
        self.wait_for_load()

    def document_viewer_visible(self) -> bool:
        return self.is_visible(self.DOCUMENT_VIEWER)

    def get_document_content(self) -> str:
        return self.get_text(self.DOCUMENT_CONTENT).strip()

    def file_size_warning_visible(self) -> bool:
        return self.is_visible(self.FILE_SIZE_WARNING)

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------

    def get_displayed_error(self) -> str:
        if self.is_visible(self.ERROR_DISPLAY):
            return self.get_text(self.ERROR_DISPLAY).strip()
        return self.get_error_message()

    def get_operational_outcome(self) -> str:
        return self.get_text(self.OPERATIONAL_OUTCOME).strip()

    def get_diagnostic_details(self) -> str:
        return self.get_text(self.DIAGNOSTIC_DETAILS).strip()

    def get_response_status(self) -> str:
        return self.get_text(self.RESPONSE_STATUS).strip()

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    def get_audit_log(self) -> str:
        return self.get_text(self.AUDIT_LOG).strip()
