import re
import datetime


def validate_card_data(card_number: str, exp_date: str, cvc: str):
    # 1) Quita todo lo que no sea dígito
    clean = re.sub(r'\D', '', card_number)

    # 2) Debe quedarte exactamente 16 dígitos
    if not re.fullmatch(r'\d{16}', clean):
        return {'error': 'Invalid card number'}

    # (Opcional) vuelve a formatear con guiones si lo necesitas internamente
    # formatted = '-'.join(clean[i:i+4] for i in range(0, 16, 4))

    # 3) Validar CVC (3 o 4 dígitos, según tu caso)
    if not re.fullmatch(r'\d{3,4}', cvc):
        return {'error': 'Invalid CVC'}

    # 4) Fecha de expiración MM/YYYY o MM/YY
    #    Aquí permitimos tanto 2 dígitos año como 4 dígitos:
    if not re.fullmatch(r'\d{2}/(\d{2}|\d{4})', exp_date):
        return {'error': 'Invalid expiration date'}

    # Convierte MM/YY o MM/YYYY a valores numéricos
    month_str, year_str = exp_date.split('/')
    month = int(month_str)
    year  = int(year_str) + (2000 if len(year_str) == 2 else 0)

    if month < 1 or month > 12:
        return {'error': 'Invalid expiration date'}

    now = datetime.datetime.now()
    if year < now.year or (year == now.year and month < now.month):
        return {'error': 'Card expired'}

    return None