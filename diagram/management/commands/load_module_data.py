import csv
from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from diagram.models import Module, Links
from pytz import UTC


# DATETIME_FORMAT = '%m/%d/%Y %H:%M'

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the module data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from database.csv into our Database mode"

    def handle(self, *args, **options):

        if Module.objects.exists():
            print('Module data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return


        print("Loading module data")
        for row in DictReader(open('./mod_info.csv')):

            #For each row, make a Module object
            module = Module()

            module.name = row['Core name']
            module.code = row['Code']
            module.year = row['Year']
            module.term = row['Term']
            module.credits = row['Credits']
            module.department = row['Department']
            module.category = row['Category']
            module.website = row['Module Descriptor']
            module.pre_req = row['Pre Req']
            module.co_req = row['Co Req']

            # module.lecturer = row['Lecturer']

            # module.core_Natural_Sciences = row['Core Natural Sciences']
            # module.core_Mathematics = row['Core Mathematics']
            # module.core_Physics = row['Physics (MPhys)']
            # module.core_Physics_BPhys = row['Core Physics (BPhys)']
            # module.core_Biochemistry = row['Core Biochemistry']
            # module.core_Biological_Sciences = row['Core Biological Sciences']
            # module.core_Biological_and_Medicinal_Chemistry = row['Core Biological and Medicinal Chemistry']
            # module.natural_Sciences_History = row['Natural Science History']
            # module.topic_pathway = row['Topic Pathway']



            module.save()

            '''
            old example stuff
            '''
            #raw_vaccination_names = row['vaccinations']
            #vaccination_names = [name for name in raw_vaccination_names.split('| ') if name]
            #for vac_name in vaccination_names:
            #    vac = Vaccine.objects.get(name=vac_name)
            #    pet.vaccinations.add(vac)
            #pet.save()
