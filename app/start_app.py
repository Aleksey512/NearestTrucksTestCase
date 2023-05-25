import os
import random

import django
from pathlib import Path
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NearestTrucksTestCase.settings")
django.setup()

from django.db import IntegrityError
from cargo.models import Location, Truck, get_random_location


def load_locations():
    if Path.is_file(Path('./uszips.csv')):
        df = pd.read_csv('./uszips.csv')
        for _, j in df.iterrows():
            try:
                Location.objects.create(city=j['city'],
                                        state=j['state_name'],
                                        zip_code=j['zip'],
                                        latitude=j['lat'],
                                        longitude=j['lng'])
            except IntegrityError:
                continue
        print("Locations loaded")
        return
    else:
        print("File with data does not exists")
        return


def create_trucks():
    if Truck.objects.count() > 21:
        print("Trucks already exists")
        return
    else:
        for i in range(20):
            truck = Truck.objects.create(current_location=get_random_location())
        print("success created")


if __name__ == "__main__":
    load_locations()
    create_trucks()
