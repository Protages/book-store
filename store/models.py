import os
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from .storage import OverwriteStorage


USER_MODEL = get_user_model()


def slug_path(instance, filename):
    model_name = instance._meta.model_name
    image_name = f'{model_name}_image.png'
    return os.path.join(
        f'{model_name}',
        f'{instance.slug}',
        f'{image_name}'
    )


def slug_file_path(instance, filename):
    model_name = instance._meta.model_name
    return f'{model_name}/{instance.slug}/files/{filename}'


class Author(models.Model):
    name = models.CharField(verbose_name='имя', max_length=120, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=120, unique=True)
    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        default='default_author_image/default_author_img.png'
    )
    biograpy = models.TextField(verbose_name='биография')
    centry_of_life = models.PositiveSmallIntegerField(verbose_name='век')
    country = models.CharField(verbose_name='страна', max_length=120)

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'slug': self.slug})


class Genre(models.Model):
    title = models.CharField(verbose_name='название', max_length=120, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=120, unique=True)
    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        default='default_genre_image/default_genre_img.png',
        storage=OverwriteStorage()
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre-detail', kwargs={'slug': self.slug})


class Collection(models.Model):
    title = models.CharField(verbose_name='название', max_length=120, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=120, unique=True)
    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        default='default_collection_image/default_collection_img.jpg',
        storage=OverwriteStorage()
    )

    class Meta:
        verbose_name = 'коллекция'
        verbose_name_plural = 'коллекции'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('collection-detail', kwargs={'slug': self.slug})


class SubCollections(models.Model):
    title = models.CharField(verbose_name='название', max_length=120, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=120, unique=True)
    collection = models.ForeignKey(
        Collection,
        verbose_name='коллекция',
        on_delete=models.CASCADE,
        blank=True
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        blank=True, null=True,
        storage=OverwriteStorage()
    )
    description = models.CharField(
        verbose_name='описание',
        max_length=256,
        blank=True
    )

    class Meta:
        verbose_name = 'подколлекция'
        verbose_name_plural = 'подколлекции'

    def __str__(self):
        return self.title


class AgeRead(models.Model):
    title = models.CharField(verbose_name='название', max_length=120, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=120, unique=True)

    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        blank=True, null=True,
        storage=OverwriteStorage()
    )
    description = models.CharField(
        verbose_name='описание',
        max_length=256,
        blank=True
    )

    class Meta:
        verbose_name = 'возвраст читателя'
        verbose_name_plural = 'возвраста читателя'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ageread-detail', kwargs={
            'slug': self.slug
        })


class LocationEvents(models.Model):
    title = models.CharField(verbose_name='название', max_length=120, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=120, unique=True)

    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        blank=True, null=True,
        storage=OverwriteStorage()
    )
    description = models.CharField(
        verbose_name='описание',
        max_length=256,
        blank=True
    )

    class Meta:
        verbose_name = 'место действия'
        verbose_name_plural = 'места действия'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('location-detail', kwargs={
            'slug': self.slug
        })


class Book(models.Model):
    title = models.CharField(verbose_name='название', max_length=120, unique=True)
    original_title = models.CharField(
        verbose_name='оригинальное название',
        max_length=120,
        blank=True
    )
    slug = models.SlugField(verbose_name='слаг', max_length=120, unique=True)
    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        default='default_book_image/default_book_img.png',
        storage=OverwriteStorage()
    )
    book_file = models.FileField(
        verbose_name='файл',
        upload_to=slug_file_path,
        blank=True, null=True
    )

    author = models.ForeignKey(
        Author,
        verbose_name='автор',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, verbose_name='жанры', blank=True)

    description = models.TextField(verbose_name='описание', max_length=512)
    full_description = models.TextField(
        verbose_name='полное описание',
        blank=True
    )
    year = models.CharField(
        verbose_name='время событий',
        max_length=30,
        blank=True
    )
    pages = models.PositiveIntegerField(
        verbose_name='кол-во страниц',
        blank=True, null=True
    )

    age = models.ManyToManyField(
        AgeRead,
        verbose_name='возвраст читателя',
        blank=True
    )
    location = models.ManyToManyField(
        LocationEvents,
        verbose_name='место событий',
        blank=True
    )
    collection = models.ManyToManyField(
        Collection,
        verbose_name='коллекции',
        blank=True
    )
    sub_collection = models.ManyToManyField(
        SubCollections,
        verbose_name='подколлекции',
        blank=True
    )

    price = models.PositiveIntegerField(verbose_name='текущая цена')
    old_price = models.PositiveIntegerField(
        verbose_name='старая цена',
        blank=True, null=True
    )

    date_added = models.DateTimeField(
        verbose_name='дата добавления',
        default=timezone.now
    )

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    comment_to = models.ForeignKey(
        'self',
        verbose_name='на комментарий',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    main_comment = models.ForeignKey(
        'self',
        related_name='subcomments',
        verbose_name='главный комментарий',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    user = models.ForeignKey(
        USER_MODEL,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, verbose_name='книга', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст')
    date = models.DateTimeField(verbose_name='дата написания', default=timezone.now)
    date_change = models.DateTimeField(
        verbose_name='дата изменения',
        blank=True, null=True
    )
    is_delete = models.BooleanField(verbose_name='удален', default=False)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.book.title} - {self.pk}'
