# SQL-PRACTICE medium exercises using Django ORM
[https://www.sql-practice.com/](https://www.sql-practice.com/)

This walkalong consists of medium questions and their solutions from sql-practice.com, written in both **SQL** and **django
ORM**, They query results are also compared for equality.  
Insert, Update and Delete queries are not included to keep database consistent.

## Try it yourself
The notebook (Django Shell-plus) is located in [here](https://github.com/julkaar9/walkalongs/blob/main/server/notebooks/sql-practice-medium-practice.ipynb)   
First cd into the notebook directory `cd server/notebook`  
Then open the notebook using `python ../manage.py shell_plus --notebook`  

```python
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from utils import *
from sqlparse import format
```


```python
from django.db.models import (
    Q,
    F,
    Case,
    When,
    Count,
    Func,
    Min,
    Max,
    Sum,
    Avg,
    Value,
    OuterRef,
    Subquery,
    CharField,
)
from django.db.models.functions import Concat, Cast, Round, Length, Upper, Lower
from django.db import connection
from customer_db.models import Provinces, Patients, Doctors, Admissions
```


```python
def print_sql(queryset):
    formatted = format(str(queryset.query), reindent=True)
    print(formatted)
```


```python
admission_fields = [
    "id",
    "patient_id",
    "admission_date",
    "discharge_date",
    "diagnosis",
    "attending_doctor_id",
]
```


```python
class NonAggrCount(Count):
    """
    This aggregation will not trigger a group by
    """

    contains_aggregate = False


class NonAggrSum(Sum):
    contains_aggregate = False
```

## Medium 1
Show unique birth years from patients and order them by ascending.


```python
# Use YEAR(birth_date) for most databases
qstr = """
SELECT
  DISTINCT strftime('%Y', birth_date) birth_year
FROM patients
ORDER BY birth_year;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.annotate(birth_year=Cast(F("birth_date__year"), CharField()))
    .distinct()
    .order_by("birth_year")
    .values("birth_year")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT DISTINCT CAST(django_date_extract(year, "patients"."birth_date") AS text) AS "birth_year"
    FROM "patients"
    ORDER BY 1 ASC
    


```python
orm_to_df(ormq[:3])
```

    |    |   birth_year |
    |---:|-------------:|
    |  0 |         1975 |
    |  1 |         1976 |
    |  2 |         1977 |
    

## Medium 2
Show unique first names from the patients table which only occurs once in the list.

For example, if two or more people are named 'John' in the first_name column then don't include their name in the output list. If only 1 person is named 'Leo' then include them in the output.


```python
qstr = """
SELECT first_name
FROM patients
GROUP BY first_name
HAVING COUNT(first_name) = 1
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values("first_name")
    .annotate(occurance=Count("first_name"))
    .filter(occurance=1)
    .values("first_name")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name"
    FROM "patients"
    GROUP BY "patients"."first_name"
    HAVING COUNT("patients"."first_name") = 1
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   |
    |---:|:-------------|
    |  0 | Abigail      |
    |  1 | Alicia       |
    |  2 | Allison      |
    

## Medium 3
Show patient_id and first_name from patients where their first_name start and ends with 's' and is at least 6 characters long.
We will do start and ends with 'n' and is at least 6 characters long.


```python
qstr = """
SELECT
  patient_id,
  first_name
FROM patients
WHERE first_name LIKe "n____%n"
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(first_name__regex=r"(?i)^n\w{4,}n$").values(
    "first_name", patient_id=F("id")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."patient_id" AS "patient_id"
    FROM "patients"
    WHERE "patients"."first_name" REGEXP (?i)^n\w{4,}n$
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   |   patient_id |
    |---:|:-------------|-------------:|
    |  0 | Nathan       |           54 |
    |  1 | Nathan       |          100 |
    

## Medium 4
Show patient_id, first_name, last_name from patients whos diagnosis is 'Dementia'.
We will do Diabetes.
Primary diagnosis is stored in the admissions table.


```python
qstr = """
SELECT
  p.patient_id,
  first_name,
  last_name
FROM patients p
  INNER JOIN admissions a ON p.patient_id = a.patient_id
WHERE diagnosis = 'Diabetes'
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Admissions.objects.filter(diagnosis="Diabetes").values(
    "patient_id", first_name=F("patient__first_name"), last_name=F("patient__last_name")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."patient_id",
           "patients"."first_name" AS "first_name",
           "patients"."last_name" AS "last_name"
    FROM "admissions"
    INNER JOIN "patients" ON ("admissions"."patient_id" = "patients"."patient_id")
    WHERE "admissions"."diagnosis" = Diabetes
    


```python
# Note the result of the ORM query in the next cell is equivalent to that of the last cell,
# except for the ordering.

qstr = """
SELECT
  p.patient_id,
  first_name,
  last_name
FROM patients p
  INNER JOIN admissions a ON p.patient_id = a.patient_id
WHERE diagnosis = 'Diabetes'
ORDER BY p.patient_id
"""
sqlq = sql_raw(qstr)
```


```python
diabetic_patients = (
    Admissions.objects.filter(diagnosis="Diabetes").values_list("patient_id").distinct()
)
ormq1 = (
    Patients.objects.filter(id__in=diabetic_patients)
    .values("first_name", "last_name", patient_id=F("id"))
    .order_by("patient_id")
    .values("patient_id", "first_name", "last_name")
)
equal(sqlq, ormq1)
print_sql(ormq1)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."patient_id" AS "patient_id"
    FROM "patients"
    WHERE "patients"."patient_id" IN
        (SELECT DISTINCT U0."patient_id"
         FROM "admissions" U0
         WHERE U0."diagnosis" = Diabetes)
    ORDER BY 3 ASC
    


```python
orm_to_df(ormq[:3])
```

    |    |   patient_id | first_name   | last_name   |
    |---:|-------------:|:-------------|:------------|
    |  0 |            6 | Gavin        | Bryant      |
    |  1 |           17 | Emily        | Tran        |
    |  2 |           27 | Allison      | Rogers      |
    

## Medium 5
Display every patient's first_name.
Order the list by the length of each name and then by alphbetically


```python
qstr = """
SELECT
  first_name
FROM patients p
ORDER BY
  LENGTH(first_name),
  first_name;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.order_by(Length("first_name"), "first_name").values(
    "first_name"
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name"
    FROM "patients"
    ORDER BY LENGTH("patients"."first_name") ASC, "patients"."first_name" ASC
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   |
    |---:|:-------------|
    |  0 | Eli          |
    |  1 | Eli          |
    |  2 | Eli          |
    

## Medium 6
Show the total amount of male patients and the total amount of female patients in the patients table.
Display the two results in the same row.


```python
qstr = """
SELECT (
    SELECT COUNT(gender)
    FROM patients
    WHERE gender = 'M'
  ) AS male, (
    SELECT COUNT(gender)
    FROM patients
    WHERE gender = 'F'
  ) AS female;
"""
sqlq = sql_raw(qstr)
```


```python
male_subquery, female_subquery = [
    Patients.objects.filter(gender=g)
    .annotate(**{f"{g}_count": Func(F("gender"), function="COUNT")})
    .values(f"{g}_count")
    for g in ["M", "F"]
]

ormq = Patients.objects.annotate(
    male=Subquery(male_subquery), female=Subquery(female_subquery)
).values("male", "female")[:1]
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT
      (SELECT COUNT(U0."gender") AS "M_count"
       FROM "patients" U0
       WHERE U0."gender" = M) AS "male",
    
      (SELECT COUNT(U0."gender") AS "F_count"
       FROM "patients" U0
       WHERE U0."gender" = F) AS "female"
    FROM "patients"
    LIMIT 1
    


```python
ormq = Patients.objects.annotate(
    male=NonAggrSum(Case(When(gender="M", then=1))),
    female=NonAggrSum(Case(When(gender="F", then=1))),
).values("male", "female")
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT SUM(CASE
                   WHEN "patients"."gender" = M THEN 1
                   ELSE NULL
               END) AS "male",
           SUM(CASE
                   WHEN "patients"."gender" = F THEN 1
                   ELSE NULL
               END) AS "female"
    FROM "patients"
    


```python
orm_to_df(ormq)
```

    |    |   male |   female |
    |---:|-------:|---------:|
    |  0 |     50 |       51 |
    

## Medium 7
Show first and last name, allergies from patients which have allergies to either 'Penicillin' or 'Morphine'. Show results ordered ascending by allergies then by first_name then by last_name.


```python
qstr = """
SELECT
  first_name,
  last_name,
  allergies
FROM patients
WHERE
  allergies IN ('Penicillin', 'Morphine')
ORDER BY
  allergies,
  first_name,
  last_name;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.filter(allergies__in=["Penicillin", "Morphine"])
    .values("first_name", "last_name", "allergies")
    .order_by("allergies", "first_name", "last_name")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."allergies"
    FROM "patients"
    WHERE "patients"."allergies" IN (Penicillin,
                                     Morphine)
    ORDER BY "patients"."allergies" ASC,
             "patients"."first_name" ASC,
             "patients"."last_name" ASC
    


```python
orm_to_df(ormq)
```

    |    | first_name   | last_name   | allergies   |
    |---:|:-------------|:------------|:------------|
    |  0 | Gavin        | Bryant      | Penicillin  |
    |  1 | Jeremy       | Kim         | Penicillin  |
    |  2 | Trevor       | Baker       | Penicillin  |
    

## Medium 8
Show patient_id, diagnosis from admissions. Find patients admitted multiple times for the same diagnosis.


```python
qstr = """
SELECT
  patient_id,
  diagnosis
FROM admissions
GROUP BY
  patient_id,
  diagnosis
HAVING COUNT(*) > 1
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.values("patient_id", "diagnosis")
    .annotate(count=Count("patient_id"))
    .filter(count__gt=1)
    .values("patient_id", "diagnosis")
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."patient_id",
           "admissions"."diagnosis"
    FROM "admissions"
    GROUP BY "admissions"."patient_id",
             "admissions"."diagnosis"
    HAVING COUNT("admissions"."patient_id") > 1
    


```python
orm_to_df(ormq)
```

    |    |   patient_id | diagnosis   |
    |---:|-------------:|:------------|
    |  0 |            5 | Meningitis  |
    

## Medium 9
Show the city and the total number of patients in the city.
Order from most to least patients and then by city name ascending.


```python
qstr = """
SELECT
  city,
  COUNT(*) population
FROM patients
GROUP BY city 
ORDER BY population DESC, city
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values("city")
    .annotate(population=Count("id"))
    .order_by("-population", "city")
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."city",
           COUNT("patients"."patient_id") AS "population"
    FROM "patients"
    GROUP BY "patients"."city"
    ORDER BY 2 DESC,
             "patients"."city" ASC
    


```python
orm_to_df(ormq)
```

    |    | city      |   population |
    |---:|:----------|-------------:|
    |  0 | Montreal  |           14 |
    |  1 | Calgary   |           13 |
    |  2 | Toronto   |           13 |
    |  3 | Vancouver |           13 |
    |  4 | Halifax   |           12 |
    |  5 | Ottawa    |           12 |
    |  6 | Victoria  |           12 |
    |  7 | Winnipeg  |           12 |
    

## Medium 10
Show first name, last name and role of every person that is either patient or doctor.
The roles are either "Patient" or "Doctor"


```python
qstr = """
SELECT
  first_name,
  last_name,
  'patient' AS Role
FROM patients
UNION ALL
SELECT
  first_name,
  last_name,
  'doctor' AS Role
FROM doctors;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.annotate(role=Value("patient", output_field=CharField()))
    .values("first_name", "last_name", "role")
    .union(
        Doctors.objects.annotate(role=Value("doctor", output_field=CharField())).values(
            "first_name", "last_name", "role"
        ),
        all=True,
    )
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name" AS "col1",
           "patients"."last_name" AS "col2",
           patient AS "role"
    FROM "patients"
    UNION ALL
    SELECT "doctors"."first_name" AS "col1",
           "doctors"."last_name" AS "col2",
           doctor AS "role"
    FROM "doctors"
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   | role    |
    |---:|:-------------|:------------|:--------|
    |  0 | Cheryl       | Mason       | patient |
    |  1 | Jason        | Fleming     | patient |
    |  2 | Tiffany      | McDonald    | patient |
    

## Medium 11
Show all allergies and their occurance ordered by occurance. Remove NULL values from query.


```python
qstr = """
SELECT
  allergies,
  COUNT (*) AS total_occurance
FROM patients
WHERE allergies IS NOT null
GROUP BY allergies
ORDER BY total_occurance DESC
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values("allergies")
    .filter(allergies__isnull=False)
    .annotate(total_occurance=Count("allergies"))
    .order_by("-total_occurance")
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."allergies",
           COUNT("patients"."allergies") AS "total_occurance"
    FROM "patients"
    WHERE "patients"."allergies" IS NOT NULL
    GROUP BY "patients"."allergies"
    ORDER BY 2 DESC
    


```python
orm_to_df(ormq[:3])
```

    |    | allergies   |   total_occurance |
    |---:|:------------|------------------:|
    |  0 | Pollen      |                15 |
    |  1 | Lactose     |                13 |
    |  2 | Sulfa drugs |                 8 |
    

## Medium 12
Show all patient's first_name, last_name, and birth_date who were born in the 1970s decade. Sort the list starting from the earliest birth_date.


```python
# use YEAR(birth_date) if year function is available
qstr = """
SELECT
  first_name,
  last_name,
  birth_date
FROM patients
WHERE CAST(strftime('%Y', birth_date) AS INT) BETWEEN 1970 AND 1979
ORDER BY birth_date
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.filter(birth_date__year__gte=1970, birth_date__year__lte=1979)
    .order_by("birth_date")
    .values("first_name", "last_name", "birth_date")
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."birth_date"
    FROM "patients"
    WHERE ("patients"."birth_date" >= 1970-01-01
           AND "patients"."birth_date" <= 1979-12-31)
    ORDER BY "patients"."birth_date" ASC
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   | birth_date   |
    |---:|:-------------|:------------|:-------------|
    |  0 | Jeremy       | Kim         | 1975-07-19   |
    |  1 | Samantha     | Garcia      | 1975-11-30   |
    |  2 | Olivia       | Li          | 1976-03-11   |
    

## Medium 13
We want to display each patient's full name in a single column. Their last_name in all upper letters must appear first, then first_name in all lower case letters. Separate the last_name and first_name with a comma. Order the list by the first_name in decending order
EX: SMITH,jane


```python
qstr = """
SELECT
   UPPER(last_name) || ',' || LOWER(first_name) AS full_name
FROM patients
ORDER BY first_name DESC
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.values(
    full_name=Concat(Upper("last_name"), Value(","), Lower("first_name"))
).order_by("-first_name")
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT COALESCE(UPPER("patients"."last_name"),) || COALESCE(COALESCE(,,) || COALESCE(LOWER("patients"."first_name"),),) AS "full_name"
    FROM "patients"
    ORDER BY "patients"."first_name" DESC
    


```python
orm_to_df(ormq[:3])
```

    |    | full_name      |
    |---:|:---------------|
    |  0 | NGUYEN,william |
    |  1 | LIU,victor     |
    |  2 | BAKER,trevor   |
    

## Medium 14
Show the province_id(s), sum of height; where the total sum of its patient's height is greater than or equal to 7,000.
We will do 3000


```python
qstr = """
SELECT
  province_id,
  SUM(height) AS sum_height
FROM patients
GROUP BY province_id
HAVING SUM(height) > 3000;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values("province_id")
    .annotate(sum_height=Sum("height"))
    .filter(sum_height__gt=3000)
    .values("province_id", "sum_height")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."province_id",
           SUM("patients"."height") AS "sum_height"
    FROM "patients"
    GROUP BY "patients"."province_id"
    HAVING SUM("patients"."height") > 3000
    


```python
orm_to_df(ormq[:3])
```

    |    | province_id   |   sum_height |
    |---:|:--------------|-------------:|
    |  0 | BC            |         4357 |
    |  1 | ON            |         4331 |
    

## Medium 15
Show the difference between the largest weight and smallest weight for patients with the last name 'Maroni'.
We will do Lee.


```python
qstr = """
SELECT
  (MAX(weight) - MIN(weight)) AS weight_dif
FROM patients
WHERE last_name = 'Lee';
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(last_name="Lee").aggregate(
    weight_dif=Max("weight") - Min("weight")
)
equal(sqlq, ormq)
# print_sql(ormq)
```

    Equal ✔️
    


```python
ormq = (
    Patients.objects.filter(last_name="Lee")
    .annotate(
        weight_dif=Func(F("weight"), function="MAX") - Func(F("weight"), function="MIN")
    )
    .values("weight_dif")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT (MAX("patients"."weight") - MIN("patients"."weight")) AS "weight_dif"
    FROM "patients"
    WHERE "patients"."last_name" = Lee
    


```python
orm_to_df(ormq)
```

    |    |   weight_dif |
    |---:|-------------:|
    |  0 |           23 |
    

## Medium 16
Show all of the days of the month (1-31) and how many admission_dates occurred on that day. Sort by the day with most admissions to least admissions.


```python
qstr = """
SELECT
  CAST(strftime('%d', admission_date) as INT) AS month_day,
  COUNT(patient_id) AS daily_admission
FROM admissions
GROUP BY strftime('%d', admission_date)
ORDER BY daily_admission DESC;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.values(month_day=F("admission_date__day"))
    .annotate(daily_admission=Count("id"))
    .order_by("-daily_admission")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT django_date_extract(day, "admissions"."admission_date") AS "month_day",
           COUNT("admissions"."id") AS "daily_admission"
    FROM "admissions"
    GROUP BY 1
    ORDER BY 2 DESC
    


```python
orm_to_df(ormq[:3])
```

    |    |   month_day |   daily_admission |
    |---:|------------:|------------------:|
    |  0 |          28 |                 6 |
    |  1 |          18 |                 6 |
    |  2 |          17 |                 6 |
    

## Medium 17
Show all columns for patient_id 54's most recent admission_date.


```python
qstr = """
SELECT *
FROM admissions
WHERE patient_id = 54 AND admission_date = (
    SELECT max(admission_date)
    FROM admissions
    WHERE patient_id = 54
  )
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Admissions.objects.filter(
    patient_id=54,
    admission_date=Admissions.objects.filter(patient_id=54).aggregate(
        max_admission=Max("admission_date")
    )["max_admission"],
).values(*admission_fields)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."id",
           "admissions"."patient_id",
           "admissions"."admission_date",
           "admissions"."discharge_date",
           "admissions"."diagnosis",
           "admissions"."attending_doctor_id"
    FROM "admissions"
    WHERE ("admissions"."admission_date" = 2022-06-02
           AND "admissions"."patient_id" = 54)
    


```python
ormq = Admissions.objects.filter(
    patient_id=54,
    admission_date=Subquery(
        Admissions.objects.filter(patient_id=54)
        .annotate(max_admission=Func(F("admission_date"), function="Max"))
        .values("max_admission")
    ),
).values(*admission_fields)


equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."id",
           "admissions"."patient_id",
           "admissions"."admission_date",
           "admissions"."discharge_date",
           "admissions"."diagnosis",
           "admissions"."attending_doctor_id"
    FROM "admissions"
    WHERE ("admissions"."admission_date" =
             (SELECT Max(U0."admission_date") AS "max_admission"
              FROM "admissions" U0
              WHERE U0."patient_id" = 54)
           AND "admissions"."patient_id" = 54)
    


```python
ormq = (
    Admissions.objects.filter(patient_id=54)
    .order_by("-admission_date")[:1]
    .values(*admission_fields)
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."id",
           "admissions"."patient_id",
           "admissions"."admission_date",
           "admissions"."discharge_date",
           "admissions"."diagnosis",
           "admissions"."attending_doctor_id"
    FROM "admissions"
    WHERE "admissions"."patient_id" = 54
    ORDER BY "admissions"."admission_date" DESC
    LIMIT 1
    


```python
orm_to_df(ormq[:3])
```

    |    |   id |   patient_id | admission_date   | discharge_date   | diagnosis   |   attending_doctor_id |
    |---:|-----:|-------------:|:-----------------|:-----------------|:------------|----------------------:|
    |  0 |  154 |           54 | 2022-06-02       | 2022-06-06       | Migraine    |                    11 |
    

## Medium 18
Show patient_id, attending_doctor_id, and diagnosis for admissions that match one of the two criteria:
1. patient_id is an odd number and attending_doctor_id is either 1, 5, or 19.
2. attending_doctor_id contains a 2 and the length of patient_id is 3 characters.


```python
qstr = """
SELECT
  patient_id,
  attending_doctor_id,
  diagnosis
FROM admissions
WHERE
  (
    patient_id % 2 = 1
    and attending_doctor_id IN (1, 5, 19)
  )
  OR (
    CAST(attending_doctor_id AS varchar) LIKE "%2%"
    AND length(CAST(patient_id AS VARCHAR)) = 2
  )
"""
sqlq = sql_raw(qstr)
```


```python
f1 = Q(attending_doctor_id__in=[1, 5, 19], pi_mod=1)
f2 = Q(adi_str__icontains="2", pi_len=2)

ormq = (
    Admissions.objects.annotate(
        pi_mod=F("patient_id") % 2,
        adi_str=Cast(F("attending_doctor_id"), CharField()),
        pi_len=Length(Cast(F("patient_id"), CharField())),
    )
    .filter(f1 | f2)
    .values("patient_id", "attending_doctor_id", "diagnosis")
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."patient_id",
           "admissions"."attending_doctor_id",
           "admissions"."diagnosis"
    FROM "admissions"
    WHERE (("admissions"."attending_doctor_id" IN (1,
                                                   5,
                                                   19)
            AND ("admissions"."patient_id" % 2) = 1)
           OR (CAST("admissions"."attending_doctor_id" AS text) LIKE %2% ESCAPE '\'
               AND LENGTH(CAST("admissions"."patient_id" AS text)) = 2))
    


```python
orm_to_df(ormq[:3])
```

    |    |   patient_id |   attending_doctor_id | diagnosis   |
    |---:|-------------:|----------------------:|:------------|
    |  0 |           14 |                    20 | Arthritis   |
    |  1 |           15 |                     2 | Bronchitis  |
    |  2 |           25 |                    20 | Asthma      |
    

## Medium 19
Show first_name, last_name, and the total number of admissions attended for each doctor.

Every admission has been attended by a doctor.


```python
qstr = """
SELECT
  first_name,
  last_name,
  COUNT(*) AS patient_count
FROM admissions
  JOIN doctors ON attending_doctor_id = doctor_id
GROUP BY attending_doctor_id
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.values("attending_doctor_id")
    .annotate(patient_count=Count("attending_doctor_id"))
    .values(
        "patient_count",
        first_name=F("attending_doctor_id__first_name"),
        last_name=F("attending_doctor_id__last_name"),
    )
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT COUNT("admissions"."attending_doctor_id") AS "patient_count",
           "doctors"."first_name" AS "first_name",
           "doctors"."last_name" AS "last_name"
    FROM "admissions"
    INNER JOIN "doctors" ON ("admissions"."attending_doctor_id" = "doctors"."doctor_id")
    GROUP BY "admissions"."attending_doctor_id",
             2,
             3
    


```python
orm_to_df(ormq[:3])
```

    |    |   patient_count | first_name   | last_name   |
    |---:|----------------:|:-------------|:------------|
    |  0 |               8 | Maggie       | Chen        |
    |  1 |               8 | Karen        | Wong        |
    |  2 |               7 | Samuel       | Nguyen      |
    

## Medium 20
For each doctor, display their id, full name, and the first and last admission date they attended.


```python
qstr = """
SELECT
  doctor_id,
  first_name || ' ' || last_name AS full_name,
  MIN(admission_date) AS min_admission,
  MAX(admission_date) AS max_admission
FROM doctors
  JOIN admissions ON attending_doctor_id = doctor_id
GROUP BY doctor_id
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.values("attending_doctor_id")
    .annotate(
        min_admission=Cast(Min("admission_date"), CharField()),
        max_admission=Cast(Max("admission_date"), CharField()),
    )
    .values(
        "min_admission",
        "max_admission",
        doctor_id=F("attending_doctor_id"),
        full_name=Concat(
            F("attending_doctor_id__first_name"),
            Value(" "),
            F("attending_doctor_id__last_name"),
        ),
    )
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT CAST(MIN("admissions"."admission_date") AS text) AS "min_admission",
           CAST(MAX("admissions"."admission_date") AS text) AS "max_admission",
           "admissions"."attending_doctor_id" AS "doctor_id",
           COALESCE("doctors"."first_name",) || COALESCE(COALESCE(,) || COALESCE("doctors"."last_name",),) AS "full_name"
    FROM "admissions"
    INNER JOIN "doctors" ON ("admissions"."attending_doctor_id" = "doctors"."doctor_id")
    GROUP BY 3,
             4
    


```python
orm_to_df(ormq[:3])
```

    |    | min_admission   | max_admission   |   doctor_id | full_name     |
    |---:|:----------------|:----------------|------------:|:--------------|
    |  0 | 2022-01-08      | 2022-06-11      |           1 | Maggie Chen   |
    |  1 | 2022-01-15      | 2022-06-18      |           2 | Karen Wong    |
    |  2 | 2022-01-01      | 2022-05-27      |           3 | Samuel Nguyen |
    

## Medium 21
Display the total amount of patients for each province. Order by descending.


```python
qstr = """
SELECT
  pn.province_name,
  count(patient_id) population
FROM patients p
  JOIN province_names pn ON p.province_id = pn.province_id
GROUP BY pn.province_id
ORDER BY population desc
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values("province")
    .annotate(population=Count("province"))
    .filter(province__name__isnull=False)
    .order_by("-population")
    .values("population", province_name=F("province__name"))
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT COUNT("patients"."province_id") AS "population",
           "province_names"."province_name" AS "province_name"
    FROM "patients"
    INNER JOIN "province_names" ON ("patients"."province_id" = "province_names"."province_id")
    WHERE "province_names"."province_name" IS NOT NULL
    GROUP BY "patients"."province_id",
             2
    ORDER BY 1 DESC
    


```python
orm_to_df(ormq)
```

    |    |   population | province_name    |
    |---:|-------------:|:-----------------|
    |  0 |           25 | British Columbia |
    |  1 |           25 | Ontario          |
    |  2 |           14 | Quebec           |
    |  3 |           13 | Alberta          |
    |  4 |           12 | Manitoba         |
    |  5 |           12 | Nova Scotia      |
    

## Medium 22
For every admission, display the patient's full name, their admission diagnosis, and their doctor's full name who diagnosed their problem.


```python
qstr = """
SELECT
  p.first_name || ' ' || p.last_name AS patient_name,
  diagnosis,
  d.first_name || ' ' || d.last_name AS doctor_name
FROM patients p
  JOIN admissions a ON p.patient_id = a.patient_id
  JOIN doctors d ON a.attending_doctor_id = d.doctor_id
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Admissions.objects.values(
    "diagnosis",
    patient_name=Concat(F("patient__first_name"), Value(" "), F("patient__last_name")),
    doctor_name=Concat(
        F("attending_doctor__first_name"), Value(" "), F("attending_doctor__last_name")
    ),
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."diagnosis",
           COALESCE("patients"."first_name",) || COALESCE(COALESCE(,) || COALESCE("patients"."last_name",),) AS "patient_name",
           COALESCE("doctors"."first_name",) || COALESCE(COALESCE(,) || COALESCE("doctors"."last_name",),) AS "doctor_name"
    FROM "admissions"
    INNER JOIN "patients" ON ("admissions"."patient_id" = "patients"."patient_id")
    INNER JOIN "doctors" ON ("admissions"."attending_doctor_id" = "doctors"."doctor_id")
    


```python
orm_to_df(ormq[:3])
```

    |    | diagnosis   | patient_name     | doctor_name     |
    |---:|:------------|:-----------------|:----------------|
    |  0 | Bronchitis  | Cheryl Mason     | Samuel Nguyen   |
    |  1 | Migraine    | Jason Fleming    | Lisa Tran       |
    |  2 | Pneumonia   | Tiffany McDonald | Catherine Cheng |
    

## Medium 23
display the number of duplicate patients based on their first_name and last_name.


```python
# use YEAR(birth_date) if year function is available
qstr = """
SELECT
  first_name,
  last_name,
  count(*) duplicates
FROM patients
GROUP BY
  first_name,
  last_name
HAVING COUNT(*) > 1
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values("first_name", "last_name")
    .annotate(duplicates=Count("id"))
    .filter(duplicates__gt=1)
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           COUNT("patients"."patient_id") AS "duplicates"
    FROM "patients"
    GROUP BY "patients"."first_name",
             "patients"."last_name"
    HAVING COUNT("patients"."patient_id") > 1
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   |   duplicates |
    |---:|:-------------|:------------|-------------:|
    |  0 | Emma         | Gagnon      |            2 |
    |  1 | Isaac        | Nguyen      |            2 |
    |  2 | Nora         | Singh       |            2 |
    

## Medium 24
Display patient's full name,
height in the units feet rounded to 1 decimal,
weight in the unit pounds rounded to 0 decimals,
birth_date,
gender non abbreviated.

Convert CM to feet by dividing by 30.48.
Convert KG to pounds by multiplying by 2.205.


```python
qstr = """
SELECT
  first_name || ' ' || last_name AS full_name,
  ROUND(height / 30.48, 1) AS height_inc,
  ROUND(weight * 2.205, 0) AS weight_pound,
  birth_date,
  CASE
    WHEN gender = 'M' THEN 'Male'
    WHEN gender = 'F' THEN 'Female'
  END AS gender_full
FROM patients
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.values(
    "birth_date",
    full_name=Concat(F("first_name"), Value(" "), F("last_name")),
    height_inc=Round(F("height") / 30.48, 1),
    weight_pound=Round(F("weight") * 2.205, 0),
    gender_full=Case(
        When(gender="M", then=Value("Male")), When(gender="F", then=Value("Female"))
    ),
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."birth_date",
           COALESCE("patients"."first_name",) || COALESCE(COALESCE(,) || COALESCE("patients"."last_name",),) AS "full_name",
           ROUND(("patients"."height" / 30.48), 1) AS "height_inc",
           ROUND(("patients"."weight" * 2.205), 0) AS "weight_pound",
           CASE
               WHEN "patients"."gender" = M THEN Male
               WHEN "patients"."gender" = F THEN Female
               ELSE NULL
           END AS "gender_full"
    FROM "patients"
    


```python
orm_to_df(ormq[:3])
```

    |    | birth_date   | full_name        |   height_inc |   weight_pound | gender_full   |
    |---:|:-------------|:-----------------|-------------:|---------------:|:--------------|
    |  0 | 1978-05-14   | Cheryl Mason     |          5.6 |            143 | Female        |
    |  1 | 1990-08-02   | Jason Fleming    |          6.1 |            176 | Male          |
    |  2 | 1985-03-27   | Tiffany McDonald |          5.1 |            128 | Female        |
    

## Medium 25
Show patient_id, first_name, last_name from patients whose does not have any records in the admissions table. (Their patient_id does not exist in any admissions.patient_id rows.)


```python
qstr = """
SELECT
  patient_id,
  first_name,
  last_name
FROM patients
WHERE patient_id NOT IN (
    SELECT patient_id
    FROM admissions
  )
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(
    ~Q(id__in=Subquery(Admissions.objects.values("patient_id")))
).values(
    "first_name",
    "last_name",
    patient_id=F("id"),
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."patient_id" AS "patient_id"
    FROM "patients"
    WHERE NOT ("patients"."patient_id" IN
                 (SELECT U0."patient_id"
                  FROM "admissions" U0))
    


```python
orm_to_df(sqlq)
```

    |    |   patient_id | first_name   | last_name   |
    |---:|-------------:|:-------------|:------------|
    |  0 |          101 | Edward       | Kenway      |
    
