from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=50)
    role=models.CharField(max_length=50)
class Booking(models.Model):
    number=models.CharField(max_length=3)
    data=models.CharField(max_length=50)
    ora=models.CharField(max_length=50)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

class Booking_managed(models.Model):
    id_booking=models.ForeignKey(Booking, on_delete=models.CASCADE)
    id_user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)