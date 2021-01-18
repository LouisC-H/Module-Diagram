import csv
from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from department.models import Module#, Requisites
from pytz import UTC


DATETIME_FORMAT = '%m/%d/%Y %H:%M'

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the pet data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from database.csv into our Database mode"

    def handle(self, *args, **options):
        if Module.objects.exists(): #or Requisites.objects.exists():
            print('Module data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Creating requisites data")
        #for vaccine_name in VACCINES_NAMES:
            #vac = Vaccine(name=vaccine_name)
            #vac.save()
        #print("Loading pet data for pets available for adoption")
        for row in DictReader(open('./Database.csv')):
            module = Module()

            module.code = row['Code']
            module.department = row['Department']
            module.year = row['Year']
            module.term = row['Term']
            module.credits = row['Credits']
            module.lecturer = row['Lecturer']
            module.core_Natural_Sciences = row['Core Natural Sciences']
            module.core_Mathematics = row['Core Mathematics']
            module.core_Physics = row['Physics (MPhys)']
            module.core_Physics_BPhys = row['Core Physics (BPhys)']
            module.core_Biochemistry = row['Core Biochemistry']
            module.core_Biological_Sciences = row['Core Biological Sciences']
            module.core_Biological_and_Medicinal_Chemistry = row['Core Biological and Medicinal Chemistry']
            module.natural_Sciences_History = row['Natural Science History']
            module.topic_pathway = row['Topic Pathway']
            module.module_descriptor = row['Module Descriptor']
            module.Name = row['name']
            module.save()
            #Requisites.Pre_req = row['Pre Req']
            #Requisites.Co_req = row['Co Req']

            #raw_vaccination_names = row['vaccinations']
            #vaccination_names = [name for name in raw_vaccination_names.split('| ') if name]
            #for vac_name in vaccination_names:
            #    vac = Vaccine.objects.get(name=vac_name)
            #    pet.vaccinations.add(vac)
            #pet.save()
