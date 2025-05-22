import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()
from api.models import Card

new_card = Card(
    name='Magic Card',
    mana_cost='3G',  
    type_line='Creature',  
    text='A magical creature card',  
    power='4', 
    toughness='4',  
    loyalty=None, 
    colors='Green', 
    image_uris=None,  
    quantity=10,  
    rarity='Rare',  
    price=20, 
    set_name='Core Set 2020', 
    set_code='M20',  
    release_date='2020-07-01',  
)
new_card.save()
