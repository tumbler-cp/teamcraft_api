import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['general']

    async def connect(self):
        await self.accept()
        if not isinstance(self.scope['user'], AnonymousUser):
            self.user_id = self.scope['user'].id
            await self.channel_layer.group_add(f'{self.user_id}-message', self.channel_name)
        else:
            print('User not found!')

    async def send_info_to_many(self, event):
        message = event['text']
        await self.send(text_data=json.dumps(message))

    async def send_last_message(self, event):
        last_message = await self.get_last_message(self.user_id)
        last_message['status'] = event['text']
        await self.send(text_data=json.dumps(last_message))

    @database_sync_to_async
    def get_last_message(self, user_id):
        message = Message.objects.filter(user_id=user_id).last()
        return {
            'message': message.message,
            'timestamp': message.timestamp.isoformat()
        }
