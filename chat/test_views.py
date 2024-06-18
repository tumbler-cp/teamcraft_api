import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from chat.models import Message

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamcraft_api.settings')


@pytest.mark.django_db
def test_room_view_get():
    user = User.objects.create_user(username='testuser', password='password')
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.get(reverse('room-view'))
    assert response.status_code == 200
    assert response.data['status']


@pytest.mark.django_db
def test_room_view_post():
    user = User.objects.create_user(username='testuser', password='password')
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('room-view'), {'message': 'Hello'})
    assert response.status_code == 200
    assert response.data['status']
    message = Message.objects.last()
    assert message.message == "Hello"
    assert message.user == user
