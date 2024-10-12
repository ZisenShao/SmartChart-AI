from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})

class ChatView(APIView):
    def get(self, request):
        return Response({"message": "Empty chat interface"}, status=status.HTTP_200_OK)
