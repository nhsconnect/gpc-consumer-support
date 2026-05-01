"""Workflow adapter built from screen-based page objects for step definitions.

This is intentionally located in the test layer (not pages/) so the page
object model remains screen-oriented.
"""
from pages.gp_record_page import GpRecordPage
from pages.home_page import HomePage
from pages.nms_episode_page import NmsEpisodePage
from pages.structured_record_page import StructuredRecordPage


class AccessRecordScreens:
    """Step-definition helper that composes screen-specific page objects."""

    NHS_NUMBER_INPUT = StructuredRecordPage.NHS_NUMBER_INPUT
    SEARCH_BTN = StructuredRecordPage.SEARCH_BTN

    GIVEN_NAME_INPUT = NmsEpisodePage.GIVEN_NAME_INPUT
    FAMILY_NAME_INPUT = NmsEpisodePage.FAMILY_NAME_INPUT
    DATE_OF_BIRTH_INPUT = NmsEpisodePage.DATE_OF_BIRTH_INPUT
    POSTCODE_INPUT = NmsEpisodePage.POSTCODE_INPUT
    ADD_NEW_PATIENT_BTN = NmsEpisodePage.ADD_NEW_PATIENT_BTN
    NHS_NUMBER_SEARCH_BUTTON = NmsEpisodePage.NHS_NUMBER_SEARCH_BUTTON

    def __init__(
        self,
        home_page: HomePage,
        nms_episode_page: NmsEpisodePage,
        gp_record_page: GpRecordPage,
        structured_record_page: StructuredRecordPage,
    ):
        self.home_page = home_page
        self.nms_episode_page = nms_episode_page
        self.gp_record_page = gp_record_page
        self.structured_record_page = structured_record_page

        # Preserve access used by existing steps.
        self.page = structured_record_page.page

    def navigate(self, path: str = "") -> None:
        self.structured_record_page.navigate(path)

    def wait_for_load(self, timeout: int = 15_000) -> None:
        self.structured_record_page.wait_for_load(timeout=timeout)

    def highlight_text_assertion(self, text: str, duration_ms: int = 1500) -> None:
        self.structured_record_page.highlight_text_assertion(text, duration_ms=duration_ms)

    @property
    def current_url(self) -> str:
        return self.gp_record_page.current_url

    # ------------------------------------------------------------------
    # Patient search
    # ------------------------------------------------------------------

    def open_patient_search(self) -> None:
        self.home_page.open_new_nms_episode()

    def search_patient(self, nhs_number: str) -> None:
        self.structured_record_page.search_patient(nhs_number)

    def search_patient_by_demographics(
        self,
        *,
        given_name: str,
        family_name: str,
        date_of_birth: str,
        postcode: str = "",
        expected_result_text: str = "",
    ) -> None:
        _ = expected_result_text
        self.nms_episode_page.search_by_demographics(
            given_name=given_name,
            family_name=family_name,
            date_of_birth=date_of_birth,
            postcode=postcode,
        )
        self.select_top_patient_result()
        self.click_view_gp_record()

    def search_patient_by_family_name_only(
        self,
        *,
        family_name: str,
        expected_result_text: str = "",
        select_result: bool = True,
    ) -> None:
        _ = expected_result_text
        self.nms_episode_page.search_by_family_name_only(family_name=family_name)
        if select_result:
            self.select_top_patient_result()

    def open_nhs_number_search(self) -> None:
        self.open_patient_search()
        self.nms_episode_page.open_nhs_number_search_mode()

    def search_patient_by_pds_trace(self, *, nhs_number: str, date_of_birth: str) -> None:
        self.nms_episode_page.search_by_pds_trace(nhs_number=nhs_number, date_of_birth=date_of_birth)

    def select_top_patient_result(self, expected_result_text: str = "") -> None:
        _ = expected_result_text
        self.nms_episode_page.select_top_patient_result()

    def click_view_gp_record(self) -> None:
        self.gp_record_page.click_view_gp_record()

    def _normalise_value(self, value: str) -> str:
        return self.gp_record_page.normalise_value(value)

    def local_patient_data_matches(self, expected: dict[str, str]) -> bool:
        return self.gp_record_page.local_patient_data_matches(
            expected,
            format_dob=self._format_dob_for_search,
        )

    def mismatch_icon_visible(self) -> bool:
        return self.gp_record_page.mismatch_icon_visible()

    def get_gp_access_practice_name(self) -> str:
        return self.gp_record_page.get_gp_access_practice_name()

    def can_view_gp_record(self) -> bool:
        return self.gp_record_page.can_view_gp_record()

    def is_view_gp_record_disabled(self) -> bool:
        return self.gp_record_page.is_view_gp_record_disabled()

    def get_deceased_patient_notice(self) -> str:
        return self.gp_record_page.get_deceased_patient_notice()

    def refresh_patient_data_link_visible(self) -> bool:
        return self.gp_record_page.refresh_patient_data_link_visible()

    def click_refresh_patient_data_via_pds(self) -> bool:
        return self.gp_record_page.click_refresh_patient_data_via_pds()

    def get_gp_details_gp_access_values(self) -> dict[str, str]:
        return self.gp_record_page.get_gp_details_gp_access_values()

    def is_blocked_after_pds_trace(self) -> bool:
        return self.gp_record_page.is_blocked_after_pds_trace()

    def _format_dob_for_search(self, date_of_birth: str) -> str:
        return self.nms_episode_page.format_dob_for_search(date_of_birth)

    # ------------------------------------------------------------------
    # Structured request controls
    # ------------------------------------------------------------------

    def toggle_clinical_area(self, area: str, enabled: bool) -> None:
        self.structured_record_page.toggle_clinical_area(area, enabled)

    def set_prescription_issues(self, value: bool) -> None:
        self.structured_record_page.set_prescription_issues(value)

    def set_medication_search_from_date(self, date_str: str) -> None:
        self.structured_record_page.set_medication_search_from_date(date_str)

    def clear_medication_search_from_date(self) -> None:
        self.structured_record_page.clear_medication_search_from_date()

    def set_include_resolved_allergies(self, value: bool) -> None:
        self.structured_record_page.set_include_resolved_allergies(value)

    def set_search_period(self, start: str = "", end: str = "") -> None:
        self.structured_record_page.set_search_period(start=start, end=end)

    def set_problem_filters(self, status: str = "", significance: str = "") -> None:
        self.structured_record_page.set_problem_filters(status=status, significance=significance)

    def set_immunisation_filters(self, not_given: str = "", status: str = "") -> None:
        self.structured_record_page.set_immunisation_filters(not_given=not_given, status=status)

    def set_most_recent_count(self, count: int) -> None:
        self.structured_record_page.set_most_recent_count(count)

    def submit_request(self) -> None:
        self.structured_record_page.submit_request()

    # ------------------------------------------------------------------
    # Results, warnings, errors, and import
    # ------------------------------------------------------------------

    def response_visible(self) -> bool:
        return self.structured_record_page.response_visible()

    def get_medication_results(self) -> str:
        return self.structured_record_page.get_medication_results()

    def get_allergy_results(self) -> str:
        return self.structured_record_page.get_allergy_results()

    def get_investigation_results(self) -> str:
        return self.structured_record_page.get_investigation_results()

    def get_referral_results(self) -> str:
        return self.structured_record_page.get_referral_results()

    def get_diary_results(self) -> str:
        return self.structured_record_page.get_diary_results()

    def get_problem_results(self) -> str:
        return self.structured_record_page.get_problem_results()

    def get_immunisation_results(self) -> str:
        return self.structured_record_page.get_immunisation_results()

    def get_uncategorised_results(self) -> str:
        return self.structured_record_page.get_uncategorised_results()

    def get_consultation_results(self) -> str:
        return self.structured_record_page.get_consultation_results()

    def has_results_for(self, area: str) -> bool:
        return self.structured_record_page.has_results_for(area)

    def warning_panel_visible(self) -> bool:
        return self.structured_record_page.warning_panel_visible()

    def get_warning_text(self) -> str:
        return self.structured_record_page.get_warning_text()

    def confidential_warning_visible(self) -> bool:
        return self.structured_record_page.confidential_warning_visible()

    def transit_warning_visible(self) -> bool:
        return self.structured_record_page.transit_warning_visible()

    def get_empty_list_reason(self) -> str:
        return self.structured_record_page.get_empty_list_reason()

    def import_data(self) -> None:
        self.structured_record_page.import_data()

    def get_resource_identifiers(self) -> str:
        return self.structured_record_page.get_resource_identifiers()

    def get_displayed_error(self) -> str:
        return self.structured_record_page.get_displayed_error()

    def no_patients_found_visible(self) -> bool:
        return self.nms_episode_page.no_patients_found_visible()

    def get_no_patients_found_text(self) -> str:
        return self.nms_episode_page.get_no_patients_found_text()
