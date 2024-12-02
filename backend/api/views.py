import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, MedicalData, ChatSession, ChatMessage, QuestionLog
from .serializers import RegisterSerializer, LoginSerializer
from .medical_data_service import MedicalDataService
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Optional
import json
from datetime import datetime
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def read_medical_report(request):
    report_path = os.path.join(
        settings.BASE_DIR, "medical_reports", "john_davis_report.json"
    )

    try:
        with open(report_path, "r", encoding="utf-8") as file:
            report_data = json.load(file)

        return JsonResponse(
            {
                "success": True,
                "medicalReport": report_data,
            }
        )
    except FileNotFoundError:
        return JsonResponse(
            {"success": False, "error": "Medical report file not found"}, status=404
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid medical report format"}, status=400
        )
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return JsonResponse(
            {"success": False, "error": f"An error occurred: {str(e)}"}, status=500
        )


@csrf_exempt
def convert_to_friendly_mode(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            medical_report = data.get("medicalReport", "{}")
            
            # If it's just text content, create a basic structure
            if isinstance(medical_report, str):
                report_dict = {"txtContent": medical_report}
            else:
                report_dict = json.loads(medical_report)

            # Handle both structured and unstructured medical reports
            if 'txtContent' in report_dict:
                # For user uploaded text
                prompt = f"""Convert the following medical report into a clear, concise patient-friendly format.
                            Follow these strict guidelines:
                            - Use simple, direct language
                            - Limit each section to 2-3 sentences
                            - Avoid medical jargon
                            - Provide practical, actionable information

                            Format your response EXACTLY like this:
                            
                            Diagnosis: [Brief, clear explanation of the medical condition]
                            Symptoms: [What the patient experiences]
                            Medications: [List of medications with simple explanations]
                            Test Results: [Key findings explained simply]
                            Health Tips: [Practical lifestyle recommendations]
                            Next Steps: [Specific upcoming medical actions or recommendations]

                            Medical Report:
                            {report_dict['txtContent']}
                            """
            else:
                # For structured sample data
                prompt = f"""Convert the medical report into a clear, concise patient-friendly format.... 
                        [rest of your existing prompt remains the same]
                        """

            genai.configure(api_key=os.environ["API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            friendly_report = response.text

            return JsonResponse({"success": True, "friendlyReport": friendly_report})

        except Exception as e:
            print(f"Error in convert_to_friendly_mode: {str(e)}")  # Add logging
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse(
        {"success": False, "error": "Invalid request method"}, status=405
    )

class PatientInfoManager:
    @staticmethod
    def get_context_from_text(text: str) -> str:
        """Generate patient context from uploaded text"""
        return f"""
        You are a medical assistant chatbot helping with a patient's medical condition.
        You have access to their latest medical report: 
        
        {text}
        
        Important Guidelines:
        1. Maintain a professional and empathetic tone
        2. For any severe symptoms or emergency conditions, immediately advise calling emergency services
        3. Don't make new diagnoses or change any medical advice
        4. Refer complex medical questions to healthcare providers
        5. Help patient understand their condition and follow their care plan
        """

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
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get_sample_report(self):
        """Get the content of john_davis_report.txt"""
        try:
            report_path = os.path.join(
                settings.BASE_DIR,
                'medical_reports',
                'john_davis_report.txt'
            )
            with open(report_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading sample report: {str(e)}")
            return None

    def post(self, request):
        try:
            message = request.data.get("message")
            is_sample = request.data.get("is_sample", False)
            
            if not message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # Get context based on mode
            context = None
            if is_sample:
                context = self.get_sample_report()
                # print(f"Sample context loaded: {bool(context)}")
            elif request.user.is_authenticated:
                context = MedicalDataService.get_latest_report(request.user.user_id)
                # print(f"User context loaded: {bool(context)}")

            if not context:
                return JsonResponse({
                    "success": True,
                    "message": "Hi there! I notice you haven't provided a medical report yet. To best assist you, please upload your medical report first."
                })

            prompt = f"""You are a medical assistant chatbot. Here's the context:

            Medical Report:
            {context}

            User Question:
            {message}

            Please provide a helpful response based on the medical report context. 
            Use simple, clear language and be empathetic.
            If you encounter any severe symptoms or emergency conditions, immediately advise calling emergency services.
            Do not make new diagnoses or change any medical advice.
            Refer complex medical questions to healthcare providers.
            Help the patient understand their condition and follow their care plan.
            """

            genai.configure(api_key=os.environ["API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            return JsonResponse({
                "success": True,
                "message": response.text
            })

        except Exception as e:
            print(f"Error in EnhancedChatView: {str(e)}")
            return JsonResponse({
                "success": False, 
                "error": f"Error processing request: {str(e)}"
            }, status=500)

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

class MedicalDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Save a new medical report"""
        text_content = request.data.get('text')
        if not text_content:
            return JsonResponse({"error": "No text content provided"}, status=400)

        try:
            MedicalDataService.save_medical_report(request.user.user_id, text_content)  # Changed from id to user_id
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        """Get medical report history"""
        try:
            reports = MedicalDataService.get_report_history(request.user.user_id)  # Changed from id to user_id
            return JsonResponse({"reports": reports})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


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
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                user.last_login = timezone.now()
                user.save(update_fields=["last_login"])

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "token": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
