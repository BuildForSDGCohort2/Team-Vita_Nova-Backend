
import random

from django.db import models
from api.models import AppUser
from ewallet.utils import create_order_id

# Create your models here.
class Transactions(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    transaction_no = models.CharField(max_length=50, unique=True, default=create_order_id())
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.transaction_no


class Accounts(models.Model):
    user = models.OneToOneField(AppUser,on_delete=models.CASCADE)
    transaction_no = models.OneToOneField(Transactions, on_delete=models.CASCADE, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.balance

    def on_user_create(self, amount, instance):
        transaction = Transactions()
        self.transaction_no = transaction
        transaction.amount = amount
        transaction.user = instance
        transaction.save()

        self.user = instance
        self.balance = 0
        self.save()