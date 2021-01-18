from django.contrib import admin

# Register your models here.
from .models import Module

@admin.register(Module)
class departmentadmin(admin.ModelAdmin):
    pass 
