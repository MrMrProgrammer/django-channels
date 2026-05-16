import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe

from . import models


@login_required(login_url="login")
def index(request):
    rooms = models.Chat.objects.filter(members=request.user)

    context = {
        "rooms": rooms
    }

    return render(request, "chat/index.html", context)


@login_required(login_url="login")
def room(request, room_name):

    chat: models.Chat | None = models.Chat.objects.filter(
        room_name=room_name
    ).first()

    user = request.user

    if not chat:
        chat = models.Chat.objects.create(room_name=room_name)
        chat.members.add(user)

    else:
        chat.members.add(user)

    username = request.user.username
    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username))
    }
    return render(request, "chat/room.html", context)
