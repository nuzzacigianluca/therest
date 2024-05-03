from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from datetime import datetime
# Create your views here.
def therest(request):
    return render(request, 'therest/index.html')

def aboutview(request):
    return render(request, 'therest/about.html')

def bookview(request):
    return render(request, 'therest/book.html', {
        'dateToday': datetime.today().strftime('%Y-%m-%d')
    })

def loginview(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'therest/login.html')

def manageview(request):
    return render(request, 'therest/manage.html')

def registrationview(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        name=request.POST['name']
        password=request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(username=username, password=password)
        UserProfile.objects.create(user=user, role='Client', name=name)
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'therest/registration.html')
def logoutview(request):
    logout(request)
    return render(request, 'therest/login.html')

def mybookingviews(request):
    return render(request, 'therest/mybookings.html')

#manager
#nuzzaci1
