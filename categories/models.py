from django.db import models
from django.contrib.auth.models import User

from hashid_field import HashidAutoField


class Category(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=15)
