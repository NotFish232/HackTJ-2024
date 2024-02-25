from django import forms
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 
            'middle_name',
            'last_name', 
            'sex',
            'race',
            'date_of_birth',
            'height',
            'weight',
            'hair_color',
            'eye_color',
            'photo',
            'description',
        ]