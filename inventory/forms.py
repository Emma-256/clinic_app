from django import forms
from .models import InventoryItem, DrugCategory, Formulation, StorageCondition, SaleUnit


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            "brand_name",
            "generic_name",
            "drug_categories",
            "formulation",
            "storage_condition",
            "reorder_level",
            "stock_target",
            "sale_price",
            "sale_unit",
            "discontinued",
            "pause_stocking",
            "is_active",
            "clinic",
        ]

        widgets = {
            "brand_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter brand name"
            }),
            "generic_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter generic name"
            }),
            "drug_categories": forms.SelectMultiple(attrs={
                "class": "form-select"
            }),
            "formulation": forms.Select(attrs={
                "class": "form-select"
            }),
            "storage_condition": forms.Select(attrs={
                "class": "form-select"
            }),
            "reorder_level": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),
            "stock_target": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
            "sale_price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
            "sale_unit": forms.Select(attrs={
                "class": "form-select"
            }),
            "discontinued": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "pause_stocking": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "clinic": forms.Select(attrs={
                "class": "form-select"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sort dropdowns alphabetically for usability
        self.fields["drug_categories"].queryset = DrugCategory.objects.order_by("name")
        self.fields["formulation"].queryset = Formulation.objects.order_by("name")
        self.fields["storage_condition"].queryset = StorageCondition.objects.order_by("name")
        self.fields["sale_unit"].queryset = SaleUnit.objects.order_by("name")

        # Add Bootstrap form-control class to all text/number fields automatically
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Select, forms.SelectMultiple)):
                field.widget.attrs["class"] = field.widget.attrs.get("class", "") + " form-control"
