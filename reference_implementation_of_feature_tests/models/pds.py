"""Typed model for the PDS patient-details aggregator response.

Maps the JSON returned by /aggregator/pds/patient-details into Python
dataclasses so step definitions can assert on typed fields rather than
raw dict access.

Example response shape::

    {
        "nhsNumber": "9726905230",
        "confidentialityCode": "U",
        "patientDetails": {
            "title": "Mr",
            "givenName": "Basil",
            "otherName": "Bert",
            "familyName": "Wadham",
            "gender": "m",
            "dateOfBirth": "1999-03-14",
            "dateOfDeath": null,
            "confidentialityCode": null,
            "addresses": [{"addressLines": [...], "postcode": "LS18 1AE", "use": "H"}],
            "telecoms": [{"communication": "...", "communicationType": "TEL", "communicationUse": "H"}]
        },
        "practice": {
            "odsCode": "P83007",
            "name": "RADCLIFFE MEDICAL PRACTICE",
            "address": {"addressLines": [...], "postcode": "M26 1WS", "use": null},
            "telecoms": [...]
        },
        "supersededNhsNumber": false,
        "localIdentifier": null
    }
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PdsTelecom:
    communication: Optional[str]
    communication_type: Optional[str]
    communication_use: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> PdsTelecom:
        return cls(
            communication=data.get("communication"),
            communication_type=data.get("communicationType"),
            communication_use=data.get("communicationUse"),
        )


@dataclass
class PdsAddress:
    address_lines: list[str]
    postcode: Optional[str]
    use: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> PdsAddress:
        return cls(
            address_lines=list(data.get("addressLines") or []),
            postcode=data.get("postcode"),
            use=data.get("use"),
        )


@dataclass
class PdsPatientDetails:
    title: Optional[str]
    given_name: Optional[str]
    other_name: Optional[str]
    family_name: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[str]
    date_of_death: Optional[str]
    confidentiality_code: Optional[str]
    addresses: list[PdsAddress] = field(default_factory=list)
    telecoms: list[PdsTelecom] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> PdsPatientDetails:
        return cls(
            title=data.get("title"),
            given_name=data.get("givenName"),
            other_name=data.get("otherName"),
            family_name=data.get("familyName"),
            gender=data.get("gender"),
            date_of_birth=data.get("dateOfBirth"),
            date_of_death=data.get("dateOfDeath"),
            confidentiality_code=data.get("confidentialityCode"),
            addresses=[PdsAddress.from_dict(a) for a in data.get("addresses") or []],
            telecoms=[PdsTelecom.from_dict(t) for t in data.get("telecoms") or []],
        )

    @property
    def is_deceased(self) -> bool:
        """True when PDS has a non-null dateOfDeath for this patient."""
        return self.date_of_death is not None

    @property
    def full_name(self) -> str:
        parts = [self.given_name, self.other_name, self.family_name]
        return " ".join(p for p in parts if p)


@dataclass
class PdsPractice:
    ods_code: Optional[str]
    name: Optional[str]
    address: Optional[PdsAddress]
    telecoms: list[PdsTelecom] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> PdsPractice:
        address_data = data.get("address")
        return cls(
            ods_code=data.get("odsCode"),
            name=data.get("name"),
            address=PdsAddress.from_dict(address_data) if address_data else None,
            telecoms=[PdsTelecom.from_dict(t) for t in data.get("telecoms") or []],
        )


@dataclass
class PdsPatientDetailsResponse:
    nhs_number: str
    confidentiality_code: Optional[str]
    patient_details: Optional[PdsPatientDetails]
    practice: Optional[PdsPractice]
    superseded_nhs_number: bool
    local_identifier: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> PdsPatientDetailsResponse:
        pd_data = data.get("patientDetails")
        practice_data = data.get("practice")
        return cls(
            nhs_number=data.get("nhsNumber", ""),
            confidentiality_code=data.get("confidentialityCode"),
            patient_details=PdsPatientDetails.from_dict(pd_data) if pd_data else None,
            practice=PdsPractice.from_dict(practice_data) if practice_data else None,
            superseded_nhs_number=bool(data.get("supersededNhsNumber", False)),
            local_identifier=data.get("localIdentifier"),
        )
