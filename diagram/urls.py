from django.urls import path

from . import views

urlpatterns = [
    path('map/', include('map.urls')),
    path('admin/', admin.site.urls),
]
