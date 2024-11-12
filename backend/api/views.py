from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .models import User, MedicalData, ChatSession, ChatMessage, QuestionLog
from .serializers import RegisterSerializer, LoginSerializer
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Optional
import json
from datetime import datetime


# Change it after completing database settings
class PatientInfo:
    """Static patient information for John Davis"""

    def __init__(self):
        self.patient_data = {
            "name": "John Davis",
            "diagnosis": "Stable heart disease with occasional chest pain",
            "symptoms": "Chest pain during activity, relieved by rest. No nausea, dizziness, or other symptoms.",
            "medications": [
                {"name": "Aspirin", "dosage": "81 mg", "frequency": "once daily"},
                {"name": "Atorvastatin", "dosage": "40 mg", "frequency": "once daily"},
                {"name": "Metoprolol", "dosage": "25 mg", "frequency": "twice daily"},
                {"name": "Nitroglycerin", "dosage": "0.4 mg", "frequency": "as needed"},
            ],
            "vitals": {"blood_pressure": "142/88 mmHg", "cholesterol": "210 mg/dL"},
            "test_results": {
                "stress_test": "Reduced blood flow to the heart was found"
            },
            "appointments": [
                {
                    "type": "angiogram",
                    "date": "2024-10-05",
                    "provider": "Dr. Jane Smith",
                },
                {
                    "type": "follow_up",
                    "date": "2024-10-14",
                    "provider": "Dr. Jane Smith",
                },
            ],
            "provider": "Dr. Jane Smith",
            "provider_type": "Cardiologist",
            "last_visit": "2024-09-30",
            "health_tips": [
                "Eat a low-sodium and low-cholesterol diet",
                "Avoid smoking",
                "Join a cardiac rehabilitation program",
            ],
        }

    def get_system_context(self) -> str:
        """Generate system context for the AI"""
        medications_str = ", ".join(
            [
                f"{med['name']} {med['dosage']} {med['frequency']}"
                for med in self.patient_data["medications"]
            ]
        )

        return f"""
        You are a medical assistant chatbot helping with {self.patient_data['name']}'s cardiac condition. 
        You have access to his latest medical records from {self.patient_data['last_visit']}.

        Patient Profile:
        - Name: {self.patient_data['name']}
        - Provider: {self.patient_data['provider']} ({self.patient_data['provider_type']})
        - Diagnosis: {self.patient_data['diagnosis']}
        - Current Symptoms: {self.patient_data['symptoms']}
        
        Medications:
        {medications_str}
        
        Recent Vitals:
        - Blood Pressure: {self.patient_data['vitals']['blood_pressure']}
        - Cholesterol: {self.patient_data['vitals']['cholesterol']}
        
        Test Results:
        - Stress Test: {self.patient_data['test_results']['stress_test']}
        
        Upcoming Appointments:
        - {self.patient_data['appointments'][0]['type']} on {self.patient_data['appointments'][0]['date']}
        - Follow-up visit on {self.patient_data['appointments'][1]['date']}
        
        Health Guidelines:
        {', '.join(self.patient_data['health_tips'])}

        Important Guidelines:
        1. Maintain a professional and empathetic tone
        2. For any severe chest pain or emergency symptoms, immediately advise calling emergency services
        3. Don't make new diagnoses or change any medical advice
        4. Refer complex medical questions to Dr. Jane Smith
        5. Help patient understand their condition and follow their care plan
        
        """


class EnhancedChatView(APIView):
    def __init__(self):
        super().__init__()
        self.patient_info = PatientInfo()

    def format_prompt(self, user_message: str) -> str:
        """Combines system context and user message"""
        return f"""
        {self.patient_info.get_system_context()}
        
        User message: {user_message}
        
        Please provide a helpful response based on the available patient information and guidelines.
        The user is {self.patient_info.patient_data['name']}
        You don't need to tell the user what you know in every message unless he/she ask you to do so
        """

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
            # Format the prompt with patient context
            formatted_prompt = self.format_prompt(message)

            # Generate response
            response = model.generate_content(formatted_prompt)
            response_message = response.text

            if response_message:
                # Check for emergency keywords
                emergency_keywords = [
                    "severe pain",
                    "unbearable",
                    "emergency",
                    "911",
                    "chest pain",
                    "shortness of breath",
                    "difficulty breathing",
                ]
                if any(keyword in message.lower() for keyword in emergency_keywords):
                    response_message = (
                        "⚠️ IMPORTANT: If you're experiencing severe chest pain or other "
                        "emergency symptoms, please call emergency services (911) immediately. "
                        "Do not wait. Your nitroglycerin is available for use as prescribed. "
                        "\n\n" + response_message
                    )

                return JsonResponse(
                    {
                        "message": response_message,
                        "context": {
                            "patient_name": self.patient_info.patient_data["name"],
                            "last_visit": self.patient_info.patient_data["last_visit"],
                            "next_appointment": {
                                "type": self.patient_info.patient_data["appointments"][
                                    0
                                ]["type"],
                                "date": self.patient_info.patient_data["appointments"][
                                    0
                                ]["date"],
                            },
                        },
                    },
                    status=200,
                )
            else:
                return JsonResponse({"error": "No response from GEMINI."}, status=500)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "Error calling GEMINI API"}, status=500)

    def get_medication_info(self, medication_name: str) -> dict:
        """Helper method to get specific medication information"""
        for med in self.patient_info.patient_data["medications"]:
            if med["name"].lower() == medication_name.lower():
                return med
        return None

from django.utils import timezone

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
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            name=name, email=email, password=password, my_chart_id=my_chart_id
        )
        return Response(
            {"message": "User created", "user_id": user.user_id},
            status=status.HTTP_201_CREATED,
        )
    

class AddMedicalDataView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        data_type = request.data.get("data_type")
        data_content = request.data.get("data_content")
        source = request.data.get("source")

        if not all([user_id, data_type, data_content, source]):
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(user_id=user_id)
        medical_data = MedicalData.objects.create(
            user=user, data_type=data_type, data_content=data_content, source=source
        )
        return Response(
            {
                "message": "Medical data added",
                "medical_data_id": medical_data.medical_data_id,
            },
            status=status.HTTP_201_CREATED,
        )    
        
class StartChatSessionView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(user_id=user_id)
        chat_session = ChatSession.objects.create(user=user)
        return Response(
            {"message": "Chat session started", "session_id": chat_session.session_id},
            status=status.HTTP_201_CREATED,
        )


class AddChatMessageView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        user_id = request.data.get("user_id")
        message_text = request.data.get("message_text")
        message_type = request.data.get("message_type")

        if not all([session_id, user_id, message_text, message_type]):
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        chat_session = ChatSession.objects.get(session_id=session_id)
        user = User.objects.get(user_id=user_id)
        chat_message = ChatMessage.objects.create(
            session=chat_session,
            user=user,
            message_text=message_text,
            message_type=message_type,
        )
        return Response(
            {"message": "Chat message added", "message_id": chat_message.message_id},
            status=status.HTTP_201_CREATED,
        )


class LogQuestionView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        question_text = request.data.get("question_text")
        answer_text = request.data.get("answer_text")
        confidence_score = request.data.get("confidence_score")
        source = request.data.get("source")

        if not all([user_id, question_text, answer_text, confidence_score, source]):
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(user_id=user_id)
        question_log = QuestionLog.objects.create(
            user=user,
            question_text=question_text,
            answer_text=answer_text,
            confidence_score=confidence_score,
            source=source,
        )
        return Response(
            {"message": "Question logged", "question_id": question_log.question_id},
            status=status.HTTP_201_CREATED,
        )


# User Authentication

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
