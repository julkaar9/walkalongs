# SQL-PRACTICE easy exercises using Django ORM
[https://www.sql-practice.com/](https://www.sql-practice.com/)

This walkalong consists of easy questions and their solutions from sql-practice.com, written in both **SQL** and **django
ORM**, They query results are also compared for equality.  
Insert, Update and Delete queries are not included to keep database consistent.

## Try it yourself
The notebook (Django Shell-plus) is located in [here](https://github.com/julkaar9/walkalongs/blob/main/server/notebooks/sql-practice-easy-practice.ipynb)   
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
from django.db.models.functions import Concat, Cast, Round, Length
from django.db import connection
from customer_db.models import Provinces, Patients, Doctors, Admissions
```


```python
def print_sql(queryset):
    formatted = format(str(queryset.query), reindent=True)
    print(formatted)
```

## Testing some basic queries


```python
sqlq = sql_raw("SELECT * FROM Patients LIMIT 3") 
```

```python
common_fields = [
    "first_name",
    "last_name",
    "gender",
    "birth_date",
    "city",
    "province_id",
    "allergies",
    "height",
    "weight",
]
```


```python
ormq = Patients.objects.values(patient_id=F("id"), *common_fields)[:3]
orm_to_df(ormq)
```

    |    | first_name   | last_name   | gender   | birth_date   | city      | province_id   | allergies   |   height |   weight |   patient_id |
    |---:|:-------------|:------------|:---------|:-------------|:----------|:--------------|:------------|---------:|---------:|-------------:|
    |  0 | Cheryl       | Mason       | F        | 1978-05-14   | Toronto   | ON            | Peanuts     |      170 |       65 |            1 |
    |  1 | Jason        | Fleming     | M        | 1990-08-02   | Vancouver | BC            | Sulfa drugs |      185 |       80 |            2 |
    |  2 | Tiffany      | McDonald    | F        | 1985-03-27   | Calgary   | AB            | Lactose     |      155 |       58 |            3 |
    


```python
equal(sqlq, ormq)
```

    Equal ✔️
    

## Easy 1
Show first name, last name, and gender of patients who's gender is 'M'


```python
qstr = """
SELECT
  first_name,
  last_name,
  gender
FROM Patients
WHERE gender = 'M';
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(gender="M").values("first_name", "last_name", "gender")
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."gender"
    FROM "patients"
    WHERE "patients"."gender" = M
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   | gender   |
    |---:|:-------------|:------------|:---------|
    |  0 | Jason        | Fleming     | M        |
    |  1 | Alex         | Carter      | M        |
    |  2 | Gavin        | Bryant      | M        |
    

## Easy 2
Show first name and last name of patients who does not have allergies. (null)


```python
qstr = """
SELECT
  first_name,
  last_name
FROM Patients
WHERE allergies IS NULL;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(allergies=None).values("first_name", "last_name")
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name"
    FROM "patients"
    WHERE "patients"."allergies" IS NULL
    


```python
ormq1 = Patients.objects.filter(allergies__isnull=True).values(
    "first_name", "last_name"
)
equal(sqlq, ormq1)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name"
    FROM "patients"
    WHERE "patients"."allergies" IS NULL
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   |
    |---:|:-------------|:------------|
    |  0 | Alex         | Carter      |
    |  1 | Adam         | Nguyen      |
    |  2 | Shane        | Simpson     |
    

## Easy 3
Show first name of patients that start with the letter 'C'


```python
qstr = """
SELECT first_name
FROM Patients
WHERE first_name LIKE 'C%';
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(first_name__startswith="C").values("first_name")
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name"
    FROM "patients"
    WHERE "patients"."first_name" LIKE C% ESCAPE '\'
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   |
    |---:|:-------------|
    |  0 | Cheryl       |
    |  1 | Cassandra    |
    |  2 | Cameron      |
    

## Easy 4
Show first name and last name of patients that weight within the range of 100 to 120 (inclusive)
We will do 70 - 80


```python
qstr = """
SELECT
  first_name,
  last_name
FROM Patients
WHERE weight BETWEEN 70 AND 80;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(weight__range=[70, 80]).values("first_name", "last_name")
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name"
    FROM "patients"
    WHERE "patients"."weight" BETWEEN 70 AND 80
    


```python
ormq1 = Patients.objects.filter(weight__gte=70, weight__lte=80).values(
    "first_name", "last_name"
)
equal(sqlq, ormq1)
print_sql(ormq1)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name"
    FROM "patients"
    WHERE ("patients"."weight" >= 70
           AND "patients"."weight" <= 80)
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   |
    |---:|:-------------|:------------|
    |  0 | Jason        | Fleming     |
    |  1 | Alex         | Carter      |
    |  2 | Gavin        | Bryant      |
    

## Easy 5
Show first name and last name concatinated into one column to show their full name.


```python
qstr = """
SELECT
  first_name || ' ' || last_name AS full_name
FROM patients;
"""
sqlq = sql_raw(qstr)
```


```python
# sqlq =  sql_raw("SELECT CONCAT(first_name,' ', last_name) full_name FROM Patients;")

ormq = Patients.objects.values(full_name=Concat("first_name", Value(" "), "last_name"))
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT COALESCE("patients"."first_name",) || COALESCE(COALESCE(,) || COALESCE("patients"."last_name",),) AS "full_name"
    FROM "patients"
    


```python
orm_to_df(ormq[:3])
```

    |    | full_name        |
    |---:|:-----------------|
    |  0 | Cheryl Mason     |
    |  1 | Jason Fleming    |
    |  2 | Tiffany McDonald |
    

## Easy 6
Show first name, last name, and the **full** province name of each patient.

Example: 'Ontario' instead of 'ON'


```python
qstr = """
SELECT
  first_name,
  last_name,
  province_name
FROM Patients p
  INNER JOIN province_names pn ON p.province_id = pn.province_id;
"""
sqlq = sql_raw(qstr)
```


```python
# The filter ensures an Inner join is performed
ormq = Patients.objects.filter(province__isnull=False).values(
    "first_name", "last_name", province_name=F("province__name")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "province_names"."province_name" AS "province_name"
    FROM "patients"
    INNER JOIN "province_names" ON ("patients"."province_id" = "province_names"."province_id")
    WHERE "patients"."province_id" IS NOT NULL
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   | province_name    |
    |---:|:-------------|:------------|:-----------------|
    |  0 | Cheryl       | Mason       | Ontario          |
    |  1 | Jason        | Fleming     | British Columbia |
    |  2 | Tiffany      | McDonald    | Alberta          |
    

## Easy 7
Show how many patients have a birth_date with 2010 as the birth year.
We will do 1995


```python
# sqlq =  sql_raw("SELECT COUNT(*) birth_year FROM Patients WHERE YEAR(birth_date) = 2010;")

# for sqlite (Notice the '1995' instead of 1995)
qstr = """
SELECT COUNT(*) AS birth_count
FROM Patients
WHERE strftime('%Y', birth_date) = '1995';
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.filter(birth_date__year=1995)
    .annotate(birth_count=Func(F("id"), function="Count"))
    .values("birth_count")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT Count("patients"."patient_id") AS "birth_count"
    FROM "patients"
    WHERE "patients"."birth_date" BETWEEN 1995-01-01 AND 1995-12-31
    


```python
ormq = Patients.objects.filter(birth_date__year=1995).aggregate(
    birth_count=Count("birth_date")
)
print(ormq)
equal(sqlq, ormq)
```

    {'birth_count': 5}
    Equal ✔️
    


```python
ormq1 = Patients.objects.filter(birth_date__year=1995).count()
ormq1 = [{"birth_count": ormq1}]
equal(sqlq, ormq1)
```

    Equal ✔️
    


```python
orm_to_df(ormq)
```

    |    |   birth_count |
    |---:|--------------:|
    |  0 |             5 |
    

## Easy 8
Show the first_name, last_name, and height of the patient with the greatest height.


```python
qstr = """
SELECT
  first_name,
  last_name,
  Max(height) AS max_height
FROM patients;
"""
sqlq = sql_raw(qstr)
```


```python
# Subclassing Max and setting contains_aggregate = False also works
# class NonAggrMax(Max):
#     contains_aggregate = False

ormq = Patients.objects.annotate(max_height=Func("height", function="Max")).values(
    "first_name", "last_name", "max_height"
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           Max("patients"."height") AS "max_height"
    FROM "patients"
    


```python
orm_to_df(ormq)
```

    |    | first_name   | last_name   |   max_height |
    |---:|:-------------|:------------|-------------:|
    |  0 | Cameron      | Gupta       |          190 |
    

## Easy 9
Show all columns for patients who have one of the following patient_ids:
1,45,534,879,1000
We will use 1,45,53,87,100


```python
qstr = """
SELECT
  *
FROM patients
WHERE patient_id IN (1, 45, 53, 87, 100);
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(id__in=[1, 45, 53, 87, 100]).values(
    patient_id=F("id"), *common_fields
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."gender",
           "patients"."birth_date",
           "patients"."city",
           "patients"."province_id",
           "patients"."allergies",
           "patients"."height",
           "patients"."weight",
           "patients"."patient_id" AS "patient_id"
    FROM "patients"
    WHERE "patients"."patient_id" IN (1,
                                      45,
                                      53,
                                      87,
                                      100)
    


```python
orm_to_df(ormq)
```

    |    | first_name   | last_name   | gender   | birth_date   | city     | province_id   | allergies   |   height |   weight |   patient_id |
    |---:|:-------------|:------------|:---------|:-------------|:---------|:--------------|:------------|---------:|---------:|-------------:|
    |  0 | Cheryl       | Mason       | F        | 1978-05-14   | Toronto  | ON            | Peanuts     |      170 |       65 |            1 |
    |  1 | Ella         | Lemieux     | F        | 1991-05-01   | Halifax  | NS            | Lactose     |      164 |       60 |           45 |
    |  2 | Avery        | Roy         | F        | 1993-05-08   | Halifax  | NS            |             |      165 |       61 |           53 |
    |  3 | Avery        | Chen        | F        | 1989-12-07   | Winnipeg | MB            |             |      163 |       58 |           87 |
    |  4 | Nathan       | Gupta       | M        | 1986-01-14   | Victoria | BC            | Lactose     |      184 |       82 |          100 |
    

## Easy 10
Show the total number of admissions


```python
sqlq = sql_raw("SELECT COUNT(*) AS total FROM admissions;")
ormq = Admissions.objects.aggregate(total=Count("id"))
equal(sqlq, ormq)
```

    Equal ✔️
    


```python
ormq1 = Admissions.objects.count()
ormq1 = [{"total": ormq1}]
equal(sqlq, ormq1)
```

    Equal ✔️
    


```python
orm_to_df(ormq)
```

    |    |   total |
    |---:|--------:|
    |  0 |     170 |
    

## Easy 11
Show all the columns from admissions where the patient was admitted and discharged on the same day.


```python
qstr = """
SELECT *
FROM admissions
WHERE admission_date = discharge_date;
"""
sqlq = sql_raw(qstr)
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
ormq = Admissions.objects.filter(admission_date=F("discharge_date")).values(
    *admission_fields
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
    WHERE "admissions"."admission_date" = ("admissions"."discharge_date")
    


```python
orm_to_df(ormq[:3])
```

    |    |   id |   patient_id | admission_date   | discharge_date   | diagnosis       |   attending_doctor_id |
    |---:|-----:|-------------:|:-----------------|:-----------------|:----------------|----------------------:|
    |  0 |  159 |           59 | 2022-06-07       | 2022-06-07       | Meningitis      |                     5 |
    |  1 |  160 |           60 | 2022-06-08       | 2022-06-08       | Anemia          |                    12 |
    |  2 |  162 |           62 | 2022-06-10       | 2022-06-10       | Gastroenteritis |                    16 |
    

## Easy 12
Show the patient id and the total number of admissions for patient_id 579.
We will do 57


```python
qstr = """
SELECT
  patient_id,
  Count(patient_id) admissions
FROM admissions
WHERE patient_id = 57;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.filter(patient_id=57)
    .annotate(admissions=Func(F("patient_id"), function="Count"))
    .values("patient_id", "admissions")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."patient_id",
           Count("admissions"."patient_id") AS "admissions"
    FROM "admissions"
    WHERE "admissions"."patient_id" = 57
    


```python
orm_to_df(ormq[:3])
```

    |    |   patient_id |   admissions |
    |---:|-------------:|-------------:|
    |  0 |           57 |            2 |
    

## Easy 13
Based on the cities that our patients live in, show unique cities that are in province_id 'NS'?


```python
qstr = """
SELECT DISTINCT city
FROM patients
WHERE province_id = 'NS';
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(province__id="NS").values("city").distinct()
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT DISTINCT "patients"."city"
    FROM "patients"
    WHERE "patients"."province_id" = NS
    


```python
orm_to_df(ormq)
```

    |    | city    |
    |---:|:--------|
    |  0 | Halifax |
    

## Easy 14
Write a query to find the first_name, last name and birth date of patients who has height greater than 160 and weight greater than 70


```python
qstr = """
SELECT
  first_name,
  last_name,
  birth_date
FROM patients
WHERE height > 160 AND weight > 70;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(height__gt=160, weight__gt=70).values(
    "first_name", "last_name", "birth_date"
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."birth_date"
    FROM "patients"
    WHERE ("patients"."height" > 160
           AND "patients"."weight" > 70)
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   | birth_date   |
    |---:|:-------------|:------------|:-------------|
    |  0 | Jason        | Fleming     | 1990-08-02   |
    |  1 | Alex         | Carter      | 1976-11-18   |
    |  2 | Gavin        | Bryant      | 1980-02-06   |
    

## Easy 15
Write a query to find list of patients first_name, last_name, and allergies from Hamilton where allergies are not null.
We will use Toronto


```python
qstr = """
SELECT
  first_name,
  last_name,
  allergies
FROM patients
WHERE
  city = 'Toronto'
  AND allergies IS NOT NULL;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(city="Toronto", allergies__isnull=False).values(
    "first_name", "last_name", "allergies"
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."allergies"
    FROM "patients"
    WHERE ("patients"."allergies" IS NOT NULL
           AND "patients"."city" = Toronto)
    


```python
ormq1 = Patients.objects.filter(
    ~Q(allergies=None),
    city="Toronto",
).values("first_name", "last_name", "allergies")
equal(sqlq, ormq1)
print_sql(ormq1)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."allergies"
    FROM "patients"
    WHERE (NOT ("patients"."allergies" IS NULL)
           AND "patients"."city" = Toronto)
    


```python
ormq2 = (
    Patients.objects.filter(city="Toronto")
    .exclude(allergies=None)
    .values("first_name", "last_name", "allergies")
)
equal(sqlq, ormq2)
print_sql(ormq2)
```

    Equal ✔️
    SELECT "patients"."first_name",
           "patients"."last_name",
           "patients"."allergies"
    FROM "patients"
    WHERE ("patients"."city" = Toronto
           AND NOT ("patients"."allergies" IS NULL))
    


```python
orm_to_df(ormq[:3])
```

    |    | first_name   | last_name   | allergies   |
    |---:|:-------------|:------------|:------------|
    |  0 | Cheryl       | Mason       | Peanuts     |
    |  1 | Kimberly     | Lee         | Pollen      |
    |  2 | Maria        | Singh       | Pollen      |
    

## Easy 16
Based on cities where our patient lives in, write a query to display the list of unique city starting with a vowel (a, e, i, o, u). Show the result order in ascending by city.


```python
# You can use city LIKE '[aeiou]%'
# We are doing case insensitve matching here.
qstr = """
SELECT DISTINCT city
FROM patients
WHERE
  city LIKE 'a%'
  OR city LIKE 'e%'
  OR city LIKE 'i%'
  OR city LIKE 'o%'
  OR city LIKE 'u%'
ORDER BY city;
"""
sqlq = sql_raw(qstr)
```


```python
query = Q()
for ch in ["a", "e", "i", "o", "u"]:
    query |= Q(city__istartswith=ch)
ormq = Patients.objects.filter(query).values("city").distinct().order_by("city")
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT DISTINCT "patients"."city"
    FROM "patients"
    WHERE ("patients"."city" LIKE a% ESCAPE '\' OR "patients"."city" LIKE e% ESCAPE '\' OR "patients"."city" LIKE i% ESCAPE '\' OR "patients"."city" LIKE o% ESCAPE '\' OR "patients"."city" LIKE u% ESCAPE '\')
    ORDER BY "patients"."city" ASC
    


```python
ormq1 = (
    Patients.objects.filter(city__regex=r"(?i)^[aeiou].+")
    .values("city")
    .distinct()
    .order_by("city")
)
equal(sqlq, ormq1)
print_sql(ormq1)
```

    Equal ✔️
    SELECT DISTINCT "patients"."city"
    FROM "patients"
    WHERE "patients"."city" REGEXP (?i)^[aeiou].+
    ORDER BY "patients"."city" ASC
    


```python
orm_to_df(ormq1)
```

    |    | city   |
    |---:|:-------|
    |  0 | Ottawa |
    
