from django.shortcuts import HttpResponse, render
from django.template import loader

from .models import Map, Module, Links, Lecturer

def map(request):
    map = Map()
    table_data = map.table_data
    num_years = map.years
    template = loader.get_template('diagram/map.html')
    context = {'table_data' : table_data,'num_years' : num_years,}
    return render(request, 'diagram/map.html', context)
