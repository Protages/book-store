from django.contrib import admin
from .models import Cart, Order, Position


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_favourites')

    def get_favourites(self, obj):
        favourites = obj.favourites.all()[:3]
        if not favourites:
            return 'Список пуст'
        return ', '.join(book.title for book in favourites)

    get_favourites.short_description = 'Избранное'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'total_price', 'date', 'status', 'comment')

    def get_user(self, obj):
        return obj.cart.user

    get_user.short_description = 'Пользователь'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'count', 'get_user', 'purchase_price')

    def get_user(self, obj):
        return obj.cart.user

    get_user.short_description = 'Пользователь'
