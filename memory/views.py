from rest_framework.views import APIView
from rest_framework.response import Response

from .services import *
#savememoryapiview
#getmemoryapiview

class SaveMemoryApiView(APIView):
    
    def post(self,request):
        key=request.data.get("key")
        value=request.data.get("value")

        if not key or not value:
            return Response({
                "error":"key and value is required"
            },status=400)
        
        memory=save_memory(key,value)

        return Response({
            "message":"memory created",
            "key":memory.key,
            "value":memory.value
        },status=200)
    
class GetMemoryApiView(APIView):
    def post(self,request):
        print("TYPE:", type(request.data))
        print("DATA:", request.data)
        key=request.data.get("key")
        print(key)

        if not key:
            return Response({
                "error":"key required",
            },status=400)
        
        memory=get_memory(key)
        if not memory:
            return Response({
                "error": "Memory not found"
            }, status=404)

        return Response({
            "message":"memory present",
            "key":memory.key,
            "value":memory.value
        },status=200)
    
    def get(self, request):

        memories = list_memories()

        data = [
            {
                "key": memory.key,
                "value": memory.value
            }
            for memory in memories
        ]

        return Response(data)