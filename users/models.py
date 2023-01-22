import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from django_countries.fields import CountryField

from .storage import OverwriteStorage


def slug_path(instance, filename):
    model_name = instance._meta.model_name
    image_name = 'profile_image.png'
    return os.path.join(
        f'{model_name}',
        f'{instance.user_name}',
        'img',
        f'{image_name}'
    )


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError('Вы должны предоставить email адресс.')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)
        return self._create_user(email, user_name, password, **other_fields)

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, user_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    NOT_SELECTED = 'NS'
    MAN = 'M'
    WOOMAN = 'W'
    GENDER = [
        (NOT_SELECTED, 'Не выбрано'),
        (MAN, 'Мужчина'),
        (WOOMAN, 'Женщина'),
    ]
    user_name_validator = UnicodeUsernameValidator()

    email = models.EmailField(verbose_name='email', unique=True)
    user_name = models.CharField(
        max_length=120,
        verbose_name='логин',
        validators=[user_name_validator],
        unique=True
    )
    first_name = models.CharField(
        max_length=120,
        verbose_name='имя пользователя',
        blank=True
    )
    date_joined = models.DateTimeField(
        verbose_name='дата регистрации',
        default=timezone.now
    )

    image = models.ImageField(
        verbose_name='изображение',
        upload_to=slug_path,
        storage=OverwriteStorage(),
        default='default_user_image/default_user_img.png',

    )
    gender = models.CharField(
        verbose_name='пол',
        max_length=30,
        choices=GENDER,
        default=NOT_SELECTED
    )
    birthday = models.DateField(verbose_name='дата рождения', blank=True, null=True)
    phone = models.CharField(
        verbose_name='телефон',
        max_length=15,
        unique=True,
        blank=True, null=True
    )
    about = models.TextField(verbose_name='о себе', blank=True)
    country = CountryField(verbose_name='страна', blank_label='(выберите страну)')

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.user_name


class ConnectionHistory(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    connections = models.IntegerField(verbose_name='кол-во соединений', default=0)
    first_login = models.DateTimeField(verbose_name='первый вход', auto_now_add=True)
    last_activity = models.DateTimeField(verbose_name='последний вход', auto_now=True)

    class Meta:
        verbose_name = 'история соединений'
        verbose_name_plural = 'истории соединения'

    def __str__(self):
        return f'Соеденение {self.user.first_name}'

    @property
    def is_online(self):
        return self.connections > 0

    @property
    def is_offline(self):
        return self.connections <= 0
