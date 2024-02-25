from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.http import StreamingHttpResponse
from django.urls import reverse
from .models import *
from apis.get_live_feed import get_live_feed, AVAILABLE_CAMERA_FEEDS
import random
import datetime
from .forms import *


def get_result_path(path):
    return "static/" + path.replace("./website/apis/", "")


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
    return render(
        request,
        "profile.html",
        {
            "form": form,
        },
    )


def video_view(request):
    ctx = {"video_feeds": random.sample(AVAILABLE_CAMERA_FEEDS, 6)}
    return render(request, "video.html", ctx)


def video_stream(request, video_path):
    return StreamingHttpResponse(
        get_live_feed(video_path, save_video=False),
        content_type="multipart/x-mixed-replace; boundary=frame",
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
    return render(
        request,
        "report_missing.html",
        {
            "form": form,
        },
    )


def report_information_view(request):
    if request.method == "POST":
        form = InformationReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            messages.success(request, "Report submitted.")
            return redirect(reverse("report-information"))
    form = InformationReportForm()
    return render(
        request,
        "report_information.html",
        {
            "form": form,
        },
    )


def dashboard_view(request):
    last_facial_recognition = FacialDetectionResult.objects.last(),
    last_person_description = PersonDescriptionResult.objects.last(),
    last_people_get_all = PeopleGetAllResult.objects.last(),
    last_vehicle_identification = VehicleIdentificationResult.objects.last(),
    last_license_plate = LicensePlateResult.objects.last(),
    context = {
        "facial_source": get_result_path(last_facial_recognition[0].source_image),
        "facial_target": get_result_path(last_facial_recognition[0].target_image),
        "facial_box": get_result_path(last_facial_recognition[0].box_result),
        "facial_cropped": get_result_path(last_facial_recognition[0].cropped_result),
        "person_image": get_result_path(last_person_description[0].image),
        "person_description": last_person_description[0].description,
        "people_image": get_result_path(last_people_get_all[0].image),
        "people_box": get_result_path(last_people_get_all[0].box_result),
        "people_cropped": get_result_path(last_people_get_all[0].cropped_result),
        "vehicle_image": get_result_path(last_vehicle_identification[0].image),
        "vehicle_description": last_vehicle_identification[0].description,
        "vehicle_box": get_result_path(last_vehicle_identification[0].box_result),
        "vehicle_cropped": get_result_path(last_vehicle_identification[0].cropped_result),
        "license_image": get_result_path(last_license_plate[0].image),
        "license_plate": last_license_plate[0].license_plate,
    }
    return render(request, "dashboard.html", context)


def map_view(request):
    information_locations = [
        *map(lambda i: i.location, InformationReport.objects.all())
    ]
    alert_locations = [*map(lambda i: i.location, Alert.objects.all())]
    ctx = {
        "information_locations": information_locations,
        "alert_locations": alert_locations,
    }
    return render(request, "google-maps-address.html", ctx)
