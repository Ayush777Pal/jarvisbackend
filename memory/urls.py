from django.urls import path
from .views import SaveContactAPIView,CallContactAPIView,ForgetMemoryAPIView,GetMemoryApiView,SaveMemoryApiView,ProcessMemoryAPIView

urlpatterns=[
    path('save/',SaveMemoryApiView.as_view()),
    path('get/',GetMemoryApiView.as_view()),
    path('process/',ProcessMemoryAPIView.as_view()),
    path('forget/', ForgetMemoryAPIView.as_view()),
    path("contact/save/", SaveContactAPIView.as_view()),
    path("contact/call/",CallContactAPIView.as_view())
]