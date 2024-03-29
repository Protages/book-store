# Generated by Django 4.0.4 on 2022-05-13 07:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_agereadmodel_slug_alter_authormodel_slug_and_more'),
        ('customer', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField(verbose_name='общая цена')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время покупки')),
                ('status', models.CharField(choices=[('IP', 'В обработке'), ('S', 'Отправлен в пункт выдачи'), ('W', 'Ожидает получения'), ('CP', 'Завершен'), ('CL', 'Отменен')], default='IP', max_length=128, verbose_name='статус')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий к заказу')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.RemoveField(
            model_name='cartmodel',
            name='positions',
        ),
        migrations.AddField(
            model_name='positionmodel',
            name='cart',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='customer.cartmodel', verbose_name='корзина'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='positionmodel',
            name='is_close',
            field=models.BooleanField(default=False, verbose_name='закрыта'),
        ),
        migrations.AlterField(
            model_name='positionmodel',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.bookmodel', verbose_name='книга'),
        ),
        migrations.AlterField(
            model_name='positionmodel',
            name='count',
            field=models.PositiveIntegerField(default=1, verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='positionmodel',
            name='purchase_price',
            field=models.PositiveIntegerField(blank=True, help_text='только в момент покупки', null=True, verbose_name='цена покупки'),
        ),
        migrations.DeleteModel(
            name='BuyModel',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.cartmodel', verbose_name='корзина'),
        ),
        migrations.AddField(
            model_name='positionmodel',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.ordermodel', verbose_name='заказ'),
        ),
    ]
