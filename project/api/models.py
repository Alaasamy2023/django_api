# from datetime import timezone
from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(null=False)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username
    


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(null=False)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username