@clinical_assurance @medications
Feature: Clinical Assurance - Access Record Structured Medications
  As a GP Connect consumer
  I want to verify that medication data retrieved from the GP provider is displayed correctly
  So that clinicians can trust the medication information shown in the consumer application

  # Source: GP Connect ARS Clinical Test Pack v1.8
  # Test patient: Louise Job | 9692136744 | Born 02/05/2010
  # GP Practice: WEST FARM SURGERY (A86005)
  # Note: Display warning "Items excluded due to confidentiality and/or patient preferences"
  #       should be shown when item 2.12 is marked as private (ListWarningCode-1 confidential-items)

  # ---------------------------------------------------------------------------
  # Acute Medications (AC_TC01)
  # ---------------------------------------------------------------------------

  Rule: Acute Medications (AC_TC01)
    Tests that the consumer correctly displays acute medication data from the GP record.

    @AC_TC01_1.1
    Scenario: AC_TC01_1.1 - Acute - Delayed prescribing - Prescribed at GP practice - Future dated
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                              |
        | Medication          | Gentamicin 0.3% ear/eye drops                                                                      |
        | Dosage Instructions | Apply One Drop To The Affected Eye(s) Every Two Hours Reducing Frequency As Infection Is Controlled |
        | Quantity            | 10 ml                                                                                              |
        | Patient Notes       | Script note when prescribing an acute medication                                                   |
        | Issued Date         | 15-Apr-2026                                                                                        |
        | Prescriber          | Harvey Sembhytwo                                                                                   |

    @AC_TC01_1.2
    Scenario: AC_TC01_1.2 - Acute - Prescribed at GP practice - very old medication re-prescribed (2 entries)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                              |
        | Medication          | Arsenic 10mg/10ml solution for infusion ampoules   |
        | Dosage Instructions | use as directed                                    |
        | Quantity            | 10 ampoule                                         |
        | Prescriber Notes    | {Batch Number} {Pack Size}                         |
        | Issued Date         | 18-Mar-2026                                        |
        | Prescriber          | Harvey Sembhytwo                                   |
      And the medication list contains an entry with the following details:
        | field               | value                                                                    |
        | Medication          | Arsenic 10mg/10ml solution for infusion ampoules (Prescribed by a Hospital) |
        | Dosage Instructions | use as directed                                                          |
        | Quantity            | 10 ampoule                                                               |
        | Prescriber Notes    | {Batch Number} {Pack Size}                                               |
        | Issued Date         | 01-Feb-2026                                                              |
        | Prescriber          | Harvey Sembhytwo                                                         |
      # Intended Result: System shows the two items with correct drug, dose and quantity.
      # Displays dates correctly and classifies one as hospital prescription.

    @AC_TC01_1.3
    Scenario: AC_TC01_1.3 - Acute - Prescribed at GP practice
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                    |
        | Medication          | Donepezil 5mg tablets    |
        | Dosage Instructions | One To Be Taken At Night |
        | Quantity            | 1 tablet                 |
        | Prescriber Notes    | Pharmacy                 |
        | Patient Notes       | Patient                  |
        | Issued Date         | 24-Mar-2026              |
        | Prescriber          | Harvey Sembhytwo         |

    @AC_TC01_1.4
    Scenario: AC_TC01_1.4 - Acute - Prescribed at GP practice - long dose max character limit
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                                                                                                                                                                                             |
        | Medication          | Amoxicillin 500mg capsules                                                                                                                                                                                                                                        |
        | Dosage Instructions | This is a very long dosage instructions This is a very long dosage instructions This is a very long dosage instructions This is a very long dosage instructions This is a very long dosage instructions This is a very long dosage instructions This is a v END |
        | Quantity            | 100 capsule                                                                                                                                                                                                                                                       |
        | Issued Date         | 18-Mar-2026                                                                                                                                                                                                                                                       |
        | Prescriber          | Harvey Sembhytwo                                                                                                                                                                                                                                                  |
      # Intended Result: System should display the dose instructions as per the text above,
      # including the word 'END'. Max 255 characters.

    @AC_TC01_1.5
    Scenario: AC_TC01_1.5 - Acute - Prescribed at GP practice - long drug name (auto-added Prescriber Notes text)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                                                                                                                           |
        | Medication          | Comirnaty JN.1 COVID-19 mRNA Vaccine 30micrograms/0.3ml dose dispersion for injection pre-filled syringes (Pfizer Ltd)                                                                          |
        | Dosage Instructions | 1 dose via intramuscular injection                                                                                                                                                              |
        | Quantity            | 18 syringe                                                                                                                                                                                      |
        | Prescriber Notes    | {Batch Number} {Pack Size} PFIZER LTD                                                                                                                                                           |
        | Issued Date         | 18-Mar-2026                                                                                                                                                                                     |
        | Prescriber          | Harvey Sembhytwo                                                                                                                                                                                |
      # Intended Result: System displays the full name without truncation. NB this item is discontinued.

    @AC_TC01_1.6
    Scenario: AC_TC01_1.6 - Acute - Prescribed at GP practice - special characters
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                              |
        | Medication          | Ibuprofen 5% gel                                                   |
        | Dosage Instructions | Dosage with special characters: !"%&*()+-=;',./:<>?                |
        | Quantity            | 50 gram                                                            |
        | Prescriber Notes    | Administrative notes with special characters:!@£$%^&*()_+-={}[]:"\|;'\\<>?,./~` |
        | Patient Notes       | Script notes with special characters:!@£$%^&*()_+-={}[]:"\|;'\\<>?,./~`         |
        | Issued Date         | 18-Mar-2026                                                        |
        | Prescriber          | Harvey Sembhytwo                                                   |
      # Intended Result: System displays all the information above, special characters are not excluded.

    @AC_TC01_1.7
    Scenario: AC_TC01_1.7 - Acute - Prescribed at GP practice - long dosage patient instructions, max char limit
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                                                                                                                                                                                                        |
        | Medication          | E45 cream (Karo Healthcare UK Ltd)                                                                                                                                                                                                                                           |
        | Dosage Instructions | Apply When Required                                                                                                                                                                                                                                                          |
        | Quantity            | 50 gram                                                                                                                                                                                                                                                                      |
        | Additional Notes    | This is very long script note and patient dosage instructions This is very long script note and patient dosage instructions This is very long script note and patient dosage instructions This is very long script note and patient dosage instruction END                   |
        | Patient Notes       | This is very long script note and patient dosage instructions This is very long script note and patient dosage instructions This is very long script note and patient dosage instructions This is very long script note and patient dosage instruction END                   |
        | Issued Date         | 18-Mar-2026                                                                                                                                                                                                                                                                  |
        | Prescriber          | Harvey Sembhytwo                                                                                                                                                                                                                                                             |
      # Intended Result: System does not truncate the two sets of notes (250 chars each).

    @AC_TC01_1.8
    Scenario: AC_TC01_1.8 - Acute - Prescribed at GP practice - Transfer degraded medication free text item
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                       |
        | Medication          | Aciclovir 400mg dispersible tablets (Alliance Healthcare (Distribution) Ltd) (Transfer-degraded medication entry) |
        | Dosage Instructions | Two tablets five times a day                                                                |
        | Quantity            | 70 tablet                                                                                   |
        | Issued Date         | 20-Mar-2026                                                                                 |
        | Prescriber          | Harvey Sembhytwo                                                                            |

    @AC_TC01_1.9
    Scenario: AC_TC01_1.9 - Acute CD - Prescribed at GP practice - no notes
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                    |
        | Medication          | Fentanyl 1.2mg lozenges  |
        | Dosage Instructions | use as directed          |
        | Quantity            | 30 lozenge               |
        | Issued Date         | 24-Mar-2026              |
        | Prescriber          | Harvey Sembhytwo         |
      # Intended Result: System displays only the information provided - no notes in either field.
      # NB this is a Controlled Drug (CD).

    @AC_TC01_1.10
    Scenario: AC_TC01_1.10 - Acute - Prescribed at GP practice - long medication name
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                                                                                                                                  |
        | Medication          | Rebif 22micrograms/0.5ml (6million units) solution for injection pre-filled syringes and Rebif 8.8micrograms/0.2ml (2.4million units) solution for injection pre-filled syringes (Merck Serono Ltd)     |
        | Dosage Instructions | inject one 3 times a week                                                                                                                                                                              |
        | Quantity            | 12 pre-filled disposable injection                                                                                                                                                                     |
        | Prescriber Notes    | {Batch Number - 93862} {Pack Size - 12} MERCK SERONO                                                                                                                                                   |
        | Issued Date         | 25-Mar-2026                                                                                                                                                                                            |
        | Prescriber          | Harvey Sembhytwo                                                                                                                                                                                       |
      # Intended Result: System displays the full medication name, no truncation.

    @AC_TC01_1.11
    Scenario: AC_TC01_1.11 - Acute - Delayed prescribing - Prescribed at GP practice - backdated approx 15 months ago (465 days)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                       |
        | Medication          | Warfarin 3mg tablets                        |
        | Dosage Instructions | use as directed                             |
        | Quantity            | 28 tablet                                   |
        | Patient Notes       | backdated acute medication approx 15 months |
        | Issued Date         | 15-Dec-2024                                 |
        | Prescriber          | Harvey Sembhytwo                            |

    @AC_TC01_1.12
    Scenario: AC_TC01_1.12 - Acute - Delayed prescribing - Prescribed at GP practice - backdated more than 16 months ago (505 days)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication list contains an entry with the following details:
        | field               | value                                              |
        | Medication          | Warfarin 5mg tablets                               |
        | Dosage Instructions | use as directed                                    |
        | Quantity            | 28 tablet                                          |
        | Patient Notes       | backdated acute medication more than 15 months     |
        | Issued Date         | 17-Dec-2024                                        |
        | Prescriber          | Harvey Sembhytwo                                   |

    @AC_TC01_1.13
    Scenario: AC_TC01_1.13 - Acute - non NHS marked as private
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the acute medications
      Then the medication marked as private is not displayed
      And the system displays a warning indicating items have been excluded due to confidentiality
      # Medication: Temazepam 10mg tablets | Dose: take one at night | Quantity: 28 tablet
      # Patient Notes: Should this be displayed?
      # Issued Date: 25-Mar-2026 | Prescriber: Harvey Sembhytwo

  # ---------------------------------------------------------------------------
  # Repeat Medications (AC_TC02)
  # ---------------------------------------------------------------------------

  Rule: Repeat Medications (AC_TC02)
    Tests that the consumer correctly displays repeat and repeat dispensing medication data from the GP record.

    @AC_TC02_2.1
    Scenario: AC_TC02_2.1 - Repeat - Prescribed at GP practice - long prescriber note max limit
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                                                                                                                                                       |
        | Medication          | NovoPen Echo Plus hypodermic insulin injection pen reusable for 3ml cartridge 0.5 unit dial up / range 0.5-30 units Blue (Novo Nordisk Ltd)                                                                                  |
        | Dosage Instructions | as directed by diabetic clinic edited dosage                                                                                                                                                                                 |
        | Quantity            | 1 device                                                                                                                                                                                                                     |
        | Additional Notes    | This is a very long instructions This is a very long instructions This is a very long instructions This is a very long instructions This is a very long instructions This is a very long instructions This is a very long instructions This max 250 ch END |
        | Most Recent Issue   | 25-Mar-2026                                                                                                                                                                                                                  |
        | Prescriber          | Harvey Sembhytwo                                                                                                                                                                                                             |
        | Issues              | 1 of 6                                                                                                                                                                                                                       |
      # Intended Result: System displays the long prescriber note without truncation (250 chars).

    @AC_TC02_2.2
    Scenario: AC_TC02_2.2 - Repeat - Prescribed at GP practice - Not Issued, future dated
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                          |
        | Medication          | Beclometasone 0.0025% in White soft paraffin   |
        | Dosage Instructions | use as directed                                |
        | Quantity            | 100 gram                                       |
        | Most Recent Issue   | 01-May-2026                                    |
        | Date Added          | 30-Apr-2026                                    |
        | Prescriber          | Harvey Sembhytwo                               |
        | Issues              | 1 of 5                                         |

    @AC_TC02_2.3
    Scenario: AC_TC02_2.3 - Repeat - Prescribed at GP practice - stopped Issue
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                   |
        | Medication          | Liquid paraffin liquid  |
        | Dosage Instructions | use as needed           |
        | Quantity            | 250 ml                  |
        | Patient Notes       | Some notes for patient  |
        | Most Recent Issue   | 01-Apr-2026             |
        | Date Stopped        | 02-Apr-2026             |
        | Prescriber          | Harvey Sembhytwo        |
        | Issues              | 2 of 12                 |

    @AC_TC02_2.4
    Scenario: AC_TC02_2.4 - Repeat - Prescribed at GP practice - backdated more than 15 months
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                  |
        | Medication          | Aspirin 75mg dispersible tablets       |
        | Dosage Instructions | take one daily                         |
        | Quantity            | 28 tablet                              |
        | Patient Notes       | repeat backdated more than 15 months   |
        | Most Recent Issue   | 26-Mar-2026                            |
        | Date Added          | 06-Dec-2024                            |
        | Prescriber          | Harvey Sembhytwo                       |
        | Issues              | 2 of 12                                |

    @AC_TC02_2.5
    Scenario: AC_TC02_2.5 - Repeat - Prescribed at GP practice - re-authorised (see stopped details under Discontinued tab scenario 4.7)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                    |
        | Medication          | Ramipril 1.25mg capsules |
        | Dosage Instructions | take one daily           |
        | Quantity            | 14 capsule               |
        | Most Recent Issue   | 12-Mar-2026              |
        | Date Added          | 12-Mar-2026              |
        | Prescriber          | Harvey Sembhytwo         |
        | Issues              | 2 of 6                   |

    @AC_TC02_2.6
    Scenario: AC_TC02_2.6 - Repeat - Prescribed at GP practice - Controlled drug
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                       |
        | Medication          | Methadone 1mg/ml oral solution (A A H Pharmaceuticals Ltd)  |
        | Dosage Instructions | use as directed                                             |
        | Quantity            | 500 ml                                                      |
        | Additional Notes    | administrative notes                                        |
        | Patient Notes       | Control drug - script notes                                 |
        | Most Recent Issue   | 25-Mar-2026                                                 |
        | Date Added          | 30-Oct-2025                                                 |
        | Prescriber          | Harvey Sembhytwo                                            |
        | Issues              | 2 of 6                                                      |

    @AC_TC02_2.7
    Scenario: AC_TC02_2.7 - Repeat - Prescribed at GP practice - discontinued medication
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                            |
        | Medication          | Cetirizine 10mg tablets (Actavis UK Ltd)                                                         |
        | Dosage Instructions | take one daily                                                                                   |
        | Quantity            | 30 tablet                                                                                        |
        | Patient Notes       | adding notes for patient of how to take medication - discontinued medication without review date  |
        | Most Recent Issue   | 25-Mar-2026                                                                                      |
        | Date Added          | 25-Mar-2026                                                                                      |
        | Prescriber          | Harvey Sembhytwo                                                                                 |
        | Issues              | 2 of 6                                                                                           |

    @AC_TC02_2.8
    Scenario: AC_TC02_2.8 - Repeat - Prescribed at GP practice - 1st Issue without start date
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                  |
        | Medication          | Omeprazole 20mg gastro-resistant tablets |
        | Dosage Instructions | take one daily                         |
        | Quantity            | 28 tablet                              |
        | Most Recent Issue   | 25-Mar-2026                            |
        | Date Added          | 25-Jan-2026                            |
        | Prescriber          | Harvey Sembhytwo                       |
        | Issues              | 3 of 3                                 |

    @AC_TC02_2.9
    Scenario: AC_TC02_2.9 - Repeat - Prescribed at GP practice - no review date
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                    |
        | Medication          | Captopril 50mg tablets                   |
        | Dosage Instructions | take one twice daily                     |
        | Quantity            | 56 tablet                                |
        | Patient Notes       | max Issues set to 5 - no review date     |
        | Most Recent Issue   | 12-Mar-2026                              |
        | Date Added          | 25-Jan-2026                              |
        | Prescriber          | Harvey Sembhytwo                         |
        | Issues              | 3                                        |

    @AC_TC02_2.10
    Scenario: AC_TC02_2.10 - Repeat - Prescribed at GP practice - reauthorised (see stopped details under Discontinued tab scenario 4.8)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                                            |
        | Medication          | Epanutin Ready-Mixed Parenteral 250mg/5ml solution for injection ampoules (Viatris UK Healthcare Ltd)            |
        | Dosage Instructions | use as directed                                                                                                  |
        | Quantity            | 30 ampoule                                                                                                       |
        | Additional Notes    | {Batch Number 22222} {Pack Size 10} VIATRIS UK HEALTHCARE LTD                                                    |
        | Most Recent Issue   | 01-Apr-2026                                                                                                      |
        | Prescriber          | Harvey Sembhytwo                                                                                                 |
        | Issues              | 1                                                                                                                |

    @AC_TC02_2.11
    Scenario: AC_TC02_2.11 - Repeat - Prescribed at GP practice - notes contain only additional (patient) instructions
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                        |
        | Medication          | Co-codamol 30mg/500mg capsules                                               |
        | Dosage Instructions | [08:00-first dose][12:00-second dose][16:00-third dose][22:00-4th dose]       |
        | Quantity            | 100 capsule                                                                  |
        | Patient Notes       | adding some script notes for patient                                         |
        | Most Recent Issue   | 25-Mar-2026                                                                  |
        | Prescriber          | Harvey Sembhytwo                                                             |
        | Issues              | 1                                                                            |

    @AC_TC02_2.12
    Scenario: AC_TC02_2.12 - Repeat - Prescribed at GP practice - marked as private - Should not be Displayed
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication marked as private is not displayed
      And the system displays a warning indicating items have been excluded due to confidentiality
      # Medication: Latanoprost 50micrograms/ml eye drops
      # Dosage Instructions: One Drop To Be Used At Night In The Affected Eye(s)
      # Quantity: 2.5 ml | Prescriber: Harvey Sembhytwo
      # This item triggers the ListWarningCode-1 confidential-items warning

    # -------------------------------------------------------------------------
    # Repeat Dispensing
    # -------------------------------------------------------------------------

    @AC_TC02_2.13
    Scenario: AC_TC02_2.13 - Repeat dispensing - Prescribed at GP practice - future dated
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                               |
        | Medication          | Yasmin tablets (Bayer Plc)                           |
        | Dosage Instructions | take one as directed                                |
        | Quantity            | 63 tablet                                           |
        | Prescription Type   | Repeat Dispensing                                   |
        | Additional Notes    | prescriber notes admin notes - future dated          |
        | Patient Notes       | patient notes script notes - future dated            |
        | Most Recent Issue   | 01-Apr-2026                                         |
        | Date Added          | 25-Jan-2026                                         |
        | Prescriber          | Harvey Sembhytwo                                    |
        | Issues              | 1                                                   |

    @AC_TC02_2.14
    Scenario: AC_TC02_2.14 - Repeat dispensing - Prescribed at GP practice - long medication name, min char length for dose, notes and additional patient instructions
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                          |
        | Medication          | EuroTec adjustable elastic ostomy belt large SB 50 L 50mm wide, 110cm - 130cm length (Peak Medical Ltd) |
        | Dosage Instructions | A                                                                                              |
        | Quantity            | 1 device                                                                                       |
        | Prescription Type   | Repeat Dispensing                                                                              |
        | Additional Notes    | C                                                                                              |
        | Patient Notes       | B                                                                                              |
        | Most Recent Issue   | 12-Mar-2026                                                                                    |
        | Date Added          | 25-Jan-2026                                                                                    |
        | Prescriber          | Harvey Sembhytwo                                                                               |
        | Issues              | 1                                                                                              |

    @AC_TC02_2.15
    Scenario: AC_TC02_2.15 - Repeat dispensing - Prescribed at GP practice - transfer degraded medication name
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                     |
        | Medication          | EPIPEN AUTO-INJECTOR injection 300micrograms/0.3ml dose (1:1000) [MEDA]   |
        | Dosage Instructions | use as directed                                                           |
        | Quantity            | 1 syringe                                                                 |
        | Prescription Type   | Repeat Dispensing                                                         |
        | Most Recent Issue   | 12-Mar-2026                                                               |
        | Date Added          | 25-Jan-2026                                                               |
        | Prescriber          | Harvey Sembhytwo                                                          |
        | Issues              | 1                                                                         |

    @AC_TC02_2.16
    Scenario: AC_TC02_2.16 - Repeat dispensing - Prescribed at GP practice - repeat backdated and then made to repeat dispensed
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                     |
        | Medication          | Bisoprolol 10mg tablets                                   |
        | Dosage Instructions | take one daily                                            |
        | Quantity            | 28 tablet                                                 |
        | Patient Notes       | repeat dispensed medication backdated more than 15 months  |
        | Most Recent Issue   | 12-Mar-2026                                               |
        | Date Added          | 25-Jan-2026                                               |
        | Prescriber          | Harvey Sembhytwo                                          |
        | Issues              | 1                                                         |

    @AC_TC02_2.17
    Scenario: AC_TC02_2.17 - Repeat dispensing - Prescribed at GP practice - Irregularly Issued template
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                                                                                      |
        | Medication          | EpiPen Jr. 150micrograms/0.3ml (1 in 2,000) solution for injection auto-injectors (Viatris UK Healthcare Ltd)              |
        | Dosage Instructions | use as directed                                                                                                            |
        | Quantity            | 1 pre-filled disposable injection                                                                                          |
        | Prescription Type   | Repeat Dispensing                                                                                                          |
        | Additional Notes    | {Batch Number} {Pack Size} MYLAN                                                                                           |
        | Most Recent Issue   | 12-Mar-2026                                                                                                                |
        | Date Added          | 25-Jan-2026                                                                                                                |
        | Prescriber          | Harvey Sembhytwo                                                                                                           |
        | Issues              | 1                                                                                                                          |

    @AC_TC02_2.18
    Scenario: AC_TC02_2.18 - Repeat dispensing - Prescribed at GP practice - Issue stopped
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the repeat medications
      Then the medication list contains an entry with the following details:
        | field               | value                       |
        | Medication          | Clopidogrel 300mg tablets   |
        | Dosage Instructions | use as directed             |
        | Quantity            | 7 tablet                    |
        | Prescription Type   | Repeat Dispensing           |
        | Additional Notes    | Notes for someone           |
        | Patient Notes       | Notes for someone           |
        | Most Recent Issue   | 01-Apr-2026                 |
        | Prescriber          | Harvey Sembhytwo            |
        | Issues              | 1                           |

  # ---------------------------------------------------------------------------
  # Prescribed Elsewhere (AC_TC03)
  # ---------------------------------------------------------------------------

  Rule: Prescribed Elsewhere (AC_TC03)
    Tests that the consumer correctly displays medications prescribed by another organisation (Hospital, Dental, Other).

    @AC_TC03_3.1
    Scenario: AC_TC03_3.1 - Stopped - Delayed prescribing - Prescribed by another organisation (Hospital)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the prescribed elsewhere medications
      Then the medication list contains an entry with the following details:
        | field                | value                                                          |
        | Medication           | Oxybuprocaine 0.4% eye drops 0.5ml unit dose preservative free |
        | Dosage Instructions  | 1                                                              |
        | Quantity             | 7 days                                                         |
        | Discontinued Reason  | Clinical contra-indication                                     |
        | Most Recent Issue    | 30-Apr-2026                                                    |
        | Date Added           | 25-Jan-2026                                                    |
        | Prescriber           | Harvey Sembhytwo                                               |
        | Issues               | 1                                                              |

    @AC_TC03_3.2
    Scenario: AC_TC03_3.2 - Delayed prescribing - Prescribed by another organisation (Other medication) - no end date, no quantity
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the prescribed elsewhere medications
      Then the medication list contains an entry with the following details:
        | field               | value                                                    |
        | Medication          | Salbutamol 5mg/5ml solution for infusion ampoules        |
        | Dosage Instructions | 1ml                                                      |
        | Quantity            | 1ml                                                      |
        | Most Recent Issue   | 30-Apr-2026                                              |
        | Date Added          | 25-Jan-2026                                              |
        | Prescriber          | Harvey Sembhytwo                                         |
        | Issues              | 1                                                        |

    @AC_TC03_3.3
    Scenario: AC_TC03_3.3 - Stopped - Acute - Prescribed by another organisation (Dental) - notes
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the prescribed elsewhere medications
      Then the medication list contains an entry with the following details:
        | field                | value                                              |
        | Medication           | Fluoxetine 20mg capsules (A A H Pharmaceuticals Ltd) |
        | Dosage Instructions  | take daily                                         |
        | Quantity             | 7                                                  |
        | Additional Notes     | notes from prescriber                              |
        | Patient Notes        | notes for patient                                  |
        | Discontinued Reason  | Clinical contra-indication                         |
        | Most Recent Issue    | 25-Mar-2026                                        |
        | Date Added           | 25-Mar-2026                                        |
        | Prescriber           | Harvey Sembhytwo                                   |
        | Issues               | 1                                                  |

    @AC_TC03_3.4
    Scenario: AC_TC03_3.4 - Delayed prescribing - Prescribed by another organisation (Other medication) - special characters, no end date
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the prescribed elsewhere medications
      Then the medication list contains an entry with the following details:
        | field               | value                                |
        | Medication          | Ibuprofen 10% gel                    |
        | Dosage Instructions | Dosage !"%&*()+:<>?-=;',./           |
        | Quantity            | 10 gram !"%&*()+:<>?-=;',./          |
        | Most Recent Issue   | 25-Mar-2026                          |
        | Date Added          | 25-Mar-2026                          |
        | Prescriber          | Harvey Sembhytwo                     |
        | Issues              | 1                                    |
      # Intended Result: System displays special characters correctly without exclusion.

    @AC_TC03_3.5
    Scenario: AC_TC03_3.5 - Acute - Prescribed by another organisation (Hospital)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the prescribed elsewhere medications
      Then the medication list contains an entry with the following details:
        | field               | value                           |
        | Medication          | Methadone 5mg tablets           |
        | Dosage Instructions | 30ml To Be Taken Each Day       |
        | Quantity            | 210ml                           |
        | Most Recent Issue   | 01-Feb-2026                     |
        | Date Added          | 25-Mar-2026                     |
        | Prescriber          | Harvey Sembhytwo                |
        | Issues              | 1                               |

    @AC_TC03_3.6
    Scenario: AC_TC03_3.6 - Acute - Prescribed by another organisation (Dental) - no end date
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the prescribed elsewhere medications
      Then the medication list contains an entry with the following details:
        | field               | value                           |
        | Medication          | Clopidogrel 75mg tablets        |
        | Dosage Instructions | take as required                |
        | Quantity            | take as required                |
        | Additional Notes    | admin notes - no end date       |
        | Most Recent Issue   | 01-Feb-2026                     |
        | Date Added          | 25-Jan-2026                     |
        | Prescriber          | Harvey Sembhytwo                |
        | Issues              | 1                               |

  # ---------------------------------------------------------------------------
  # Discontinued Medications (AC_TC04)
  # ---------------------------------------------------------------------------

  Rule: Discontinued Medications (AC_TC04)
    Tests that the consumer correctly displays discontinued/stopped medication data from the GP record.

    @AC_TC04_4.1
    Scenario: AC_TC04_4.1 - Repeat - Prescribed at GP practice - reauthorised (repeat details under Med - Repeat tab scenario 2.6)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the discontinued medications
      Then the medication list contains an entry with the following details:
        | field                | value                                                                                                 |
        | Medication           | Epanutin Ready-Mixed Parenteral 250mg/5ml solution for injection ampoules (Viatris UK Healthcare Ltd) |
        | Dosage Instructions  | use as directed                                                                                       |
        | Quantity             | 30 ampoule                                                                                            |
        | Additional Notes     | {Batch Number 22222} {Pack Size 10} VIATRIS UK HEALTHCARE LTD                                         |
        | Discontinued Reason  | Re-Authorised                                                                                         |
        | Most Recent Issue    | 25-Mar-2026                                                                                           |
        | Prescriber           | Harvey Sembhytwo                                                                                      |

    @AC_TC04_4.2
    Scenario: AC_TC04_4.2 - Repeat dispensing - Prescribed at GP practice - reauthorised (repeat details under Med - Repeat tab scenario 2.4)
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the discontinued medications
      Then the medication list contains an entry with the following details:
        | field                | value                    |
        | Medication           | Ramipril 1.25mg capsules |
        | Dosage Instructions  | take one daily           |
        | Quantity             | 14 capsule               |
        | Discontinued Reason  | Re-Authorised            |
        | Most Recent Issue    | 25-Mar-2026              |
        | Prescriber           | Harvey Sembhytwo         |

    @AC_TC04_4.3
    Scenario: AC_TC04_4.3 - Stopped - Acute - Prescribed at GP practice
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the discontinued medications
      Then the medication list contains an entry with the following details:
        | field                | value                                                            |
        | Medication           | Desomono 75microgram Tablets (Genesis Pharmaceuticals Ltd)       |
        | Dosage Instructions  | Take one tablet daily at the same time each day                  |
        | Quantity             | 84 Tablets                                                       |
        | Additional Notes     | This is a test of stopping an acute                              |
        | Discontinued Reason  | Clinical Grounds                                                 |
        | Most Recent Issue    | 06-Mar-2026                                                      |
        | Date Stopped         | 18-Mar-2026                                                      |
        | Prescriber           | Harvey Sembhytwo                                                 |
        | Issues               | 1                                                                |

    @AC_TC04_4.4
    Scenario: AC_TC04_4.4 - Stopped - Acute - Prescribed at GP practice - long reason max character limit
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the discontinued medications
      Then the medication list contains an entry with the following details:
        | field                | value                                                                                                                                                                                                                                    |
        | Medication           | Quetiapine 25mg tablets                                                                                                                                                                                                                  |
        | Dosage Instructions  | One To Be Taken Each Day                                                                                                                                                                                                                 |
        | Quantity             | 30 tablet                                                                                                                                                                                                                                |
        | Additional Notes     | This is a very long reason. This is a very long reason.This is a very long reason.This is a very long reason.This is a very long reason.This is a very long reason.This is a very long reason.END                                        |
        | Discontinued Reason  | At the patients's request                                                                                                                                                                                                                |
        | Most Recent Issue    | 13-Feb-2026                                                                                                                                                                                                                              |
        | Date Stopped         | 18-Mar-2026                                                                                                                                                                                                                              |
        | Prescriber           | Harvey Sembhytwo                                                                                                                                                                                                                         |
        | Issues               | 1                                                                                                                                                                                                                                        |
      # Intended Result: System displays the long reason text without truncation.

    @AC_TC04_4.5
    Scenario: AC_TC04_4.5 - Repeat - Prescribed at GP practice - prescribed more than 15 months ago
      Given the consumer requests the structured record for patient "9692136744"
      When the consumer displays the discontinued medications
      Then the medication list contains an entry with the following details:
        | field                | value                                                                                                          |
        | Medication           | Salamol 100micrograms/dose inhaler CFC free (Teva UK Ltd)                                                      |
        | Dosage Instructions  | inhale 2 doses as needed                                                                                       |
        | Quantity             | 200 dose                                                                                                       |
        | Patient Notes        | stopped med - prescribed more than 15 months ago                                                               |
        | Discontinued Reason  | Change to medication treatment regime (Stopped repeat med - prescribed more than 15 months ago from date 31/05/2024) |
        | Most Recent Issue    | 15-Dec-2024                                                                                                    |
        | Date Added           | 15-Dec-2024                                                                                                    |
        | Prescriber           | Harvey Sembhytwo                                                                                               |
        | Issues               | 1                                                                                                              |
