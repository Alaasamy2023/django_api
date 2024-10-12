from django.contrib import admin

# Register your models here.
from .models import Customer,Company, MyModelPermission,Post


# 6
admin.site.register(Customer)
admin.site.register(Company)

admin.site.register(Post)




admin.site.register(MyModelPermission)


