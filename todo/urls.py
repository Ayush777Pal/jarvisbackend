from django.urls import path
from .views import ProcessTodoAPIView

urlpatterns = [
    path('process/', ProcessTodoAPIView.as_view())
]