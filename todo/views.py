from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import extract_tasks, save_tasks, get_task_summary, complete_task

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
        stats=save_tasks(result["tasks"])

        speech =(
            f"{stats['added']} task(s) added succesfully sir."
            f"You now have {stats['total_today']} task(s) for today."
        )

        return Response({            
            "speech":speech,
            "added":stats["added"],
            "skipped":stats["skipped"],
            'total_today':stats["total_today"]
        })
    
class TodoSummaryView(APIView):
    def get(self, request):
        data = get_task_summary()
        return Response(data)
    
class CompletedTaskAPIView(APIView):
    def post(self, request):
        task_number = request.data.get("task_number")
        if task_number is None:

            return Response(
                {
                    "error":"task_number required"
                },
                status=400
            )
        
        result = complete_task(int(task_number))
        return Response(result)