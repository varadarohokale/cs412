# File: models.py
# Author: Varada Rohokale (YOUR_BU_EMAIL), 3/20/2026
# Description: Model definitions and data-loading utilities for the
# voter_analytics application. This file defines the Voter model and
# includes a function for importing voter records from a CSV file.

"""Define models and CSV import logic for the voter_analytics app."""

import csv
from datetime import datetime

from django.db import models


class Voter(models.Model):
    """Represent one registered voter in Newton, Massachusetts."""

    # Store the voter's personal identification information.
    last_name = models.TextField()
    first_name = models.TextField()

    # Store the voter's residential address information.
    street_number = models.CharField(max_length=20)
    street_name = models.TextField()
    apartment_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10)

    # Store important dates for the voter.
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    # Store political affiliation and precinct assignment.
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.IntegerField()

    # Store whether the voter participated in recent elections.
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # Store the number of these five elections in which the voter voted.
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a readable string representation of this voter."""
        return (
            f"{self.first_name} {self.last_name}, "
            f"{self.street_number} {self.street_name}, "
            f"Precinct {self.precinct_number}"
        )


def parse_date(date_string):
    """Return a date object created from a CSV date string."""
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def parse_boolean(value):
    """Return whether a CSV value should be interpreted as True."""
    return str(value).strip().upper() == "TRUE"


def load_data():
    """Load voter data from the CSV file into the database."""
    # Delete old records first so that reloading the file does not
    # create duplicate voter records.
    Voter.objects.all().delete()

    # Store the path to the CSV file that contains the voter data.
    filename = "/Users/azs/Desktop/newton_voters.csv"

    # Open the CSV file and use a DictReader so that fields can be
    # accessed by column name instead of numerical index.
    input_file = open(filename, encoding="utf-8-sig")
    csv_reader = csv.DictReader(input_file)

    # Process each row from the CSV file and create one Voter object.
    for row in csv_reader:
        try:
            # Create a new Voter instance from the current CSV row.
            voter = Voter(
                last_name=row["Last Name"],
                first_name=row["First Name"],
                street_number=row[
                    "Residential Address - Street Number"
                ],
                street_name=row[
                    "Residential Address - Street Name"
                ],
                apartment_number=row[
                    "Residential Address - Apartment Number"
                ],
                zip_code=row["Residential Address - Zip Code"],
                date_of_birth=parse_date(row["Date of Birth"]),
                date_of_registration=parse_date(
                    row["Date of Registration"]
                ),
                party_affiliation=row["Party Affiliation"],
                precinct_number=row["Precinct Number"],
                v20state=parse_boolean(row["v20state"]),
                v21town=parse_boolean(row["v21town"]),
                v21primary=parse_boolean(row["v21primary"]),
                v22general=parse_boolean(row["v22general"]),
                v23town=parse_boolean(row["v23town"]),
                voter_score=row["voter_score"],
            )

            # Save the new Voter object to the database.
            voter.save()
            print(f"Created voter: {voter}")

        except Exception:
            # Skip malformed rows so that one bad record does not stop
            # the entire import process.
            print(f"Skipped: {row}")

    # Close the file after all rows have been processed.
    input_file.close()

    print(f"Done. Created {len(Voter.objects.all())} Voters.")
