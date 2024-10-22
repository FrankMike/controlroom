from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10, choices=[("expense", "Expense"), ("income", "Income")]
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.description} - {self.amount}"
