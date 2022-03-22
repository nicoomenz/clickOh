from django.contrib import admin
from .models import *

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Products, ProductsAdmin)

