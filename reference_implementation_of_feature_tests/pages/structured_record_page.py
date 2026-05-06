"""Page object for access record structured request and response panels."""
from pages.base_page import BasePage


class StructuredRecordPage(BasePage):
    """Encapsulates structured request controls, results, warnings, and errors."""

    NHS_NUMBER_INPUT = "#ar-structured-nhs-number"
    SEARCH_BTN = "#ar-structured-search-btn"

    INCLUDE_MEDICATIONS_CHK = "#include-medications"
    INCLUDE_ALLERGIES_CHK = "#include-allergies"
    INCLUDE_INVESTIGATIONS_CHK = "#include-investigations"
    INCLUDE_REFERRALS_CHK = "#include-referrals"
    INCLUDE_DIARY_ENTRIES_CHK = "#include-diary-entries"
    INCLUDE_PROBLEMS_CHK = "#include-problems"
    INCLUDE_IMMUNISATIONS_CHK = "#include-immunisations"
    INCLUDE_UNCATEGORISED_CHK = "#include-uncategorised"
    INCLUDE_CONSULTATIONS_CHK = "#include-consultations"

    PRESCRIPTION_ISSUES_CHK = "#include-prescription-issues"
    MED_SEARCH_FROM_DATE = "#medication-search-from-date"

    INCLUDE_RESOLVED_CHK = "#include-resolved-allergies"

    SEARCH_PERIOD_START = "#search-period-start"
    SEARCH_PERIOD_END = "#search-period-end"

    FILTER_STATUS = "#filter-status"
    FILTER_SIGNIFICANCE = "#filter-significance"

    FILTER_NOT_GIVEN = "#filter-not-given"
    FILTER_IMM_STATUS = "#filter-imm-status"

    MOST_RECENT_COUNT = "#most-recent-count"

    SUBMIT_REQUEST_BTN = "#submit-structured-request"

    RESPONSE_PANEL = ".structured-response-panel"
    MEDICATION_RESULTS = ".medication-results"
    ALLERGY_RESULTS = ".allergy-results"
    INVESTIGATION_RESULTS = ".investigation-results"
    REFERRAL_RESULTS = ".referral-results"
    DIARY_RESULTS = ".diary-results"
    PROBLEM_RESULTS = ".problem-results"
    IMMUNISATION_RESULTS = ".immunisation-results"
    UNCATEGORISED_RESULTS = ".uncategorised-results"
    CONSULTATION_RESULTS = ".consultation-results"

    WARNING_PANEL = ".warning-panel"
    CONFIDENTIAL_WARNING = ".confidential-warning"
    TRANSIT_WARNING = ".transit-warning"
    EMPTY_LIST_REASON = ".empty-list-reason"
    ERROR_DISPLAY = ".error-display"

    IMPORT_BTN = "#import-data-btn"
    RESOURCE_IDENTIFIERS = ".resource-identifiers"

    def search_patient(self, nhs_number: str) -> None:
        self.fill(self.NHS_NUMBER_INPUT, nhs_number)
        self.click(self.SEARCH_BTN)
        self.wait_for_load()

    def toggle_clinical_area(self, area: str, enabled: bool) -> None:
        checkbox_map = {
            "medications": self.INCLUDE_MEDICATIONS_CHK,
            "allergies": self.INCLUDE_ALLERGIES_CHK,
            "investigations": self.INCLUDE_INVESTIGATIONS_CHK,
            "referrals": self.INCLUDE_REFERRALS_CHK,
            "diary_entries": self.INCLUDE_DIARY_ENTRIES_CHK,
            "problems": self.INCLUDE_PROBLEMS_CHK,
            "immunisations": self.INCLUDE_IMMUNISATIONS_CHK,
            "uncategorised": self.INCLUDE_UNCATEGORISED_CHK,
            "consultations": self.INCLUDE_CONSULTATIONS_CHK,
        }
        selector = checkbox_map.get(area)
        if selector:
            is_checked = self.page.is_checked(selector)
            if enabled != is_checked:
                self.click(selector)

    def set_prescription_issues(self, value: bool) -> None:
        is_checked = self.page.is_checked(self.PRESCRIPTION_ISSUES_CHK)
        if value != is_checked:
            self.click(self.PRESCRIPTION_ISSUES_CHK)

    def set_medication_search_from_date(self, date_str: str) -> None:
        self.fill(self.MED_SEARCH_FROM_DATE, date_str)

    def clear_medication_search_from_date(self) -> None:
        self.fill(self.MED_SEARCH_FROM_DATE, "")

    def set_include_resolved_allergies(self, value: bool) -> None:
        is_checked = self.page.is_checked(self.INCLUDE_RESOLVED_CHK)
        if value != is_checked:
            self.click(self.INCLUDE_RESOLVED_CHK)

    def set_search_period(self, start: str = "", end: str = "") -> None:
        if start:
            self.fill(self.SEARCH_PERIOD_START, start)
        if end:
            self.fill(self.SEARCH_PERIOD_END, end)

    def set_problem_filters(self, status: str = "", significance: str = "") -> None:
        if status:
            self.select_option(self.FILTER_STATUS, status)
        if significance:
            self.select_option(self.FILTER_SIGNIFICANCE, significance)

    def set_immunisation_filters(self, not_given: str = "", status: str = "") -> None:
        if not_given:
            self.select_option(self.FILTER_NOT_GIVEN, not_given)
        if status:
            self.select_option(self.FILTER_IMM_STATUS, status)

    def set_most_recent_count(self, count: int) -> None:
        self.fill(self.MOST_RECENT_COUNT, str(count))

    def submit_request(self) -> None:
        self.click(self.SUBMIT_REQUEST_BTN)
        self.wait_for_load()

    def response_visible(self) -> bool:
        return self.is_visible(self.RESPONSE_PANEL)

    def get_medication_results(self) -> str:
        return self.get_text(self.MEDICATION_RESULTS).strip()

    def get_allergy_results(self) -> str:
        return self.get_text(self.ALLERGY_RESULTS).strip()

    def get_investigation_results(self) -> str:
        return self.get_text(self.INVESTIGATION_RESULTS).strip()

    def get_referral_results(self) -> str:
        return self.get_text(self.REFERRAL_RESULTS).strip()

    def get_diary_results(self) -> str:
        return self.get_text(self.DIARY_RESULTS).strip()

    def get_problem_results(self) -> str:
        return self.get_text(self.PROBLEM_RESULTS).strip()

    def get_immunisation_results(self) -> str:
        return self.get_text(self.IMMUNISATION_RESULTS).strip()

    def get_uncategorised_results(self) -> str:
        return self.get_text(self.UNCATEGORISED_RESULTS).strip()

    def get_consultation_results(self) -> str:
        return self.get_text(self.CONSULTATION_RESULTS).strip()

    def has_results_for(self, area: str) -> bool:
        selector_map = {
            "medications": self.MEDICATION_RESULTS,
            "allergies": self.ALLERGY_RESULTS,
            "investigations": self.INVESTIGATION_RESULTS,
            "referrals": self.REFERRAL_RESULTS,
            "diary_entries": self.DIARY_RESULTS,
            "problems": self.PROBLEM_RESULTS,
            "immunisations": self.IMMUNISATION_RESULTS,
            "uncategorised": self.UNCATEGORISED_RESULTS,
            "consultations": self.CONSULTATION_RESULTS,
        }
        selector = selector_map.get(area)
        return self.is_visible(selector) if selector else False

    def warning_panel_visible(self) -> bool:
        return self.is_visible(self.WARNING_PANEL)

    def get_warning_text(self) -> str:
        return self.get_text(self.WARNING_PANEL).strip()

    def confidential_warning_visible(self) -> bool:
        return self.is_visible(self.CONFIDENTIAL_WARNING)

    def transit_warning_visible(self) -> bool:
        return self.is_visible(self.TRANSIT_WARNING)

    def get_empty_list_reason(self) -> str:
        return self.get_text(self.EMPTY_LIST_REASON).strip()

    def import_data(self) -> None:
        self.click(self.IMPORT_BTN)
        self.wait_for_load()

    def get_resource_identifiers(self) -> str:
        return self.get_text(self.RESOURCE_IDENTIFIERS).strip()

    def get_displayed_error(self) -> str:
        if self.is_visible(self.ERROR_DISPLAY):
            return self.get_text(self.ERROR_DISPLAY).strip()
        return self.get_error_message()
