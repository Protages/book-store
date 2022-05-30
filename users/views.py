from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib import messages

from urllib.parse import urlencode

from .forms import UserLoginForm, UserRegistrationForm


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = 'main-page'
    next_url = ''

    def post(self, request, *args, **kwargs):
        self.next_url = self.request.POST.get('next')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            self.next_url = self.request.GET.get('next')
        context.update({'next_url': self.next_url})

        return context

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        if email and password:
            user = authenticate(self.request, email=email, password=password)

            if user is not None:
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                messages.add_message(
                    self.request,
                    messages.INFO,
                    'EMAIL или ПАРОЛЬ введены не правильно.'
                )
                context = self.get_context_data()
                return self.render_to_response(context)

    def get_success_url(self):
        if self.next_url:
            return self.next_url
        return self.success_url


class RegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = 'login'
    next_url = ''

    def post(self, request, *args, **kwargs):
        self.next_url = self.request.POST.get('next')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            self.next_url = self.request.GET.get('next')
        context.update({'next_url': self.next_url})

        return context

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.next_url:
            base_url = reverse(self.success_url)
            query_next_url = urlencode({'next': self.next_url})
            return f'{base_url}?{query_next_url}'

        return self.success_url


class LogoutView(View):
    next_url = 'main-page'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('next'):
            self.next_url = self.request.GET.get('next')

        if request.user.is_authenticated:
            logout(request)

        return redirect(self.next_url)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
