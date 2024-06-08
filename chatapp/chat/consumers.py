import json

from user.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        message = data['message']
        email = data['email']
        room = data['room']

        user = await sync_to_async(User.objects.get)(email=email)
        avatar_url = user.avatar.url if user.avatar else 'media/avatar/no_image.png'


        await self.save_message(email, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'email': email,
                'avatar_url': avatar_url
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        email = event['email']
        avatar_url = event['avatar_url']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'email': email,
            'avatar_url':avatar_url
        }))

    @sync_to_async
    def save_message(self, email, room, message):
        user = User.objects.get(email=email)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)