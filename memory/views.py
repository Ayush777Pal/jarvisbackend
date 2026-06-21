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
    
    def delete(self, request):

        key = request.data.get("key")

        if not key:
            return Response(
                {
                    "error":"key is required"
                },
                status=400
            )

        memory = get_memory(key)

        if not memory:
            return Response(
                {
                    "error":"memory not found"
                },
                status=404
            )

        delete_memory(key)

        return Response(
            {
                "message":"memory deleted",
                "key":key
            },
            status=200
        )
    
class GetMemoryApiView(APIView):
    def post(self,request):
        key=request.data.get("key")

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
    
class ProcessMemoryAPIView(APIView):
    def post(self,request):
        text = request.data.get(
            "text"
        )

        if not text:
            return Response(
                {
                    "error":"text required"
                },
                status=400
            )
        
        memory = extract_memory(text)

        save_memory(
            memory["key"],
            memory["value"]
        )

        return Response(
            {
                "message":"memory stored",
                "memory":memory
            }
        )

class ForgetMemoryAPIView(APIView):

    def post(self,request):
        text = request.data.get("text")
        if not text:
            return Response(
                {
                    "error":"text required"
                },
                status=400
            )
        
        result = extract_forget_key(text)

        key = result.get("key")

        memory = get_memory(key)

        if not memory:
            return Response(
                {
                    "error":"memory not found"
                },
                status=404
            )
        
        delete_memory(key)

        return Response(
            {
                "message":"memory deleted",
                "key":key
            }
        )
    
class SaveContactAPIView(APIView):
    def post(self, request):
        text = request.data.get("text")
        result = extract_contact(text)
        if not result:
            return Response(
                {
                    "error":"invalid"
                },
                status=400
            )
        contact = save_contact(
            result["name"],
            result["phone_number"]
        )

        return Response(
            {
                "name":contact.name,
                "phone_number":contact.phone_number
            }
        )

class CallContactAPIView(APIView):
    def post(self, request):
        text = request.data.get("text")
        name = extract_contact_name(text)
        contact = get_contact(name)
        if not contact:
            return Response(
                {
                    "error":"contact not found"
                },
                status=404
            )
        
        return Response(
            {
                "phone_number":contact.phone_number
            }
        )

