from django.shortcuts import HttpResponse

def map(request):
    return HttpResponse("This is the map page")

def detail(request):
    return HttpResponse("This is the detail page")
