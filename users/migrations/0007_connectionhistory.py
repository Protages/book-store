# Generated by Django 4.0.4 on 2022-06-03 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connectionhistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=255, verbose_name='id устройства')),
                ('status', models.CharField(choices=[('online', 'Онлайн'), ('offline', 'Офлайн')], default='online', max_length=10, verbose_name='статус')),
                ('first_login', models.DateTimeField(auto_now_add=True, verbose_name='первый вход')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='последний вход')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'история соединений',
                'verbose_name_plural': 'истории соединения',
                'unique_together': {('user', 'device_id')},
            },
        ),
    ]