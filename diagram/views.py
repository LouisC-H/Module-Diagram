from django.shortcuts import HttpResponse, render
from django.template import loader

from .models import Map, Module, Links, Lecturer

def map(request):
    map = Map()
    table_data = map.table_data
    template = loader.get_template('diagram/map.html')
    context = {'table_data' : table_data,}
    return render(request, 'diagram/map.html', context)

def detail(request, module_id):
    response = "This is the detail page for module %s."
    return HttpResponse(response % module_id)
