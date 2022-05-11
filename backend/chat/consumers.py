from email import message
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from chat.models import Thread


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        me = self.scope['user']
        print(me)
        other = self.scope['url_route']['kwargs']['username']
        other_user = User.objects.get(username=other)
        thread_obj = Thread.objects.get_or_create_personal_thread(
            me, other_user)
        self.room_name = f'personal_thread_{thread_obj.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name)
        print(f"[{self.channel_name}] - You are connected")
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name)
        print(f"[{self.channel_name}] - You are disconnected")

    def receive(self, text_data=None):
        print("Data Received.")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"[{self.channel_name}] - Received Message - {message}")

        new_message = json.dumps({
            'message': message,
            'username': self.scope['user'].username
        })
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': new_message
            }
        )

    def chat_message(self, event):
        print(f"[{self.channel_name}] - Received Message - {event['message']}")
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'broadcast'
        # print("Request for connection accepted.")
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name)
        print(f"[{self.channel_name}] - You are connected")
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name)
        print(f"[{self.channel_name}] - You are disconnected")

    def receive(self, text_data=None):
        print("Data Received.")
        print(f"[{self.channel_name}] - Received Message - {text_data}")
        return_msg = f'[{self.scope["user"]}] :- {text_data}'
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': return_msg
            }
        )

    def chat_message(self, event):
        print(f"[{self.channel_name}] - Sending Message - {event['message']}")
        message = event['message']
        self.send(text_data=message)
