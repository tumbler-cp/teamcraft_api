from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .serializers import GamerSerializer
from .models import Gamer

from . import serializers
from . import models


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def collide(request):
    user = request.user
    viewed_user = User.objects.get(id=request.data['viewed_id'])
    accepted = request.data['acception'] == 'true'
    collision = models.Collision.objects.create(
        user=user,
        viewed_user=viewed_user,
        accept=accepted,
        match=False
    )
    serializer = serializers.CollisionSerializer(collision)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def matches(request):
    match_list = models.Collision.objects.filter(user=request.user, match=True)
    serializer = serializers.CollisionSerializer(instance=match_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    user_gamer = models.Gamer.objects.get(user=user)
    serializer = serializers.GamerSerializer(user_gamer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def game(request):
    obj = models.Game.objects.get(id=request.GET.get('id'))
    serializer = serializers.GameSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def gamer(request):
    user = User.objects.get(username=request.GET.get('username'))
    obj = models.Gamer.objects.get(user=user)
    serializer = serializers.GamerSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_viewed_users(user):
    viewed_users = models.Collision.objects.filter(user=user)
    res = list(viewed_users.values_list('viewed_user_id', flat=True))
    return res


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def suggestions(request):
    user = request.user
    cache_key = f'sims_{user.id}'
    people = cache.get(cache_key)

    if not people:
        people = Gamer.objects.exclude(user=user)

    viewed_people_id = get_viewed_users(user)
    people = people.exclude(user__id__in=viewed_people_id)
    cache.set(cache_key, people, timeout=300)

    user_games = user.gamer.games.all()
    common_games_count = {}
    people_with_common_games = []

    for guest in people:
        common_games = user_games.filter(pk__in=guest.games.all())
        common_games_count[guest.user.username] = common_games.count()
        if common_games.exists():
            people_with_common_games.append(guest)

    sorted_people = sorted(people_with_common_games, key=lambda gst: common_games_count[gst.user.username],
                           reverse=True)

    serializer = GamerSerializer(sorted_people, many=True)
    return Response(serializer.data)
