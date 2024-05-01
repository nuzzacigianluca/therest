from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def therest(request):
    return render(request, 'therest/index.html')

def aboutview(request):
    return render(request, 'therest/about.html')

def bookview(request):
    return render(request, 'therest/book.html')

def loginview(request):
    return render(request, 'therest/login.html')

def registrationview(request):
    return render(request, 'therest/registration.html')

