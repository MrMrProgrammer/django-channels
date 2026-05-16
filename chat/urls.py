from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path(
        "login",
        auth_views.LoginView.as_view(template_name="chat/login.html"),
        name="login"
    )
]
