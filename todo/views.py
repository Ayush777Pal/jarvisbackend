from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import extract_tasks, save_tasks

# Create your views here.
def test(request):
    return HttpResponse("Hello")

class ProcessTodoAPIView(APIView):

    def post(self, request):
        text = request.data.get("text")

        if not text:
            return Response(
                {
                    "error":"text required"
                },
                status=400
            )
        
        result = extract_tasks(text)
        save_tasks(result["tasks"])

        return Response({
            "speech":f"{len(result['tasks'])} tasks added successfully sir. "
        })