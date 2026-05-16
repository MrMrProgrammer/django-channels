from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
    room_name = models.CharField(max_length=50, blank=True)
    members = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self) -> str:
        return self.room_name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_messages(self, room_name):
        return Message.objects.filter(
            chat__room_name=room_name
        ).order_by("-timestamp").all()

    def __str__(self) -> str:
        return self.author.username
