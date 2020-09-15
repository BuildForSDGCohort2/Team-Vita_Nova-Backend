from django.db import models
from api.models import AppUser

# Create your models here.
class Transactions(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    transaction_no = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.transaction_no

class Accounts(models.Model):
    user = models.OneToOneField(AppUser,on_delete=models.CASCADE)
    transaction_no = models.OneToOneField(Transactions, on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=10, decimal_places=2)
    debit = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.balance
    

    