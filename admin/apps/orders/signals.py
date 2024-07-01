from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from .models import CartItem, Cart


@receiver(post_save, sender=CartItem)
def update_cart_item_total_cost(sender, instance, created, **kwargs):
    if not instance.dish:
        return

    if instance.dish.discounted_price is not None:
        new_total_cost = instance.quantity * instance.dish.discounted_price
    else:
        new_total_cost = instance.quantity * instance.dish.price

        # Use update() to avoid triggering the signal again
    CartItem.objects.filter(pk=instance.pk).update(total_cost=new_total_cost)


@receiver(post_save, sender=CartItem)
def update_cart_total_cost(sender, instance, created, **kwargs):
    for cart in instance.carts.all():
        cart.total_cost = sum(item.total_cost for item in cart.items.all())
        cart.save()


@receiver(m2m_changed, sender=Cart.items.through)
def update_cart_total_cost_on_m2m(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.total_cost = sum(item.total_cost for item in instance.items.all())
        instance.save()
