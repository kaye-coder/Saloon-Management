from django.db import models
from categories.models import Category
from units.models import Unit
class InventoryItem(models.Model):
    item_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    purchasing_cost = models.DecimalField(max_digits=10, decimal_places=2)
    selling_cost = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateField(auto_now_add=True)
    stock = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item_name', 'category', 'unit'], name='unique_inventory_item')
        ]

    def __str__(self):
        return f"{self.item_name} - {self.category.name} - {self.unit.name}"
