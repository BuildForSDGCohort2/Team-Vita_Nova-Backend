from api.models import AppUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from ewallet.models import Accounts, Transactions

def create_user_account(sender,instance,created,**kwargs):
    if created:
        account = Accounts()
        account.user = instance
        account.on_user_create(0,instance)

post_save.connect(create_user_account,sender=AppUser)
        
