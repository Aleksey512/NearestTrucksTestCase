from django.contrib import admin

from cargo.models import *


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "pk", "city", "state", "zip_code", "latitude", "longitude"]
    search_fields = list_display


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = [
        "pk", "pickup_location_zip", "delivery_location_zip", "weight", "description"]
    search_fields = ["pk", "weight", "description"]


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = [
        "pk", "number", "current_location", "capacity"]
    search_fields = ["pk", "number", "capacity"]
