from rest_framework import serializers
from . import models


class GameSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Game
        fields = ['id', 'name', 'icon', 'description']


class GamerSerializer(serializers.ModelSerializer):
    games = GameSerializer(read_only=True, many=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Gamer
        fields = ['id', 'user', 'description', 'avatar', 'avatar_url', 'games']

    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None


class ShortGamerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Gamer
        fields = ['id']


class CollisionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Collision
        fields = ['user', 'viewed_user', 'accept', 'match']
