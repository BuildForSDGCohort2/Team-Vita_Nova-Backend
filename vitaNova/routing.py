from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from socialife.consumers import ChatConsumer, GlobalConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_uuid>/', ChatConsumer),
    path('ws/global/', GlobalConsumer)
]
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})