import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe


@login_required
def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    username = request.user.username
    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username))
    }
    return render(request, "chat/room.html", context)
