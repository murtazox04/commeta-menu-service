from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import CartItem, Cart


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('guid', 'total_cost')
    search_fields = ('guid', 'items', 'total_cost')
    list_filter = ('total_cost', 'items')


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ('id', 'quantity', 'total_cost')
    search_fields = ('id', 'dish', 'quantity')
    list_filter = ('id', 'dish')
