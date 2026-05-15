import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer

from . import models, serializers

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        message = data["message"]
        user_model = User.objects.filter(username=data["username"]).first()
        message_model = models.Message.objects.create(
            content=message,
            author=user_model
        )
        self.send_to_chat_message(eval(self.message_serializer(message_model)))

    def fetch_message(self, data):
        qs = models.Message.last_messages(self)
        self.message_serializer(qs)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json),
            "command": "fetch_message"
        }
        self.chat_message(content)

    def message_serializer(self, qs):
        serialized = serializers.MessageSerializers(
            qs,
            many=(
                lambda qs: True if (
                    qs.__class__.__name__ == "QuerySet"
                ) else False
            )(qs)
        )
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

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        command = text_data_json["command"]

        self.commands[command](self, text_data_json)

    def send_to_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            group=self.room_group_name,
            message={
                "type": "chat_message",
                "content": message["content"],
                "command": "new_message",
                "__str__": message["__str__"]
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
