from django.db import models
from django.core.validators import MinValueValidator
from clinic_owners.models import CustomUser
from clinics.models import Clinic




class DrugCategory(models.Model):
    """Category for drugs (e.g., Antibiotic, Analgesic)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Drug category"
        verbose_name_plural = "Drug categories"

    def __str__(self):
        return self.name


class Formulation(models.Model):
    """Formulation types (e.g., Tablet, Capsule)"""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StorageCondition(models.Model):
    """Storage conditions (e.g., Room Temperature, Refrigerated)"""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SaleUnit(models.Model):
    """Sale units (e.g., Bottle, Pack, Tablet)"""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    # Basic information
    brand_name = models.CharField(max_length=200, db_index=True)
    generic_name = models.CharField(max_length=200, blank=True, db_index=True)
    drug_categories = models.ManyToManyField(
        DrugCategory,
        related_name='items',
        blank=True
    )

    # Formulation & storage
    formulation = models.ForeignKey(Formulation, on_delete=models.PROTECT)
    storage_condition = models.ForeignKey(StorageCondition, on_delete=models.PROTECT)

    # Stock management
    reorder_level = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Reorder level"
    )
    stock_target = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Stock target"
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Sale price"
    )
    sale_unit = models.ForeignKey(SaleUnit, on_delete=models.PROTECT)

    # Status flags
    discontinued = models.BooleanField(
        default=False,
        help_text="Item is discontinued"
    )
    pause_stocking = models.BooleanField(
        default=False,
        help_text="Temporarily pause ordering/stocking"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Soft delete flag; inactive items are hidden"
    )

    # Clinic link
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )

    # Audit fields
    entered_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='inventory_entered'
    )
    entered_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_updated'
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand_name']
        verbose_name = "Inventory item"
        verbose_name_plural = "Inventory items"

    def __str__(self):
        return f"{self.brand_name} - {self.formulation} ({self.clinic.name})"

