from django.views.generic import ListView

from .models import (
    Collection,
    SubCollections,
    AgeRead,
    LocationEvents,
    Book,
)
from .utils import MenuMixin, MenuAndSortMixin


class CollectionsView(MenuMixin, ListView):
    model = Collection
    template_name = 'store/collections/collections.html'
    context_object_name = 'collections'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context(menu_selected='collections-page'))

        return context

    def get_queryset(self):
        return self.model.objects.all()


class CollectionView(MenuMixin, ListView):
    model = Book
    template_name = 'store/collections/collection_detail.html'
    context_object_name = 'books'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.collection = Collection.objects.get(slug=self.kwargs.get('slug'))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context())
        context['collection'] = self.collection

        return context

    def get_queryset(self):
        return self.collection.book_set.all()


class SubCollectionView(MenuAndSortMixin, ListView):
    model = Book
    template_name = 'store/collections/subcollection_detail.html'
    context_object_name = 'books'
    paginate_by = 3
    sub_collection_model = SubCollections

    def get(self, request, *args, **kwargs):
        self.sub_collection = self.sub_collection_model.objects.get(
            slug=self.kwargs.get('slug')
        )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_and_sort_context())
        context['sub_collection'] = self.sub_collection

        if self.sub_collection_model != AgeRead and \
           self.sub_collection_model != LocationEvents:
            context['collection'] = self.sub_collection.collection

        return context

    def get_queryset(self):
        return self.get_sort_queryset(self.sub_collection.book_set)


class AgeReadCollectionView(MenuMixin, ListView):
    model = Book
    template_name = 'store/collections/ageread_collection.html'
    context_object_name = 'books'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.sub_collections = AgeRead.objects.all()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context())
        context['sub_collections'] = self.sub_collections

        return context

    def get_queryset(self):
        return self.model.objects.all()


class AgeReadDetailView(SubCollectionView):
    template_name = 'store/collections/ageread_detail.html'
    sub_collection_model = AgeRead


class LocationEventsCollectionView(MenuMixin, ListView):
    model = Book
    template_name = 'store/collections/location_events_collection.html'
    context_object_name = 'books'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.sub_collections = LocationEvents.objects.all()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_menu_context())
        context['sub_collections'] = self.sub_collections

        return context

    def get_queryset(self):
        return self.model.objects.all()


class LocationEventsDetailView(SubCollectionView):
    template_name = 'store/collections/location_events_detail.html'
    sub_collection_model = LocationEvents
    # model = BookModel
    # context_object_name = 'books'
    # paginate_by = 3

    # def get(self, request, *args, **kwargs):
    #     self.sub_collection = LocationEventsModel.objects.get(
    # slug=self.kwargs.get('slug'))

    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     extra_context = self.get_menu_and_sort_context()

    #     context['sub_collection'] = self.sub_collection

    #     return dict(list(context.items()) + list(extra_context.items()))

    # def get_queryset(self):
    #     return self.get_sort_queryset(self.sub_collection.bookmodel_set)
