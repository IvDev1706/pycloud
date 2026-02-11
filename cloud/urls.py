from django.urls import path
from .views import *

#rutas de la nube
urlpatterns = [
    path('',LoginView.as_view()),
    path('signup',SignUpView.as_view()),
    path('myunit',UnitView.as_view()),
    path('dir/<str:dir>',DirectoryView.as_view()),
    path('file/<str:file>',FileView.as_view()),
    path('update/file/<str:file>',UpdateFileView.as_view())
]
