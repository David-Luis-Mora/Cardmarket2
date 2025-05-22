import re
import datetime


def validate_card_data(card_number: str, exp_date: str, cvc: str):
    clean = re.sub(r'\D', '', card_number)

    if not re.fullmatch(r'\d{16}', clean):
        return {'error': 'Invalid card number'}

    if not re.fullmatch(r'\d{3,4}', cvc):
        return {'error': 'Invalid CVC'}

    if not re.fullmatch(r'\d{2}/(\d{2}|\d{4})', exp_date):
        return {'error': 'Invalid expiration date'}

    month_str, year_str = exp_date.split('/')
    month = int(month_str)
    year  = int(year_str) + (2000 if len(year_str) == 2 else 0)

    if month < 1 or month > 12:
        return {'error': 'Invalid expiration date'}

    now = datetime.datetime.now()
    if year < now.year or (year == now.year and month < now.month):
        return {'error': 'Card expired'}

    return None