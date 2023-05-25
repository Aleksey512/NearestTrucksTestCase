from rest_framework import serializers
from cargo.models import Location, Cargo, Truck
from django.forms.models import model_to_dict
from cargo.models import calculate_distance


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class CargoListSerializer(serializers.ModelSerializer):
    pickup_location_zip = LocationSerializer()
    delivery_location_zip = LocationSerializer()
    nearest_trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = '__all__'

    def get_nearest_trucks(self, obj):
        trucks = Truck.objects.all()
        new_truck_list = []
        truck_list = [(truck, truck.current_location) for truck in trucks if calculate_distance(
            (truck.current_location.latitude, truck.current_location.longitude),
            (obj.pickup_location_zip.latitude, obj.pickup_location_zip.longitude)) <= 450]
        for tr in truck_list:
            new_tr = model_to_dict(tr[0], exclude=['id', 'current_location'])
            new_tr['current_location'] = model_to_dict(tr[1], exclude=['id'])
            new_truck_list.append(new_tr)
        return new_truck_list


class TruckListSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer()

    class Meta:
        model = Truck
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'
