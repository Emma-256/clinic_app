from django.db import migrations

def load_sale_units(apps, schema_editor):
    SaleUnit = apps.get_model("inventory", "SaleUnit")
    sale_units = [
        "Tablet", "Bottle", "Amp", "Capsule", "Kit", "Lozenge", "Pack",
        "Sacket", "Tin", "Tube", "Vail", "Piece", "Pair", "Cycle",
    ]
    for name in sale_units:
        SaleUnit.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0003_load_formulations"),  # adjust to your last migration
    ]

    operations = [
        migrations.RunPython(load_sale_units),
    ]
