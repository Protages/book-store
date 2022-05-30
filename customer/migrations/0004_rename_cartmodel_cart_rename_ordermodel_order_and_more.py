# Generated by Django 4.0.4 on 2022-05-19 08:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_agereadmodel_slug_alter_authormodel_slug_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0003_ordermodel_remove_cartmodel_positions_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartModel',
            new_name='Cart',
        ),
        migrations.RenameModel(
            old_name='OrderModel',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='PositionModel',
            new_name='Position',
        ),
    ]