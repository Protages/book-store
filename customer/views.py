from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View, FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cart, Order, Position, BrowsingHistory
from .utils import UserMenuMixin, OrderSortAndUserMenuMixin
from .forms import UserSettingForm
from store.models import Book


USER_MODEL = get_user_model()


class ProfileView(LoginRequiredMixin, UserMenuMixin, DetailView):
    model = USER_MODEL
    template_name = 'customer/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_menu_context())

        return context

    def get_object(self, queryset=None):
        return self.request.user


class FavouritesView(LoginRequiredMixin, UserMenuMixin, ListView):
    model = Book
    template_name = 'customer/favourites.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_menu_context(user_menu_selected='favourites'))

        return context

    def get_queryset(self):
        return Cart.objects.get(user=self.request.user).favourites.all()


class CartView(LoginRequiredMixin, UserMenuMixin, ListView):
    model = Position
    template_name = 'customer/cart.html'
    context_object_name = 'positions'

    def get(self, request, *args, **kwargs):
        self.cart = Cart.objects.get(user=self.request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_menu_context(user_menu_selected='cart'))

        return context

    def get_queryset(self):
        return Position.objects.filter(cart=self.cart, is_close=False)


class MakeOrderView(LoginRequiredMixin, UserMenuMixin, View):  # CreateView mb!!!
    template_name = 'customer/make_order.html'
    success_url = 'orders'

    def get(self, request, *args, **kwargs):
        context = self.get_user_menu_context(user_menu_selected='cart')

        positons = Position.objects.filter(
            cart=self.request.user.cart,
            is_active=True,
            is_close=False
        )
        total_price = sum([
            position.book.price * position.count for position in positons
        ])

        context.update({'positions': positons, 'total_price': total_price})
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        positions_id = [int(id) for id in self.request.POST.getlist('position_id')]

        positons = Position.objects.filter(id__in=positions_id)
        total_price = sum([
            position.book.price * position.count for position in positons
        ])
        comment = self.request.POST.get('comment')
        new_order = Order.objects.create(
            cart=self.request.user.cart,
            total_price=total_price,
            comment=comment
        )
        for position in positons:
            position.order = new_order
            position.purchase_price = position.book.price
            position.is_close = True
            position.save()

        return redirect(self.success_url)


class OrdersView(LoginRequiredMixin, OrderSortAndUserMenuMixin, ListView):
    model = Order
    template_name = 'customer/orders.html'
    context_object_name = 'orders'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.query = self.request.GET.get('q')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_user_menu_and_order_sort_context(
                user_menu_selected='orders',
                order_sort_selected=self.query
            )
        )
        return context

    def get_queryset(self):
        if self.query:
            return Cart.objects.get(user=self.request.user).order_set.filter(
                status=self.query
            )
        return Cart.objects.get(user=self.request.user).order_set.all()


class OrderDetailView(LoginRequiredMixin, UserMenuMixin, ListView):
    model = Position
    template_name = 'customer/order_detail.html'
    context_object_name = 'positions'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.order = Order.objects.get(id=kwargs.get('order_id'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_menu_context())
        context.update({'order': self.order})

        return context

    def get_queryset(self):
        return Position.objects.filter(order=self.order)


class MessagesView(LoginRequiredMixin, UserMenuMixin, View):
    template_name = 'customer/messages.html'

    def get(self, request, *args, **kwargs):
        context = self.get_user_menu_context(user_menu_selected='messages')
        return render(request, self.template_name, context)


class BrowsingHistoryView(LoginRequiredMixin, UserMenuMixin, ListView):
    model = BrowsingHistory
    template_name = 'customer/history.html'
    context_object_name = 'stories'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.user_cart = Cart.objects.get(user=self.request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_menu_context(user_menu_selected='history'))

        return context

    def get_queryset(self):
        return BrowsingHistory.objects.filter(cart=self.user_cart)


class SettingsView(LoginRequiredMixin, UserMenuMixin, FormView):
    form_class = UserSettingForm
    template_name = 'customer/settings.html'
    success_url = 'settings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_menu_context(user_menu_selected='settings'))
        return context

    def form_valid(self, form):
        print(form.files)
        form.save()
        return redirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    # def get_form(self, form_class=None):
    #     return self.form_class(instance=self.request.user, **self.get_form_kwargs())


class ResetPasswordView(LoginRequiredMixin, UserMenuMixin, View):
    template_name = 'customer/reset_password.html'

    def get(self, request, *args, **kwargs):
        context = self.get_user_menu_context(user_menu_selected='reset_password')
        return render(request, self.template_name, context)
