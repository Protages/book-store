import json

from django.utils import timezone
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer

from customer.models import Cart, Position
from users.models import ConnectionHistory
from .models import Book, Comment


USER_MODEL = get_user_model()


class FavouritesUserConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message_type = text_data['message_type']

        if message_type == 'books_in_favourites':
            self.get_all_books_id_favourites()
        elif message_type == 'add_remove_book_favourites':
            self.add_remove_book_favourites(int(text_data['book_id']))

    def get_all_books_id_favourites(self):
        if self.user.is_authenticated:
            user_favourites_books = Cart.objects.get(user=self.user).favourites.all()
            books_id_set = [book.id for book in user_favourites_books]

            self.send(text_data=json.dumps({
                'books_id_set': books_id_set
            }))
        else:
            self.send(text_data=json.dumps({
                'books_id_set': []
            }))

    def add_remove_book_favourites(self, book_id):
        user_cart = Cart.objects.get(user=self.user)
        book = Book.objects.get(id=book_id)
        if book in user_cart.favourites.all():
            user_cart.favourites.remove(book)
            self.send(text_data=json.dumps({
                'message': f'Book {book_id} was remove!'
            }))
        else:
            user_cart.favourites.add(book)
            self.send(text_data=json.dumps({
                'message': f'Book {book_id} was added!'
            }))


class CartBooksConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message_type = text_data['message_type']

        if message_type == 'books_in_cart':
            self.get_all_books_id_cart()
        elif message_type == 'add_remove_book_cart':
            self.add_remove_book_cart(int(text_data['book_id']))

    def get_all_books_id_cart(self):
        if self.user.is_authenticated:
            user_cart = Cart.objects.get(user=self.user)
            user_cart_books = Position.objects.filter(cart=user_cart, is_close=False)
            books_id_set = [cart.book.id for cart in user_cart_books]

            self.send(text_data=json.dumps({
                'books_id_set': books_id_set
            }))
        else:
            self.send(text_data=json.dumps({
                'books_id_set': []
            }))

    def add_remove_book_cart(self, book_id):
        user_cart = Cart.objects.get(user=self.user)
        book = Book.objects.get(id=book_id)
        Position.objects.create(cart=user_cart, book=book)


class CartUserConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message_type = text_data['message_type']

        if message_type == 'activate_position':
            self.activate_position(text_data['position_id'])
        elif message_type == 'deactivate_position':
            self.deactivate_position(text_data['position_id'])

        elif message_type == 'minus_book_count':
            self.minus_book_count(text_data['position_id'])
        elif message_type == 'plus_book_count':
            self.plus_book_count(text_data['position_id'])

        elif message_type == 'remove_position_from_cart':
            self.remove_position_from_cart(text_data['position_id'])
        elif message_type == 'recover_position_from_cart':
            self.recover_position_from_cart(text_data['book_id'], text_data['count'])

    def activate_position(self, position_id):
        position = Position.objects.get(id=int(position_id))
        position.is_active = True
        position.save()

    def deactivate_position(self, position_id):
        position = Position.objects.get(id=int(position_id))
        position.is_active = False
        position.save()

    def minus_book_count(self, position_id):
        position = Position.objects.get(id=int(position_id))
        position.count -= 1
        position.save()

    def plus_book_count(self, position_id):
        position = Position.objects.get(id=int(position_id))
        position.count += 1
        position.save()

    def remove_position_from_cart(self, position_id):
        position = Position.objects.get(id=int(position_id))
        position.delete()

    def recover_position_from_cart(self, book_id, count):
        user_cart = Cart.objects.get(user=self.user)
        book = Book.objects.get(id=book_id)
        Position.objects.create(cart=user_cart, book=book, count=count)


class CommentUserConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message_type = text_data['message_type']

        if message_type == 'comment_delete':
            self.comment_delete(int(text_data['comment_id']))

        elif message_type == 'send_subcomment':
            self.save_subcomment(
                int(text_data['book_id']),
                int(text_data['comment_id']),
                text_data['comment_text']
            )

        elif message_type == 'comment_change':
            self.comment_change(int(text_data['comment_id']), text_data['new_text'])

    def comment_delete(self, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if comment.user == self.user:
            if not comment.comment_set.all():
                comment.delete()
            else:
                comment.is_delete = True
                comment.date_change = timezone.now()
                comment.save()

    def save_subcomment(self, book_id, comment_id, comment_text):
        book = Book.objects.get(id=book_id)
        comment = Comment.objects.get(id=comment_id)
        if comment.main_comment:
            Comment.objects.create(
                user=self.user,
                book=book,
                comment_to=comment,
                main_comment=comment.main_comment,
                text=comment_text
            )
        else:
            Comment.objects.create(
                user=self.user,
                book=book,
                comment_to=comment,
                main_comment=comment,
                text=comment_text
            )

    def comment_change(self, comment_id, new_text):
        comment = Comment.objects.get(id=comment_id)
        if self.user == comment.user:
            comment.text = new_text
            comment.date_change = timezone.now()
            comment.save()


class ConnectionHistoryConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.update_user_status('online')
        self.accept()

    def disconnect(self, code=None):
        if self.user.is_authenticated:
            self.update_user_status('offline')

    def receive(self, text_data):
        text_data = json.loads(text_data)

    def update_user_status(self, status):
        connection, created = ConnectionHistory.objects.get_or_create(user=self.user)
        if status == 'online':
            connection.connections += 1
        else:
            connection.connections -= 1
            connection.last_activity = timezone.now()
        connection.save()
