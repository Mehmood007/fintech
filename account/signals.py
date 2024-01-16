from django.db.models.signals import post_save
from django.dispatch import receiver

from userauths.models import User

from .models import Account


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(
    sender: User, instance: User, created: bool, **kwargs
) -> None:
    if created:
        Account.objects.create(user=instance)
    else:
        if not Account.objects.filter(user=instance).exists():
            Account.objects.create(user=instance)
