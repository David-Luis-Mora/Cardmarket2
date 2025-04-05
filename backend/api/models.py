from django.db import models

# Create your models here.

from django.db import models

class Card(models.Model):
    multiverse_id = models.IntegerField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=255)
    mana_cost = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=255)
    rarity = models.CharField(max_length=50)
    set_name = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    power = models.CharField(max_length=10, null=True, blank=True)
    toughness = models.CharField(max_length=10, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name
