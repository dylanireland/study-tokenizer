from django.urls import path

from . import views
from . import auth

urlpatterns = [
    path('index', views.index, name='index'),
    path('auth', auth.auth, name='auth'),
    path('download', views.download, name='download'),
]
