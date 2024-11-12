from django.urls import path
from .views import (
    ChatView,
    EnhancedChatView,
    CreateUserView,
    AddMedicalDataView,
    StartChatSessionView,
    AddChatMessageView,
    LogQuestionView,
    RegisterView,
    LoginView
)

urlpatterns = [
    path("chat/", EnhancedChatView.as_view(), name="chat"),  # Endpoint for ChatView
    path('user/create/', CreateUserView.as_view(), name='create_user'),  # Endpoint for user creation
    path('medical-data/add/', AddMedicalDataView.as_view(), name='add_medical_data'),  # Endpoint for adding medical data
    path('chat/session/start/', StartChatSessionView.as_view(), name='start_chat_session'),  # Endpoint to start a chat session
    path('chat/message/add/', AddChatMessageView.as_view(), name='add_chat_message'),  # Endpoint to add a chat message
    path('question/log/', LogQuestionView.as_view(), name='log_question'),  # Endpoint to log questions
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
