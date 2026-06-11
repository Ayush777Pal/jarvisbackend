from django.urls import path
from .views import GetMemoryApiView,SaveMemoryApiView,ProcessMemoryAPIView

urlpatterns=[
    path('save/',SaveMemoryApiView.as_view()),
    path('get/',GetMemoryApiView.as_view()),
    path('process/',ProcessMemoryAPIView.as_view())
]