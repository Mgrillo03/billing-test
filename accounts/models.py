from email.policy import default
from django.contrib.auth.models import User
from django.db import models

from hashid_field import HashidAutoField

from categories.models import Category
class Account(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    bank = models.CharField(max_length= 70)
    balance = models.FloatField(default=0)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Operation_ac(models.Model):
    id = HashidAutoField(primary_key=True)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=70)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transfer_id = models.IntegerField(default=0)
    

    

