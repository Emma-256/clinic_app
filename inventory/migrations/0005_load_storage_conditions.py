from django.db import migrations

def load_storage_conditions(apps, schema_editor):
    StorageCondition = apps.get_model("inventory", "StorageCondition")
    storage_conditions = [
        "Room Temperature",
        "Refrigerated (2-8°C)",
        "Frozen (-20°C)",
        "Cool & Dry Place",
        "Other",
    ]
    for name in storage_conditions:
        StorageCondition.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0004_load_sale_units"),  # adjust to your last migration
    ]

    operations = [
        migrations.RunPython(load_storage_conditions),
    ]
