from django.contrib import admin
from .custom_models import Occupation, Person
from .hospital_models import Patients, Admissions

# Register your models here.

admin.site.register(Occupation)
admin.site.register(Person)

admin.site.register(Patients)
admin.site.register(Admissions)
