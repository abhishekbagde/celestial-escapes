from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Planet(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    gltf_model_url = models.TextField(default='https://example.com/default-planet-link')
    distance_from_earth_km = models.FloatField(default=0.0, help_text="Distance in millions of km")
    travel_time_days = models.IntegerField(default=0, help_text="Travel time in days")
    emoji = models.CharField(max_length=10, default='🪐')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['distance_from_earth_km']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Flight(models.Model):
    FLIGHT_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    flight_number = models.CharField(max_length=20, unique=True)
    origin_planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='origin_flights')
    destination_planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='destination_flights')
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    seats_total = models.IntegerField(default=100)
    seats_available = models.IntegerField(default=100)
    price_credits = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=FLIGHT_STATUS, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-departure_datetime']

    def __str__(self):
        return f"{self.flight_number}: {self.origin_planet} → {self.destination_planet}"


class Pod(models.Model):
    POD_TYPES = [
        ('standard', 'Standard'),
        ('luxury', 'Luxury'),
        ('cryo', 'Cryo Sleep'),
    ]
    
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='pods')
    pod_number = models.CharField(max_length=10)
    pod_type = models.CharField(max_length=20, choices=POD_TYPES, default='standard')
    price_credits = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['flight', 'pod_number']
        ordering = ['pod_type', 'pod_number']

    def __str__(self):
        return f"Pod {self.pod_number} ({self.pod_type}) - {self.flight.flight_number}"


class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    pod = models.ForeignKey(Pod, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booked_at']
        unique_together = ['user', 'flight', 'pod']

    def __str__(self):
        return f"{self.user.username} → {self.flight.flight_number}"


# Deprecated models (kept for backward compatibility)
class PlanetBase(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='bases')

    def __str__(self):
        return self.name
    
class BaseImage(models.Model):
    image = models.ImageField(upload_to='base_images')
    base = models.ForeignKey(PlanetBase, on_delete=models.CASCADE, related_name='images')


class FlightSchedule(models.Model):
    flight_number = models.CharField(max_length=20)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    destination_base = models.ForeignKey(PlanetBase, on_delete=models.CASCADE, related_name='destination_flights')
    arrival_base = models.ForeignKey(PlanetBase, on_delete=models.CASCADE, related_name='arrival_flights', default="")
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
