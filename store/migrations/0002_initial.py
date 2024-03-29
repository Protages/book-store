# Generated by Django 4.0.4 on 2022-05-11 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='age',
            field=models.ManyToManyField(blank=True, to='store.agereadmodel', verbose_name='возвраст читателя'),
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.authormodel', verbose_name='автор'),
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='collection',
            field=models.ManyToManyField(blank=True, to='store.collectionmodel', verbose_name='коллекции'),
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='genre',
            field=models.ManyToManyField(blank=True, to='store.genremodel', verbose_name='жанры'),
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='location',
            field=models.ManyToManyField(blank=True, to='store.locationeventsmodel', verbose_name='место событий'),
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='sub_collection',
            field=models.ManyToManyField(blank=True, to='store.subcollectionsmodel', verbose_name='подколлекции'),
        ),
    ]
