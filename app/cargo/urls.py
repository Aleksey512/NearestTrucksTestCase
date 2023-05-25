from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cargo.views import LocationViewSet, CargoViewSet, TruckViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'cargo', CargoViewSet)
router.register(r'trucks', TruckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]