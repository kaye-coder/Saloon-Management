from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)  # Optional email
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
