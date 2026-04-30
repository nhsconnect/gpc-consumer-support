"""Page object for Access Record Structured interactions.

Covers: Medication requests, allergy requests, structured record retrieval,
clinical area filtering, date parameters, warning handling, and
extended areas (investigations, referrals, diary entries, problems,
immunisations, uncategorised data, consultations, linkages, search queries).
"""
from pages.base_page import BasePage


class AccessRecordStructuredPage(BasePage):
    """Page object for GP Connect Access Record Structured capability."""

    # ------------------------------------------------------------------
    # Selectors
    # ------------------------------------------------------------------

    # Patient search
    NHS_NUMBER_INPUT = "#ar-structured-nhs-number"
    SEARCH_BTN = "#ar-structured-search-btn"
    GIVEN_NAME_INPUT = "#givenName"
    FAMILY_NAME_INPUT = "#familyName"
    DATE_OF_BIRTH_INPUT = "#dateOfBirth"
    POSTCODE_INPUT = "#postcode"
    ADD_NEW_PATIENT_BTN = "#add-new-patient"
    NHS_NUMBER_SEARCH_BUTTON = "[id='patient-search=NHS NUMBER SEARCH']"

    # Clinical area selection
    CLINICAL_AREA_PANEL = ".clinical-area-panel"
    INCLUDE_MEDICATIONS_CHK = "#include-medications"
    INCLUDE_ALLERGIES_CHK = "#include-allergies"
    INCLUDE_INVESTIGATIONS_CHK = "#include-investigations"
    INCLUDE_REFERRALS_CHK = "#include-referrals"
    INCLUDE_DIARY_ENTRIES_CHK = "#include-diary-entries"
    INCLUDE_PROBLEMS_CHK = "#include-problems"
    INCLUDE_IMMUNISATIONS_CHK = "#include-immunisations"
    INCLUDE_UNCATEGORISED_CHK = "#include-uncategorised"
    INCLUDE_CONSULTATIONS_CHK = "#include-consultations"

    # Medication parameters
    PRESCRIPTION_ISSUES_CHK = "#include-prescription-issues"
    MED_SEARCH_FROM_DATE = "#medication-search-from-date"

    # Allergy parameters
    INCLUDE_RESOLVED_CHK = "#include-resolved-allergies"

    # Date period parameters (generic pattern per clinical area)
    SEARCH_PERIOD_START = "#search-period-start"
    SEARCH_PERIOD_END = "#search-period-end"

    # Problem filters
    FILTER_STATUS = "#filter-status"
    FILTER_SIGNIFICANCE = "#filter-significance"

    # Immunisation filters
    FILTER_NOT_GIVEN = "#filter-not-given"
    FILTER_IMM_STATUS = "#filter-imm-status"

    # Consultation count
    MOST_RECENT_COUNT = "#most-recent-count"

    # Submit
    SUBMIT_REQUEST_BTN = "#submit-structured-request"

    # Response panels
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

    # Warnings & errors
    WARNING_PANEL = ".warning-panel"
    CONFIDENTIAL_WARNING = ".confidential-warning"
    TRANSIT_WARNING = ".transit-warning"
    EMPTY_LIST_REASON = ".empty-list-reason"
    ERROR_DISPLAY = ".error-display"

    # Data import
    IMPORT_BTN = "#import-data-btn"
    RESOURCE_IDENTIFIERS = ".resource-identifiers"

    # ------------------------------------------------------------------
    # Patient search
    # ------------------------------------------------------------------

    def open_patient_search(self) -> None:
        self.navigate()
        self.page.get_by_role("link", name="NMS").click()
        self.wait_for_load()

        # Must click "Start New NMS" to reach the episode page with the demographic form
        start_btn = self.page.get_by_role("button", name="Start New NMS")
        start_btn.wait_for(state="visible", timeout=15000)
        start_btn.click()
        self.wait_for_load()

        name_search_button = self.page.get_by_role("button", name="NAME SEARCH")
        if name_search_button.is_visible():
            aria_pressed = name_search_button.get_attribute("aria-pressed")
            if aria_pressed != "true":
                name_search_button.click()
                self.wait_for_load()

    def search_patient(self, nhs_number: str) -> None:
        self.fill(self.NHS_NUMBER_INPUT, nhs_number)
        self.click(self.SEARCH_BTN)
        self.wait_for_load()

    def search_patient_by_demographics(
        self,
        *,
        given_name: str,
        family_name: str,
        date_of_birth: str,
        postcode: str = "",
        expected_result_text: str = "",
    ) -> None:
        formatted_dob = self._format_dob_for_search(date_of_birth)
        if self.page.locator(self.FAMILY_NAME_INPUT).count() > 0:
            self.fill(self.FAMILY_NAME_INPUT, family_name)
            self.fill(self.GIVEN_NAME_INPUT, given_name)
            self.fill(self.DATE_OF_BIRTH_INPUT, formatted_dob)
            self.fill(self.POSTCODE_INPUT, postcode)
        else:
            # Form order: family name, given name, date of birth, postcode
            textboxes = self.page.get_by_role("textbox")
            textboxes.nth(0).fill(family_name)
            textboxes.nth(1).fill(given_name)
            textboxes.nth(2).fill(formatted_dob)
            textboxes.nth(3).fill(postcode)
        self.page.locator("#submit").click(force=True)
        self.wait_for_load()
        self.select_top_patient_result(expected_result_text=expected_result_text)
        self.click_view_gp_record()

    def search_patient_by_family_name_only(
        self,
        *,
        family_name: str,
        expected_result_text: str = "",
    ) -> None:
        if self.page.locator(self.FAMILY_NAME_INPUT).count() > 0:
            self.fill(self.FAMILY_NAME_INPUT, family_name)
            self.fill(self.GIVEN_NAME_INPUT, "")
            self.fill(self.DATE_OF_BIRTH_INPUT, "")
            self.fill(self.POSTCODE_INPUT, "")
        else:
            textboxes = self.page.get_by_role("textbox")
            textboxes.nth(0).fill(family_name)
            textboxes.nth(1).fill("")
            textboxes.nth(2).fill("")
            textboxes.nth(3).fill("")

        self.page.locator("#submit").click(force=True)
        self.wait_for_load()
        self.select_top_patient_result(expected_result_text=expected_result_text)

    def open_nhs_number_search(self) -> None:
        self.open_patient_search()

        add_new_patient = self.page.locator(self.ADD_NEW_PATIENT_BTN)
        if add_new_patient.count() > 0 and add_new_patient.first.is_visible():
            add_new_patient.first.click(force=True)
        elif self.page.get_by_role("button", name="Add New Patient").count() > 0:
            self.page.get_by_role("button", name="Add New Patient").first.click(force=True)
            self.wait_for_load()

        nhs_search = self.page.locator(self.NHS_NUMBER_SEARCH_BUTTON)
        if nhs_search.count() > 0 and nhs_search.first.is_visible():
            nhs_search.first.click(force=True)
        elif self.page.get_by_role("button", name="NHS NUMBER SEARCH").count() > 0:
            self.page.get_by_role("button", name="NHS NUMBER SEARCH").click()
        elif self.page.get_by_text("NHS NUMBER SEARCH", exact=False).count() > 0:
            self.page.get_by_text("NHS NUMBER SEARCH", exact=False).first.click(force=True)
        # If no explicit toggle is visible, continue; some UI states already default to NHS search.
        self.wait_for_load()

    def search_patient_by_pds_trace(self, *, nhs_number: str, date_of_birth: str) -> None:
        formatted_dob = self._format_dob_for_search(date_of_birth)

        nhs_filled = self._fill_first_visible(
            [
                "#nhsNumber",
                "#nhs-number",
                "input[name='nhsNumber']",
                "input[id*='nhs'][id*='number' i]",
            ],
            nhs_number,
        )
        dob_filled = self._fill_first_visible(
            [
                "#dateOfBirth",
                "#dob",
                "input[name='dateOfBirth']",
                "input[name='dob']",
            ],
            formatted_dob,
        )

        if not nhs_filled or not dob_filled:
            textboxes = self.page.locator("input")
            if textboxes.count() >= 2:
                if not nhs_filled:
                    textboxes.nth(0).fill(nhs_number)
                if not dob_filled:
                    textboxes.nth(1).fill(formatted_dob)

        if self.page.locator("#submit").count() > 0:
            self.page.locator("#submit").first.click(force=True)
        elif self.page.get_by_role("button", name="Search").count() > 0:
            self.page.get_by_role("button", name="Search").first.click(force=True)
        self.wait_for_load()

    def _fill_first_visible(self, selectors: list[str], value: str) -> bool:
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0 and locator.first.is_visible():
                locator.first.fill(value)
                return True

        return False

    def select_top_patient_result(self, expected_result_text: str = "") -> None:
        choose_patient = self.page.locator("#ChoosePatient").first
        choose_patient.wait_for(state="visible", timeout=20000)
        choose_patient.click(force=True)
        self.wait_for_load()

    def click_view_gp_record(self) -> None:
        view_gp_record = self.page.locator("#view-gp-record")
        view_gp_record.wait_for(state="visible", timeout=20000)

        if not view_gp_record.is_enabled():
            refresh_link = self.page.get_by_role("link", name="Refresh patient data via PDS")
            if refresh_link.count() > 0 and refresh_link.first.is_visible():
                refresh_link.first.click(force=True)
                self.wait_for_load()
                view_gp_record.wait_for(state="visible", timeout=20000)

        view_gp_record.click(force=True)
        self.wait_for_load()
        self.page.get_by_role("heading", name="Local Patient Data").wait_for(
            state="visible", timeout=20000
        )

    def _get_patient_gp_record_comparison(self) -> dict[str, dict[str, str]]:
        return self.page.evaluate(
            r"""() => {
                const result = {};
                const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'));
                const localHeading = headings.find(h => (h.textContent || '').trim() === 'Local Patient Data');
                const gpHeading = headings.find(h => (h.textContent || '').trim() === 'GP Access Patient Data');
                if (!localHeading || !gpHeading) return result;

                let gridRoot = localHeading.parentElement;
                while (gridRoot && !gridRoot.textContent.includes('GP Access Patient Data')) {
                    gridRoot = gridRoot.parentElement;
                }
                if (!gridRoot || !gridRoot.parentElement) return result;

                const rowContainer = gridRoot.parentElement;
                const rows = Array.from(rowContainer.children).filter(el => {
                    if (el === gridRoot) return false;
                    const role = (el.getAttribute('role') || '').toLowerCase();
                    if (role === 'separator') return false;
                    const text = (el.textContent || '').trim();
                    return text.length > 0;
                });

                for (const row of rows) {
                    const values = Array.from(row.querySelectorAll('div,span,p'))
                        .map(el => (el.textContent || '').trim())
                        .filter(Boolean);
                    if (values.length < 3) continue;
                    const label = values[0];
                    const localValue = values[values.length - 2];
                    const gpValue = values[values.length - 1];
                    result[label] = { local: localValue, gp: gpValue };
                }

                return result;
            }"""
        )

    def _normalise_value(self, value: str) -> str:
        return " ".join(value.lower().replace("-", " ").replace("/", " ").split())

    def local_patient_data_matches(self, expected: dict[str, str]) -> bool:
        comparison = self._get_patient_gp_record_comparison()
        if not comparison:
            return False

        local_gender = expected.get("local_gender", expected.get("gender", ""))
        local_gp_ods = expected.get("local_gp_ods_code", expected.get("gp_ods_code", ""))

        field_checks = {
            "Family Name": expected.get("family_name", ""),
            "First name": expected.get("given_name", ""),
            "Gender": local_gender,
            "GP ODS Code": local_gp_ods,
        }

        # Date of birth in the UI is DD/MM/YYYY.
        dob = expected.get("dob", "")
        if dob:
            field_checks["Date of Birth"] = self._format_dob_for_search(dob)

        for label, expected_value in field_checks.items():
            if not expected_value:
                continue
            actual_local = comparison.get(label, {}).get("local", "")
            if self._normalise_value(actual_local) != self._normalise_value(expected_value):
                return False

        return True

    def mismatch_icon_visible(self) -> bool:
        return self.page.locator("[data-testid='ErrorOutlineIcon']").count() > 0

    def can_view_gp_record(self) -> bool:
        view_button = self.page.locator("#view-gp-record")
        return view_button.count() > 0 and view_button.first.is_visible()

    def is_view_gp_record_disabled(self) -> bool:
        view_button = self.page.locator("#view-gp-record")
        return (
            view_button.count() > 0
            and view_button.first.is_visible()
            and not view_button.first.is_enabled()
        )

    def refresh_patient_data_link_visible(self) -> bool:
        refresh_link = self.page.get_by_role("link", name="Refresh patient data via PDS")
        return refresh_link.count() > 0 and refresh_link.first.is_visible()

    def is_blocked_after_pds_trace(self) -> bool:
        """Return True when the PDS trace route cannot progress to GP record access.

        For GEN-09/s-flag cases the user should remain on the NMS episode route,
        without actionable patient selection or GP record entry controls.
        """
        on_nms_episode = "nms-episode" in self.current_url

        choose_patient = self.page.locator("#ChoosePatient")
        choose_patient_visible = choose_patient.count() > 0 and choose_patient.first.is_visible()

        local_data_heading = self.page.get_by_role("heading", name="Local Patient Data")
        local_data_visible = (
            local_data_heading.count() > 0 and local_data_heading.first.is_visible()
        )

        return (
            on_nms_episode
            and not self.can_view_gp_record()
            and not choose_patient_visible
            and not local_data_visible
        )

    def _format_dob_for_search(self, date_of_birth: str) -> str:
        if "/" in date_of_birth:
            return date_of_birth

        year, month, day = date_of_birth.split("-")
        return f"{day}/{month}/{year}"

    # ------------------------------------------------------------------
    # Clinical area selection
    # ------------------------------------------------------------------

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
        sel = checkbox_map.get(area)
        if sel:
            is_checked = self.page.is_checked(sel)
            if enabled != is_checked:
                self.click(sel)

    # ------------------------------------------------------------------
    # Medication parameters
    # ------------------------------------------------------------------

    def set_prescription_issues(self, value: bool) -> None:
        is_checked = self.page.is_checked(self.PRESCRIPTION_ISSUES_CHK)
        if value != is_checked:
            self.click(self.PRESCRIPTION_ISSUES_CHK)

    def set_medication_search_from_date(self, date_str: str) -> None:
        self.fill(self.MED_SEARCH_FROM_DATE, date_str)

    def clear_medication_search_from_date(self) -> None:
        self.fill(self.MED_SEARCH_FROM_DATE, "")

    # ------------------------------------------------------------------
    # Allergy parameters
    # ------------------------------------------------------------------

    def set_include_resolved_allergies(self, value: bool) -> None:
        is_checked = self.page.is_checked(self.INCLUDE_RESOLVED_CHK)
        if value != is_checked:
            self.click(self.INCLUDE_RESOLVED_CHK)

    # ------------------------------------------------------------------
    # Generic date period parameters
    # ------------------------------------------------------------------

    def set_search_period(self, start: str = "", end: str = "") -> None:
        if start:
            self.fill(self.SEARCH_PERIOD_START, start)
        if end:
            self.fill(self.SEARCH_PERIOD_END, end)

    # ------------------------------------------------------------------
    # Problem filters
    # ------------------------------------------------------------------

    def set_problem_filters(self, status: str = "", significance: str = "") -> None:
        if status:
            self.select_option(self.FILTER_STATUS, status)
        if significance:
            self.select_option(self.FILTER_SIGNIFICANCE, significance)

    # ------------------------------------------------------------------
    # Immunisation filters
    # ------------------------------------------------------------------

    def set_immunisation_filters(self, not_given: str = "", status: str = "") -> None:
        if not_given:
            self.select_option(self.FILTER_NOT_GIVEN, not_given)
        if status:
            self.select_option(self.FILTER_IMM_STATUS, status)

    # ------------------------------------------------------------------
    # Consultation count
    # ------------------------------------------------------------------

    def set_most_recent_count(self, count: int) -> None:
        self.fill(self.MOST_RECENT_COUNT, str(count))

    # ------------------------------------------------------------------
    # Submit
    # ------------------------------------------------------------------

    def submit_request(self) -> None:
        self.click(self.SUBMIT_REQUEST_BTN)
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Response reading
    # ------------------------------------------------------------------

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
        sel = selector_map.get(area)
        return self.is_visible(sel) if sel else False

    # ------------------------------------------------------------------
    # Warnings
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Data import & identifiers
    # ------------------------------------------------------------------

    def import_data(self) -> None:
        self.click(self.IMPORT_BTN)
        self.wait_for_load()

    def get_resource_identifiers(self) -> str:
        return self.get_text(self.RESOURCE_IDENTIFIERS).strip()

    # ------------------------------------------------------------------
    # Errors
    # ------------------------------------------------------------------

    def get_displayed_error(self) -> str:
        if self.is_visible(self.ERROR_DISPLAY):
            return self.get_text(self.ERROR_DISPLAY).strip()
        return self.get_error_message()
