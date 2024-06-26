from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("",views.therest),
    path("home/",views.therest, name='home'),
    path('about/', views.aboutview,name='about'),
    path('book/', views.bookview,name='book'),
    path('login/', views.loginview,name='login'),
    path('manage/', views.manageview,name='manage'),
    path('registration/', views.registrationview,name='registration'),
    path('logout/', views.logoutview,name='logout'),
    path('mybookings', views.mybookingviews, name="mybookings"),
    path('managed_bookings/', views.managedbookingviews, name="managed_bookings"),
]