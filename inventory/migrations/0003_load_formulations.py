from django.db import migrations

def load_formulations(apps, schema_editor):
    Formulation = apps.get_model("inventory", "Formulation")
    formulations = [
        "Capsules", "Cream", "Drops", "Emulsion", "Gel", "Implant", "Injection",
        "Kit", "Lozenges", "Nebulizer", "Ointment", "Pellets", "Powder", "Roll",
        "Solution", "Spray (Aerosols)", "Suspension", "Swabs", "Syrup", "Tablets",
    ]
    for name in formulations:
        Formulation.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0002_load_drug_categories"),  # make sure dependency points to your last migration
    ]

    operations = [
        migrations.RunPython(load_formulations),
    ]
