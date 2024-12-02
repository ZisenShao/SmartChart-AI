from django.urls import path
from .views import (
    ChatView,
    EnhancedChatView,
    CreateUserView,
    AddMedicalDataView,
    MedicalDataView,
    StartChatSessionView,
    AddChatMessageView,
    LogQuestionView,
    RegisterView,
    LoginView,
    convert_to_friendly_mode,
    read_medical_report
)


urlpatterns = [
    path("chat/", EnhancedChatView.as_view(), name="chat"),  
    path('user/create/', CreateUserView.as_view(), name='create_user'),  
    path('medical-data/add/', AddMedicalDataView.as_view(), name='add_medical_data'),  
    path('chat/session/start/', StartChatSessionView.as_view(), name='start_chat_session'),  
    path('chat/message/add/', AddChatMessageView.as_view(), name='add_chat_message'), 
    path('question/log/', LogQuestionView.as_view(), name='log_question'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('convert_to_friendly_mode/', convert_to_friendly_mode, name='convert_to_friendly_mode'),
    path('read_medical_report/', read_medical_report, name='read_medical_report'),
    path('medical-data/', MedicalDataView.as_view(), name='medical_data'),

]
