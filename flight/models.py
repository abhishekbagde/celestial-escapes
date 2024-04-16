from django.db import models

# Create your models here.
class Planet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    object_url = models.TextField(default='https://example.com/default-planet-link')
    distance = models.FloatField(default=0.0)
    fare = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
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


# class UserBooking(models.Model):
#     #user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user = models.CharField(max_length=20)
#     flight_schedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)
#     booking_date = models.DateTimeField(auto_now_add=True)
#     ticket_type = models.CharField(max_length=20)  # OneWay or Return
#     departure_date = models.DateField()
#     departure_time = models.TimeField()
#     return_date = models.DateField(blank=True, null=True)
#     return_time = models.TimeField(blank=True, null=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     destination_base = models.TextField(default='California Base')
#     arrival_base = models.ForeignKey(PlanetBase, on_delete=models.CASCADE, related_name='UserBookingsArrival')

#     def __str__(self):
#         return f"{self.user.username} - {self.flight_schedule.departure_airport} to {self.flight_schedule.arrival_airport}"