"""Page object for Spine Integration interactions.

Covers: SDS LDAP lookups, JWT construction, SSP proxy, HTTP headers,
content types, audit trail, and error handling.
"""
from pages.base_page import BasePage


class SpineIntegrationPage(BasePage):
    """Page object for GP Connect Spine Integration capability."""

    # ------------------------------------------------------------------
    # Selectors
    # ------------------------------------------------------------------
    SDS_ORG_CODE_INPUT = "#sds-org-code"
    SDS_INTERACTION_ID_INPUT = "#sds-interaction-id"
    SDS_LOOKUP_BTN = "#sds-lookup-btn"
    SDS_ASID_RESULT = ".sds-asid"
    SDS_MHS_PARTY_KEY = ".sds-mhs-party-key"
    SDS_ENDPOINT_RESULT = ".sds-endpoint"

    JWT_PANEL = ".jwt-panel"
    JWT_HEADER = ".jwt-header"
    JWT_PAYLOAD = ".jwt-payload"

    REQUEST_HEADERS_PANEL = ".request-headers"
    CONTENT_TYPE_SELECT = "#content-type"
    ACCEPT_HEADER_SELECT = "#accept-header"
    FORMAT_PARAM_INPUT = "#format-param"

    SSP_TRACE_ID = "#ssp-trace-id"
    SSP_FROM = "#ssp-from"
    SSP_TO = "#ssp-to"
    SSP_INTERACTION_ID = "#ssp-interaction-id"

    SUBMIT_REQUEST_BTN = "#submit-request"
    RESPONSE_STATUS = ".response-status"
    RESPONSE_BODY = ".response-body"
    AUDIT_LOG = ".audit-log"
    ERROR_DISPLAY = ".error-display"

    # ------------------------------------------------------------------
    # SDS LDAP lookups
    # ------------------------------------------------------------------

    def perform_sds_lookup(self, org_code: str, interaction_id: str) -> None:
        self.fill(self.SDS_ORG_CODE_INPUT, org_code)
        self.fill(self.SDS_INTERACTION_ID_INPUT, interaction_id)
        self.click(self.SDS_LOOKUP_BTN)
        self.wait_for_load()

    def get_asid(self) -> str:
        return self.get_text(self.SDS_ASID_RESULT).strip()

    def get_mhs_party_key(self) -> str:
        return self.get_text(self.SDS_MHS_PARTY_KEY).strip()

    def get_fhir_endpoint(self) -> str:
        return self.get_text(self.SDS_ENDPOINT_RESULT).strip()

    # ------------------------------------------------------------------
    # JWT construction
    # ------------------------------------------------------------------

    def get_jwt_header(self) -> str:
        return self.get_text(self.JWT_HEADER).strip()

    def get_jwt_payload(self) -> str:
        return self.get_text(self.JWT_PAYLOAD).strip()

    def jwt_panel_visible(self) -> bool:
        return self.is_visible(self.JWT_PANEL)

    # ------------------------------------------------------------------
    # HTTP request configuration
    # ------------------------------------------------------------------

    def set_content_type(self, content_type: str) -> None:
        self.select_option(self.CONTENT_TYPE_SELECT, content_type)

    def set_accept_header(self, accept: str) -> None:
        self.select_option(self.ACCEPT_HEADER_SELECT, accept)

    def set_format_param(self, value: str) -> None:
        self.fill(self.FORMAT_PARAM_INPUT, value)

    def set_ssp_headers(self, trace_id: str, ssp_from: str,
                        ssp_to: str, interaction_id: str) -> None:
        self.fill(self.SSP_TRACE_ID, trace_id)
        self.fill(self.SSP_FROM, ssp_from)
        self.fill(self.SSP_TO, ssp_to)
        self.fill(self.SSP_INTERACTION_ID, interaction_id)

    # ------------------------------------------------------------------
    # Request submission
    # ------------------------------------------------------------------

    def submit_request(self) -> None:
        self.click(self.SUBMIT_REQUEST_BTN)
        self.wait_for_load()

    def get_response_status(self) -> str:
        return self.get_text(self.RESPONSE_STATUS).strip()

    def get_response_body(self) -> str:
        return self.get_text(self.RESPONSE_BODY).strip()

    def response_is_fhir_json(self) -> bool:
        body = self.get_response_body()
        return '"resourceType"' in body

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    def get_audit_log(self) -> str:
        return self.get_text(self.AUDIT_LOG).strip()

    # ------------------------------------------------------------------
    # Errors
    # ------------------------------------------------------------------

    def get_displayed_error(self) -> str:
        if self.is_visible(self.ERROR_DISPLAY):
            return self.get_text(self.ERROR_DISPLAY).strip()
        return self.get_error_message()
