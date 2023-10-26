from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import url
from base import views

urlpatterns = [
    path(r'^login$',views.loginApi),
    path(r'^login$',views.loginApi),
    path(r'^login/([0-9]+)$',views.loginApi),
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]