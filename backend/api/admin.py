from django.contrib import admin

# Register your models here.

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]
