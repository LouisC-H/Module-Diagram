from django.shortcuts import HttpResponse
from django.template import loader

from .models import Map, Module, Links, Lecturer

def map(request):
    module_list = Module.objects.all()
    template = loader.get_template('diagram/map.html')
    context = {'module_list' : module_list,}
    return HttpResponse(template.render(context, request))

def detail(request, module_id):
    response = "This is the detail page for module %s."
    return HttpResponse(response % module_id)
