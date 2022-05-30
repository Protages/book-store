from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(
        r'ws/socket-server/store/book_favourites/',
        consumers.FavouritesUserConsumer.as_asgi()
    ),
    re_path(r'ws/socket-server/store/book_cart/', consumers.CartUserConsumer.as_asgi()),
]
