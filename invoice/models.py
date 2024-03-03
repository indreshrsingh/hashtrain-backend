from django.db import models

class Invoice(models.Model):
    customer_name = models.CharField(max_length=100)
    training_id = models.IntegerField(default=0)
    training_name = models.CharField(max_length=100)
    training_description = models.TextField()
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.training_name} - {self.customer_name}"
    
    
