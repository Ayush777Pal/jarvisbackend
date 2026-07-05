from django.urls import path
from .views import ProcessTodoAPIView,TodoSummaryView

urlpatterns = [
    path('process/', ProcessTodoAPIView.as_view()),
    path("summary/",TodoSummaryView.as_view())
]