from django.urls import path

from . import views

urlpatterns = [
    path('', views.map, name = 'Module map'),
    path("<int:module_id>/", views.detail, name = 'detail'),
]
