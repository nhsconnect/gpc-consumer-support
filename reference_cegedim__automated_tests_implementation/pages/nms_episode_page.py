"""Page object for patient search interactions on the NMS episode screen."""
from pages.base_page import BasePage
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class NmsEpisodePage(BasePage):
    """Encapsulates demographic and NHS-number search flows on NMS episode."""

    GIVEN_NAME_INPUT = "#givenName"
    FAMILY_NAME_INPUT = "#familyName"
    DATE_OF_BIRTH_INPUT = "#dateOfBirth"
    POSTCODE_INPUT = "#postcode"
    ADD_NEW_PATIENT_BTN = "#add-new-patient"
    NHS_NUMBER_SEARCH_BUTTON = "[id='patient-search=NHS NUMBER SEARCH']"

    def search_by_demographics(
        self,
        *,
        given_name: str,
        family_name: str,
        date_of_birth: str,
        postcode: str = "",
    ) -> None:
        formatted_dob = self.format_dob_for_search(date_of_birth)

        if self.page.locator(self.FAMILY_NAME_INPUT).count() > 0:
            self.fill(self.FAMILY_NAME_INPUT, family_name)
            self.fill(self.GIVEN_NAME_INPUT, given_name)
            self.fill(self.DATE_OF_BIRTH_INPUT, formatted_dob)
            self.fill(self.POSTCODE_INPUT, postcode)
        else:
            textboxes = self.page.get_by_role("textbox")
            textboxes.nth(0).fill(family_name)
            textboxes.nth(1).fill(given_name)
            textboxes.nth(2).fill(formatted_dob)
            textboxes.nth(3).fill(postcode)

        self.page.locator("#submit").click(force=True)
        self.wait_for_load()

    def search_by_family_name_only(self, *, family_name: str) -> None:
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

    def open_nhs_number_search_mode(self) -> None:
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

        self.wait_for_load()

    def search_by_pds_trace(self, *, nhs_number: str, date_of_birth: str) -> None:
        formatted_dob = self.format_dob_for_search(date_of_birth)

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

    def select_top_patient_result(self) -> None:
        choose_patient = self.page.locator("#ChoosePatient").first
        choose_patient.wait_for(state="visible", timeout=20000)
        choose_patient.click(force=True)

        try:
            self.wait_for_load(timeout=10000)
            return
        except PlaywrightTimeoutError:
            # Some NMS transitions keep background loaders alive; anchor on the
            # patient-details controls that indicate navigation succeeded.
            view_gp_record = self.page.locator("#view-gp-record")
            if view_gp_record.count() > 0:
                view_gp_record.first.wait_for(state="visible", timeout=20000)
                return

            session_heading = self.page.get_by_role("heading", name="Session 1 - Engagement")
            session_heading.first.wait_for(state="visible", timeout=20000)

    def no_patients_found_visible(self) -> bool:
        marker = self.page.get_by_text("No Patients Found", exact=False)
        return marker.count() > 0 and marker.first.is_visible()

    def get_no_patients_found_text(self) -> str:
        marker = self.page.get_by_text("No Patients Found", exact=False)
        if marker.count() > 0 and marker.first.is_visible():
            return marker.first.inner_text().strip()

        page_text = self.page.locator("body").inner_text(timeout=5000)
        for line in (line.strip() for line in page_text.splitlines() if line.strip()):
            if line.lower() == "no patients found":
                return line

        return ""

    def _fill_first_visible(self, selectors: list[str], value: str) -> bool:
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0 and locator.first.is_visible():
                locator.first.fill(value)
                return True

        return False

    @staticmethod
    def format_dob_for_search(date_of_birth: str) -> str:
        if "/" in date_of_birth:
            return date_of_birth

        year, month, day = date_of_birth.split("-")
        return f"{day}/{month}/{year}"
