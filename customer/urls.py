from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('favorites/', views.FavouritesView.as_view(), name='favourites'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('make_order/', views.MakeOrderView.as_view(), name='make_order'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path(
        'order_detail/<int:order_id>/',
        views.OrderDetailView.as_view(),
        name='order_detail'
    ),
    path('messages/', views.MessagesView.as_view(), name='messages'),
    path('history/', views.BrowsingHistoryView.as_view(), name='history'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
]
