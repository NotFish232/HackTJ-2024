from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Person)
admin.site.register(Alert)
admin.site.register(InformationReport)
admin.site.register(FacialDetectionResult)
admin.site.register(PersonDescriptionResult)
admin.site.register(PeopleGetAllResult)
admin.site.register(VehicleIdentificationResult)
admin.site.register(LicensePlateResult)

