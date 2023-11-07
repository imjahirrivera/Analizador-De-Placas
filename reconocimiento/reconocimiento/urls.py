from django.contrib import admin
from django.urls import path
from app.views import reconocimiento_placa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', reconocimiento_placa),
]