from django.contrib import admin

# Register your models here.

from .models import Card


@admin.register(Joint)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('labels',)
