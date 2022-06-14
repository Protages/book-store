from django.urls import path

from . import views
from . import collections_views


urlpatterns = [
    path('', views.MainView.as_view(), name='main-page'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/<slug:slug>/', views.BookView.as_view(), name='book-detail'),

    path('genres/', views.GenresView.as_view(), name='genres-page'),
    path('genres/<slug:slug>/', views.GenreView.as_view(), name='genre-detail'),

    path(
        'collections/',
        collections_views.CollectionsView.as_view(),
        name='collections-page'
    ),

    path(
        'collection/po-vozrstam/',
        collections_views.AgeReadCollectionView.as_view(),
        name='ageread-collection'
    ),
    path(
        'collection/po-vozrstam/<slug:slug>/',
        collections_views.AgeReadDetailView.as_view(),
        name='ageread-detail'
    ),

    path(
        'collection/mesto-deystviya/',
        collections_views.LocationEventsCollectionView.as_view(),
        name='location-collection'
    ),
    path(
        'collection/mesto-deystviya/<slug:slug>/',
        collections_views.LocationEventsDetailView.as_view(),
        name='location-detail'
    ),

    path(
        'collection/<slug:slug>/',
        collections_views.CollectionView.as_view(),
        name='collection-detail'
    ),
    path(
        'collection/<slug:collection_slug>/<slug:slug>/',
        collections_views.SubCollectionView.as_view(),
        name='subcollection-detail'
    ),

    path('authors/', views.AuthorsView.as_view(), name='authors-page'),
    path('author/<slug:slug>/', views.AuthorView.as_view(), name='author-detail'),

    path(
        'user/<slug:user_name>/',
        views.UserProfileView.as_view(),
        name='user-profile'
    ),
]
