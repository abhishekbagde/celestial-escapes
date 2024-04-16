from django.contrib import admin

# Register your models here.

from .models import *

# Register your models here.

admin.site.register(Planet)
admin.site.register(PlanetBase)
admin.site.register(BaseImage)
admin.site.register(FlightSchedule)
#admin.site.register(UserBooking)
