"""Page object for patient-selection and GP record view screens."""
from pages.base_page import BasePage


class GpRecordPage(BasePage):
    """Encapsulates View GP Record and related patient-details states."""

    PATIENT_GP_RECORD_TITLE = "Patient GP Record"
    CONFIRM_DETAILS_BUTTON = "CONFIRM DETAILS"

    MEDICATIONS_HEADING = "Medications"
    ACUTE_MEDICATIONS_TAB = "Acute Medications"
    REPEAT_MEDICATIONS_TAB = "Repeat Medications"
    PRESCRIBED_ELSEWHERE_MEDICATIONS_TAB = "Prescribed Elsewhere Medications"
    DISCONTINUED_MEDICATIONS_TAB = "Discontinued Medications"
    MEDICATION_RANGE_SELECT = "#select"
    MEDICATION_RANGE_DEFAULT = "Showing 15 months of medication data"

    ACUTE_NO_DATA_LINE_1 = "No Issued Acute Medication data is recorded for this patient."
    ACUTE_NO_DATA_LINE_2 = (
        "There may be some unissued medication data available in the 'Not Issued' tab"
    )

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

        local_heading = self.page.get_by_role("heading", name="Local Patient Data")
        gp_heading = self.page.get_by_role("heading", name="GP Access Patient Data")
        practice_name_label = self.page.get_by_text("Practice Name", exact=True)

        if local_heading.count() > 0 and local_heading.first.is_visible():
            return
        if gp_heading.count() > 0 and gp_heading.first.is_visible():
            return
        if practice_name_label.count() > 0 and practice_name_label.first.is_visible():
            return

        practice_name_label.wait_for(state="visible", timeout=20000)

    def confirm_details_if_prompted(self) -> bool:
        """Confirm demographics when the Patient GP Record overlay requests it."""
        confirm_button = self.page.get_by_role("button", name=self.CONFIRM_DETAILS_BUTTON)
        if confirm_button.count() > 0 and confirm_button.first.is_visible():
            confirm_button.first.click(force=True)
            self.wait_for_load()

        medications_heading = self.page.get_by_role("heading", name=self.MEDICATIONS_HEADING)
        if medications_heading.count() > 0 and medications_heading.first.is_visible():
            return True

        return False

    def open_patient_gp_record(self) -> None:
        self.click_view_gp_record()
        self.confirm_details_if_prompted()

    def select_medication_tab(self, tab_name: str) -> None:
        tab = self.page.get_by_role("button", name=tab_name)
        tab.first.wait_for(state="visible", timeout=20000)
        tab.first.click(force=True)
        self.wait_for_load()
        self._wait_for_spinners_to_clear()

    def medication_range_filter_visible(self) -> bool:
        range_button = self.page.get_by_role("button", name=self.MEDICATION_RANGE_DEFAULT)
        if range_button.count() > 0 and range_button.first.is_visible():
            return True

        fallback = self.page.locator(self.MEDICATION_RANGE_SELECT)
        return fallback.count() > 0 and fallback.first.is_visible()

    def repeat_medication_item_count(self) -> int:
        # Repeat cards include "Most Recent Issue Date" in the clickable item summary.
        return self.page.get_by_role("button", name="Most Recent Issue Date", exact=False).count()

    def get_first_repeat_medication_name(self) -> str:
        """Return the medication name from the first item in Repeat Medications."""
        items = self.page.get_by_role("button", name="Most Recent Issue Date", exact=False)
        if items.count() == 0:
            return ""

        raw_text = items.first.inner_text(timeout=5000)
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        non_name_tokens = {
            "repeat",
            "repeat dispensing",
            "most recent issue date",
            "date added to the system",
            "issue",
            "authorised issue(s)",
            "dosage instructions",
            "patient notes",
            "additional notes",
            "as directed",
        }

        for line in lines:
            lower = line.lower()
            if lower in non_name_tokens:
                continue
            if lower.startswith("most recent issue date"):
                continue
            if lower.startswith("date added to the system"):
                continue
            if lower.replace(" ", "").isdigit():
                continue

            # Medication lines contain letters and are not metadata labels.
            if any(char.isalpha() for char in line):
                return line

        return ""

    def get_acute_medication_empty_message(self) -> str:
        line_1 = self.page.get_by_text(self.ACUTE_NO_DATA_LINE_1, exact=False)
        line_2 = self.page.get_by_text(self.ACUTE_NO_DATA_LINE_2, exact=False)

        if line_1.count() > 0 and line_2.count() > 0:
            return f"{line_1.first.inner_text().strip()}\n{line_2.first.inner_text().strip()}"

        body_text = self.page.locator("body").inner_text(timeout=5000)
        if self.ACUTE_NO_DATA_LINE_1 in body_text and self.ACUTE_NO_DATA_LINE_2 in body_text:
            return f"{self.ACUTE_NO_DATA_LINE_1}\n{self.ACUTE_NO_DATA_LINE_2}"

        return ""

    def _wait_for_spinners_to_clear(self) -> None:
        self.page.wait_for_function(
            r"""() => {
                const isVisible = (element) => {
                    if (!element || !element.isConnected) return false;
                    const style = window.getComputedStyle(element);
                    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
                        return false;
                    }
                    const rect = element.getBoundingClientRect();
                    return rect.width > 0 && rect.height > 0;
                };

                const selectors = [
                    '.MuiCircularProgress-root[role="progressbar"]',
                    '[role="progressbar"]:not([aria-label="notification timer"])',
                ];

                return selectors
                    .flatMap((selector) => Array.from(document.querySelectorAll(selector)))
                    .filter(isVisible)
                    .length === 0;
            }""",
            timeout=15000,
        )

    def get_gp_access_practice_name(self) -> str:
        comparison = self._get_patient_gp_record_comparison()

        for label in ("Practice Name", "GP Practice Name", "Name"):
            value = comparison.get(label, {}).get("gp", "").strip()
            if value:
                return value

        page_text = self.page.locator("body").inner_text(timeout=5000)
        lines = [line.strip() for line in page_text.splitlines() if line.strip()]
        for index, line in enumerate(lines):
            if line == "Practice Name" and index + 1 < len(lines):
                return lines[index + 1]

        available = ", ".join(sorted(comparison.keys()))
        raise AssertionError(
            "Could not extract Practice Name from GP record view. "
            f"Available labels: {available}"
        )

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

    def get_deceased_patient_notice(self) -> str:
        notice = self.page.get_by_text("Patient deceased", exact=False)
        if notice.count() > 0 and notice.first.is_visible():
            return notice.first.inner_text().strip()

        page_text = self.page.locator("body").inner_text(timeout=5000)
        for line in (line.strip() for line in page_text.splitlines() if line.strip()):
            if "patient deceased" in line.lower():
                return line

        return ""

    def refresh_patient_data_link_visible(self) -> bool:
        refresh_link = self.page.get_by_role("link", name="Refresh patient data via PDS")
        return refresh_link.count() > 0 and refresh_link.first.is_visible()

    def click_refresh_patient_data_via_pds(self) -> bool:
        refresh_link = self.page.get_by_role("link", name="Refresh patient data via PDS")
        if refresh_link.count() > 0 and refresh_link.first.is_visible():
            refresh_link.first.click(force=True)
            self.wait_for_load()
            return True

        verify_link = self.page.get_by_role("link", name="Verify patient via PDS")
        if verify_link.count() > 0 and verify_link.first.is_visible():
            verify_link.first.click(force=True)
            self.wait_for_load()
            return True

        verify_button = self.page.get_by_role("button", name="Verify patient via PDS")
        if verify_button.count() > 0 and verify_button.first.is_visible():
            verify_button.first.click(force=True)
            self.wait_for_load()
            return True

        generic_pds_link = self.page.locator("a:has-text('PDS')")
        if generic_pds_link.count() > 0 and generic_pds_link.first.is_visible():
            generic_pds_link.first.click(force=True)
            self.wait_for_load()
            return True

        generic_pds_button = self.page.locator("button:has-text('PDS')")
        if generic_pds_button.count() > 0 and generic_pds_button.first.is_visible():
            generic_pds_button.first.click(force=True)
            self.wait_for_load()
            return True

        return False

    def local_patient_data_matches(self, expected: dict[str, str], format_dob) -> bool:
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

        dob = expected.get("dob", "")
        if dob:
            field_checks["Date of Birth"] = format_dob(dob)

        for label, expected_value in field_checks.items():
            if not expected_value:
                continue

            actual_local = comparison.get(label, {}).get("local", "")
            if self.normalise_value(actual_local) != self.normalise_value(expected_value):
                return False

        return True

    def mismatch_icon_visible(self) -> bool:
        return self.page.locator("[data-testid='ErrorOutlineIcon']").count() > 0

    def get_gp_details_gp_access_values(self) -> dict[str, str]:
        section_values = self.page.evaluate(
            r"""() => {
                const wanted = ['Name', 'Telephone', 'Address'];
                const out = {};
                const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'));
                const gpHeading = headings.find(h => (h.textContent || '').trim() === 'GP Details');
                if (!gpHeading) return out;

                let root = gpHeading.parentElement;
                while (root && !wanted.some(k => (root.textContent || '').includes(k))) {
                    root = root.parentElement;
                }
                if (!root) return out;

                const allText = Array.from(root.querySelectorAll('div,span,p,td,th,label'))
                    .map(el => (el.textContent || '').trim())
                    .filter(Boolean);

                for (const field of wanted) {
                    const idx = allText.indexOf(field);
                    if (idx >= 0) {
                        for (let i = idx + 1; i < allText.length; i += 1) {
                            const candidate = allText[i];
                            if (!wanted.includes(candidate)) {
                                out[field] = candidate;
                                break;
                            }
                        }
                    }
                }

                return out;
            }"""
        )

        if all(section_values.get(k, "").strip() for k in ("Name", "Telephone", "Address")):
            return {
                "Name": section_values["Name"].strip(),
                "Telephone": section_values["Telephone"].strip(),
                "Address": section_values["Address"].strip(),
            }

        page_text = self.page.locator("body").inner_text(timeout=5000)
        text_values = self._extract_gp_details_from_text(page_text)
        if all(text_values.get(k, "").strip() for k in ("Name", "Telephone", "Address")):
            return text_values

        comparison = self._get_patient_gp_record_comparison()
        field_aliases = {
            "Name": ["Name", "GP Name"],
            "Telephone": ["Telephone", "Phone", "Telephone Number"],
            "Address": ["Address", "GP Address"],
        }

        gp_details: dict[str, str] = {}
        missing_fields: list[str] = []

        for field, aliases in field_aliases.items():
            value = ""
            for alias in aliases:
                if alias in comparison:
                    value = comparison.get(alias, {}).get("gp", "").strip()
                    if value:
                        break
            if value:
                gp_details[field] = value
            else:
                missing_fields.append(field)

        if missing_fields:
            available = ", ".join(sorted(comparison.keys()))
            raise AssertionError(
                "Could not extract GP Details fields for GEN-08. "
                f"Missing: {', '.join(missing_fields)}. Available labels: {available}"
            )

        return gp_details

    def is_blocked_after_pds_trace(self) -> bool:
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

    def _extract_gp_details_from_text(self, page_text: str) -> dict[str, str]:
        lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
        wanted = ("name", "telephone", "address")
        values: dict[str, str] = {}

        start_idx = 0
        for i, line in enumerate(lines):
            if "gp details" in line.lower():
                start_idx = i
                break

        scoped_lines = lines[start_idx:start_idx + 80] if lines else []

        for field in wanted:
            label_idx = -1
            for i, line in enumerate(scoped_lines):
                if line.lower() == field:
                    label_idx = i
                    break
            if label_idx < 0:
                continue

            for i in range(label_idx + 1, min(label_idx + 10, len(scoped_lines))):
                candidate = scoped_lines[i]
                lower = candidate.lower()
                if lower in wanted:
                    continue
                if "gp details" in lower:
                    continue
                values[field.title()] = candidate
                break

        return values

    @staticmethod
    def normalise_value(value: str) -> str:
        return " ".join(value.lower().replace("-", " ").replace("/", " ").split())
