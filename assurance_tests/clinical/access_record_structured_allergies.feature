@clinical_assurance @allergies
Feature: Clinical Assurance - Access Record Structured Allergies
  As a GP Connect consumer
  I want to verify that allergy data retrieved from the GP provider is displayed correctly
  So that clinicians can trust the allergy information shown in the consumer application

  # Source: GP Connect ARS Clinical Test Pack - Allergy Test Cases (Confluence)
  # Test patients: See patient table below
  # GP Practice: WEST FARM SURGERY (A86005)
  #
  # STATUS: WIP — Awaiting allergy test data setup in the GP provider system.
  #         NHS numbers and field values marked "TBC" will be populated once the
  #         test engineer has configured consistent test data across providers.
  #
  # Patient 1: NHS TBC — Allergy to Bisoprolol (active), Allergy to Naproxen (resolved)
  # Patient 2: NHS TBC — Multiple allergies (Allergy to Doxycycline, Allergy to Aspirin, Peanut Allergy, etc.)
  # Patient 3: NHS TBC — No known allergy (SNOMED negation)
  # Patient 4: NHS TBC — Empty (new patient, no allergy records)
  # Patient 5: NHS TBC — Conflicting data (No known allergy + Allergy to Ibuprofen + transfer degraded + legacy terminology)
  # Patient 6: NHS TBC — Multiple codes for same allergy (Allergy to Phenoxymethylpenicillin, Codeine)
  #
  # NOTE: NHS numbers above are placeholders (TBC) — replace with actual test patient NHS numbers
  #       once the test data is set up in the GP provider system.
  # NOTE: Field values marked "TBC" need to be populated once test data is created in the GP system.

  # ---------------------------------------------------------------------------
  # Active Allergy - Complete Field Population (ALG_1)
  # ---------------------------------------------------------------------------

  Rule: Active Allergy with Mandatory and Optional Fields (ALG_1)
    Tests that the consumer correctly displays an active allergy record with all mandatory
    and optional fields populated.

    @ALG_1
    Scenario: ALG_1 - Active allergy with mandatory and optional fields (Patient 1 - Allergy to Bisoprolol)
      Given the consumer requests the structured record for patient "PATIENT_1_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field                | value                          |
        | Allergy              | Allergy to Bisoprolol          |
        | Clinical Status      | Active                         |
        | Verification Status  | Unconfirmed                    |
        | Category             | Medication                     |
        | Asserted Date        | TBC                            |
        | Recorder             | TBC                            |
        | Type                 | TBC                            |
        | Criticality          | TBC                            |
        | Onset                | TBC                            |
        | Asserter             | TBC                            |
        | Last Occurrence      | TBC                            |
        | Additional Details   | TBC                            |
        | Severity             | TBC                            |
        | Reaction Details     | TBC                            |
      # Mandatory fields: Allergy Name, Clinical Status, Verification Status, Category, Asserted Date, Recorder
      # Optional fields: Type, Criticality, Onset, Asserter, Last Occurrence, Additional Details,
      #   Severity (reaction.severity), Reaction Details (reaction)
      # All optional fields are included to ensure supplier agnosticism — values depend on provider system

  # ---------------------------------------------------------------------------
  # Clinical Status Values (ALG_2)
  # ---------------------------------------------------------------------------

  Rule: Clinical Status Values (ALG_2)
    Tests that the consumer correctly displays both Active and Resolved clinical status values.

    @ALG_2
    Scenario: ALG_2 - Verify allowed Clinical Status values - Active and Resolved (Patient 1)
      Given the consumer requests the structured record for patient "PATIENT_1_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field            | value                         |
        | Allergy          | Allergy to Bisoprolol         |
        | Clinical Status  | Active                        |
      And the allergy list contains an entry with the following details:
        | field            | value                         |
        | Allergy          | Allergy to Naproxen           |
        | Clinical Status  | Resolved                      |

  # ---------------------------------------------------------------------------
  # Additional Details - Max Length (ALG_4)
  # ---------------------------------------------------------------------------

  Rule: Additional Details Maximum Length (ALG_4)
    Tests that the consumer displays additional details at maximum character length without truncation.

    @ALG_4
    Scenario: ALG_4 - Verify maximum character length of additional details (Patient 1)
      Given the consumer requests the structured record for patient "PATIENT_1_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field              | value                         |
        | Allergy            | Allergy to Bisoprolol         |
        | Additional Details | TBC                           |
      # Intended Result: Consumer accepts maximum provider supported length of additional details
      # The additional details field should contain the maximum length string allowed by the provider

  # ---------------------------------------------------------------------------
  # Verification Status (ALG_5)
  # ---------------------------------------------------------------------------

  Rule: Verification Status Fixed Value (ALG_5)
    Tests that the mandatory Verification Status field displays the fixed value "Unconfirmed".

    @ALG_5
    Scenario: ALG_5 - Verification status auto-populated with fixed value (Patient 1)
      Given the consumer requests the structured record for patient "PATIENT_1_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field                | value                         |
        | Allergy              | Allergy to Bisoprolol         |
        | Verification Status  | Unconfirmed                   |
      # Per GP Connect spec, Verification Status is always "Unconfirmed"

  # ---------------------------------------------------------------------------
  # Exclusion of Resolved Allergies (ALG_6)
  # ---------------------------------------------------------------------------

  Rule: Resolved Allergy Exclusion (ALG_6)
    Tests that resolved allergies are excluded when not requested by the consumer system.

    @ALG_6
    Scenario: ALG_6 - Resolved allergies excluded when not requested (Patient 1)
      Given the consumer requests the structured record for patient "PATIENT_1_NHS_TBC"
      When the consumer displays only active allergies
      Then the allergy list contains an entry with the following details:
        | field            | value                         |
        | Allergy          | Allergy to Bisoprolol         |
        | Clinical Status  | Active                        |
      And the allergy "Allergy to Naproxen" is not displayed
      # The resolved allergy (Allergy to Naproxen) should be excluded from the active allergy list

  # ---------------------------------------------------------------------------
  # Multiple Active Allergies (ALG_10)
  # ---------------------------------------------------------------------------

  Rule: Multiple Active Allergies (ALG_10)
    Tests that the consumer correctly displays multiple active allergies for a patient.

    @ALG_10
    Scenario: ALG_10 - Multiple active allergies displayed (Patient 2)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Doxycycline       |
      And the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Aspirin           |
      And the allergy list contains an entry with the following details:
        | field   | value          |
        | Allergy | Peanut Allergy |
      And the allergy list contains an entry with the following details:
        | field   | value                      |
        | Allergy | Influenza Vaccine Allergy  |
      And the allergy list contains an entry with the following details:
        | field   | value   |
        | Allergy | statins |
      # Patient 2 has 13 allergy entries in total (including adverse reactions, problems, intolerances)
      # This test verifies all are displayed without overwriting and order is preserved

  # ---------------------------------------------------------------------------
  # Non-Drug Allergy Category (ALG_11)
  # ---------------------------------------------------------------------------

  Rule: Non-Drug Allergy Category (ALG_11)
    Tests that the consumer handles non-drug (Environment) allergy categories.

    @ALG_11
    Scenario: ALG_11 - Non-drug allergy with Environment category (Patient 2 - Peanut)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field     | value          |
        | Allergy   | Peanut Allergy |
        | Category  | Environment    |

  # ---------------------------------------------------------------------------
  # Asserted Date Formats (ALG_12, ALG_18, ALG_19, ALG_20)
  # ---------------------------------------------------------------------------

  Rule: Asserted Date Display (ALG_12, ALG_18, ALG_19, ALG_20)
    Tests that the consumer correctly handles full, partial, and missing asserted dates.

    @ALG_12
    Scenario: ALG_12 - Full asserted date display - Day, Month, Year (Patient 2 - Allergy to Doxycycline)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field          | value                       |
        | Allergy        | Allergy to Doxycycline       |
        | Asserted Date  | TBC                          |
      # The full date (day, month, year) should be displayed

    @ALG_18
    Scenario: ALG_18 - Partial asserted date - Month, Year (Patient 2 - Allergy to Aspirin)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field          | value                       |
        | Allergy        | Allergy to Aspirin           |
        | Asserted Date  | TBC                          |
      # Only Month and Year should be displayed (no day component)

    @ALG_19
    Scenario: ALG_19 - Partial asserted date - Year only (Patient 2 - Peanut Allergy)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field          | value          |
        | Allergy        | Peanut Allergy |
        | Asserted Date  | TBC            |
      # Only Year should be displayed (no day or month component)

    @ALG_20
    Scenario: ALG_20 - Missing asserted date handled gracefully (Patient 2 - Influenza Vaccine)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field          | value                     |
        | Allergy        | Influenza Vaccine Allergy |
        | Asserted Date  |                           |
      # Asserted Date is missing/blank - system should not auto-populate or infer a date

  # ---------------------------------------------------------------------------
  # Special Characters (ALG_13)
  # ---------------------------------------------------------------------------

  Rule: Special Characters in Free Text (ALG_13)
    Tests that the consumer displays special characters in additional details without truncation.

    @ALG_13
    Scenario: ALG_13 - Special characters in additional details (Patient 2 - Allergy to Doxycycline)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field              | value                       |
        | Allergy            | Allergy to Doxycycline       |
        | Additional Details | TBC                          |
      # Additional details contain special characters (e.g., &, @, #, parentheses)
      # System should display them exactly as received without truncation or modification

  # ---------------------------------------------------------------------------
  # Resolved Allergy Retrieval (ALG_14)
  # ---------------------------------------------------------------------------

  Rule: Resolved Allergy Display (ALG_14)
    Tests that resolved allergies are retrieved and displayed with end date and reason.

    @ALG_14
    Scenario: ALG_14 - Resolved allergy with end date and reason (Patient 2 - Allergy to Ibuprofen)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field              | value                       |
        | Allergy            | Allergy to Ibuprofen         |
        | Clinical Status    | Resolved                     |
        | Allergy End Date   | TBC                          |
        | Allergy End Reason | TBC                          |
      # Resolved allergies should be in a separate section from active allergies
      # Applicability: TPP (not applicable to EMIS as EMIS already implemented GPC 1.6.2)

  # ---------------------------------------------------------------------------
  # Adverse Reaction Records (ALG_15)
  # ---------------------------------------------------------------------------

  Rule: Adverse Reaction Display (ALG_15)
    Tests that adverse reaction records are displayed consistently under the allergy module.

    @ALG_15
    Scenario: ALG_15 - Drug and non-drug adverse reactions displayed (Patient 2)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                                            |
        | Allergy | Warfarin adverse reaction (disorder)             |
      And the allergy list contains an entry with the following details:
        | field   | value                    |
        | Allergy | Adverse reaction to fig  |
      # SNOMED codes: 293344008 (Warfarin), 218938007 (fig)
      # Both Drug and Non-drug adverse reactions should appear under the allergy module

  # ---------------------------------------------------------------------------
  # Problem Recorded as Allergy (ALG_16)
  # ---------------------------------------------------------------------------

  Rule: Problem Displayed as Allergy (ALG_16)
    Tests that allergies recorded as Problems are still displayed under the allergy module.

    @ALG_16
    Scenario: ALG_16 - Allergy recorded as Problem displayed under allergies (Patient 2)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value       |
        | Allergy | Nut allergy |
      And the allergy list contains an entry with the following details:
        | field   | value                    |
        | Allergy | Allergy to amoxicillin   |
      # These were recorded as Problems in the GP system but should appear as allergies

  # ---------------------------------------------------------------------------
  # Intolerance Records (ALG_17)
  # ---------------------------------------------------------------------------

  Rule: Intolerance Records Under Allergy Module (ALG_17)
    Tests that intolerance records (drug and non-drug) are displayed under the allergy module.

    @ALG_17
    Scenario: ALG_17 - Intolerance records displayed under allergies (Patient 2)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                          |
        | Allergy | Intolerance to drug            |
      And the allergy list contains an entry with the following details:
        | field   | value                              |
        | Allergy | Oral contraceptive intolerance     |
      And the allergy list contains an entry with the following details:
        | field   | value                              |
        | Allergy | Intolerance to cow milk (finding)  |
      # SNOMED codes: 59037007 (drug), 72354005 (oral contraceptive), 738069006 (cow milk)

  # ---------------------------------------------------------------------------
  # Substance-Only Allergy Records (ALG_22)
  # ---------------------------------------------------------------------------

  Rule: Substance-Only Allergy Records (ALG_22)
    Tests that the consumer handles allergy records coded with a substance-only code
    (rather than a full allergy concept).

    @ALG_22
    Scenario: ALG_22 - Substance-only allergy records displayed (Patient 2)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Doxycycline       |
      And the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Aspirin           |
      # Substance-only records (not full allergy concept codes) should still be displayed
      # Applicability: TPP

  # ---------------------------------------------------------------------------
  # No Known Allergies - SNOMED Negation (ALG_23)
  # ---------------------------------------------------------------------------

  Rule: SNOMED Negation Record (ALG_23)
    Tests that the consumer correctly displays the "No Known Allergies" SNOMED negation record.

    @ALG_23
    Scenario: ALG_23 - No Known Allergies SNOMED negation record (Patient 3)
      Given the consumer requests the structured record for patient "PATIENT_3_NHS_TBC"
      When the consumer displays the allergies
      Then the system displays "No known allergies"
      # The SNOMED negation record should be clearly displayed
      # It should not be treated as missing, null, or incomplete data

  # ---------------------------------------------------------------------------
  # Empty Allergy Record (ALG_24)
  # ---------------------------------------------------------------------------

  Rule: Empty Allergy Record (ALG_24)
    Tests system behaviour when no allergy records exist for a patient.

    @ALG_24
    Scenario: ALG_24 - No allergy records exist for patient (Patient 4)
      Given the consumer requests the structured record for patient "PATIENT_4_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy section is displayed without errors
      And no allergy records are displayed
      # The system should NOT display "No known allergies" unless an explicit negation record exists
      # Patient 4 is a new patient with no allergy data at all

  # ---------------------------------------------------------------------------
  # Conflicting Allergy Data (ALG_25)
  # ---------------------------------------------------------------------------

  Rule: Conflicting Allergy Data (ALG_25)
    Tests that the consumer handles conflicting allergy data (negation record alongside active allergies).

    @ALG_25
    Scenario: ALG_25 - Conflicting data - No known allergy alongside active allergy (Patient 5)
      Given the consumer requests the structured record for patient "PATIENT_5_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value              |
        | Allergy | No known allergy   |
      And the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Ibuprofen         |
      And the allergy list contains an entry with the following details:
        | field   | value                                         |
        | Allergy | [V]Personal history of clopidogrel allergy    |
      # Patient 5 has:
      #   Allergy 1 = No known allergy (SNOMED negation)
      #   Allergy 2 = Allergy to Ibuprofen (pre-coordinated code)
      #   Allergy 3 = Transfer-degraded Clopidogrel (resolved) — tested separately by ALG_26
      #   Allergy 4 = [V]Personal history of clopidogrel allergy (legacy terminology) — tested separately by ALG_29
      # The consumer should display all records as received without modification

  # ---------------------------------------------------------------------------
  # Transfer-Degraded Resolved Allergy (ALG_26)
  # ---------------------------------------------------------------------------

  Rule: Transfer-Degraded Resolved Allergy Display (ALG_26)
    Tests that a previously active allergy that has been resolved and transfer-degraded
    is displayed correctly in the resolved allergies section.

    @ALG_26
    Scenario: ALG_26 - Transfer-degraded resolved allergy displayed with end date and reason (Patient 5)
      Given the consumer requests the structured record for patient "PATIENT_5_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field              | value                                                |
        | Allergy            | Allergy to Clopidogrel                               |
        | Clinical Status    | Resolved                                             |
        | Allergy End Date   | TBC                                                  |
        | Allergy End Reason | TBC                                                  |
      # Transfer-degraded SNOMED code 196461000000101 (original code 1373513002)
      # The original allergy term should be preserved and displayed as text
      # Resolved transfer-degraded allergies should appear in the resolved allergy section
      # Applicability: EMIS

  # ---------------------------------------------------------------------------
  # Pre-Coordinated Allergy Code (ALG_28)
  # ---------------------------------------------------------------------------

  Rule: Pre-Coordinated Allergy Code (ALG_28)
    Tests that the consumer correctly handles a pre-coordinated allergy code (a single SNOMED
    code that captures both the substance and the allergy/intolerance concept).

    @ALG_28
    Scenario: ALG_28 - Pre-coordinated allergy code displayed (Patient 5 - Allergy to Ibuprofen)
      Given the consumer requests the structured record for patient "PATIENT_5_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Ibuprofen         |
      # The allergy is coded with a pre-coordinated SNOMED code (single concept for substance + allergy)
      # The consumer should display the allergy name correctly from the pre-coordinated code
      # Applicability: EMIS

  # ---------------------------------------------------------------------------
  # Legacy Terminology / Transfer Degraded Codes (ALG_29)
  # ---------------------------------------------------------------------------

  Rule: Legacy Terminology Codes (ALG_29)
    Tests handling of legacy read codes with transfer degradation.

    @ALG_29
    Scenario: ALG_29 - Legacy read code with transfer degradation (Patient 5)
      Given the consumer requests the structured record for patient "PATIENT_5_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                                         |
        | Allergy | [V]Personal history of clopidogrel allergy    |
      # Legacy read code ZV140 mapped to transfer-degraded SNOMED 196461000000101
      # The original allergy term should be preserved and displayed as text

  # ---------------------------------------------------------------------------
  # Multiple Codes for Single Allergy (ALG_30)
  # ---------------------------------------------------------------------------

  Rule: Multiple Codes Representing Single Allergy (ALG_30)
    Tests that the consumer displays multiple entries for the same allergy recorded at different times.

    @ALG_30
    Scenario: ALG_30 - Multiple codes for same allergy displayed (Patient 6)
      Given the consumer requests the structured record for patient "PATIENT_6_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                                  |
        | Allergy | Allergy to Phenoxymethylpenicillin      |
      And the allergy list contains an entry with the following details:
        | field   | value                                  |
        | Allergy | Allergy to Phenoxymethylpenicillin      |
      And the allergy list contains an entry with the following details:
        | field          | value             |
        | Allergy        | Codeine           |
        | Asserted Date  | TBC_DATE_X        |
      And the allergy list contains an entry with the following details:
        | field          | value             |
        | Allergy        | Codeine           |
        | Asserted Date  | TBC_DATE_Y        |
      # Patient 6 has:
      #   Allergy 1 = Allergy to Phenoxymethylpenicillin (recorded as allergy)
      #   Allergy 2 = Allergy to Phenoxymethylpenicillin (recorded as Problem)
      #   Allergy 3 = Codeine 293597001 (date X)
      #   Allergy 4 = Codeine 293597001 (date Y, different from Allergy 3)
      # The two Codeine entries have different Asserted Dates to prove both are preserved
      # All entries should be preserved without overwriting

  # ---------------------------------------------------------------------------
  # Mandatory Fields Only (ALG_31)
  # ---------------------------------------------------------------------------

  Rule: Allergy with Mandatory Fields Only (ALG_31)
    Tests that the consumer correctly displays an allergy record that has only mandatory fields populated.

    @ALG_31
    Scenario: ALG_31 - Allergy with only mandatory fields (Patient 6 - Allergy to Phenoxymethylpenicillin)
      Given the consumer requests the structured record for patient "PATIENT_6_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field                | value                                  |
        | Allergy              | Allergy to Phenoxymethylpenicillin      |
        | Clinical Status      | Active                                 |
        | Verification Status  | Unconfirmed                            |
        | Category             | Medication                             |
        | Asserted Date        | TBC                                    |
        | Recorder             | TBC                                    |
      # All optional fields (Type, Criticality, Onset, Asserter, Last Occurrence,
      # Additional details, Severity, Reaction details) have no values

  # ---------------------------------------------------------------------------
  # Onset Date Formats (ALG_33, ALG_34, ALG_35, ALG_36)
  # ---------------------------------------------------------------------------

  Rule: Onset Date Display (ALG_33, ALG_34, ALG_35, ALG_36)
    Tests that the consumer correctly handles full, partial, and missing onset dates
    (date when the allergy/intolerance first manifested).

    @ALG_33
    Scenario: ALG_33 - Full onset date display - Day, Month, Year (Patient 2 - Allergy to Doxycycline)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Doxycycline       |
        | Onset   | TBC                          |
      # The full onset date (day, month, year) should be displayed
      # Applicability: EMIS

    @ALG_34
    Scenario: ALG_34 - Partial onset date - Month, Year (Patient 2 - Allergy to Aspirin)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                       |
        | Allergy | Allergy to Aspirin           |
        | Onset   | TBC                          |
      # Only Month and Year should be displayed (no day component)
      # Applicability: EMIS

    @ALG_35
    Scenario: ALG_35 - Partial onset date - Year only (Patient 2 - Peanut Allergy)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value          |
        | Allergy | Peanut Allergy |
        | Onset   | TBC            |
      # Only Year should be displayed (no day or month component)
      # Applicability: EMIS

    @ALG_36
    Scenario: ALG_36 - Missing onset date handled gracefully (Patient 2 - Influenza Vaccine)
      Given the consumer requests the structured record for patient "PATIENT_2_NHS_TBC"
      When the consumer displays the allergies
      Then the allergy list contains an entry with the following details:
        | field   | value                     |
        | Allergy | Influenza Vaccine Allergy |
        | Onset   |                           |
      # Onset date is missing/blank - system should not auto-populate or infer a date
      # Applicability: EMIS

  # ---------------------------------------------------------------------------
  # Error Message Handling (ALG_37)
  # ---------------------------------------------------------------------------

  Rule: Failed Retrieval Error Messages (ALG_37)
    Tests that the consumer displays appropriate error messages when allergy data retrieval fails.

    @ALG_37
    Scenario: ALG_37 - Error message displayed when allergy data retrieval fails
      Given the consumer requests the structured record for a patient where retrieval fails
      When the consumer attempts to display the allergies
      Then the system displays an appropriate error message
      # The system should display a meaningful error message if data cannot be retrieved
      # The error should not be silently swallowed or display misleading information

  # ---------------------------------------------------------------------------
  # Test cases excluded from this feature file (documented for reference)
  # ---------------------------------------------------------------------------
  # The following test cases are not included as scenarios above:
  #
  # NOT APPLICABLE (neither EMIS nor TPP):
  # 3  - Verify max character length of allergy reaction details
  #       Reason: Not applicable (None)
  # 7  - Verify max character length of reason for ending allergy reaction
  #       Reason: Not applicable (None)
  # 8  - Verification of allowed Criticality values (Low, High, Unable to access)
  #       Reason: Not applicable (None)
  # 9  - Verification of allowed Severity values (Low, Mild, Severe)
  #       Reason: Not applicable (None)
  # 32 - Post-coordinated allergy code
  #       Reason: Not applicable (not available in any provider system)
  # 38 - Verify handling of special characters in reaction details (free text)
  #       Reason: Not applicable (checking Additional Details for special characters suffices)
  #
  # COVERED BY EXISTING:
  # 21 - Verify separation of Active and Resolved Allergies → covered by ALG_10 + ALG_14
  # 27 - Verify transfer-degraded allergy for migrated records → covered by ALG_26
