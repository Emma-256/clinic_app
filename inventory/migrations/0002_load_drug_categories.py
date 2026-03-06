# clinics/migrations/0002_load_drug_categories.py
from django.db import migrations

def load_drug_categories(apps, schema_editor):
    DrugCategory = apps.get_model("inventory", "DrugCategory")
    categories = [
        "Analgesic",
        "Antianxiety",
        "Antiarrhythmic",
        "Antibacterial (Antibiotic)",
        "Anticid",
        "Anticoagulant",
        "Anticold",
        "Anticonvulsant",
        "Antidepressant",
        "Antidiabetics",
        "Antidiarrheal",
        "Antiemetic",
        "Antifungal",
        "Antigout Agent",
        "Antihelminthic",
        "Antihistamine",
        "Antihypertensive",
        "Anti-inflammatory (Corticosteroids)",
        "Antimalarial",
        "Antineoplastic",
        "Antiparasitics",
        "Antiprotozoal",
        "Antipsychotic",
        "Antipyretic",
        "Antisecretory",
        "Antiseptic",
        "Antispasmodic",
        "Antitubercular",
        "Antiviral",
        "Beta-blocker",
        "Bronchodilator",
        "Corticosteroid",
        "Dermatological Agent",
        "Disinfectant",
        "Diuretic",
        "Family planning Agent",
        "Genital Wash",
        "Hemostatic",
        "Herbal",
        "Hormone",
        "Immunosuppresant",
        "Intravenous Fluid",
        "Mineral Supplement",
        "Opiod",
        "Opthalamic Agent",
        "Postaglandins",
        "Steroid",
        "Sundries",
        "Thrombolytic",
        "Urological",
        "Vitamin",
    ]
    for name in categories:
        DrugCategory.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_drug_categories),
    ]
