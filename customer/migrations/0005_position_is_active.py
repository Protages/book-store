# Generated by Django 4.0.4 on 2022-05-26 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_rename_cartmodel_cart_rename_ordermodel_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
    ]
