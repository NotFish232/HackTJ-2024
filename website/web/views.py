from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import StreamingHttpResponse
from django.urls import reverse
from .models import *
from apis.get_live_feed import get_live_feed, AVAILABLE_CAMERA_FEEDS
import random
from .forms import *


def home_view(request):
    return render(request, "home.html")


def alerts_view(request):
    active_alerts = Alert.objects.filter(resolved=False)
    resolved_alerts = Alert.objects.filter(resolved=True)

    return render(
        request,
        "alerts.html",
        {
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                request,
                "login.html",
                {
                    "error": "The credentials you entered were incorrect. Please try again.",
                    "email": email,
                },
            )

        user = authenticate(username=user.email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse("index"))
        return render(
            request,
            "login.html",
            {
                "error": "The credentials you entered were incorrect. Please try again.",
                "email": email,
            },
        )

    return render(request, "login.html")


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect(reverse("login"))


def sign_up_view(request):
    pass


def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.person)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            messages.success(request, "Profile updated.")
            return redirect(reverse("profile"))
    form = ProfileForm(instance=request.user.person)
    return render(request, "profile.html", {
        "form": form,
    })


def video_view(request):
    ctx = {"video_feeds": random.sample(AVAILABLE_CAMERA_FEEDS, 12)}
    return render(request, "video.html", ctx)


def video_stream(request, video_path):
    return StreamingHttpResponse(
        get_live_feed(video_path, save_video=False),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )
