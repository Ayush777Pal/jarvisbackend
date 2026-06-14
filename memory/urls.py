from django.urls import path
from .views import ForgetMemoryAPIView,GetMemoryApiView,SaveMemoryApiView,ProcessMemoryAPIView

urlpatterns=[
    path('save/',SaveMemoryApiView.as_view()),
    path('get/',GetMemoryApiView.as_view()),
    path('process/',ProcessMemoryAPIView.as_view()),
    path('forget/', ForgetMemoryAPIView.as_view())
]