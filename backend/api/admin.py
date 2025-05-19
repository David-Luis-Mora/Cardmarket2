from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Card, CardForSale, CartItem, Profile, Purchase


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'card_for_sale',
        'quantity',
        'added_at',
    ]


@admin.register(CardForSale)
class CardForSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'seller', 'price', 'quantity', 'listed_at')
    list_filter = ('listed_at', 'seller', 'card')
    search_fields = ('card__name', 'seller__nickname')
    ordering = ('-listed_at',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = [
        'buyer',
        'card',
        'seller',
        'quantity',
        'price',
        'purchased_at',
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'nickname',
        'email',
        'phone',
        'country',
        'balance',
        'address',
        'bio',
        'avatar_preview',
    )
    list_filter = ('country',)
    search_fields = ('user__username', 'nickname', 'email')

    readonly_fields = ('avatar_preview',)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'user',
                    'nickname',
                    'email',
                    'country',
                    'balance',
                    'address',
                    'phone',
                    'bio',
                    'avatar_url',
                    'avatar_file',
                    'avatar_preview',
                )
            },
        ),
    )

    def avatar_preview(self, obj):
        if obj.avatar_url:
            return format_html('<img src="{}" style="height:50px;" />', obj.avatar_url)
        elif obj.avatar_file:
            return format_html('<img src="{}" style="height:50px;" />', obj.avatar_file.url)
        return '-'

    avatar_preview.short_description = 'Avatar'
