from django import template
from store.models import Genre, Book


register = template.Library()


@register.inclusion_tag('store/sidebar_genres_tag.html')
def sidebar_genres_tag():
    genres = Genre.objects.all()[:7]
    return {'sidebar_genres': genres}


@register.inclusion_tag('store/sidebar_books_tag.html')
def sidebar_books_tag():
    books = Book.objects.all()[:7]
    return {'sidebar_books': books}
