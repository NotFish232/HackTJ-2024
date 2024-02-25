from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home_view, name="index"),
    path('alerts', alerts_view, name="alerts"),
    path('login', login_view, name="login"),
    path('sign_up', sign_up_view, name="sign_up"),
    path('profile', profile_view, name="profile"),
    path('logout', logout, name="logout"),
    path('video', video_view, name="video"),
    path('video_stream/<path:video_path>', video_stream, name="video_stream"),
    path('report-missing', report_missing_view, name="report-missing"),
    path("report-information", report_information_view, name="report-information"),
    path('dashboard', dashboard_view, name="dashboard"),
]
