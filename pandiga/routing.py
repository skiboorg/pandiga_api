from channels.auth import AuthMiddlewareStack
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
# import p2p.routing
import user.routing
from user.consumers import UserOnline
from chat.consumers import ChatConsumer
# from stream.consumers import VideoCallSignalConsumer
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # user.routing.websocket_urlpatterns
            path('ws/user/online/', UserOnline),
            path('ws/chat/<chat_id>', ChatConsumer),
        ])
    ),

})
