from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home_view, name="index"),
    path('alerts', alerts_view, name="alerts")
]
