from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    """
    Purpose: Represents a financial transaction (income or expense) for a user.
    Attributes:
        user: Foreign key linking the transaction to a specific user.
        description: A brief description of the transaction.
        amount: The amount of money involved in the transaction.
        transaction_type: The type of transaction (either 'income' or 'expense').
        date: The date and time when the transaction was created.
    """
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.transaction_type})"
