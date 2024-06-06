from rest_framework import serializers
from . import models


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatGroup
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatMessage
        fields = '__all__'

