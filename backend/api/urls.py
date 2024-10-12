from django.urls import path
from .views import HelloWorld, ChatView

urlpatterns = [
    path("hello/", HelloWorld.as_view(), name="hello_world"),
    path("chat/", ChatView.as_view(), name="chat"),
]
