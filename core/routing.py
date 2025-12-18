import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Only import notify routing (chat removed completely)
try:
    import notify.routing
    websocket_routes = notify.routing.websocket_urlpatterns
except ImportError:
    websocket_routes = []

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_routes
        )
    ),
})
