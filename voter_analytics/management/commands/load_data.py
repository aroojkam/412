import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from voter_analytics.models import Voter

class Command(BaseCommand):
    help = 'Load voter data from CSV'

    def handle(self, *args, **kwargs):
        with open('/Users/aroojkamran/Desktop/newton_voters.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Voter.objects.create(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'] or None,
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d'),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d'),
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=row['Precinct Number'],
                    v20state=row['v20state'].lower() == 'true',
                    v21town=row['v21town'].lower() == 'true',
                    v21primary=row['v21primary'].lower() == 'true',
                    v22general=row['v22general'].lower() == 'true',
                    v23town=row['v23town'].lower() == 'true',
                    voter_score=int(row['voter_score']),
                )
