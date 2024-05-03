from django.contrib import admin
from .models import UserProfile, Booking, Booking_managed

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Booking)
admin.site.register(Booking_managed)