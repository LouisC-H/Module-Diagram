from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Module
# Create your views here.

def homepage(request):
    modules = Module.objects
    return render(request, 'modules/home.html', {'modules':modules})


def detail(request, module_id):
    module_detail = get_object_or_404(Module, pk=module_id)
    return render(request, 'modules/module_detail.html', {'module':module_detail})
