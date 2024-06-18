import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authtoken.models import Token
from chat.middleware import TokenAuthMiddlewareStack
from channels.generic.websocket import AsyncWebsocketConsumer

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamcraft_api.settings')


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(
            {"user_id": self.scope['user'].id if not isinstance(self.scope['user'], AnonymousUser) else None})


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_token_auth_middleware_authenticated():
    user = User.objects.create_user(username='testuser', password='password')
    token = Token.objects.create(user=user)
    communicator = WebsocketCommunicator(
        TokenAuthMiddlewareStack(TestConsumer.as_asgi()),
        "/ws/test/",
        headers=[(b'authorization', f'Token {token.key}'.encode())]
    )
    connected, subprotocol = await communicator.connect()
    assert connected
    response = await communicator.receive_json_from()
    assert response['user_id'] == user.id
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_token_auth_middleware_anonymous():
    communicator = WebsocketCommunicator(
        TokenAuthMiddlewareStack(TestConsumer.as_asgi()),
        "/ws/test/",
        headers=[]
    )
    connected, subprotocol = await communicator.connect()
    assert connected
    response = await communicator.receive_json_from()
    assert response['user_id'] is None
    await communicator.disconnect()
