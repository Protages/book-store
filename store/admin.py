from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Author,
    Genre,
    Collection,
    SubCollections,
    AgeRead,
    LocationEvents,
    Book,
    Comment
)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'get_genres', 'get_ages', 'pages', 'price')
    prepopulated_fields = {'slug': ('title',)}

    def get_genres(self, obj):
        return ', '.join(genre.title for genre in obj.genre.all())

    def get_ages(self, obj):
        return ', '.join(age.title for age in obj.age.all())

    get_genres.short_description = 'жанры'
    get_ages.short_description = 'возвраст читателя'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'centry_of_life', 'country', 'image_preview')
    prepopulated_fields = {'slug': ('name',)}

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" height="30" style="object-fit:contain" />'
            )
        else:
            return 'Нет изображения'

    image_preview.short_description = 'изображение'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image_preview')
    prepopulated_fields = {'slug': ('title',)}

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" height="30" style="object-fit:contain" />'
            )
        else:
            return 'Нет изображения'

    image_preview.short_description = 'изображение'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SubCollections)
class SubCollectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'collection')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(AgeRead)
class AgeReadAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(LocationEvents)
class LocationEventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'date', 'date_change')
