from django.urls import path
from .views import ChatAPIView,LaunchAppView
urlpatterns = [
    path('chat/', ChatAPIView.as_view()),
    path('extract/',LaunchAppView.as_view())
]