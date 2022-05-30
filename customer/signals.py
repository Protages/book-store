from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Cart


@receiver(post_save, sender=get_user_model())
def user_card_signal(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        cart = Cart.objects.create(user=instance)
        cart.save()
