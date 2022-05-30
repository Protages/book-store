from django.views.generic import DetailView, ListView
from django.db.models import Count

from .models import (
    Author,
    Genre,
    Book,
)
from .utils import MenuAndSortMixin, MenuMixin


class MainView(MenuAndSortMixin, ListView):
    model = Book
    template_name = 'store/main.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_and_sort_context())

        return context

    def get_queryset(self):
        return self.get_sort_queryset(self.model.objects)


class BookView(MenuMixin, DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context())

        return context

    def get_object(self):
        return self.model.objects.get(slug=self.kwargs.get('slug'))


class GenresView(MenuMixin, ListView):
    model = Genre
    template_name = 'store/genres.html'
    context_object_name = 'genres'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context(menu_selected='genres-page'))

        return context

    def get_queryset(self):
        return self.model.objects.all()


class GenreView(MenuAndSortMixin, ListView):
    model = Book
    template_name = 'store/genre_detail.html'
    context_object_name = 'books'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.genre = Genre.objects.get(slug=self.kwargs.get('slug'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_and_sort_context())
        context['genre'] = self.genre

        return context

    def get_queryset(self):
        return self.get_sort_queryset(self.genre.book_set)


class AuthorsView(MenuMixin, ListView):
    model = Author
    template_name = 'store/authors.html'
    context_object_name = 'authors'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context(menu_selected='authors-page'))

        if self.query:
            context['query'] = self.query

        return context

    def get_queryset(self):
        self.query = self.request.GET.get('q')
        if self.query:
            return self.model.objects.filter(name__icontains=self.query)\
                .annotate(books_count=Count('book'))
        else:
            return self.model.objects.all().annotate(books_count=Count('book'))


class AuthorView(MenuMixin, ListView):
    model = Book
    template_name = 'store/author_detail.html'
    context_object_name = 'books'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.author = Author.objects.get(slug=self.kwargs.get('slug'))
        self.books = self.author.book_set.all()
        self.genres = Genre.objects.filter(book__in=self.books).distinct().\
            annotate(books_count=Count('book'))
        self.query = self.request.GET.get('genre')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context())
        context['author'] = self.author
        context['genres'] = self.genres

        if self.query:
            context['genre_selected'] = self.query
        else:
            context['genre_selected'] = 'all'

        return context

    def get_queryset(self):
        if self.query:
            return self.books.filter(genre__slug=self.query)
        return self.books
