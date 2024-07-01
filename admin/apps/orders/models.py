from uuid import uuid4
from django.db import models

from apps.common.models import BaseModel


class CartItem(BaseModel):
    dish = models.ForeignKey('products.Dish', related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_cost = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'cart_items'
        managed = False

    def __str__(self):
        return f'"ID: "{self.pk} {self.quantity} {self.total_cost}'


class Cart(BaseModel):
    guid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    total_cost = models.FloatField(default=0.0)
    items = models.ManyToManyField(CartItem, related_name='carts', db_table='cart_cart_items')

    class Meta:
        db_table = 'carts'
        managed = False

    def __str__(self):
        return str(self.guid)
