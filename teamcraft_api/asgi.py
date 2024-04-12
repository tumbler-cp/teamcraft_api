import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat_app import routing as chat_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamcraft_api.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter (
        chat_routing.websocket_urlpatters
    ),
})
