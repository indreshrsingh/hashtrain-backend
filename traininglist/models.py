from django.db import models

class Training(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)

    def __str__(self):
        return self.title
