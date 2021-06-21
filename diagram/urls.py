from django.urls import path

from . import views

urlpatterns = [
    path('', views.map, name = 'Module map'),
    path('/user_options/', views.user_options, name = 'User Options'),
    path('/<str:user_options>/', views.map, name = 'Module map'),
]
