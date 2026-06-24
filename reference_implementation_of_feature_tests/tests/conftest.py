"""Shared fixtures and test data for GP Connect Consumer Support Tests."""
import pytest


# ---------------------------------------------------------------------------
# EMIS Test Patients
# ---------------------------------------------------------------------------

EMIS_PATIENTS = {
    "liston_janine": {
        "nhs_number": "9730147140", "name": "Ms Janine Liston",
        "dob": "2011-01-24", "gender": "Female",
        "address": "3 COUNCIL HOUSES, LOW HESKET, CARLISLE, CA4 0HF",
        "notes": "Do not amend, main AR:S test patient",
    },
    "munyaradzi_naaif": {
        "nhs_number": "9730146896", "name": "Mr Naaif Munyaradzi",
        "dob": "1980-07-08", "gender": "Male",
        "address": "1 GLENWILLEY, GREAT CORBY, CARLISLE, CA4 8NF",
        "notes": "Do not amend",
    },
    "dai_ya_qiu": {
        "nhs_number": "9730333939", "name": "Mrs Ya Qiu Dai",
        "dob": "1998-02-24", "gender": "Female",
        "address": "BRAMPTON, SKIRWITH, PENRITH, CA10 1RB",
        "notes": "Do not amend",
    },
    "howitt_doreas": {
        "nhs_number": "9730333831", "name": "Ms Doreas Howitt",
        "dob": "1984-01-10", "gender": "Female",
        "address": "1 OLD LONDON ROAD, PENRITH, CUMBRIA, CA11 8JL",
        "notes": "Do not amend",
    },
    "gandy_stan": {
        "nhs_number": "9730147019", "name": "Mr Stan Gandy",
        "dob": "2016-06-12", "gender": "Male",
        "address": "2 STATION TERRACE, SHAP, PENRITH, CUMBRIA, CA10 3PX",
        "notes": "Do not amend",
    },
    "fennar_edina": {
        "nhs_number": "9730333874", "name": "Ms Edina Susan Fennar",
        "dob": "2003-01-20", "gender": "Female",
        "address": "10 WETHERIGGS LANE, PENRITH, CUMBRIA, CA11 8PD",
    },
    "brawn_annie": {
        "nhs_number": "9730333882", "name": "Mrs Annie Evelyn Brawn",
        "dob": "1994-05-06", "gender": "Female",
        "address": "MIDDLE SCEUGH FOOT, IVEGILL, CARLISLE, CA4 0NN",
    },
    "huxtable_dorothy": {
        "nhs_number": "9730333890", "name": "Mrs Dorothy Kristen Huxtable",
        "dob": "1993-12-11", "gender": "Female",
        "address": "GARTH MARR, CASTLE CARROCK, BRAMPTON, CUMBRIA, CA8 9NF",
    },
    "onion_dulcie": {
        "nhs_number": "9730333904", "name": "Ms Dulcie Onion",
        "dob": "1989-04-08", "gender": "Female",
        "address": "EAST COTTAGE, EASBY LANE END, BRAMPTON, CUMBRIA, CA8 2EZ",
    },
    "falvey_anita": {
        "nhs_number": "9730333912", "name": "Mrs Anita Falvey",
        "dob": "1989-01-24", "gender": "Female",
        "address": "2 THE LANE, GLASSONBY, PENRITH, CUMBRIA, CA10 1DS",
    },
    "ducie_ron": {
        "nhs_number": "9730333920", "name": "Mrs Ron Kimberlyn Ducie",
        "dob": "2004-11-24", "gender": "Female",
        "address": "ASKERTON CASTLE, ASKERTON, BRAMPTON, CA8 2BD",
    },
    "wharf_rhetta": {
        "nhs_number": "9730147078", "name": "Ms Rhetta Wharf",
        "dob": "2019-05-29", "gender": "Female",
        "address": "COANWOOD MANOR BROW KESWICK CUMBRIA CA12 4AW",
    },
    "heber_debra": {
        "nhs_number": "9730147116", "name": "Miss Debra Heber",
        "dob": "2023-07-29", "gender": "Female",
        "address": "10 MILLFIELD, BRAMPTON, CUMBRIA, CA8 1TT",
    },
    "cherupara_deviprasad": {
        "nhs_number": "9730146950", "name": "Mr Deviprasad Cherupara",
        "dob": "2000-12-30", "gender": "Male",
        "address": "STANLEY HOUSE, KIRKLINTON, CARLISLE, CA6 6DZ",
    },
    "boyce_archie": {
        "nhs_number": "9730146942", "name": "Mr Archie Boyce",
        "dob": "2015-06-12", "gender": "Male",
        "address": "21 HUNTLEY AVENUE, PENRITH, CUMBRIA, CA11 8NU",
    },
    "bold_mikala": {
        "nhs_number": "9730147035", "name": "Ms Mikala Grace Bold",
        "dob": "1928-01-01", "gender": "Female",
        "address": "BEECHWOOD, Park Lane, Alston, Cumbria, CA9 3AB",
    },
}

# Primary EMIS test patient for Access Record: Structured
EMIS_PRIMARY_PATIENT = EMIS_PATIENTS["liston_janine"]


# ---------------------------------------------------------------------------
# TPP Test Patients
# ---------------------------------------------------------------------------

TPP_PATIENTS = {
    "job_louise": {
        "nhs_number": "9692136744", "name": "Miss Louise Job",
        "dob": "2010-05-02", "gender": "Female",
        "address": "103 High Street, Belton, Doncaster DN9 1NR",
        "notes": "Do not amend, main AR:S test patient",
    },
    "skelly_horace": {
        "nhs_number": "9690937286", "name": "Mr Horace Skelly",
        "dob": "1925-04-21", "gender": "Male",
        "address": "3 BOWESFIELD CRESCENT, STOCKTON-ON-TEES, TS18 3BL",
        "given_name": "Horace",
        "family_name": "Skelly",
        "postcode": "TS18 3BL",
        "local_gender": "Female",
        "local_gp_ods_code": "B82617",
        "notes": "GEN-07 demographics comparison assurance patient",
    },
    "stale_pds_smith": {
        "family_name": "Smith",
        "notes": "GEN-06 dedicated stale-PDS search anchor; reserve for >24h no-refresh flow only and do not reuse in other tests",
    },
    "pds_trace_fail_9690938533": {
        "nhs_number": "9690938533", "name": "PDS Trace Fail 9690938533",
        "dob": "2000-09-09", "gender": "Unknown",
        "notes": "GEN-09 PDS trace fail scenario (cannot confirm registered practice)",
    },
    "pds_trace_fail_9690938541": {
        "nhs_number": "9690938541", "name": "PDS Trace Fail 9690938541",
        "dob": "1960-03-28", "gender": "Unknown",
        "notes": "GEN-09 PDS trace fail scenario (cannot confirm registered practice)",
    },
    "hitchcott_derryl": {
        "nhs_number": "9465693839", "name": "Mr Derryl Hitchcott",
        "dob": "1977-02-06", "gender": "Male",
        "address": "The House, 1 Northern Parade, Portsmouth PO2 9PF",
        "notes": "Do not amend",
    },
    "adams_sophia": {
        "nhs_number": "9692136701", "name": "Mrs Sophia Adams",
        "dob": "1986-10-13", "gender": "Female",
        "address": "2 Rectory Croft, High Street, Wroot, Doncaster DN9 2BF",
        "notes": "Do not amend",
    },
    "greenford_oliver": {
        "nhs_number": "5990275439", "name": "Oliver Greenford",
        "dob": "2020-11-08", "gender": "Male",
        "address": "22 West Green Drive, Crawley RH11 7DH",
        "notes": "Do not amend",
    },
    "nirmal_sumanna": {
        "nhs_number": "9465694819", "name": "Ms Sumanna Nirmal",
        "dob": "1997-01-29", "gender": "Female",
        "address": "1 Bentley Grove, Leeds LS6 4AT",
    },
    "cudmore_maleah": {
        "nhs_number": "9450038082", "name": "Ms Maleah Cudmore",
        "dob": "1991-04-11", "gender": "Female",
        "address": "21 West Green Drive, Crawley RH11 7DH",
    },
    "greenrod_corrine": {
        "nhs_number": "9450067899", "name": 'Ms Corrine Greenrod "Corrie"',
        "dob": "1997-01-01", "gender": "Female",
        "address": "22 West Green Drive, Crawley RH11 7DH",
    },
    "panganiban_bryana": {
        "nhs_number": "9465730793", "name": "Ms Bryana Panganiban",
        "dob": "2001-08-04", "gender": "Female",
        "address": "N/a, Thelwall Cottage, Little Redbourne, Gainsborough DN21 4QL",
    },
    "assadi_najeema": {
        "nhs_number": "9437702047", "name": "Ms Najeema Assadi",
        "dob": "2008-11-03", "gender": "Female",
        "address": "18 Broadway Avenue, Birmingham B9 5FD",
    },
    "daniel_arlene": {
        "nhs_number": "9692137996", "name": "Ms Arlene Daniel",
        "dob": "2019-01-24", "gender": "Female",
        "address": "10 Queen Elizabeth Way, Barton-upon-Humber, S Humberside DN18 6AJ",
    },
    "gavin_gorsedd": {
        "nhs_number": "9437702055", "name": "Mr Gorsedd Gavin",
        "dob": "2000-06-12", "gender": "Male",
        "address": "1 Bramble Dell, Birmingham B9 5FE",
    },
    "galli_wade": {
        "nhs_number": "9465736678", "name": "Mr Wade Galli",
        "dob": "2000-09-29", "gender": "Male",
        "address": "355 Ashby Road, Scunthorpe DN16 2RT",
    },
    "hitchcox_quanah": {
        "nhs_number": "9450076340", "name": "Mr Quanah Hitchcox",
        "dob": "2001-03-20", "gender": "Male",
        "address": "10 Howe Close, New Milton BH25 5LS",
    },
    "wynne_pete": {
        "nhs_number": "9692136728", "name": "Mr Pete Wynne",
        "dob": "2003-08-27", "gender": "Male",
        "address": "1A High Street, Crowle, Scunthorpe DN17 4LD",
    },
}

# Primary TPP test patient for Access Record: Structured
TPP_PRIMARY_PATIENT = TPP_PATIENTS["job_louise"]


# ---------------------------------------------------------------------------
# GP Connect API v1.5 Demonstrator (orange.testlab.nhs.uk)
# ---------------------------------------------------------------------------

GP_CONNECT_V15_ORGANISATION = {
    "ods_code": "B82617",
    "provider_asid": "918999198738",
    "organization_name": "Coxwold Surgery",
    "notes": "The ODS code and ASID of the GP practice represented by the GP Connect demonstrator v1.5",
}

GP_CONNECT_V15_PATIENTS = {
    "9690937278": {
        "id": 1, "nhs_number": "9690937278", "dob": "11-Dec-1938", "title": "Mr",
        "given_name": "Lucien", "family_name": "Samual", "gender": "Male", "notes": "",
    },
    "9690937286": {
        "id": 2, "nhs_number": "9690937286", "dob": "21-Apr-1925", "title": "Mr",
        "given_name": "Horace", "family_name": "Skelly", "gender": "Male", "notes": "",
    },
    "9690937294": {
        "id": 3, "nhs_number": "9690937294", "dob": "17-Mar-1936", "title": "Mr",
        "given_name": "Samuel", "family_name": "Heslby", "gender": "Male", "notes": "",
    },
    "9690937308": {
        "id": 4, "nhs_number": "9690937308", "dob": "04-Jul-1925", "title": "Mr",
        "given_name": "West", "family_name": "Crank", "gender": "Male", "notes": "",
    },
    "9690937375": {
        "id": 5, "nhs_number": "9690937375", "dob": "10-Mar-1928", "title": "Mrs",
        "given_name": "Rosa", "family_name": "Lobb", "gender": "Female", "notes": "",
    },
    "9690937383": {
        "id": 6, "nhs_number": "9690937383", "dob": "14-Jun-1953", "title": "Ms",
        "given_name": "Angela", "family_name": "Doulby", "gender": "Female", "notes": "",
    },
    "9690937391": {
        "id": 7, "nhs_number": "9690937391", "dob": "30-Jun-1953", "title": "Mrs",
        "given_name": "Mina", "family_name": "Bailey", "gender": "Female", "notes": "",
    },
    "9690937405": {
        "id": 8, "nhs_number": "9690937405", "dob": "20-Oct-1929", "title": "Mrs",
        "given_name": "Winnie", "family_name": "Pring", "gender": "Female", "notes": "",
    },
    "9690938533": {
        "id": 9, "nhs_number": "9690938533", "dob": "09-Sep-2000", "title": "Mrs",
        "given_name": "Anita", "family_name": "Clay", "gender": "Female", "notes": "Patient has S flag",
    },
    "9690938541": {
        "id": 10, "nhs_number": "9690938541", "dob": "28-Mar-1960", "title": "Ms",
        "given_name": "Tania", "family_name": "Reeves", "gender": "Female", "notes": "Patient has S flag",
    },
    "9690938622": {
        "id": 11, "nhs_number": "9690938622", "dob": "28-Nov-1978", "title": "Mrs",
        "given_name": "Alexi", "family_name": "Horn", "gender": "Female", "notes": "",
    },
    "9690938614": {
        "id": 12, "nhs_number": "9690938614", "dob": "17-Dec-1965", "title": "Miss",
        "given_name": "Elsa", "family_name": "Leary", "gender": "Female", "notes": "",
    },
    "9690938096": {
        "id": 13, "nhs_number": "9690938096", "dob": "16-Mar-2001", "title": "Ms",
        "given_name": "Cecile", "family_name": "Beston", "gender": "Female", "notes": "",
    },
    "9690938576": {
        "id": 15, "nhs_number": "9690938576", "dob": "16-Sep-1972", "title": "Mrs",
        "given_name": "Dora", "family_name": "McCain", "gender": "Female", "notes": "Patient has S flag",
    },
    "9690938118": {
        "id": 16, "nhs_number": "9690938118", "dob": "24-Nov-1983", "title": "Mrs",
        "given_name": "Sibyl", "family_name": "Craine", "gender": "Female", "notes": "",
    },
    "9690938126": {
        "id": 17, "nhs_number": "9690938126", "dob": "09-Jun-1984", "title": "Mrs",
        "given_name": "Doris", "family_name": "Bourke", "gender": "Female", "notes": "",
    },
    "9690938681": {
        "id": 18, "nhs_number": "9690938681", "dob": "03-Feb-1968", "title": "Mr",
        "given_name": "James", "family_name": "Rooney", "gender": "Male", "notes": "Patient deceased",
    },
    "9690938134": {
        "id": 20, "nhs_number": "9690938134", "dob": "06-Jul-1983", "title": "Ms",
        "given_name": "Lori", "family_name": "Gildea", "gender": "Female", "notes": "",
    },
    "9690938142": {
        "id": 21, "nhs_number": "9690938142", "dob": "13-Apr-1999", "title": "Miss",
        "given_name": "Eve", "family_name": "Buck", "gender": "Female", "notes": "Patient inactive",
    },
    "9690937316": {
        "id": 22, "nhs_number": "9690937316", "dob": "17-Sep-1950", "title": "Mr",
        "given_name": "Dean", "family_name": "Pye", "gender": "Male", "notes": "Access Record Structured - meds only",
    },
    "9690937324": {
        "id": 23, "nhs_number": "9690937324", "dob": "26-Nov-1927", "title": "Mr",
        "given_name": "Morris", "family_name": "Oakes", "gender": "Male", "notes": "Access Record Structured - meds only",
    },
    "9690937332": {
        "id": 24, "nhs_number": "9690937332", "dob": "12-Oct-1947", "title": "Mr",
        "given_name": "Samuel", "family_name": "Beyer", "gender": "Male", "notes": "Access Record Structured - allergies only",
    },
    "9690938207": {
        "id": 28, "nhs_number": "9690938207", "dob": "14-Jun-1972", "title": "Ms",
        "given_name": "Jenna", "family_name": "Gillon", "gender": "Female", "notes": "Access Record Structured - Rich Immunizations only",
    },
    "9690938215": {
        "id": 29, "nhs_number": "9690938215", "dob": "15-Dec-1964", "title": "Ms",
        "given_name": "Gina", "family_name": "WOOKEY", "gender": "Female", "notes": "Access Record Structured - Rich Uncategorised only",
    },
    "9690937367": {
        "id": 30, "nhs_number": "9690937367", "dob": "28-Aug-1946", "title": "Mr",
        "given_name": "lloyd", "family_name": "LEWIN", "gender": "Male", "notes": "Access Record Structured - Rich Investigations only",
    },
    "9690938223": {
        "id": 31, "nhs_number": "9690938223", "dob": "05-Jan-1978", "title": "Mrs",
        "given_name": "Susan", "family_name": "Grace", "gender": "Female", "notes": "Access Record Structured - Rich Consultations only",
    },
    "9690937340": {
        "id": 32, "nhs_number": "9690937340", "dob": "08-Jun-1947", "title": "Mr",
        "given_name": "Ray", "family_name": "MULLEN", "gender": "Male", "notes": "Access Record Structured - Rich Problems only",
    },
    "9690938088": {
        "id": 33, "nhs_number": "9690938088", "dob": "31-Jul-1955", "title": "Mr",
        "given_name": "Ivor", "family_name": "CAVE", "gender": "Male", "notes": "Access Record Structured - EMIS Docs consolidated",
    },
    "9690937693": {
        "id": 34, "nhs_number": "9690937693", "dob": "18-Dec-2014", "title": "Ms",
        "given_name": "Elaine", "family_name": "Day", "gender": "Female", "notes": "Access Record Structured - Rich Referrals only",
    },
    "9690938770": {
        "id": 35, "nhs_number": "9690938770", "dob": "30-Oct-1945", "title": "Mr",
        "given_name": "Josh", "family_name": "HYLAND", "gender": "Male", "notes": "Access Record Structured - Rich Diary Entries",
    },
}


# ---------------------------------------------------------------------------
# Medicus Test Patients
# ---------------------------------------------------------------------------

MEDICUS_ORGANISATION = {
    "name": "TBC",
    "ods_code": "N82090",
    "asid": "200000001865",
    "endpoint": "https://gpc-YGMYW-staging.medicus.thirdparty.nhs.uk/N82090/STU3/1/gpconnect/structured",
}

MEDICUS_PATIENTS = {
    "baggs_james": {
        "nhs_number": "9693646525", "name": "Mr James Baggs",
        "dob": "1971-07-09", "gender": "Male",
    },
    "sachsukh": {
        "nhs_number": "9465704954", "name": "Mrs Sachsukh",
        "dob": "1948-03-22", "gender": "Female",
    },
    "tower_katy": {
        "nhs_number": "9465704970", "name": "Mrs Katy Tower",
        "dob": "1985-09-09", "gender": "Female",
    },
    "garthside_liliana": {
        "nhs_number": "9465704997", "name": "Mrs Liliana Garthside",
        "dob": "1955-02-04", "gender": "Female",
    },
    "leedham_nigella": {
        "nhs_number": "9465705039", "name": "Mrs Nigella Leedham",
        "dob": "1953-11-18", "gender": "Female",
    },
    "hayley_lynda": {
        "nhs_number": "9726623545", "name": "Mrs Lynda Clare Hayley",
        "dob": "1995-11-07", "gender": "Female",
    },
    "smout_ivor": {
        "nhs_number": "9727400299", "name": "Mr Ivor Smout",
        "dob": "1943-03-07", "gender": "Male",
    },
    "conley_alison": {
        "nhs_number": "9726623588", "name": "Ms Alison Conley",
        "dob": "1983-07-21", "gender": "Female",
    },
    "wadham_basil": {
        "nhs_number": "9726905230", "name": "Mr Basil Wadham",
        "dob": "1999-03-14", "gender": "Male",
    },
}

# Invalid / special NHS numbers for error testing
INVALID_NHS_NUMBER = "9999999999"
INVALID_NHS_PATIENT = {
    "nhs_number": INVALID_NHS_NUMBER,
    "name": "unknown",
}

# Primary Medicus test patient
MEDICUS_PRIMARY_PATIENT = MEDICUS_PATIENTS["baggs_james"]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def emis_patients():
    """Return EMIS test patient data."""
    return EMIS_PATIENTS


@pytest.fixture(scope="session")
def tpp_patients():
    """Return TPP test patient data."""
    return TPP_PATIENTS


@pytest.fixture(scope="session")
def medicus_patients():
    """Return Medicus test patient data."""
    return MEDICUS_PATIENTS


@pytest.fixture(scope="session")
def medicus_organisation():
    """Return Medicus organisation data."""
    return MEDICUS_ORGANISATION


@pytest.fixture(scope="session")
def emis_primary_patient():
    """Return the primary EMIS test patient (Liston, Janine)."""
    return EMIS_PRIMARY_PATIENT


@pytest.fixture(scope="session")
def tpp_primary_patient():
    """Return the primary TPP test patient (Job, Louise)."""
    return TPP_PRIMARY_PATIENT


@pytest.fixture(scope="session")
def gp_connect_v15_patients():
    """Return all GP Connect API v1.5 demonstrator patient rows from orange.testlab."""
    return GP_CONNECT_V15_PATIENTS


@pytest.fixture(scope="session")
def gp_connect_v15_organisation():
    """Return GP Connect API v1.5 demonstrator organisation row from orange.testlab."""
    return GP_CONNECT_V15_ORGANISATION


@pytest.fixture(scope="session")
def gp_connect_v15_patient_by_nhs_number(gp_connect_v15_patients):
    """Return a lookup helper for GP Connect API v1.5 patient rows by NHS number."""

    def _lookup(nhs_number):
        patient = gp_connect_v15_patients.get(str(nhs_number))
        if not patient:
            raise KeyError(f"No GP Connect API v1.5 patient data found for NHS number: {nhs_number}")
        return patient

    return _lookup


@pytest.fixture(scope="session")
def medicus_primary_patient():
    """Return the primary Medicus test patient (Baggs, James)."""
    return MEDICUS_PRIMARY_PATIENT


@pytest.fixture(scope="session")
def invalid_nhs_patient():
    """Return the invalid NHS-number patient anchor used for GEN-11 searches."""
    return INVALID_NHS_PATIENT
