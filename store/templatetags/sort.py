from django import template


register = template.Library()


@register.inclusion_tag('store/sort_tag.html')
def sort_tag(sort_selected):
    if not sort_selected:
        sort_selected = 'all'
    return {'sort_selected': sort_selected}


@register.inclusion_tag('store/author_genre_sort_tag.html')
def author_genre_sort_tag(genres, author, genre_selected='all'):
    return {'genres': genres, 'author': author, 'genre_selected': genre_selected}
