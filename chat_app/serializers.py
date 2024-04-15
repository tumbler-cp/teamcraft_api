from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Message
        fields = ['user', 'text', 'file']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.ChatRoom
        fields = ['id', 'users']