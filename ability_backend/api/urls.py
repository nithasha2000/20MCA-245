from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_api),
    path('logout/', views.logout_api),
    path('change_password/', views.change_password_api),
    path('register/', views.register_api),
    path('view-users/', views.view_users),
    path('notifications/', views.view_notifications),
    path('account_activation/', views.account_activation),
    path('forgot-password/', views.forgot_password),
    path('verify-otp/', views.verify_otp),
    path('dashboard-sidebar/', views.dashboard_sidebar)
]