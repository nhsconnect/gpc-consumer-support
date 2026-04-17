"""Page object for Access Record HTML interactions.

Covers: Patient tracing, record retrieval, HTML view rendering,
date filters, banners, demographics comparison, data sharing,
and GP2GP transfer handling.
"""
from pages.base_page import BasePage


class AccessRecordHtmlPage(BasePage):
    """Page object for GP Connect Access Record HTML capability."""

    # ------------------------------------------------------------------
    # Selectors
    # ------------------------------------------------------------------
    NHS_NUMBER_INPUT = "#ar-html-nhs-number"
    SEARCH_BTN = "#ar-html-search-btn"
    RETRIEVE_RECORD_BTN = "#retrieve-record-btn"

    # Patient banner
    PATIENT_BANNER = ".patient-banner"
    PATIENT_BANNER_NAME = ".patient-banner .patient-name"
    PATIENT_BANNER_NHS = ".patient-banner .patient-nhs"
    PATIENT_BANNER_DOB = ".patient-banner .patient-dob"
    PATIENT_BANNER_GENDER = ".patient-banner .patient-gender"
    PATIENT_BANNER_GP = ".patient-banner .patient-gp-practice"

    # Demographics comparison
    DEMOGRAPHICS_ALERT = ".demographics-mismatch-alert"
    DEMOGRAPHICS_DIFF = ".demographics-diff"

    # HTML record sections
    RECORD_SECTION = ".record-section"
    SECTION_BANNER = ".section-banner"
    SUBSECTION_BANNER = ".subsection-banner"
    DATE_BANNER = ".date-banner"
    EXCLUSION_BANNER = ".exclusion-banner"
    TRANSFER_BANNER = ".transfer-banner"

    # Date filter controls
    DATE_FILTER_SECTION = "#date-filter-section"
    DATE_FROM_INPUT = "#date-from"
    DATE_TO_INPUT = "#date-to"
    APPLY_DATE_FILTER_BTN = "#apply-date-filter"

    # Section dropdown
    SECTION_SELECT = "#record-section-select"

    # Response details
    RESPONSE_STATUS = ".response-status"
    XHTML_CONTENT = ".xhtml-content"
    ERROR_DISPLAY = ".error-display"
    ODS_CODE_DISPLAY = ".ods-code"

    # Data sharing
    DSA_STATUS = ".dsa-status"

    # ------------------------------------------------------------------
    # Patient tracing & search
    # ------------------------------------------------------------------

    def search_patient(self, nhs_number: str) -> None:
        self.fill(self.NHS_NUMBER_INPUT, nhs_number)
        self.click(self.SEARCH_BTN)
        self.wait_for_load()

    def retrieve_record(self) -> None:
        self.click(self.RETRIEVE_RECORD_BTN)
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Patient banner
    # ------------------------------------------------------------------

    def patient_banner_visible(self) -> bool:
        return self.is_visible(self.PATIENT_BANNER)

    def get_banner_name(self) -> str:
        return self.get_text(self.PATIENT_BANNER_NAME).strip()

    def get_banner_nhs(self) -> str:
        return self.get_text(self.PATIENT_BANNER_NHS).strip()

    def get_banner_dob(self) -> str:
        return self.get_text(self.PATIENT_BANNER_DOB).strip()

    def get_banner_gender(self) -> str:
        return self.get_text(self.PATIENT_BANNER_GENDER).strip()

    def get_banner_gp_practice(self) -> str:
        return self.get_text(self.PATIENT_BANNER_GP).strip()

    # ------------------------------------------------------------------
    # Demographics comparison
    # ------------------------------------------------------------------

    def demographics_alert_visible(self) -> bool:
        return self.is_visible(self.DEMOGRAPHICS_ALERT)

    def get_demographics_differences(self) -> str:
        return self.get_text(self.DEMOGRAPHICS_DIFF).strip()

    # ------------------------------------------------------------------
    # Record sections & HTML views
    # ------------------------------------------------------------------

    def select_section(self, section_name: str) -> None:
        self.select_option(self.SECTION_SELECT, section_name)

    def get_section_count(self) -> int:
        return len(self.page.query_selector_all(self.RECORD_SECTION))

    def section_banner_visible(self) -> bool:
        return self.is_visible(self.SECTION_BANNER)

    def subsection_banner_visible(self) -> bool:
        return self.is_visible(self.SUBSECTION_BANNER)

    def get_section_banner_text(self) -> str:
        return self.get_text(self.SECTION_BANNER).strip()

    def get_subsection_banner_text(self) -> str:
        return self.get_text(self.SUBSECTION_BANNER).strip()

    def get_xhtml_content(self) -> str:
        return self.get_text(self.XHTML_CONTENT).strip()

    # ------------------------------------------------------------------
    # Date filters & banners
    # ------------------------------------------------------------------

    def apply_date_filter(self, date_from: str = "", date_to: str = "") -> None:
        if date_from:
            self.fill(self.DATE_FROM_INPUT, date_from)
        if date_to:
            self.fill(self.DATE_TO_INPUT, date_to)
        self.click(self.APPLY_DATE_FILTER_BTN)
        self.wait_for_load()

    def date_banner_visible(self) -> bool:
        return self.is_visible(self.DATE_BANNER)

    def get_date_banner_text(self) -> str:
        return self.get_text(self.DATE_BANNER).strip()

    def exclusion_banner_visible(self) -> bool:
        return self.is_visible(self.EXCLUSION_BANNER)

    def get_exclusion_banner_text(self) -> str:
        return self.get_text(self.EXCLUSION_BANNER).strip()

    # ------------------------------------------------------------------
    # GP2GP transfer
    # ------------------------------------------------------------------

    def transfer_banner_visible(self) -> bool:
        return self.is_visible(self.TRANSFER_BANNER)

    def get_transfer_banner_text(self) -> str:
        return self.get_text(self.TRANSFER_BANNER).strip()

    # ------------------------------------------------------------------
    # Data sharing
    # ------------------------------------------------------------------

    def get_dsa_status(self) -> str:
        return self.get_text(self.DSA_STATUS).strip()

    # ------------------------------------------------------------------
    # Response & error
    # ------------------------------------------------------------------

    def get_response_status(self) -> str:
        return self.get_text(self.RESPONSE_STATUS).strip()

    def get_ods_code(self) -> str:
        return self.get_text(self.ODS_CODE_DISPLAY).strip()

    def get_displayed_error(self) -> str:
        if self.is_visible(self.ERROR_DISPLAY):
            return self.get_text(self.ERROR_DISPLAY).strip()
        return self.get_error_message()
