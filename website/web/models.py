from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
import datetime


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    USERNAME_FIELD = "email"

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    person = models.OneToOneField(
        "Person", on_delete=models.SET_NULL, null=True, blank=True
    )

    trusted_contacts = models.ManyToManyField(
        "User", blank=True, related_name="trusted_contact_set"
    )

    def __str__(self):
        if self.person:
            return self.person.full_name
        return self.email


class Person(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    sex = models.CharField(
        choices=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        max_length=255,
        blank=True,
        null=True,
    )
    race = models.CharField(
        choices=[
            ("white", "White"),
            ("black", "Black or African American"),
            ("hispanic", "Hispanic or Latino"),
            ("asian", "Asian"),
            ("native", "American Indian or Alaska Native"),
            ("hawaiian", "Native Hawaiian or Other Pacific Islander"),
            ("other", "Other"),
            ("unknown", "Unknown"),
        ],
        max_length=500,
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    hair_color = models.CharField(max_length=255, blank=True, null=True)
    eye_color = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="static/photos", blank=True, null=True)

    missing = models.BooleanField(default=False)

    @property
    def age(self):
        return (datetime.datetime.now().date() - self.date_of_birth).days // 365

    @property
    def full_name(self):
        return f"{self.first_name}{f' {self.middle_name}' if self.middle_name else ''} {self.last_name}"

    @property
    def photo_url(self):
        if self.photo:
            return self.photo
        return "/static/photos/no-photo.png"

    def __str__(self):
        return self.full_name


class Alert(models.Model):
    # title = models.CharField(max_length=500)
    description = models.TextField()
    type = models.CharField(
        choices=[
            ("vigilant", "Vigilant"),
            ("amber", "AMBER"),
            ("silver", "Silver"),
            ("endangered", "Endangered Missing Person"),
            ("blue", "Blue"),
            ("camo", "Camo"),
        ],
        max_length=255,
    )
    resolved = models.BooleanField(default=False)

    person = models.ForeignKey(
        "Person", on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    contact = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.get_type_display()} Alert for {self.person.full_name} at {self.date}"

    class Meta:
        ordering = ["-date"]


class FacialDetectionResult(models.Model):
    source_image = models.CharField(max_length=500)
    target_image = models.CharField(max_length=500)
    found_match = models.BooleanField()
    box_result = models.CharField(max_length=500, null=True, blank=True)
    cropped_result = models.CharField(max_length=500, null=True, blank=True)


class PersonDescriptionResult(models.Model):
    image = models.CharField(max_length=500)
    description = models.CharField(max_length=500)



class InformationReport(models.Model):
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=500, null=True, blank=True)
    photo = models.ImageField(upload_to="static/reports", blank=True, null=True)

