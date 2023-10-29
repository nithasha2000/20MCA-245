from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.index),
    path('login/', views.login)
]