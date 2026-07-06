from django.urls import path
from .views import ProcessTodoAPIView,TodoSummaryView, CompletedTaskAPIView

urlpatterns = [
    path('process/', ProcessTodoAPIView.as_view()),
    path('summary/',TodoSummaryView.as_view()),
    path('complete/', CompletedTaskAPIView.as_view())
]