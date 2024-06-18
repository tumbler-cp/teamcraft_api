from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message


class RoomView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'general',
            {
                'type': 'send_info_to_many',
                'text':
                    {
                        'status': 'done'
                    }
            }
        )

        return Response({'status': True}, status=status.HTTP_200_OK)

    def post(self, request):
        msg = Message.objects.create(user=request.user, message={"message": request.data['message']})
        socket_message = f"New message {msg.id}"
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'{request.user.id}-message',
            {
                'type': 'send_info_to_many',
                'text': socket_message
            }
        )

        return Response({'status': True}, status=status.HTTP_200_OK)
