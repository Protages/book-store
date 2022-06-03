from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from store.models import Book


USER = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        USER,
        primary_key=True,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    favourites = models.ManyToManyField(Book, verbose_name='избранное', blank=True)

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'Корзина польз. {self.user.first_name}'


class Order(models.Model):
    IN_PROCESSING = 'IP'
    SENT = 'S'
    WAIT = 'W'
    COMPLETED = 'CP'
    CANCEL = 'CL'
    STATUS = [
        (IN_PROCESSING, 'В обработке'),
        (SENT, 'Отправлен в пункт выдачи'),
        (WAIT, 'Ожидает получения'),
        (COMPLETED, 'Завершен'),
        (CANCEL, 'Отменен')
    ]

    cart = models.ForeignKey(
        Cart,
        verbose_name='корзина',
        on_delete=models.CASCADE
    )
    total_price = models.PositiveIntegerField(verbose_name='общая цена')
    date = models.DateTimeField(verbose_name='время покупки', default=timezone.now)
    status = models.CharField(
        verbose_name='статус',
        max_length=128,
        choices=STATUS,
        default=IN_PROCESSING
    )
    comment = models.TextField(
        verbose_name='комментарий к заказу',
        blank=True
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'заказ польз. {self.cart.user.first_name}'

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'order_id': self.pk})


class Position(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name='книга',
        on_delete=models.SET_NULL,
        null=True
    )
    cart = models.ForeignKey(
        Cart,
        verbose_name='корзина',
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        verbose_name='заказ',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    count = models.PositiveIntegerField(verbose_name='количество', default=1)
    purchase_price = models.PositiveIntegerField(
        verbose_name='цена покупки',
        help_text='только в момент покупки',
        blank=True, null=True
    )
    is_active = models.BooleanField(verbose_name='активна', default=True)
    is_close = models.BooleanField(verbose_name='закрыта', default=False)

    class Meta:
        verbose_name = 'позиция'
        verbose_name_plural = 'позиции'

    def __str__(self):
        return f'Позиция польз. {self.cart.user.first_name}'


class BrowsingHistory(models.Model):
    book = models.ForeignKey(Book, verbose_name='книга', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='корзина', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='дата', default=timezone.now)

    class Meta:
        verbose_name = 'история просмотра'
        verbose_name_plural = 'истории просмотров'
        ordering = ['-date']

    def __str__(self):
        return f'История просмотра {self.pk}'
