# Generated by Django 4.0.4 on 2022-06-05 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_connectionhistory_unique_together_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectionhistory',
            old_name='last_login',
            new_name='last_activity',
        ),
    ]
