import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pandiga_api.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()
from django.urls import path
from user.consumers import UserOnline
from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(      [

                path('ws/user/online', UserOnline.as_asgi()),
                path('ws/chat/<chat_id>', ChatConsumer.as_asgi()),
                ]
            )
        )
    ),
})