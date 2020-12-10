from django.contrib import admin

from .models import Module, Links, Lecturer

class LinksInline(admin.TabularInline):
    model = Links
    fk_name = 'parent_module'
    extra = 3

class LecturerInline(admin.TabularInline):
    model = Lecturer
    extra = 1

class ModuleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['name', 'code', 'year', 'term', 'credits']}),
        ('Additional information', {'fields': ['department', 'category', 'ELE', 'website']}),
    ]
    inlines = [LinksInline, LecturerInline]
    list_display = ('code', 'name', 'department')
    list_filter = ['department', 'year', 'term']
    search_fields = ['name', 'code']


admin.site.register(Module, ModuleAdmin)
