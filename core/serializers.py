from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class GameSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Game
        fields = ['id', 'name', 'icon', 'description']

class GamerSerializer(serializers.ModelSerializer):
    games = GameSerializer(read_only=True, many=True)
    class Meta(object):
        model = models.Gamer
        fields = ['id', 'user', 'description', 'avatar', 'games']

class ShortGamerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Gamer
        fields = ['id']

class CollisionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Collision
        fields = ['user', 'viewed_user', 'accept', 'match']