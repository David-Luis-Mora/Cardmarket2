import uuid

from django.db import models

# from django.contrib.postgres.fields import ArrayField, JSONField
# Create your models here.


# class Card(models.Model):
#     scryfall_id = models.UUIDField(primary_key=True)
#     oracle_id = models.UUIDField(null=True, blank=True)
#     name = models.CharField(max_length=255)
#     layout = models.CharField(max_length=50)
#     lang = models.CharField(max_length=10)
#     mana_cost = models.CharField(max_length=50, null=True, blank=True)
#     cmc = models.DecimalField(max_digits=5, decimal_places=2)
#     type_line = models.CharField(max_length=255)
#     oracle_text = models.TextField(null=True, blank=True)
#     power = models.CharField(max_length=10, null=True, blank=True)
#     toughness = models.CharField(max_length=10, null=True, blank=True)
#     loyalty = models.CharField(max_length=10, null=True, blank=True)
#     # colors = ArrayField(models.CharField(max_length=10), null=True, blank=True)
#     # color_identity = ArrayField(models.CharField(max_length=10), null=True, blank=True)
#     # keywords = ArrayField(models.CharField(max_length=50), null=True, blank=True)
#     # legalities = JSONField()
#     rarity = models.CharField(max_length=20)
#     set_name = models.CharField(max_length=100)
#     set_code = models.CharField(max_length=10)
#     collector_number = models.CharField(max_length=10)
#     released_at = models.DateField()
#     # image_uris = JSONField(null=True, blank=True)
#     # prices = JSONField()
#     scryfall_uri = models.URLField()
#     uri = models.URLField()
#     # card_faces = JSONField(null=True, blank=True)
#     def __str__(self):
#         return self.name


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    mana_cost = models.TextField(null=True, blank=True)  # Usar TextField si puede ser largo
    type_line = models.TextField(null=True, blank=True)  # Usar TextField
    text = models.TextField(null=True, blank=True)
    power = models.TextField(null=True, blank=True)  # Usar TextField
    toughness = models.TextField(null=True, blank=True)  # Usar TextField
    loyalty = models.TextField(null=True, blank=True)  # Usar TextField
    colors = models.TextField(null=True, blank=True)  # Si es una lista, convertirla a cadena
    image_uris = models.TextField(null=True, blank=True)  # Usar TextField para URLs múltiples
    quantity = models.IntegerField()
    rarity = models.CharField(max_length=20)
    price = models.IntegerField()
    set_name = models.CharField(max_length=100)
    set_code = models.CharField(max_length=10, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
