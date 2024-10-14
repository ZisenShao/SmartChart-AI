from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    my_chart_id = models.CharField(max_length=255)  # Link to MyChart account
    date_created = models.DateTimeField(auto_now_add=True)

class MedicalData(models.Model):
    medical_data_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_type = models.CharField(max_length=255)  # e.g., prescriptions, test results
    data_content = models.JSONField()  # Medical data stored in JSON or structured format
    date_uploaded = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255)  # Source of the data (e.g., hospital name)

class ChatSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_started = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(null=True, blank=True)

class ChatMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.TextField()
    message_type = models.CharField(max_length=50)  # e.g., user message, bot response
    timestamp = models.DateTimeField(auto_now_add=True)

class QuestionLog(models.Model):
    question_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField()
    date_asked = models.DateTimeField(auto_now_add=True)
    confidence_score = models.FloatField()  # Confidence score for the chatbot’s answer
    source = models.CharField(max_length=255)  # e.g., medical data or external knowledge
