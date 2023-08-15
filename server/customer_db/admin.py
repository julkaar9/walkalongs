from django.contrib import admin
from .custom_models import Occupation, Person
from .hospital_models import Patients, Admissions, Doctors

# Register your models here.


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "gender",
        "birth_date",
        "city",
        "province",
        "allergies",
        "height",
        "weight",
    )


class AdmssionAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id",
        "admission_date",
        "discharge_date",
        "diagnosis",
        "attending_doctor",
    )
    ordering = ("patient_id",)
    list_editable = ("diagnosis",)


class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "first_name",
        "last_name",
        "speciality",
    )
    ordering = ("pk",)


admin.site.register(Occupation)
admin.site.register(Person)

admin.site.register(Patients, PatientAdmin)
admin.site.register(Admissions, AdmssionAdmin)
admin.site.register(Doctors, DoctorAdmin)
