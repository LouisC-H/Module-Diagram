from django.urls import path

from . import views

urlpatterns = [
    path('', views.map, name = 'Module map'),
    path("<int:pk>/", views.detail, name = 'detail'),
]
