from django.urls import path
from . import views

urlpatterns= [
    path('', views.intro_page, name='intro'),
    path('calculate/', views.calculate_option, name='calculate_option')
    
]