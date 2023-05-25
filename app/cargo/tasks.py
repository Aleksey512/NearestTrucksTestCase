import random

from django.db.models import Max

from NearestTrucksTestCase.celery import celery_app
from cargo.models import Truck, Location


def get_random_location():
    max_id = Location.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        location = Location.objects.filter(pk=pk).first()
        if location:
            return location


@celery_app.task
def change_location():
    """Every 3 minutes change Trucks location"""
    try:
        all_trucks = Truck.objects.all()
        for truck in all_trucks:
            truck.current_location = get_random_location()
            truck.save()
    except SystemExit:
        print("Task stopped on purpose")
    except Exception as e:
        print(f"An error has occurred which has led to the termination of the task \n Error: {e}")
