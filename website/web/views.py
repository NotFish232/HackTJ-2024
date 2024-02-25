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
import datetime
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

            if request.GET.get("next"):
                try:
                    url = reverse(request.GET.get("next").replace("/", ""))
                    return redirect(url)
                except:
                    pass
            
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
    ctx = {"video_feeds": random.sample(AVAILABLE_CAMERA_FEEDS, 6)}
    return render(request, "video.html", ctx)


def video_stream(request, video_path):
    return StreamingHttpResponse(
        get_live_feed(video_path, save_video=False),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )


def report_missing_view(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must be logged in to report someone missing.")
        return redirect(reverse("login") + "?next=/report-missing")
    if request.method == "POST":
        form = MissingPersonReportForm(request.user, request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.type = "vigilant"
            alert.date = datetime.datetime.now()
            alert.contact = f"{request.user.person.first_name} {request.user.person.last_name}. Email: {request.user.email}. Phone: {request.user.phone_number}."
            alert.save()
            alert.person.missing = True
            alert.person.save()
            messages.success(request, "Report submitted.")
            return redirect(reverse("alerts"))
    form = MissingPersonReportForm(request.user)
    return render(request, "report_missing.html", {
        "form": form,
    })


def report_information_view(request):
    if request.method == "POST":
        form = InformationReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            messages.success(request, "Report submitted.")
            return redirect(reverse("report-information"))
    form = InformationReportForm()
    return render(request, "report_information.html", {
        "form": form,
    })

def dashboard_view(request):
    return render(request, "dashboard.html")