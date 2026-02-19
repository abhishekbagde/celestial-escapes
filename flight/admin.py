from django.contrib import admin
from .models import Planet, Flight, Pod, Booking, PlanetBase, FlightSchedule, BaseImage


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['name', 'emoji', 'distance_from_earth_km', 'travel_time_days', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    readonly_fields = ['slug', 'created_at', 'updated_at']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'origin_planet', 'destination_planet', 'departure_datetime', 'seats_available', 'price_credits', 'status']
    list_filter = ['status', 'origin_planet', 'destination_planet']
    search_fields = ['flight_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Pod)
class PodAdmin(admin.ModelAdmin):
    list_display = ['pod_number', 'flight', 'pod_type', 'price_credits', 'is_available']
    list_filter = ['pod_type', 'is_available']
    readonly_fields = ['created_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'flight', 'status', 'total_price', 'booked_at']
    list_filter = ['status', 'booked_at']
    search_fields = ['user__username', 'flight__flight_number']
    readonly_fields = ['booked_at', 'updated_at']


# Deprecated models
@admin.register(PlanetBase)
class PlanetBaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'planet']
    search_fields = ['name']


@admin.register(FlightSchedule)
class FlightScheduleAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'destination_base', 'departure_date']
    list_filter = ['departure_date']


@admin.register(BaseImage)
class BaseImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'base']
