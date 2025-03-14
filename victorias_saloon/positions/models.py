from django.db import models

class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
