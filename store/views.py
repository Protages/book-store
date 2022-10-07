from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from customer.models import Cart, BrowsingHistory

from .models import (
    Author,
    Genre,
    Book,
    Comment
)
from .utils import MenuAndSortMixin, MenuMixin


USER_MODEL = get_user_model()


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


class SearchView(MenuMixin, View):
    template_name = 'store/search.html'

    def get(self, request, *args, **kwargs):
        context = self.get_menu_context()

        query = ' '.join(self.request.GET.get('q').split())
        category = self.request.GET.get('category')

        books = Book.objects.filter(title__icontains=query)
        authors = Author.objects.filter(name__icontains=query)
        genres = Genre.objects.filter(title__icontains=query)

        search_filter = []
        if books:
            search_filter.append({
                'title': 'Книги',
                'category': 'books',
                'count': len(books)
            })
        if authors:
            search_filter.append({
                'title': 'Авторы',
                'category': 'authors',
                'count': len(authors)
            })
        if genres:
            search_filter.append({
                'title': 'Жанры',
                'category': 'genres',
                'count': len(genres)
            })

        if not category and search_filter:
            category = search_filter[0]['category']

        context.update({
            'query': query,
            'books': books,
            'authors': authors,
            'genres': genres,
            'category': category,
            'search_filter': search_filter
        })

        return render(request, self.template_name, context)


class BookView(MenuMixin, DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'

    def get(self, request, *args, **kwargs):
        self.add_history_cart()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            Comment.objects.create(
                user=self.request.user,
                book=self.get_object(),
                text=self.request.POST.get('comment-text')
            )
        return redirect('book-detail', slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context())
        context.update({'comments': self.book.comment_set.filter(comment_to=None)})

        return context

    def get_object(self):
        self.book = Book.objects.get(slug=self.kwargs.get('slug'))
        return self.book

    def add_history_cart(self):
        if self.request.user.is_authenticated:
            user_cart = Cart.objects.get(user=self.request.user)
            BrowsingHistory.objects.update_or_create(
                book=self.get_object(),
                cart=user_cart,
                defaults={'date': timezone.now()}
            )


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

    def get(self, request, *args, **kwargs):
        self.query = self.request.GET.get('q')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context(menu_selected='authors-page'))

        if self.query:
            context['query'] = self.query

        return context

    def get_queryset(self):
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


class UserProfileView(MenuMixin, DetailView):
    model = USER_MODEL
    template_name = 'store/user_profile.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        user_cart = self.get_object().cart

        user_cart_books = user_cart.favourites.all()
        user_positions_books = Book.objects.filter(
            position__in=user_cart.position_set.all()
        )

        self.books_interest = user_cart_books.union(user_positions_books)[0:10]

        self.authors_interest = Author.objects.filter(
            book__in=self.books_interest.values('pk')
        ).distinct()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context())
        context.update({
            'books_interest': self.books_interest,
            'authors_interest': self.authors_interest
        })

        return context

    def get_object(self):
        return USER_MODEL.objects.get(user_name=self.kwargs.get('user_name'))
