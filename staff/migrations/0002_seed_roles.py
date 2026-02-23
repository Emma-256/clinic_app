# staff/migrations/0002_seed_roles.py
from django.db import migrations

TECHNICAL_STAFF = [
    ("physician", "Physician/Doctor"),
    ("specialist", "Specialist"),
    ("nurse", "Nurse"),
    ("nurse_practitioner", "Nurse Practitioner"),
    ("physician_assistant", "Physician Assistant"),
    ("medical_assistant", "Medical Assistant"),
    ("pharmacist", "Pharmacist"),
    ("lab_technician", "Lab Technician"),
    ("radiology_technician", "Radiology Technician"),
    ("dietitian", "Dietitian/Nutritionist"),
    ("social_worker", "Social Worker/Counselor"),
]

SUPPORT_STAFF = [
    ("clinic_manager", "Clinic Manager/Administrator"),
    ("receptionist", "Receptionist/Front Desk"),
    ("billing_specialist", "Billing & Insurance Specialist"),
    ("records_clerk", "Medical Records Clerk"),
    ("it_support", "IT Support Staff"),
    ("maintenance", "Cleaning & Maintenance Staff"),
]


def seed_roles(apps, schema_editor):
    TechnicalStaff = apps.get_model("staff", "TechnicalStaff")
    SupportStaff = apps.get_model("staff", "SupportStaff")

    for code, name in TECHNICAL_STAFF:
        TechnicalStaff.objects.get_or_create(name=name, defaults={"description": code})

    for code, name in SUPPORT_STAFF:
        SupportStaff.objects.get_or_create(name=name, defaults={"description": code})


def unseed_roles(apps, schema_editor):
    TechnicalStaff = apps.get_model("staff", "TechnicalStaff")
    SupportStaff = apps.get_model("staff", "SupportStaff")
    TechnicalStaff.objects.all().delete()
    SupportStaff.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0001_initial"),  # make sure this matches your initial migration
    ]

    operations = [
        migrations.RunPython(seed_roles, unseed_roles),
    ]
