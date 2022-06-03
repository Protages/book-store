from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(
        r'ws/socket-server/store/book_favourites/',
        consumers.FavouritesUserConsumer.as_asgi()
    ),
    re_path(
        r'ws/socket-server/store/cart_book/',
        consumers.CartBooksConsumer.as_asgi()
    ),
    re_path(r'ws/socket-server/store/cart/', consumers.CartUserConsumer.as_asgi()),
    re_path(
        r'ws/socket-server/store/comment/',
        consumers.CommentUserConsumer.as_asgi()
    ),
    re_path(
        r'ws/socket-server/store/connection/',
        consumers.ConnectionHistoryConsumer.as_asgi()
    ),
]
