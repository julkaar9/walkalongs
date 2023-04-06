from django.db import models


class Patients(models.Model):
    GENDER_CHOICES = (("F", "F"), ("M", "M"))
    patient_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max=64)
    last_name = models.CharField(max=64)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    birth_date = models.DateField()
    city = models.CharField(max_length=32)
    allergies = models.CharField(max_length=64)
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    class Meta:
        db_table = "patients"


class Doctors(models.Model):
    doctor_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max=64)
    last_name = models.CharField(max=64)
    speciality = models.CharField(max_length=128)

    class Meta:
        db_table = "doctors"


class Admissions(models.Model):
    patients_id = models.ForeignKey(
        Patients, related_name="admissions", on_delete=models.CASCADE
    )
    admission_Date = models.DateField()
    discharge_date = models.DateField()
    diagnosis = models.CharField(max_length=128)
    attending_doctor_id = models.ForeignKey(
        Doctors, related_name="assigned_admissions", on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "admissions"


class Provinces(models.Model):
    PROVINCE_CHOICES = (
        ("AB", "AB"),
        ("BC", "BC"),
        ("MB", "MB"),
        ("NB", "NB"),
        ("NT", "NT"),
        ("NS", "NS"),
        ("NU", "NU"),
        ("ON", "ON"),
        ("PE", "PE"),
        ("QC", "QC"),
        ("SK", "SK"),
        ("YT", "YT"),
    )
    province_id = models.CharField(max_length=2, choices=PROVINCE_CHOICES)
    province_name = models.CharField(max_length=64)

    class Meta:
        db_table = "province_names"
