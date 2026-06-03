from django.urls import path
from .views import GetMemoryApiView,SaveMemoryApiView

urlpatterns=[
    path('save/',SaveMemoryApiView.as_view()),
    path('get/',GetMemoryApiView.as_view())
]