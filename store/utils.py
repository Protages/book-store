
class MenuMixin():
    __MENU = [
        {'title': 'Жанры', 'url_name': 'genres-page'},
        {'title': 'Подборки', 'url_name': 'collections-page'},
        {'title': 'Авторы', 'url_name': 'authors-page'},
    ]

    def get_menu_context(self, menu_selected=None):
        return {'menu': self.__MENU, 'menu_selected': menu_selected}


class SortMixin():

    def get_sort_context(self):
        if self.sort:
            return {'sort_selected': self.sort}
        return {}

    def get_sort_queryset(self, model_objects):
        self.sort = self.request.GET.get('sort')

        if self.sort == 'new':
            return model_objects.order_by('-date_added')
        elif self.sort == 'popular':
            return model_objects.all()  # CHANGE!

        return model_objects.all()


class MenuAndSortMixin(MenuMixin, SortMixin):

    def get_menu_and_sort_context(self, menu_selected=None):
        menu_context = self.get_menu_context(menu_selected=menu_selected)
        sort_context = self.get_sort_context()

        return dict(list(menu_context.items()) + list(sort_context.items()))
