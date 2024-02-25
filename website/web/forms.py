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

class MissingPersonReportForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(MissingPersonReportForm, self).__init__(*args, **kwargs)
        ids = [u.person.id for u in user.trusted_contacts.filter(person__missing=False)]
        self.fields['person'].queryset = Person.objects.filter(id__in=ids)
    
    class Meta:
        model = Alert
        fields = [
            'description',
            'location', 
            'person',
        ]

class InformationReportForm(forms.ModelForm):
    class Meta:
        model = InformationReport
        fields = [
            'person',
            'description',
            'date',
            'location',
            'photo',
        ]
        help_texts = {
            'person': 'Person who is the subject of this report (if known)',
            'date': 'Date and time of event',
            'photo': 'Photo of event or person (if available)'
        }

