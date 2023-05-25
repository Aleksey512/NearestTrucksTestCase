from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from cargo.models import Location, Cargo, Truck, calculate_distance
from cargo.serializers import LocationSerializer, CargoSerializer, TruckSerializer, CargoListSerializer, TruckListSerializer


class BaseViewSet(mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Basic view model
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'destroy':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class StandardResultsSetPagination(PageNumberPagination):
    """Paginator class"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'state', 'zip_code']


class CargoViewSet(BaseViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['weight']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return CargoListSerializer
            return self.serializer_class
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        Get all cargo objects
        @param request: GET /api/cargo
        @return: json
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Get object from id
        @param request: GET /api/cargo/{int}
        @return: json
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        trucks = Truck.objects.all()
        new_truck_list = []
        truck_list = [(truck, truck.current_location) for truck in trucks]
        for tr in truck_list:
            new_tr = model_to_dict(tr[0], exclude=['id', 'current_location'])
            new_tr['current_location'] = model_to_dict(tr[1], exclude=['id'])
            new_tr['distance'] = calculate_distance((tr[1].latitude, tr[1].longitude), (
                instance.pickup_location_zip.latitude, instance.pickup_location_zip.longitude))
            new_truck_list.append(new_tr)
        return Response([serializer.data, {'truck_list': new_truck_list}])


class TruckViewSet(BaseViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['capacity', 'number']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list' or self.action == 'retrieve':
                return TruckListSerializer
            return self.serializer_class
        return self.serializer_class
