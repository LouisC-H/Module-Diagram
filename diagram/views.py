from django.shortcuts import HttpResponse, render
from django.template import loader

from .models import Map, Module

def map(request, user_options = "All"):
    map = Map(user_options)
    table_data = map.table_data
    num_years = map.years
    context = {'table_data' : table_data,'num_years' : num_years,}
    return render(request, 'diagram/map.html', context)

def user_options(request):
    return render(request, 'diagram/options.html')
