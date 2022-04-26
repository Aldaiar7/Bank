from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cart, StatusChoices


@receiver(post_save, sender=Cart)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if created:
        instance.cart_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == StatusChoices.active
            instance.task.save()
