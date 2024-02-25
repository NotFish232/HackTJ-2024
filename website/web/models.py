from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
import datetime


class User(AbstractBaseUser, PermissionsMixin):   
    objects = UserManager()
    USERNAME_FIELD = 'email'

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True)
 

class Person(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    sex = models.CharField(choices=[
        ("male", "Male"),
        ("female", "Female"),
    ], max_length=255, blank=True, null=True)
    race = models.CharField(choices=[
        ("white", "White"),
        ("black", "Black or African American"),
        ("hispanic", "Hispanic or Latino"),
        ("asian", "Asian"),
        ("native", "American Indian or Alaska Native"), 
        ("hawaiian", "Native Hawaiian or Other Pacific Islander"),
        ("other", "Other"),
        ("unknown", "Unknown"),
    ], max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    hair_color = models.CharField(max_length=255, blank=True, null=True)
    eye_color = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    missing = models.BooleanField(default=False)

    @property
    def age(self):
        return (datetime.datetime.now().date() - self.date_of_birth).days // 365


class Alert(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    type = models.CharField(choices=[
        ('vigilant', 'Vigilant'),
        ('amber', 'AMBER'),
        ('silver', 'Silver'),
        ('endangered', 'Endangered Missing Person'),
        ('blue', 'Blue'),
        ('camo', 'Camo'),
    ], max_length=255)
    resolved = models.BooleanField(default=False)

    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    contact = models.CharField(max_length=500, null=True, blank=True)

