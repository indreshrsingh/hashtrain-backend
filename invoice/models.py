# models.py
from django.db import models

class Invoice(models.Model):
    customer_name = models.CharField(max_length=100)
    training_id = models.IntegerField(default=0)
    company_name = models.CharField(max_length=100)
    training_name = models.CharField(max_length=100)
    training_description = models.TextField()
    pdf_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.training_name} - {self.customer_name}"
