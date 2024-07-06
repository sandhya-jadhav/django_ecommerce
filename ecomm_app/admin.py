from django.contrib import admin
# from ecomm_app.models import product
from .models import product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','cat','is_active']
    list_filter=['cat','is_active','price']

#admin.site.register(product)
admin.site.register(product,ProductAdmin)