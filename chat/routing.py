from django.urls import path
from . import consumers
from . import views

websocket_urlpatterns = [
    path('chat', consumers.ChatConsumer.as_asgi()),
]
