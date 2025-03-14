from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation =models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
