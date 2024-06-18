from django.urls import path
from . import consumers
from . import views

websocket_urlpatterns = [
    path('', consumers.EmptyConsumer.as_asgi()),
    path('chat', consumers.ChatConsumer.as_asgi()),
]
