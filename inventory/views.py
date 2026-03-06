from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import InventoryItem
from .forms import InventoryItemForm


class InventoryItemListView(ListView):
    model = InventoryItem
    template_name = "inventory/inventory_item_list.html"
    context_object_name = "items"
    paginate_by = 20  # optional, adds pagination

    def get_queryset(self):
        # Only show active items by default
        return InventoryItem.objects.filter(is_active=True).order_by("brand_name")


class AddInventoryItemView(CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/add_inventory_item.html"
    success_url = reverse_lazy("inventory_item_list")

    def form_valid(self, form):
        # Attach the user who entered the item
        form.instance.entered_by = self.request.user
        return super().form_valid(form)


class UpdateInventoryItemView(UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/update_inventory_item.html"
    success_url = reverse_lazy("inventory_item_list")

    def form_valid(self, form):
        # Attach the user who updated the item
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class InventoryItemDetailView(DetailView):
    model = InventoryItem
    template_name = "inventory/inventory_item_detail.html"
    context_object_name = "item"
