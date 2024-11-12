from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    my_chart_id = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Define any required fields here

    objects = UserManager()  # Link custom manager

    def __str__(self):
        return self.email

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
