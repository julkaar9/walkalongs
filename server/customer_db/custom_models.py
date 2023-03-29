from django.db import models


class Occupation(models.Model):
    title = models.CharField(primary_key=True, max_length=32, db_column="title")
    avg_salary = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="avg_salary"
    )

    class Meta:
        db_table = "occupation"


class Person(models.Model):
    person_id = models.PositiveIntegerField(primary_key=True, db_column="person_id")
    name = models.CharField(max_length=64, db_column="name")
    occupation_title = models.ForeignKey(
        Occupation,
        db_column="occupation_title",
        on_delete=models.CASCADE,
        related_name="person",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "person"
