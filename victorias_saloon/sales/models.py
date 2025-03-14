from django.db import models
from inventory.models import InventoryItem
from branches.models import Branch
from customers.models import Customer
from decimal import Decimal

class Sale(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_date = models.DateTimeField(auto_now_add=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Ensure paid and total_price are both Decimal
        self.total_price = Decimal(self.total_price)
        self.paid = Decimal(self.paid)
        self.balance = self.total_price - self.paid
        super().save(*args, **kwargs)

    def update_total_price(self):
        # Ensure the total price calculation is consistent with Decimal
        self.total_price = sum(item.total_price for item in self.sale_items.all())
        self.balance = self.total_price - self.paid  # balance calculation
        self.save()

    def __str__(self):
        return f"Sale #{self.id} - {self.customer.name if self.customer else 'Walk-in'}"


class SaleItem(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name="sale_items")
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Ensure total price calculation is decimal
        self.total_price = Decimal(self.quantity_sold) * Decimal(self.selling_price)
        super().save(*args, **kwargs)

        # Update inventory stock after a sale is made
        self.item.stock -= self.quantity_sold
        self.item.save()

        # Update the total price for the sale
        self.sale.update_total_price()

    def __str__(self):
        return f"{self.item.item_name} - {self.quantity_sold} pcs"
