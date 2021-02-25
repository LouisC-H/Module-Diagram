from django.contrib import admin

# Register your models here.
from .models import Module

@admin.register(Module)
class departmentadmin(admin.ModelAdmin):
    list_display = ['code', 'department','year','term','credits','lecturer','core_Natural_Sciences','core_Mathematics','core_Physics_BPhys','core_Biochemistry','core_Physics_BPhys','core_Biological_Sciences','core_Biological_and_Medicinal_Chemistry', 'natural_Sciences_History', 'topic_pathway', 'Co_req','Pre_req' ] 
