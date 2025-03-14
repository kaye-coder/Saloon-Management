from django.contrib.auth.models import User
from django.db import models

class AppPermission(models.Model):
    READ = 'read'
    WRITE = 'write'
    NO_ACCESS = 'none'

    PERMISSION_CHOICES = [
        (NO_ACCESS, 'No Access'),
        (READ, 'Read'),
        (WRITE, 'Write'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='app_permissions')
    app_name = models.CharField(max_length=50)  # Name of the app (e.g., "employees", "sales")
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default=NO_ACCESS)

    def __str__(self):
        return f"{self.user.username} - {self.app_name}: {self.permission}"
