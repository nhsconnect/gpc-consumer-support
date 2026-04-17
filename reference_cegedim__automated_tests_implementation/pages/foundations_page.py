"""Page object for Foundations capability interactions.

Covers: Capability Statement, Find/Read Patient, Register Patient,
Find/Read Practitioner, Find/Read Organisation, Read Location.
"""
from pages.base_page import BasePage


class FoundationsPage(BasePage):
    """Page object for GP Connect Foundations capability."""

    # ------------------------------------------------------------------
    # Selectors (update once the real UI is inspected)
    # ------------------------------------------------------------------
    PATIENT_SEARCH_INPUT = "#patient-nhs-number"
    PATIENT_SEARCH_BTN = "#search-patient-btn"
    PATIENT_RESULTS_TABLE = ".patient-results"
    PATIENT_DETAIL_PANEL = ".patient-detail"
    PATIENT_NAME = ".patient-name"
    PATIENT_DOB = ".patient-dob"
    PATIENT_GENDER = ".patient-gender"
    PATIENT_NHS_NUMBER = ".patient-nhs"

    PRACTITIONER_SEARCH_INPUT = "#practitioner-sds-id"
    PRACTITIONER_SEARCH_BTN = "#search-practitioner-btn"
    PRACTITIONER_RESULTS = ".practitioner-results"

    ORGANISATION_SEARCH_INPUT = "#organisation-ods-code"
    ORGANISATION_SEARCH_BTN = "#search-organisation-btn"
    ORGANISATION_RESULTS = ".organisation-results"

    LOCATION_ID_INPUT = "#location-id"
    LOCATION_SEARCH_BTN = "#search-location-btn"
    LOCATION_RESULTS = ".location-results"

    REGISTER_PATIENT_BTN = "#register-patient-btn"
    REGISTER_NHS_INPUT = "#register-nhs-number"
    REGISTER_DOB_INPUT = "#register-dob"
    REGISTER_ADDRESS_INPUT = "#register-address"
    REGISTER_TELECOM_INPUT = "#register-telecom"
    REGISTER_SUBMIT_BTN = "#register-submit-btn"

    CAPABILITY_STATEMENT_BTN = "#get-capability-statement"
    CAPABILITY_RESPONSE = ".capability-response"

    ERROR_DISPLAY = ".error-display"
    SLOT_PICKER = "#slot-picker"
    CONFIRM_BOOKING_BTN = "#confirm-booking-btn"

    # ------------------------------------------------------------------
    # Capability Statement
    # ------------------------------------------------------------------

    def get_capability_statement(self) -> str:
        self.click(self.CAPABILITY_STATEMENT_BTN)
        self.wait_for_load()
        return self.get_text(self.CAPABILITY_RESPONSE)

    # ------------------------------------------------------------------
    # Find Patient
    # ------------------------------------------------------------------

    def search_patient(self, nhs_number: str) -> None:
        self.fill(self.PATIENT_SEARCH_INPUT, nhs_number)
        self.click(self.PATIENT_SEARCH_BTN)
        self.wait_for_load()

    def get_patient_results_count(self) -> int:
        rows = self.page.query_selector_all(f"{self.PATIENT_RESULTS_TABLE} tr")
        return max(len(rows) - 1, 0)  # exclude header row

    def patient_detail_visible(self) -> bool:
        return self.is_visible(self.PATIENT_DETAIL_PANEL)

    def get_patient_name(self) -> str:
        return self.get_text(self.PATIENT_NAME).strip()

    def get_patient_dob(self) -> str:
        return self.get_text(self.PATIENT_DOB).strip()

    def get_patient_gender(self) -> str:
        return self.get_text(self.PATIENT_GENDER).strip()

    def get_patient_nhs_number(self) -> str:
        return self.get_text(self.PATIENT_NHS_NUMBER).strip()

    # ------------------------------------------------------------------
    # Read Patient
    # ------------------------------------------------------------------

    def read_patient(self, logical_id: str) -> None:
        """Navigate to the read patient endpoint for a logical ID."""
        self.navigate(f"patient/{logical_id}")

    # ------------------------------------------------------------------
    # Register Patient
    # ------------------------------------------------------------------

    def open_register_patient(self) -> None:
        self.click(self.REGISTER_PATIENT_BTN)
        self.wait_for_load()

    def fill_registration(self, nhs_number: str, dob: str,
                          address: str = "", telecom: str = "") -> None:
        self.fill(self.REGISTER_NHS_INPUT, nhs_number)
        self.fill(self.REGISTER_DOB_INPUT, dob)
        if address:
            self.fill(self.REGISTER_ADDRESS_INPUT, address)
        if telecom:
            self.fill(self.REGISTER_TELECOM_INPUT, telecom)

    def submit_registration(self) -> None:
        self.click(self.REGISTER_SUBMIT_BTN)
        self.wait_for_load()

    def clear_registration_field(self, field: str) -> None:
        """Clear a specific field in the registration form."""
        selector_map = {
            "nhs_number": self.REGISTER_NHS_INPUT,
            "dob": self.REGISTER_DOB_INPUT,
            "address": self.REGISTER_ADDRESS_INPUT,
            "telecom": self.REGISTER_TELECOM_INPUT,
        }
        sel = selector_map.get(field)
        if sel:
            self.fill(sel, "")

    # ------------------------------------------------------------------
    # Find / Read Practitioner
    # ------------------------------------------------------------------

    def search_practitioner(self, sds_user_id: str) -> None:
        self.fill(self.PRACTITIONER_SEARCH_INPUT, sds_user_id)
        self.click(self.PRACTITIONER_SEARCH_BTN)
        self.wait_for_load()

    def get_practitioner_results_count(self) -> int:
        rows = self.page.query_selector_all(f"{self.PRACTITIONER_RESULTS} tr")
        return max(len(rows) - 1, 0)

    def read_practitioner(self, logical_id: str) -> None:
        self.navigate(f"practitioner/{logical_id}")

    # ------------------------------------------------------------------
    # Find / Read Organisation
    # ------------------------------------------------------------------

    def search_organisation(self, ods_code: str) -> None:
        self.fill(self.ORGANISATION_SEARCH_INPUT, ods_code)
        self.click(self.ORGANISATION_SEARCH_BTN)
        self.wait_for_load()

    def get_organisation_results_count(self) -> int:
        rows = self.page.query_selector_all(f"{self.ORGANISATION_RESULTS} tr")
        return max(len(rows) - 1, 0)

    def read_organisation(self, logical_id: str) -> None:
        self.navigate(f"organisation/{logical_id}")

    # ------------------------------------------------------------------
    # Read Location
    # ------------------------------------------------------------------

    def search_location(self, location_id: str) -> None:
        self.fill(self.LOCATION_ID_INPUT, location_id)
        self.click(self.LOCATION_SEARCH_BTN)
        self.wait_for_load()

    def read_location(self, logical_id: str) -> None:
        self.navigate(f"location/{logical_id}")

    # ------------------------------------------------------------------
    # Booking / Slots
    # ------------------------------------------------------------------

    def select_slot(self, slot_index: int = 0) -> None:
        slots = self.page.query_selector_all(f"{self.SLOT_PICKER} .slot-option")
        if slots and slot_index < len(slots):
            slots[slot_index].click()

    def confirm_booking(self) -> None:
        self.click(self.CONFIRM_BOOKING_BTN)
        self.wait_for_load()

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------

    def get_displayed_error(self) -> str:
        if self.is_visible(self.ERROR_DISPLAY):
            return self.get_text(self.ERROR_DISPLAY).strip()
        return self.get_error_message()
