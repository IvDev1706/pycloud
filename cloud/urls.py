from django.urls import path
from .views import *

#rutas de la nube
urlpatterns = [
    path('',LoginView.as_view()),
    path('signup',SignUpView.as_view()),
    path('myunit',UnitView.as_view())
]
