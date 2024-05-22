from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from core.models import Gamer


@api_view(['POST'])
def signin(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({
            "detail": "Not found"
        }, status=status.HTTP_404_NOT_FOUND)
    tkn, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({
        "token": tkn.key,
        "user": serializer.data
    })


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        tkn = Token.objects.create(user=user)
        Gamer.objects.create(user=user)
        return Response({
            "token": tkn.key,
            "user": serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def token(request):
    return Response("Passed for {}".format(request.user.email))
