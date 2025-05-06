from django.contrib import admin

# Register your models here.

from .models import Card, CartItem


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'card_for_sale',
        'quantity',
        'added_at',
    ]