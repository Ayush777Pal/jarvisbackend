from django.urls import path
from .views import *

urlpatterns = [
    path('process/', test, name='test')
]