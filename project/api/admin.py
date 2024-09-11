from django.contrib import admin

# Register your models here.
from .models import Customer,Company


# 6
admin.site.register(Customer)
admin.site.register(Company)