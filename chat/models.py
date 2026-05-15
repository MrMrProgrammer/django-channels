from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_messages(self):
        return Message.objects.order_by("-timestamp").all()

    def __str__(self) -> str:
        return self.author.username
