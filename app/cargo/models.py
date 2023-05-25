from django.core.exceptions import ValidationError
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django.db import models
import random
import string
from geopy import distance
from typing import Tuple


def calculate_distance(city_from: Tuple[float, float], city_to: Tuple[float, float]) -> float:
    return distance.distance(city_from, city_to).miles


def generate_unique_number():
    return f'{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}'


def generate_random_capacity():
    return random.randint(1, 1001)


def validate_weight(value):
    if value <= 0 or value > 1000:
        raise ValidationError(
            _("%(value)s is not an range 1-1000"),
            params={"value": value},
        )


def get_random_location():
    max_id = Location.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        category = Location.objects.filter(pk=pk).first()
        if category:
            return category


class Location(models.Model):
    city = models.CharField(max_length=100, verbose_name='City')
    state = models.CharField(max_length=100, verbose_name='State')
    zip_code = models.CharField(max_length=10, unique=True, verbose_name='Post index')
    latitude = models.FloatField(verbose_name='latitude')
    longitude = models.FloatField(verbose_name='longitude')

    def __str__(self):
        return f'{self.city}, {self.state}'


class Cargo(models.Model):
    pickup_location_zip = models.ForeignKey(Location, to_field="zip_code", on_delete=models.CASCADE,
                                            related_name='pickups',
                                            verbose_name='Pickup location')
    delivery_location_zip = models.ForeignKey(Location, to_field="zip_code", on_delete=models.CASCADE,
                                              related_name='deliveries',
                                              verbose_name='Delivery location')
    weight = models.IntegerField(validators=[validate_weight])
    description = models.TextField()

    def __str__(self):
        return f'Cargo {self.id}'


class Truck(models.Model):
    number = models.CharField(max_length=5, unique=True,
                              default=generate_unique_number)
    current_location = models.ForeignKey(Location, to_field='zip_code', on_delete=models.CASCADE, related_name="truck")
    capacity = models.IntegerField(default=generate_random_capacity, validators=[validate_weight])

    def __str__(self):
        return f'Truck {self.number}'
