# models.py in the purchases app
from django.db import models
from inventory.models import InventoryItem
from suppliers.models import Supplier
from units.models import Unit
from categories.models import Category

class Purchase(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Purchase of {self.inventory_item.item_name} from {self.supplier.name}"

    def save(self, *args, **kwargs):
        # Update inventory stock and price when purchase is made
        inventory_item = self.inventory_item
        inventory_item.stock += self.quantity
        inventory_item.purchasing_cost = self.purchase_price
        inventory_item.unit = self.unit
        inventory_item.category = self.category  # Update category as well
        inventory_item.save()

        super().save(*args, **kwargs)
