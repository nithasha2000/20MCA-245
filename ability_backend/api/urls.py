from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_api),
    path('logout/', views.logout_api),
    path('register/', views.register_api)
]