"""
ASGI config for sawarung project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
from django.urls import path
import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from .consumer import ProductConsumer
import sawarung.channel_routing as channel_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sawarung.settings')
django_asgi_app = get_asgi_application()
django.setup()
application = ProtocolTypeRouter({
  'http': django_asgi_app,
  'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(channel_routing.websocket_urlpatterns))
        )
})
