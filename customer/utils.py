from store.utils import MenuMixin


class UserMenuMixin(MenuMixin):
    __USER_MENU = [
        {'title': 'Избранное', 'url_name': 'favourites'},
        {'title': 'Корзина', 'url_name': 'cart'},
        {'title': 'Заказы', 'url_name': 'orders'},
        {'title': 'Сообщения', 'url_name': 'messages'},
        {'title': 'История', 'url_name': 'history'},
        {'title': 'Настройки', 'url_name': 'settings'},
        {'title': 'Сброс пароля', 'url_name': 'reset_password'},
    ]

    def get_user_menu_context(self, user_menu_selected=None):
        menu_context = self.get_menu_context()
        menu_context['user_menu'] = self.__USER_MENU
        menu_context['user_menu_selected'] = user_menu_selected

        return menu_context


class OrderSortAndUserMenuMixin(UserMenuMixin):
    __ORDER_SORT = [
        {'title': 'В обработке', 'query': 'in_processing'},
        {'title': 'Отправлен', 'query': 'sent'},
        {'title': 'Ожидает', 'query': 'wait'},
        {'title': 'Завершен', 'query': 'completed'},
        {'title': 'Отменен', 'query': 'cancel'},
    ]

    def get_user_menu_and_order_sort_context(self, user_menu_selected=None,
                                             order_sort_selected=None):
        context = self.get_user_menu_context(user_menu_selected)
        context.update({
            'order_sort': self.__ORDER_SORT,
            'order_sort_selected': order_sort_selected
        })

        return context
