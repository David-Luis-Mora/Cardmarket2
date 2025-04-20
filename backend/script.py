import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import django
import requests
from django.db import IntegrityError

# Establecer la variable de entorno para la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

# Importa tus modelos DESPUÉS de hacer setup
from api.models import Card

# Crear un objeto Lock para asegurarse de que solo un hilo escriba en la base de datos a la vez
lock = threading.Lock()


def save_card(card_data):
    """Función para guardar las cartas en la base de datos con bloqueadores."""
    try:
        # Adquirir el bloqueo para asegurarse de que solo un hilo pueda escribir
        with lock:
            card, created = Card.objects.get_or_create(
                id=card_data['id'],
                defaults={
                    'name': card_data.get('name', ''),
                    'mana_cost': card_data.get('mana_cost', ''),
                    'type_line': card_data.get('type_line', ''),
                    'text': card_data.get('oracle_text', ''),
                    'power': card_data.get('power', ''),
                    'toughness': card_data.get('toughness', ''),
                    'loyalty': card_data.get('loyalty', ''),
                    'colors': card_data.get('colors', []),
                    'image_uris': card_data.get('image_uris', {}).get('normal', ''),
                    'quantity': 1,  # Puedes ajustar la cantidad según tus necesidades
                    'rarity': card_data.get('rarity', ''),
                    'price': 0,  # No tienes precio en la API, puedes dejarlo en 0 o procesarlo si tienes datos
                    'set_name': card_data.get('set_name', ''),
                    'set_code': card_data.get('set', ''),
                    'release_date': datetime.strptime(card_data.get('released_at', ''), '%Y-%m-%d')
                    if card_data.get('released_at')
                    else None,
                },
            )
            if created:
                print(f'Carta guardada: {card.name}')
            else:
                print(f'Carta ya existente: {card.name}')

    except IntegrityError:
        print(f'Error al guardar la carta {card_data["name"]}. Verifica los datos.')
    except Exception as e:
        print(f'Error con la carta {card_data["name"]}: {e}')


def get_and_save_cards(page):
    """Función para obtener cartas de una página específica de la API de Scryfall y guardarlas en la base de datos."""
    url = f'https://api.scryfall.com/cards/search?q=*&order=released&dir=desc&page={page}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Error HTTP en la página {page}:', response.status_code)
        print('Respuesta:', response.text)
        return

    data = response.json()
    latest_cards = data.get('data', [])
    print(f'Cartas nuevas encontradas en la página {page}: {len(latest_cards)}')

    # Procesar las cartas obtenidas
    for card_data in latest_cards:
        save_card(card_data)


def get_total_pages():
    """Obtiene el número total de páginas disponibles en la API."""
    url = 'https://api.scryfall.com/cards/search?q=*&order=released&dir=desc'
    response = requests.get(url)

    if response.status_code != 200:
        print('Error HTTP al obtener el número de páginas:', response.status_code)
        return 0

    data = response.json()
    total_cards = data.get('total_cards', 0)
    cards_per_page = data.get('page_size', 175)  # Por defecto, son 175 cartas por página
    total_pages = (total_cards // cards_per_page) + (1 if total_cards % cards_per_page else 0)

    return total_pages


def main():
    """Función principal que maneja la ejecución con múltiples hilos."""
    total_pages = get_total_pages()

    if total_pages == 0:
        print('No se pudieron obtener páginas.')
        return

    print(f'Total de páginas disponibles: {total_pages}')

    # Usar ThreadPoolExecutor para procesar cada página en paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Crear una lista de números de página y asignarlos a los hilos
        pages = range(1, total_pages + 1)
        executor.map(get_and_save_cards, pages)


# Llamada a la función principal
main()
