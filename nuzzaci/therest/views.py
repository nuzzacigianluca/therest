from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def therest(request):
    return render(request, 'therest/index.html')

def aboutview(request):
    return render(request, 'therest/about.html')

def bookview(request):
    return render(request, 'therest/book.html')

def loginview(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('manage')
        else:
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('manage')
        else:
            return render(request, 'therest/login.html')

def manageview(request):
    return render(request, 'therest/manage.html')

def registrationview(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password = password)
            login(request, user)
            return redirect('manage')
    else:
        form = UserCreationForm()
    return render(request, 'therest/registration.html', {
        'form': form,
    })
def logoutview(request):
    logout(request)
    return render(request, 'therest/login.html')