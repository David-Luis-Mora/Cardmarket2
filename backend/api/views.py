# from django.shortcuts import render
from .card_serializers import CardSerializer
from .models import Card, Profile, CartItem, CardForSale, Purchase, Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Token, Profile
import uuid
from django.views.decorators.csrf import csrf_exempt
import json
from .decorators import require_get,require_post,auth_required,validate_json
from .validator import validate_card_data
# Create your views here.


def validate_email_unique(email):
    if User.objects.filter(email=email).exists():
        return False
    else:
        return True
    
def validate_username_unique(username):
    if User.objects.filter(username=username).exists():
        return False
    else:
        return True
    



def card_list(request):
    card_all = Card.objects.all()
    serializer = CardSerializer(card_all, request=request)
    return serializer.json_response()

@require_get
@validate_json(required_fields=[])
def card_detail(request,slug):
    try:
        card = Card.objects.get(id=slug)
        serializer = CardSerializer(card, request=request)
        return serializer.json_response()
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
@csrf_exempt
@require_post
@auth_required
@validate_json(required_fields=['username','password'])
def user_login(request):
    # data = json.loads(request.body)
    username =  request.json_data('username')
    password =  request.json_data('password')

    if user := authenticate(request, username=username, password=password):
        request.user = user
        token = Token.objects.get(user=user)
        return JsonResponse({'token': token.key}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    

@csrf_exempt
@require_post
@auth_required
@validate_json(required_fields=['firstname','lastname','username','password','email'])
def user_signup(request):
    # data = json.loads(request.body)
    firstname =  request.json_data('firstname')
    lastname =  request.json_data('lastname')
    username =  request.json_data('username')
    password =  request.json_data('password')
    email =  request.json_data('email')

    if not validate_email_unique(email):
        return JsonResponse({'error': 'The email is already registered'}, status=400)

    if not validate_username_unique(username):
        return JsonResponse({'error': 'The username is already registered'}, status=400)
    
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
        first_name=firstname,
        last_name=lastname
    )

    profile = Profile.objects.create(
        user=user,
        name=f"{firstname} {lastname}",
        nickname="",
        country='',
        email=email,
        balance=0,
        address='',
        phone='', 
        bio='',
    )

    token = Token.objects.create(user=user)
    return JsonResponse({'token': token.key}, status=200)

@require_post
@auth_required
@validate_json(required_fields=['country','name','nickname','address','phone','bio','avatar'])
def edit_profile(request):
    # token_key = request.data.get('token')
    country =  request.json_data('country')
    name =  request.json_data('name')
    nickname =  request.json_data('nickname')
    address =  request.json_data('address')
    phone =  request.json_data('phone')
    bio =  request.json_data('bio')
    avatar =  request.json_data('avatar')
    # try:
    #     token = Token.objects.get(key=token_key)
    # except Token.DoesNotExist:
    #     return JsonResponse({'error': 'Token not found'}, status=404)
    
    profile = Profile.objects.get(key=request.user)
    profile.country = country
    profile.name = name
    profile.nickname = nickname
    profile.address = address
    profile.phone = phone
    profile.bio = bio
    profile.avatar = avatar
    
    profile.save()

    return JsonResponse({'message': 'Profile updated successfully', 'token': token.key}, status=200)



@require_post
@validate_json(required_fields=['card-id', 'nickname','number-cards'])
@auth_required
def add_cart(request):
    # token_key = request.data.get('token')
    card_id = request.json_data('card-id')
    nickname_user_sellers = request.json_data['nickname']
    number_cards = request.json_data['number-cards']
    # token_users = request.user
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Card not found'}, status=404)
    
    try:
        profile_sellers = Profile.objects.get(nickname=nickname_user_sellers)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Card not found'}, status=404)
    
    # if number_cards > 0 and number_cards % 10 * len(number_cards) < 0 Para que el numero no sea negativo y que no tenga decimales
    
    try:
        cards_for_sellers = CardForSale.objects.get(seller=profile_sellers,card=card)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Card not found'}, status=404)
    
    if cards_for_sellers.quantity < number_cards:
        return JsonResponse({'error': 'Number not format'}, status=404) # Mirar que error devolver al no tener el formato de numero
    
    cards_for_sellers.quantity = cards_for_sellers.quantity - number_cards
    
    return JsonResponse({'message': 'Card add for CartItem',}, status=200)




    
    
# Preguntale a Sanchez si hace falta esta view
# Lo puede hacer a nivel Front nada mas

def delete_cart(request):
    pass


@require_post
@validate_json(required_fields=['card-number', 'exp-date','cvc'])
@auth_required
def checkout_cart(request):
    card_number = request.json_data['card-number']
    exp_date = request.json_data['exp-date']
    cvc = request.json_data['cvc']
    card_validation_error = validate_card_data(card_number, exp_date, cvc)
    if card_validation_error:
        return JsonResponse(card_validation_error, status=400)
    
    
    cart_items = CartItem.objects.filter(user=request.user)
    
    
    if not cart_items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)
    
    purchases_data = []

    for item in cart_items:
        card_sale = item.card_for_sale

        # Verificar stock disponible
        if item.quantity > card_sale.quantity:
            return JsonResponse({'error': f'Not enough quantity for {card_sale.card.name}'}, status=400)

        # Crear registro de compra
        purchase = Purchase.objects.create(
            buyer=request.user,
            card=card_sale.card,
            seller=card_sale.seller,
            quantity=item.quantity,
            price=card_sale.price,
        )

        
        # Restar stock
        card_sale.quantity -= item.quantity
        card_sale.save()

        # Eliminar item del carrito
        item.delete()

        purchases_data.append({
            'card': card_sale.card.name,
            'quantity': purchase.quantity,
            'price': str(purchase.price),
            'seller': purchase.seller.user.username,
            'purchased_at': purchase.purchased_at.isoformat(),
        })

    return JsonResponse({'message': 'Purchase completed', 'purchases': purchases_data}, status=200)



@require_post
@validate_json(required_fields=['card-id', 'price', 'quantity'])
@auth_required
def sell_card(request):
    card_id = request.json_data['card-id']
    price = request.json_data['price']
    quantity = request.json_data['quantity']

    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Card not found'}, status=404)

    CardForSale.objects.create(
        seller=request.user,
        card=card,
        price=price,
        quantity=quantity
    )

    return JsonResponse({'message': 'Card listed for sale'}, status=201)



@require_get
@validate_json(required_fields=['number-start'])
def cards_by_expansion(request, code):
    number_start = request.json_data['number-start']
    cards = Card.objects.filter(set_code=code.upper())
    if not cards.exists():
        return JsonResponse({'error': 'No cards found for this expansion'}, status=404)

    data = []
    for index in range(len(cards)):
        if index < (20 * number_start) - 1:
            card =
            {
                'id': str(card.id),
                'name': card.name,
                'image': card.image_uris,
                'rarity': card.rarity,
                'price': card.price,
            }
            data.append(card)


    return JsonResponse({'cards': data}, status=200)
