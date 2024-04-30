from django.urls import path
from . import views

urlpatterns = [
    path("",views.therest),
    path("home/",views.therest, name='home'),
    path('about/', views.aboutview,name='about'),
    path('book/', views.bookview,name='book'),
]