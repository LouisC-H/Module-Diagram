from django.contrib import admin

from .models import Module, Links

class LinksInline(admin.TabularInline):
    model = Links
    fk_name = 'parent_module'
    extra = 2

class ModuleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['name', 'code', 'year', 'term', 'credits']}),
        ('Additional information', {'fields': ['department', 'category']}),
    ]
    inlines = [LinksInline]
    list_display = ('code', 'name', 'department')
    list_filter = ['department', 'year', 'term']
    search_fields = ['name', 'code']


admin.site.register(Module, ModuleAdmin)
