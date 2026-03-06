from django.contrib import admin
from .models import Formulation , DrugCategory , InventoryItem, SaleUnit , StorageCondition

# Register your models here.
models = [ Formulation, DrugCategory, InventoryItem, SaleUnit, StorageCondition]

admin.site.register(models)