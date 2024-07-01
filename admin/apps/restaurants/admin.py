from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(ModelAdmin):
    list_display = ('id', 'name', 'is_verified', 'address', 'phone_number')
    search_fields = ('id', 'name', 'is_verified', 'phone_number')
    # prepopulated_fields = {"slug": ("name",)}
    list_filter = ('is_verified', 'address', 'phone_number')

