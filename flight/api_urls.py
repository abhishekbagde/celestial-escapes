from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    UserViewSet, ProfileViewSet, PlanetViewSet, 
    FlightViewSet, PodViewSet, BookingViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'planets', PlanetViewSet, basename='planet')
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'pods', PodViewSet, basename='pod')
router.register(r'bookings', BookingViewSet, basename='booking')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
