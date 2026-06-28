from rest_framework.response import Response
from rest_framework.views import APIView

from .services import generate_ai_response, extract_app


class ChatAPIView(APIView):

    def post(self, request):

        user_message = request.data.get("message")

        if not user_message:
            return Response({
                "error": "Message is required"
            }, status=400)

        ai_reply = generate_ai_response(user_message)

        return Response({
            "reply": ai_reply
        })
    
class LaunchAppView(APIView):
    def post(self, request):
        text = request.data.get("text")

        if not text:
            return Response(
                {
                    "error":"text required"
                },
                status=400
            )
        result = extract_app(text)
        return Response(result)