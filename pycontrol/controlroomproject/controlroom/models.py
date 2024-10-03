from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DiaryEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()  # Changed from DateField to DateTimeField
    title = models.CharField(max_length=120, null=False, default="")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username}'s entry on {self.date}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10, choices=[("expense", "Expense"), ("income", "Income")]
    )
    date = models.DateTimeField()  # Removed auto_now_add=True

    def __str__(self):
        return f"{self.description} - {self.amount}"
