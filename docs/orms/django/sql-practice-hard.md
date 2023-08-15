# SQL-PRACTICE hard exercises using Django ORM
[https://www.sql-practice.com/](https://www.sql-practice.com/)

This walkalong consists of hard questions and their solutions from sql-practice.com, written in both **SQL** and **django
ORM**, They query results are also compared for equality.  
Insert, Update and Delete queries are not included to keep database consistent.

## Try it yourself
The notebook (Django Shell-plus) is located in [here](https://github.com/julkaar9/walkalongs/blob/main/server/notebooks/sql-practice-hard-practice.ipynb)   
First cd into the notebook directory `cd server/notebook`  
Then open the notebook using `python ../manage.py shell_plus --notebook`  

```python
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from utils import *
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
    Window,
    CharField,
    FloatField,
)
from django.db.models.lookups import Exact, GreaterThanOrEqual
from django.db.models.functions import Concat, Cast, Round, Length, Lag
from django.db import connection
from customer_db.models import Provinces, Patients, Doctors, Admissions
```


```python
def orm_to_df(record: any) -> pd.DataFrame:
    try:
        iter(record)
    except:
        record = [record]
    if isinstance(record, dict):
        record = [record]
    df = pd.DataFrame.from_records(record)
    print(df.to_markdown())
```


```python
patient_fields = [
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

## Hard 1

Show all of the patients grouped into weight groups.
Show the total amount of patients in each weight group.
Order the list by the weight group decending.

For example, if they weight 100 to 109 they are placed in the 100 weight group, 110-119 = 110 weight group, etc.


```python
qstr = """
SELECT
  ROUND(weight / 10, 0) * 10 AS weight_class,
  COUNT(patient_id) AS patient_count
FROM patients
GROUP BY weight_class
ORDER BY weight_class DESC
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values(weight_class=Round(F("weight") / 10, 0) * 10)
    .annotate(patient_count=Count("id"))
    .order_by("-weight_class")
    .values("weight_class", "patient_count")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT (ROUND(("patients"."weight" / 10), 0) * 10) AS "weight_class",
           COUNT("patients"."patient_id") AS "patient_count"
    FROM "patients"
    GROUP BY 1
    ORDER BY 1 DESC
    


```python
orm_to_df(ormq[:3])
```

    |    |   weight_class |   patient_count |
    |---:|---------------:|----------------:|
    |  0 |             90 |               1 |
    |  1 |             80 |              20 |
    |  2 |             70 |              29 |
    

## Hard 2
Show patient_id, weight, height, isObese from the patients table.

Display isObese as a boolean 0 or 1.
Obese is defined as weight(kg)/(height(m)2) >= 30.
weight is in units kg.
height is in units cm.

We will do 24


```python
qstr = """
SELECT
  patient_id AS id,
  weight,
  height,
  CASE
    WHEN weight * 10000/ (height * height) >= 24 THEN 1
    ELSE 0
  END AS isObese
FROM patients
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.annotate(
    tmp_weight=F("weight") * 10000 / (F("height") * F("height"))
).values(
    "id", "weight", "height", isObese=Case(When(tmp_weight__gte=24, then=1), default=0)
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."patient_id",
           "patients"."weight",
           "patients"."height",
           CASE
               WHEN (("patients"."weight" * 10000) / ("patients"."height" * "patients"."height")) >= 24 THEN 1
               ELSE 0
           END AS "isObese"
    FROM "patients"
    


```python
orm_to_df(ormq[:3])
```

    |    |   id |   weight |   height |   isObese |
    |---:|-----:|---------:|---------:|----------:|
    |  0 |    1 |       65 |      170 |         0 |
    |  1 |    2 |       80 |      185 |         0 |
    |  2 |    3 |       58 |      155 |         1 |
    

## Hard 3
Show patient_id, first_name, last_name, and attending doctor's specialty.
Show only the patients who has a diagnosis as 'Epilepsy' and the doctor's first name is 'Lisa'

Check patients, admissions, and doctors tables for required information.
We will do 'Anemia'


```python
qstr = """
SELECT
  p.patient_id,
  p.first_name,
  p.last_name,
  speciality
FROM admissions AS a
  JOIN patients p ON p.patient_id = a.patient_id
  JOIN doctors d ON a.attending_doctor_id = d.doctor_id
WHERE
  diagnosis = 'Anemia'
  and d.first_name = 'Lisa'
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Admissions.objects.filter(
    diagnosis="Anemia", attending_doctor__first_name="Lisa"
).values(
    "patient_id",
    first_name=F("patient__first_name"),
    last_name=F("patient__last_name"),
    speciality=F("attending_doctor__speciality"),
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."patient_id",
           "patients"."first_name" AS "first_name",
           "patients"."last_name" AS "last_name",
           "doctors"."speciality" AS "speciality"
    FROM "admissions"
    INNER JOIN "doctors" ON ("admissions"."attending_doctor_id" = "doctors"."doctor_id")
    INNER JOIN "patients" ON ("admissions"."patient_id" = "patients"."patient_id")
    WHERE ("doctors"."first_name" = Lisa
           AND "admissions"."diagnosis" = Anemia)
    


```python
orm_to_df(ormq[:3])
```

    |    |   patient_id | first_name   | last_name   | speciality    |
    |---:|-------------:|:-------------|:------------|:--------------|
    |  0 |           51 | Isabelle     | Lee         | Endocrinology |
    

## Hard 4
All patients who have gone through admissions, can see their medical documents on our site. Those patients are given a temporary password after their first admission. Show the patient_id and temp_password.

The password must be the following, in order:
1. patient_id
2. the numerical length of patient's last_name
3. year of patient's birth_date


```python
# use YEAR(birth_date) in other databases
qstr = """
SELECT
  p.patient_id,
  p.patient_id || LENGTH(last_name) || strftime('%Y', birth_date) AS temp_password
FROM patients p
WHERE patient_id IN (
    SELECT DISTINCT(patient_id)
    FROM admissions
  )
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Patients.objects.filter(
    id__in=Subquery(Admissions.objects.values("patient_id").distinct())
).values(
    patient_id=F("id"),
    temp_password=Cast(
        Concat("id", Length("last_name"), "birth_date__year"), CharField()
    ),
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "patients"."patient_id" AS "patient_id",
           CAST(COALESCE("patients"."patient_id",) || COALESCE(COALESCE(LENGTH("patients"."last_name"),) || COALESCE(django_date_extract(year, "patients"."birth_date"),),) AS text) AS "temp_password"
    FROM "patients"
    WHERE "patients"."patient_id" IN
        (SELECT DISTINCT U0."patient_id"
         FROM "admissions" U0)
    


```python
ormq1 = (
    Patients.objects.filter(admissions__admission_date__isnull=False)
    .values(
        patient_id=F("admissions__patient_id"),
        temp_password=Cast(
            Concat("id", Length("last_name"), "birth_date__year"), CharField()
        ),
    )
    .distinct()
)
equal(sqlq, ormq1, True)
print_sql(ormq1)
```

    Equal ✔️
    SELECT DISTINCT "admissions"."patient_id" AS "patient_id",
                    CAST(COALESCE("patients"."patient_id",) || COALESCE(COALESCE(LENGTH("patients"."last_name"),) || COALESCE(django_date_extract(year, "patients"."birth_date"),),) AS text) AS "temp_password"
    FROM "patients"
    INNER JOIN "admissions" ON ("patients"."patient_id" = "admissions"."patient_id")
    WHERE "admissions"."admission_date" IS NOT NULL
    


```python
orm_to_df(ormq[:3])
```

    |    |   patient_id |   temp_password |
    |---:|-------------:|----------------:|
    |  0 |            1 |          151978 |
    |  1 |            2 |          271990 |
    |  2 |            3 |          381985 |
    

## Hard 5
Each admission costs \\$50 for patients without insurance, and \\$10 for patients with insurance. All patients with an even patient_id have insurance.

Give each patient a 'Yes' if they have insurance, and a 'No' if they don't have insurance. Add up the admission_total cost for each has_insurance group.


```python
qstr = """
SELECT has_insurance, SUM(insurance_cost) AS total_insurance_cost
FROM(
    SELECT
      CASE
        WHEN patient_id % 2 = 0 THEN "Yes"
        ELSE "No"
      END AS has_insurance,
      CASE
        WHEN patient_id % 2 = 0 THEN 10
        ELSE 50
      END AS insurance_cost
    FROM admissions
  )
GROUP BY has_insurance;
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.values(
        has_insurance=Case(
            When(Exact(F("id") % 2, 0), then=Value("Yes")), default=Value("No")
        ),
        insurance_cost=Case(When(Exact(F("patient_id") % 2, 0), then=10), default=50),
    )
    .annotate(total_insurance_cost=Sum("insurance_cost"))
    .values("has_insurance", "total_insurance_cost")
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT CASE
               WHEN ("admissions"."id" % 2) = (0) THEN Yes
               ELSE No
           END AS "has_insurance",
           SUM(CASE
                   WHEN ("admissions"."patient_id" % 2) = (0) THEN 10
                   ELSE 50
               END) AS "total_insurance_cost"
    FROM "admissions"
    GROUP BY 1,
             CASE
                 WHEN ("admissions"."patient_id" % 2) = (0) THEN 10
                 ELSE 50
             END
    


```python
ormq1 = (
    Admissions.objects.values(has_insurance=Value("Yes"))
    .filter(Exact(F("id")%2, 0))
    .annotate(total_insurance_cost=Count("has_insurance") * 10)
    .values("has_insurance", "total_insurance_cost")
    .union(
        Admissions.objects.values(has_insurance=Value("No"))
        .filter(Exact(F("id")%2, 1))
        .annotate(total_insurance_cost=Count("has_insurance") * 50)
        .values("has_insurance", "total_insurance_cost")
    )
)


equal(sqlq, ormq1, True)
print_sql(ormq1)
```

    Equal ✔️
    SELECT Yes AS "has_insurance",
           (COUNT(Yes) * 10) AS "total_insurance_cost"
    FROM "admissions"
    WHERE ("admissions"."id" % 2) = (0)
    UNION
    SELECT No AS "has_insurance",
                 (COUNT(No) * 50) AS "total_insurance_cost"
    FROM "admissions"
    WHERE ("admissions"."id" % 2) = (1)
    


```python
orm_to_df(ormq[:3])
```

    |    | has_insurance   |   total_insurance_cost |
    |---:|:----------------|-----------------------:|
    |  0 | No              |                   4250 |
    |  1 | Yes             |                    850 |
    

## Hard 6
Show the provinces that has more patients identified as 'M' than 'F'. Must only show full province_name


```python
qstr = """
SELECT pr.province_name
FROM patients AS pa
  JOIN province_names AS pr ON pa.province_id = pr.province_id
GROUP BY pr.province_name
HAVING SUM(gender = 'M') > SUM(gender = 'F')
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.values("province__name")
    .annotate(female=Sum(Q(gender="F")), male=Sum(Q(gender="M")))
    .filter(male__gt=F("female"), province__name__isnull=False)
    .values(province_name=F("province__name"))
)

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "province_names"."province_name" AS "province_name"
    FROM "patients"
    INNER JOIN "province_names" ON ("patients"."province_id" = "province_names"."province_id")
    WHERE "province_names"."province_name" IS NOT NULL
    GROUP BY 1
    HAVING SUM(("patients"."gender" = M)) > (SUM("patients"."gender" = F))
    


```python
orm_to_df(ormq[:3])
```

    |    | province_name   |
    |---:|:----------------|
    |  0 | Manitoba        |
    |  1 | Ontario         |
    |  2 | Quebec          |
    

## Hard 7

We are looking for a specific patient. Pull all columns for the patient who matches the following criteria:
- First_name contains an 'r' after the first two letters.
- Identifies their gender as 'F' (We will do 'M')
- Born in February, May, or December
- Their weight would be between 60kg and 80kg
- Their patient_id is an odd number  (We will do even)
- They are from the city 'Kingston'  (We will do 'Vancouver')


```python
qstr = """
SELECT *
FROM patients
WHERE
  first_name LIKE "__r%"
  AND gender = 'M'
  AND (
    CAST(strftime('%m', birth_date) AS INT) IN (2, 5, 12)
  )
  AND weight between 60 AND 80
  AND patient_id % 2 = 0
  AND city = 'Vancouver'
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Patients.objects.filter(
        Exact(F("id") % 2, 0),
        first_name__regex=r"(?i)^\w{2,}r\w*$",
        gender="M",
        birth_date__month__in=(2, 5, 12),
        weight__range=(60, 80),
        city="Vancouver",
    )
).values(patient_id=F("id"), *patient_fields)
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
    WHERE (("patients"."patient_id" % 2) = (0)
           AND django_date_extract(month, "patients"."birth_date") IN (2,
                                                                       5,
                                                                       12)
           AND "patients"."city" = Vancouver
           AND "patients"."first_name" REGEXP (?i)^\w{2,}r\w*$
           AND "patients"."gender" = M
           AND "patients"."weight" BETWEEN 60 AND 80)
    


```python
orm_to_df(ormq)
```

    |    | first_name   | last_name   | gender   | birth_date   | city      | province_id   | allergies   |   height |   weight |   patient_id |
    |---:|:-------------|:------------|:---------|:-------------|:----------|:--------------|:------------|---------:|---------:|-------------:|
    |  0 | Jared        | Taylor      | M        | 1986-02-20   | Vancouver | BC            |             |      178 |       75 |           34 |
    

## Hard 8
Show the percent of patients that have 'M' as their gender. Round the answer to the nearest hundreth number and in percent form.


```python
qstr = """
SELECT
  ROUND(
    CAST(AVG(gender = 'M') as FLOAT)  * 100,
    2
  ) || '%' AS pct
FROM patients
"""
sqlq = sql_raw(qstr)
```


```python
class NonAggrAvg(Avg):
    contains_aggregate = False


ormq = Patients.objects.annotate(
    pct=Concat(
        Cast(
            Round(NonAggrAvg(Q(gender="M"), output_field=FloatField()) * 100, 2),
            CharField(),
        ),
        Value("%"),
    )
).values("pct")

equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT COALESCE(CAST(ROUND((AVG("patients"."gender" = M) * 100), 2) AS text),) || COALESCE(%,) AS "pct"
    FROM "patients"
    


```python
orm_to_df(ormq)
```

    |    | pct   |
    |---:|:------|
    |  0 | 49.5% |
    

## Hard 9
For each day display the total amount of admissions on that day. Display the amount changed from the previous date.


```python
qstr = """
SELECT
  admission_date,
  daily_admissions,
  daily_admissions - prev_admissions AS admission_diff
FROM (
    SELECT
      admission_date,
      COUNT(*) daily_admissions,
      LAG(count(*), 1) OVER (
        ORDER BY
          admission_date
      ) AS prev_admissions
    FROM admissions
    GROUP BY admission_date
  )
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.values("admission_date")
    .annotate(daily_admissions=Count("patient_id"))
    .values(
        "admission_date",
        "daily_admissions",
        admission_diff=F("daily_admissions") - Window(Lag("daily_admissions")),
    )
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "admissions"."admission_date",
           COUNT("admissions"."patient_id") AS "daily_admissions",
           (COUNT("admissions"."patient_id") - LAG(COUNT("admissions"."patient_id"), 1) OVER ()) AS "admission_diff"
    FROM "admissions"
    GROUP BY "admissions"."admission_date"
    


```python
orm_to_df(ormq[:3])
```

    |    | admission_date   |   daily_admissions |   admission_diff |
    |---:|:-----------------|-------------------:|-----------------:|
    |  0 | 2022-01-01       |                  1 |              nan |
    |  1 | 2022-01-02       |                  1 |                0 |
    |  2 | 2022-01-03       |                  1 |                0 |
    

## Hard 10
Show the total number of admissions


```python
qstr = """
select province_name
from province_names
order by
  province_name = 'Ontario' desc,
  province_name
"""
sqlq = sql_raw(qstr)
```


```python
ormq = Provinces.objects.order_by(Exact(F("name"), "Ontario").desc(), "name").values(
    province_name=F("name")
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT "province_names"."province_name" AS "province_name"
    FROM "province_names"
    ORDER BY "province_names"."province_name" = (Ontario) DESC, "province_names"."province_name" ASC
    


```python
orm_to_df(ormq[:3])
```

    |    | province_name    |
    |---:|:-----------------|
    |  0 | Ontario          |
    |  1 | Alberta          |
    |  2 | British Columbia |
    

## Hard 11
We need a breakdown for the total amount of admissions each doctor has started each year. Show the doctor_id, doctor_full_name, specialty, year, total_admissions for that year.


```python
qstr = """
SELECT
  doctor_id,
  first_name || ' ' || last_name AS full_name,
  speciality,
  CAST(strftime('%Y', admission_date) AS INT) AS current_year,
  Count(strftime('%Y', admission_date)) AS patients_attended
FROM admissions a
  JOIN doctors d ON a.attending_doctor_id = d.doctor_id
GROUP BY current_year, doctor_id
"""
sqlq = sql_raw(qstr)
```


```python
ormq = (
    Admissions.objects.values("admission_date__year", "attending_doctor_id")
    .annotate(patients_attended=Count("admission_date__year"))
    .values(
        "patients_attended",
        doctor_id=F("attending_doctor_id"),
        full_name=Concat(
            "attending_doctor__first_name", Value(" "), "attending_doctor__last_name"
        ),
        speciality=F("attending_doctor__speciality"),
        current_year=F("admission_date__year"),
    )
)
equal(sqlq, ormq)
print_sql(ormq)
```

    Equal ✔️
    SELECT COUNT(django_date_extract(year, "admissions"."admission_date")) AS "patients_attended",
           "admissions"."attending_doctor_id" AS "doctor_id",
           COALESCE("doctors"."first_name",) || COALESCE(COALESCE(,) || COALESCE("doctors"."last_name",),) AS "full_name",
           "doctors"."speciality" AS "speciality",
           django_date_extract(year, "admissions"."admission_date") AS "current_year"
    FROM "admissions"
    INNER JOIN "doctors" ON ("admissions"."attending_doctor_id" = "doctors"."doctor_id")
    GROUP BY 2,
             5,
             3,
             4
    


```python
orm_to_df(ormq[:3])
```

    |    |   patients_attended |   doctor_id | full_name     | speciality   |   current_year |
    |---:|--------------------:|------------:|:--------------|:-------------|---------------:|
    |  0 |                   8 |           1 | Maggie Chen   | Cardiology   |           2022 |
    |  1 |                   8 |           2 | Karen Wong    | Neurology    |           2022 |
    |  2 |                   7 |           3 | Samuel Nguyen | Dermatology  |           2022 |
    
