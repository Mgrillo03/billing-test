from datetime import datetime
from email.policy import default
from django.contrib.auth.models import User

from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    bank = models.CharField(max_length= 70)
    balance = models.FloatField(default=0)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Operation_ac(models.Model):
    decription = models.CharField(max_length=200)
    type = models.CharField(max_length=70)
    category = models.CharField(max_length=70)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

