from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Discount


@receiver(post_save, sender=Discount)
def discount_post_save(sender, instance, **kwargs):
    now = timezone.now()

    if instance.start_date <= now <= instance.end_date and instance.is_active:
        instance.dish.discounted_price = (instance.dish.price - instance.price)
        instance.dish.save()
    else:
        instance.dish.discounted_price = None


@receiver(post_delete, sender=Discount)
def discount_post_delete(sender, instance, **kwargs):
    instance.dish.discounted_price = None
    instance.dish.save()





