from django.urls import path
from .views import *

#rutas de la nube
urlpatterns = [
    path('',LoginView.as_view())
]
