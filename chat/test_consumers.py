import pytest

from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from chat.consumers import ChatConsumer
from chat.models import Message
from channels.auth import AuthMiddlewareStack

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamcraft_api.settings')


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_connect_authenticated_user():
    user = await database_sync_to_async(User.objects.create_user)(username='testuser', password='password')
    communicator = WebsocketCommunicator(
        AuthMiddlewareStack(ChatConsumer.as_asgi()),
        "/ws/chat/",
        headers=[(b'authorization', b'Token ' + user.auth_token.key.encode())]
    )
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_send_info_to_many():
    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/")
    await communicator.connect()
    await communicator.send_json_to({"type": "send_info_to_many", "message": "Hello"})
    response = await communicator.receive_json_from()
    assert response == "Hello"
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_send_last_message():
    user = await database_sync_to_async(User.objects.create_user)(username='testuser', password='password')
    await database_sync_to_async(Message.objects.create)(user=user, message="Test message")
    communicator = WebsocketCommunicator(
        AuthMiddlewareStack(ChatConsumer.as_asgi()),
        "/ws/chat/",
        headers=[(b'authorization', b'Token ' + user.auth_token.key.encode())]
    )
    await communicator.connect()
    await communicator.send_json_to({"type": "send_last_message", "message": "done"})
    response = await communicator.receive_json_from()
    assert response['message'] == "Test message"
    assert response['status'] == "done"
    await communicator.disconnect()
