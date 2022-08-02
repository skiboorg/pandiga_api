from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/user/online', consumers.UserOnline.as_asgi()),
]