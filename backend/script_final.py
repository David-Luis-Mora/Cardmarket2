import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import django
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from api.models import Card

lock = threading.Lock()


def save_card(card_data):
    """Guardar una carta en la base de datos."""
    try:
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
                    'quantity': 1,
                    'rarity': card_data.get('rarity', ''),
                    'price': 0,
                    'set_name': card_data.get('set_name', ''),
                    'set_code': card_data.get('set', ''),
                    'release_date': datetime.strptime(card_data.get('released_at', ''), '%Y-%m-%d')
                    if card_data.get('released_at')
                    else None,
                },
            )
            if created:
                print(f'✅ Carta guardada: {card.name}')
            else:
                print(f'⏭️ Carta ya existente: {card.name}')
    except IntegrityError:
        print(f'❌ Error al guardar la carta {card_data["name"]}.')
    except Exception as e:
        print(f'⚠️ Error con la carta {card_data["name"]}: {e}')


def process_expansion_file(file_path):
    """Procesa un archivo JSON de expansión."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            cards = json.load(f)
            print(f'📦 Procesando {len(cards)} cartas de {os.path.basename(file_path)}')
            for card in cards:
                save_card(card)
    except Exception as e:
        print(f'❌ Error al procesar el archivo {file_path}: {e}')


def main():
    """Función principal."""
    folder_path = 'data_cartas'
    if not os.path.exists(folder_path):
        print('❌ La carpeta "data_cartas" no existe.')
        return

    archivos = [
        os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')
    ]
    print(f'🗂️ Archivos encontrados: {len(archivos)}')

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_expansion_file, archivos)

    print('✅ Finalizado: todas las cartas fueron procesadas.')


if __name__ == '__main__':
    main()
