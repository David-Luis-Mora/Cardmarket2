import os

import django

# Asegúrate de que la configuración de Django está cargada
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

# Ahora puedes importar tu modelo y trabajar con él
from api.models import Card

# Ejemplo de uso del modelo, por ejemplo, crear una nueva carta
new_card = Card(
    name='Magic Card',
    mana_cost='3G',  # Ejemplo de coste de maná
    type_line='Creature',  # Tipo de carta
    text='A magical creature card',  # Descripción
    power='4',  # Poder
    toughness='4',  # Resistencia
    loyalty=None,  # No tiene lealtad (es opcional)
    colors='Green',  # Color de la carta
    image_uris=None,  # Si no tienes URL de imagen
    quantity=10,  # Cantidad de cartas
    rarity='Rare',  # Rareza de la carta
    price=20,  # Precio en alguna unidad
    set_name='Core Set 2020',  # Nombre del set
    set_code='M20',  # Código del set
    release_date='2020-07-01',  # Fecha de lanzamiento
)
new_card.save()
