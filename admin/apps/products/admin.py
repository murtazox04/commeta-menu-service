from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Menu, Parameters, Dish, DishParameter, Discount


@admin.register(Menu)
class MenuAdmin(ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name', 'restaurant')
    # prepopulated_fields = {"slug": ("name",)}
    list_filter = ('id', 'name')


@admin.register(Parameters)
class ParameterAdmin(ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    # prepopulated_fields = {"slug": ("name",)}
    list_filter = ('id', 'name')


@admin.register(Dish)
class DishAdmin(ModelAdmin):
    list_display = ('id', 'name', 'price', 'discounted_price')
    search_fields = ('id', 'name', 'price', 'menu', 'discounted_price')
    # prepopulated_fields = {"slug": ("name",)}
    list_filter = ('id', 'name', 'price', 'discounted_price')


@admin.register(DishParameter)
class DishParameterAdmin(ModelAdmin):
    list_display = ('id', 'value')
    search_fields = ('id', 'key', 'value')
    # prepopulated_fields = {"slug": ("key", "value")}
    list_filter = ('id', 'value')


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'price', 'is_active')
    search_fields = ('id', 'dish', 'start_date', 'end_date', 'price', 'is_active')
    # prepopulated_fields = {"slug": ("dish",)}
    list_filter = ('id', 'start_date', 'end_date', 'price', 'is_active')
