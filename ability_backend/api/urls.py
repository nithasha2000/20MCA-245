from django.urls import path
from .views import account_views, dashboard_views

urlpatterns = [
    path('', account_views.index),
    path('login/', account_views.login_api),
    path('logout/', account_views.logout_api),
    path('change_password/', account_views.change_password_api),
    path('register/', account_views.register_api),
    path('view-users/', dashboard_views.view_users),
    path('notifications/', dashboard_views.view_notifications),
    path('account_activation/', dashboard_views.account_activation),
    path('forgot-password/', account_views.forgot_password),
    path('verify-otp/', dashboard_views.verify_otp),
    path('dashboard-sidebar/', dashboard_views.dashboard_sidebar),
    path('job-post/', dashboard_views.job_post),
    path('view-job-list/', dashboard_views.view_job_list)
]