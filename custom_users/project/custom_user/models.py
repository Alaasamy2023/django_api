from datetime import timezone
from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# 4-
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




# add new Permission 

class MyModelPermission(Permission):
    class Meta:
        permissions = [
            ("can_view_custom_rule", "Can view with custom rule"),
            ("can_change_custom_rule", "Can change with custom rule"),
            # Define more permissions as needed
        ]















# Post

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



