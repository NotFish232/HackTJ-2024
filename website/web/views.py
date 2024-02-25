from django.shortcuts import render
from .models import *


def home_view(request):
    return render(request, "home.html")


def alerts_view(request):
    active_alerts = Alert.objects.filter(resolved=False)
    resolved_alerts = Alert.objects.filter(resolved=True)

    return render(request, "alerts.html", {
        "active_alerts": active_alerts,
        "resolved_alerts": resolved_alerts,
    })