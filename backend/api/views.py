from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests
from .models import User, MedicalData, ChatSession, ChatMessage, QuestionLog
import google.generativeai as genai

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
        
    
class CreateUserView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        my_chart_id = request.data.get("my_chart_id")

        if not all([name, email, password, my_chart_id]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(name=name, email=email, password=password, my_chart_id=my_chart_id)
        return Response({"message": "User created", "user_id": user.user_id}, status=status.HTTP_201_CREATED)

class AddMedicalDataView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        data_type = request.data.get("data_type")
        data_content = request.data.get("data_content")
        source = request.data.get("source")

        if not all([user_id, data_type, data_content, source]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(user_id=user_id)
        medical_data = MedicalData.objects.create(user=user, data_type=data_type, data_content=data_content, source=source)
        return Response({"message": "Medical data added", "medical_data_id": medical_data.medical_data_id}, status=status.HTTP_201_CREATED)

        
class StartChatSessionView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(user_id=user_id)
        chat_session = ChatSession.objects.create(user=user)
        return Response({"message": "Chat session started", "session_id": chat_session.session_id}, status=status.HTTP_201_CREATED)
    

class AddChatMessageView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        user_id = request.data.get("user_id")
        message_text = request.data.get("message_text")
        message_type = request.data.get("message_type")

        if not all([session_id, user_id, message_text, message_type]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        chat_session = ChatSession.objects.get(session_id=session_id)
        user = User.objects.get(user_id=user_id)
        chat_message = ChatMessage.objects.create(
            session=chat_session, user=user, message_text=message_text, message_type=message_type
        )
        return Response({"message": "Chat message added", "message_id": chat_message.message_id}, status=status.HTTP_201_CREATED)
    

class LogQuestionView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        question_text = request.data.get("question_text")
        answer_text = request.data.get("answer_text")
        confidence_score = request.data.get("confidence_score")
        source = request.data.get("source")

        if not all([user_id, question_text, answer_text, confidence_score, source]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(user_id=user_id)
        question_log = QuestionLog.objects.create(
            user=user,
            question_text=question_text,
            answer_text=answer_text,
            confidence_score=confidence_score,
            source=source
        )
        return Response({"message": "Question logged", "question_id": question_log.question_id}, status=status.HTTP_201_CREATED)
