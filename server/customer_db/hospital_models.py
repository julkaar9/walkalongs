from django.db import models


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
    id = models.CharField(
        db_column="province_id",
        max_length=2,
        choices=PROVINCE_CHOICES,
        primary_key=True,
    )
    name = models.CharField(db_column="province_name", max_length=64)

    class Meta:
        db_table = "province_names"


class Patients(models.Model):
    GENDER_CHOICES = (("F", "F"), ("M", "M"))
    id = models.PositiveIntegerField(db_column="patient_id", primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    birth_date = models.DateField()
    city = models.CharField(max_length=32)
    province = models.ForeignKey(
        Provinces,
        db_column="province_id",
        related_name="patients",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    allergies = models.CharField(max_length=64, null=True, blank=True)
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    class Meta:
        db_table = "patients"


class Doctors(models.Model):
    id = models.PositiveIntegerField(db_column="doctor_id", primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    speciality = models.CharField(max_length=128)

    class Meta:
        db_table = "doctors"


class Admissions(models.Model):
    patient = models.ForeignKey(
        Patients,
        db_column="patient_id",
        related_name="admissions",
        on_delete=models.CASCADE,
    )
    admission_date = models.DateField()
    discharge_date = models.DateField()
    diagnosis = models.CharField(max_length=128)
    attending_doctor = models.ForeignKey(
        Doctors,
        db_column="attending_doctor_id",
        related_name="assigned_admissions",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "admissions"
        constraints = [
            models.CheckConstraint(
                check=models.Q(admission_date__lte=models.F("discharge_date")),
                name="admission_before_discharge",
            )
        ]
