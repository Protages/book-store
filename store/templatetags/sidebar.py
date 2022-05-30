from django import template
from store.models import Genre


register = template.Library()


@register.inclusion_tag('store/sidebar_genres_tag.html')
def sidebar_genres_tag():
    genres = Genre.objects.all()
    return {'genres': genres}
