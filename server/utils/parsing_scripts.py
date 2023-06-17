import json


def admission(fields, i):
    patient_id = int(i + 1) % 100
    if patient_id == 0:
        patient_id = 100
    admission_date = fields[1].strip().strip("'")
    discharge_date = fields[2].strip().strip("'")
    diagnosis = fields[3].strip().strip("'")
    attending_doctor_id = int(fields[4][2:])

    row = {
        "model": "customer_db.admissions",
        "pk": int(i + 1),
        "fields": {
            "patient_id": patient_id,
            "admission_date": admission_date,
            "discharge_date": discharge_date,
            "diagnosis": diagnosis,
            "attending_doctor_id": attending_doctor_id,
        },
    }
    return row


def patients(fields, i):
    patient_id = int(i + 1)
    first_name = fields[1].strip().strip("'")
    last_name = fields[2].strip().strip("'")
    gender = fields[3].strip().strip("'")
    birth_date = fields[4].strip().strip("'")
    city = fields[5].strip().strip("'")
    province_id = fields[6].strip().strip("'")
    allergies = fields[7].strip().strip("'")
    height = int(fields[8])
    weight = int(fields[9])
    row = {
        "model": "customer_db.patients",
        "pk": patient_id,
        "fields": {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "birth_date": birth_date,
            "province_id": province_id,
            "city": city,
            "allergies": allergies,
            "height": height,
            "weight": weight,
        },
    }
    return row


def doctors(fields, i):
    doctor_id = int(i + 1)
    first_name = fields[1].strip().strip("'")
    last_name = fields[2].strip().strip("'")
    speciality = fields[3].strip().strip("'")
    row = {
        "model": "customer_db.doctors",
        "pk": doctor_id,
        "fields": {
            "first_name": first_name,
            "last_name": last_name,
            "speciality": speciality,
        },
    }
    return row


def province(fields, *args):
    province_id = fields[0]
    province_name = fields[1]

    row = {
        "model": "customer_db.province_names",
        "pk": province_id,
        "fields": {"province_name": province_name},
    }
    return row


with open("patients.txt", "r") as f:
    data = []
    for i, line in enumerate(f):
        line = line.strip()[1:-2].replace("'", "")
        fields = line.split(",")
        row = patients(fields, i)
        data.append(row)

json_data = json.dumps(data)

with open("patients_data.json", "w") as f:
    f.write(json_data)
