from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import InventoryItemListView, AddInventoryItemView, UpdateInventoryItemView

app_name = 'inventory'


urlpatterns = [
    path("inventory/", InventoryItemListView.as_view(), name="inventory_item_list"),
    path("inventory/add/", AddInventoryItemView.as_view(), name="add_inventory_item"),
    path("inventory/<int:pk>/edit/", UpdateInventoryItemView.as_view(), name="update_inventory_item"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)