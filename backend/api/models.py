import uuid

from django.conf import settings
from django.db import models

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


class Profile(models.Model):
    country = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    balance = models.SmallIntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars',
        blank=True,
        null=True,
        default='avatars/noavatar.png',
    )

    # Cartas Comprada [Imagen de la carta, precio,vendedor, fecha,cantidad]
    # Cartas Vender [Imagen de la carta ,fecha, cantidad, precio]
    # Carrito mediante  añade el usuario

    def __str__(self):
        return self.user.username


# Cuando el usuario vende las cartas
class CardForSale(models.Model):
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cards_for_sale')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    listed_at = models.DateTimeField(auto_now_add=True)
    
# Cuando el usuario añade al carrito
class CartItem(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart_items')
    card_for_sale  = models.ForeignKey(CardForSale, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

# Cuando el usuario compra las cartas [Que se mostrara en el perfil]
class Purchase(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='purchases')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='sales')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)



class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'Conversación entre {", ".join([user.username for user in self.participants.all()])}'
        )


class Message(models.Model):
    conversation = models.ForeignKey('api.Chat', related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Mensaje de {self.sender.username} en {self.created_at}'


class CardListing(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings'
    )
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='listings')
    quantity = models.PositiveIntegerField(default=1)
    price_per_card = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.price_per_card

    def __str__(self):
        return f'{self.seller.username} vende {self.quantity}x {self.card.name}'




class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='token', on_delete=models.CASCADE
    )
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
