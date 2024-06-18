import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.middleware import TokenAuthMiddleware
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamcraft_api.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
})
