from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class Menu(BaseModel):
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        db_table = 'menus'
        managed = False

    def __str__(self):
        return self.name


class Parameters(BaseModel):
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        db_table = 'parameters'
        managed = False

    def __str__(self):
        return self.name


class Dish(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    restaurant = models.ForeignKey('restaurants.Restaurant', related_name='dishes', on_delete=models.CASCADE)
    price = models.FloatField()
    menu = models.ForeignKey(Menu, related_name='dishes', on_delete=models.CASCADE)
    discounted_price = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = 'dishes'
        managed = False

    def __str__(self):
        return self.name


class DishParameter(BaseModel):
    dish = models.ForeignKey(Dish, related_name='params', on_delete=models.CASCADE)
    key = models.ForeignKey(Parameters, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'dish_parameters'
        managed = False

    def __str__(self):
        return f'{self.key}: {self.value}'


class Discount(BaseModel):
    dish = models.OneToOneField(Dish, related_name='discount', on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    price = models.FloatField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'discounts'
        managed = False

    def __str__(self):
        return f'{self.dish.name}: {self.start_date} - {self.end_date}'
