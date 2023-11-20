from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/products/(?P<token>\w+)/$', consumer.ProductConsumer.as_asgi()),
]