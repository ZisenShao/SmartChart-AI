from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests
import google.generativeai as genai

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})


class ChatView(APIView):
    def post(self, request):
        message = request.data.get("message")
        if not message:
            return JsonResponse({"error": "No message provided"}, status=400)

        api_key = os.environ.get("API_KEY")
        if not api_key:
            return JsonResponse({"error": "API_KEY is not set."}, status=400)

        genai.configure(api_key=os.environ["API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        try:
            response = model.generate_content(message)
            response_message = response.text
            if response_message:
                return JsonResponse({"message": response_message}, status=200)
            else:
                return JsonResponse({"error": "No response from GEMINI."}, status=500)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "Error calling GEMINI API"}, status=500)
