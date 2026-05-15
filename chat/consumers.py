import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . import serializers
from . import models
from rest_framework.renderers import JSONRenderer


class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        print(f"message: {data}")

    def fetch_message(self, data):
        qs = models.Message.last_messages(self)
        self.message_serializer(qs)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json)
        }
        self.chat_message(content)

    def message_serializer(self, qs):
        serialized = serializers.MessageSerializers(qs, many=True)
        content = JSONRenderer().render(serialized.data)
        return content

    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", None)
        command = text_data_json["command"]

        self.commands[command](self, message)

    def send_to_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            group=self.room_group_name,
            message={
                "type": "chat.message",
                "message": message
            }
        )

    def chat_message(self, event):
        message = event["message"]
        print(event)
        self.send(text_data=json.dumps({"message": message}))
