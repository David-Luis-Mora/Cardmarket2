# from django.shortcuts import render
import json
import os
import random
import smtplib
from email.mime.text import MIMEText

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv

from .card_serializers import CardSerializer
from .decorators import auth_required, require_get, require_post, validate_json
from .models import Card, CardForSale, CartItem, Profile, Purchase, Token
from .validator import validate_card_data

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
EMAIL = os.environ.get('EMAIL_USER')
APP_PASSWORD = os.environ.get('EMAIL_APP_PASS')


def send_email(recipient):
    asunto = 'Gracias por tu compra'
    cuerpo = 'Hola , gracias por comprar en CardShop. ¡Esperamos que disfrutes tus cartas!'

    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = EMAIL
    msg['To'] = recipient

    try:
        conexion = smtplib.SMTP('smtp.gmail.com', 587)
        conexion.starttls()
        conexion.login(EMAIL, APP_PASSWORD)
        conexion.sendmail(EMAIL, [send_email], msg.as_string())
        conexion.quit()
        print(f'✅ Correo enviado correctamente a {recipient}')
    except Exception as e:
        print(f'❌ Error al enviar el correo: {e}')


@require_get
def random_cards(request):
    # try:
    #     count = int(request.GET.get('count', 4))
    #     if count < 1:
    #         raise ValueError()
    # except (ValueError, TypeError):
    #     return JsonResponse({'error': 'Parámetro inválido: count'}, status=400)
    count = 4
    qs = Card.objects.filter(cardforsale__quantity__gt=0).distinct()
    total = qs.count()
    if total == 0:
        return JsonResponse({'cards': [], 'total': 0}, status=200)

    if total <= count:
        selected = list(qs)
    else:
        ids = list(qs.values_list('id', flat=True))
        chosen_ids = random.sample(ids, count)
        selected = list(qs.filter(id__in=chosen_ids))

    data = []
    for card in selected:
        img_url = ''
        try:
            uris = json.loads(card.image_uris or '[]')
            if isinstance(uris, list) and uris:
                img_url = request.build_absolute_uri(uris[0])
        except (ValueError, TypeError):
            pass

        sale = CardForSale.objects.filter(card=card, quantity__gt=0).order_by('price').first()
        price = float(sale.price) if sale else 0.0

        data.append(
            {
                'id': card.id,
                'name': card.name,
                'img': card.image_uris,
                'price': price,
            }
        )

    return JsonResponse(
        {'cards': data, 'total': total}, status=200, json_dumps_params={'ensure_ascii': False}
    )


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


def logic_buyers(sale, buyer):
    all_buyers = CartItem.objects.exclude(user=buyer)
    for buy in all_buyers:
        if sale.quantity > buy.quantity:
            buy.quantity = sale.quantity
            buy.save()
            # Plantear cuando los compradores se le actualize el stock si llega a 0 se lo
            # quitamos del carrito o no?


def card_list(request):
    card_all = Card.objects.all()
    serializer = CardSerializer(card_all, request=request)
    return serializer.json_response()


# @require_get
# @validate_json(required_fields=[])
# def card_detail(request, slug):
#     try:
#         card = Card.objects.get(id=slug)
#         serializer = CardSerializer(card, request=request)
#         return serializer.json_response()
#     except Card.DoesNotExist:
#         return JsonResponse({'error': 'Game not found'}, status=404)


# def check_token(request):
#     token_key = request.headers.get('Authorization', '').replace('Token ', '')
#     try:
#         token = Token.objects.get(key=token_key)
#         return JsonResponse({'valid': True})
#     except Token.DoesNotExist:
#         return JsonResponse({'valid': False}, status=401)


@csrf_exempt
@require_post
@validate_json(required_fields=['username', 'password'])
def user_login(request):
    data = request.json_data
    username = data['username']
    password = data['password']

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({'token': str(token.key)}, status=200)


@csrf_exempt
@require_post
@validate_json(required_fields=['firstname', 'lastname', 'username', 'password', 'email'])
def user_signup(request):
    # data = json.loads(request.body)
    firstname = request.json_data['firstname']
    lastname = request.json_data['lastname']
    username = request.json_data['username']
    password = request.json_data['password']
    email = request.json_data['email']

    if not validate_email_unique(email):
        return JsonResponse({'error': 'The email is already registered'}, status=400)

    if not validate_username_unique(username):
        return JsonResponse({'error': 'The username is already registered'}, status=400)

    user = User.objects.create_user(
        email=email, username=username, password=password, first_name=firstname, last_name=lastname
    )

    nickname = request.json_data.get('nickname', username)

    profile = Profile.objects.create(
        user=user,
        name=f'{firstname} {lastname}',
        nickname=nickname,
        country='',
        email=email,
        balance=0,
        address='',
        phone='',
        bio='',
    )
    profile.save()

    token = Token.objects.create(user=user)
    return JsonResponse({'token': token.key}, status=200)


@csrf_exempt
@auth_required
@require_http_methods(['GET', 'POST'])
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'GET':
        avatar = profile.avatar_url or (
            request.build_absolute_uri(profile.avatar_file.url) if profile.avatar_file else None
        )
        return JsonResponse(
            {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'nickname': profile.nickname,
                'country': profile.country,
                'address': profile.address,
                'phone': profile.phone,
                'bio': profile.bio,
                'avatar': avatar,
            }
        )

    # POST: actualizar datos
    if request.content_type.startswith('multipart'):
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile.avatar_file = request.FILES.get('avatar_file')
        profile.avatar_url = None
        profile.nickname = request.POST.get('nickname', profile.nickname)
        profile.country = request.POST.get('country', profile.country)
        profile.address = request.POST.get('address', profile.address)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.save()

    else:
        data = json.loads(request.body)
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()

        profile.avatar_url = data.get('avatar', profile.avatar_url)
        profile.avatar_file = None  # Se usa URL, se limpia imagen
        profile.nickname = data.get('nickname', profile.nickname)
        profile.country = data.get('country', profile.country)
        profile.address = data.get('address', profile.address)
        profile.phone = data.get('phone', profile.phone)
        profile.bio = data.get('bio', profile.bio)
        profile.save()

    avatar = profile.avatar_url or (
        request.build_absolute_uri(profile.avatar_file.url) if profile.avatar_file else ''
    )
    return JsonResponse(
        {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'nickname': profile.nickname,
            'country': profile.country,
            'address': profile.address,
            'phone': profile.phone,
            'bio': profile.bio,
            'avatar': avatar,
        }
    )


@csrf_exempt
@validate_json(required_fields=['card-id', 'nickname', 'number-cards'])
@auth_required
@require_http_methods(['POST'])
# @require_post
# @method_required("POST")
def add_cart(request):
    # -- 1) Depuración inicial --
    print('🏷 Received Authorization:', request.META.get('HTTP_AUTHORIZATION'))
    print('🏷 request.json_data:', request.json_data)

    # -- 2) Extraer y validar campos obligatorios --
    try:
        id_sale_card = request.json_data['card-id']
        seller_username = request.json_data['nickname']
        qty = int(request.json_data['number-cards'])
    except KeyError as e:
        return JsonResponse({'error': f'Falta campo {e.args[0]}'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'number-cards debe ser un entero'}, status=400)

    # -- 3) Buscar Card, Profile del vendedor y CardForSale --

    # try:
    #     card = Card.objects.get(id=card_id)
    # except Card.DoesNotExist:
    #     return JsonResponse({'error': 'Perfil no encontrado'}, status=900)

    # try:
    #     seller_profile = Profile.objects.get(user__username=seller_username)
    # except Profile.DoesNotExist:
    #     return JsonResponse({'error': 'Perfil no encontrado'}, status=900)

    try:
        sale = CardForSale.objects.get(id=id_sale_card)
    except CardForSale.DoesNotExist:
        return JsonResponse({'error': 'Venta no encontrada'}, status=404)

    card = sale.card
    seller_profile = sale.seller

    # -- 4) Comprobar stock --
    if sale.quantity < qty:
        return JsonResponse({'error': 'Stock insuficiente'}, status=400)

    # -- 5) (Opcional) descontar stock si quieres persistirlo aquí
    sale.quantity -= qty
    sale.save()

    # -- 6) Crear o actualizar CartItem --
    # Si el usuario ya tenía ese ítem, aumentamos cantidad

    # try:
    #     cart = CardForSale.objects.get(id=id_sale_card)
    # except CardForSale.DoesNotExist:
    #     return JsonResponse({'error': 'Venta no encontrada'}, status=404)

    # CartItem.objects.create(
    #     user=request.user.profile,
    #     card_for_sale=sale,
    #     quantity = qty
    # )
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user.profile, card_for_sale=sale, quantity=qty
    )

    if not created:
        cart_item.quantity += qty
        cart_item.save()

    # -- 7) Preparar datos de respuesta (incluyendo todos los campos de la carta) --
    # Extraer URL de la imagen (igual que en tu card_detail view)
    try:
        uris = json.loads(card.image_uris or '[]')
        img_url = uris[0] if isinstance(uris, list) and uris else ''
    except json.JSONDecodeError:
        img_url = card.image_uris or ''

    response_data = {
        'cart_item': {
            'id': cart_item.id,
            'quantity': cart_item.quantity,
            'card': {
                'id': str(card.id),
                'name': card.name,
                'type': card.type_line,
                'rarity': card.rarity,
                'base_price': float(card.price),
                'image': request.build_absolute_uri(img_url),
            },
            'seller': {
                'username': seller_profile.user.username,
                'nickname': seller_profile.nickname,
            },
            'listed_at': sale.listed_at.isoformat(),
            'sale_price': float(sale.price),
        }
    }

    return JsonResponse(response_data, status=200, json_dumps_params={'ensure_ascii': False})


# @csrf_exempt
# @validate_json(
#     required_fields=[
#         'card-id',
#         'nickname',
#     ]
# )


@csrf_exempt
@validate_json(required_fields=['cart'])
@auth_required
@require_post
# @require_http_methods(['POST'])
def delete_cart(request):
    print('🏷 Received Authorization:', request.META.get('HTTP_AUTHORIZATION'))
    print('🏷 request.json_data:', request.json_data)
    print('Eliminar carta')

    try:
        # cart_item_id = request.json_data['cart']
        # body_unicode = request.body.decode('utf-8')
        # data = json.loads(body_unicode)
        # print('📦 JSON recibido:', data)

        # cart_item_id = data.get('cart')
        cart_item_id = request.json_data['cart']
    except KeyError as e:
        return JsonResponse({'error': f'Falta campo {e.args[0]}'}, status=300)

    try:
        cart_item = CartItem.objects.select_related('card_for_sale').get(
            id=cart_item_id, user=request.user.profile
        )
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item no encontrado en el carrito'}, status=404)

    card_for_sale = cart_item.card_for_sale
    card_for_sale.quantity += cart_item.quantity
    card_for_sale.save()

    cart_item.delete()

    return JsonResponse({'success': 'Item eliminado del carrito'}, status=200)


@auth_required
@require_http_methods(['GET'])
def user_cart(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=900)

    items = CartItem.objects.filter(user=profile).select_related('card_for_sale__card')
    data = []
    for ci in items:
        sale = ci.card_for_sale
        card = sale.card
        try:
            img = json.loads(card.image_uris or '[]')[0]
        except (ValueError, IndexError):
            img = ''
        data.append(
            {
                'id': str(ci.id),
                'id_letter_sale': str(sale.id),  # 👈 AÑADE ESTA LÍNEA
                'card': {
                    'id': str(card.id),
                    'name': card.name,
                    'img': request.build_absolute_uri(card.image_uris),
                    'price': float(sale.price),
                    'seller': sale.seller.nickname,  # 👈 este campo es necesario para el frontend
                    'rarity': card.rarity,
                },
                'quantity': ci.quantity,
            }
        )
    return JsonResponse({'cart': data}, json_dumps_params={'ensure_ascii': False}, status=200)


@auth_required
@require_http_methods(['PATCH', 'DELETE'])
def cart_item_detail(request, pk):
    ci = get_object_or_404(CartItem, pk=pk, user=request.user.profile)
    if request.method == 'PATCH':
        payload = json.loads(request.body or '{}')
        ci.quantity = payload.get('quantity', ci.quantity)
        ci.save()
        return JsonResponse({'id': ci.id, 'quantity': ci.quantity})
    if request.method == 'DELETE':
        ci.delete()
        return JsonResponse({'deleted': True}, status=204)


@csrf_exempt
@auth_required
@require_post
@validate_json(required_fields=['card-id', 'price', 'quantity'])
def sell_card(request):
    print('🔥 Entró a sell_card')
    print('Usuario:', request.user)

    try:
        body = json.loads(request.body)
        card_id = body.get('card-id')
        price = body.get('price')
        quantity = body.get('quantity')

        if not (card_id and price and quantity):
            return JsonResponse({'error': 'Faltan campos'}, status=400)

        card = Card.objects.get(id=card_id)

        CardForSale.objects.create(
            card=card,
            seller=request.user.profile,
            price=price,
            quantity=quantity,
        )

        return JsonResponse({'message': 'Carta publicada con éxito'})
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Carta no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@auth_required
@require_http_methods(['GET', 'POST'])
def my_cards_for_sale(request):
    profile = request.user.profile

    if request.method == 'POST':
        # ✅ Procesar eliminación de carta en venta
        try:
            body = json.loads(request.body.decode('utf-8'))
            card_id = body.get('id')  # ID de la venta (CardForSale.id)
            if not card_id:
                return JsonResponse({'error': 'ID no proporcionado'}, status=400)

            # Buscar la carta en venta
            card_for_sale = CardForSale.objects.get(id=card_id, seller=profile)
            card_for_sale.delete()

            return JsonResponse({'success': 'Carta eliminada correctamente'}, status=200)

        except CardForSale.DoesNotExist:
            return JsonResponse({'error': 'Carta no encontrada o no es tuya'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar: {str(e)}'}, status=500)

    # GET: devolver las cartas en venta con id de la carta y de la venta
    listings = CardForSale.objects.filter(seller=profile).select_related('card')
    cards = []
    for l in listings:
        try:
            uris = json.loads(l.card.image_uris or '[]')
            img = uris[0] if uris else ''
        except json.JSONDecodeError:
            img = l.card.image_uris or ''

        cards.append({
            'id': str(l.id),            # ID de la venta (CardForSale)
            'card_id': str(l.card.id),   # ID de la carta
            'name': l.card.name,
            'quantity': l.quantity,
            'price': float(l.price),
            'image': request.build_absolute_uri(img),
            'listed_at': l.listed_at.isoformat(),
        })

    return JsonResponse({'cards_for_sale': cards})


# @require_get
# def all_cards(request):
#     try:
#         number_start = int(request.GET.get('number-start', 1))
#         if number_start < 1:
#             raise ValueError
#     except ValueError:
#         return JsonResponse({'error': 'Invalid number-start'}, status=400)

#     search_term = request.GET.get('search', '').strip()
#     sort_by = request.GET.get('sort', 'name')

#     cards = Card.objects.all()

#     if search_term:
#         cards = cards.filter(name__isnull=False).filter(Q(name__icontains=search_term))

#     total_count = cards.count()

#     if sort_by == 'name':
#         cards = cards.order_by('name')
#     elif sort_by == 'price':
#         cards = cards.order_by('price')
#     elif sort_by == 'price_desc':
#         cards = cards.order_by('-price')


# from django.views.decorators.http import require_GET
@require_get
def all_cards(request):
    try:
        number_start = int(request.GET.get('number-start', 1))
        if number_start < 1:
            raise ValueError('El número de página debe ser mayor que 0')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Parámetro inválido: number-start'}, status=400)

    search_term = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'name')

    try:
        cards = Card.objects.all()

        if search_term:
            cards = cards.filter(name__isnull=False).filter(Q(name__icontains=search_term))

        total_count = cards.count()

        if sort_by == 'name':
            cards = cards.order_by('name')
        elif sort_by == 'price':
            cards = cards.order_by('price')
        elif sort_by == 'price_desc':
            cards = cards.order_by('-price')

        start = (number_start - 1) * 20
        end = start + 20
        cards_page = cards[start:end]

        data = []
        for card in cards_page:
            # Sólo vendedores con stock > 0
            sellers_qs = CardForSale.objects.filter(card=card, quantity__gt=0).select_related(
                'seller'
            )
            sellers = [
                {
                    'id_letter_sale': seller.id,
                    'sellerNickname': seller.seller.user.username,
                    'price': float(seller.price),
                    'quantity': seller.quantity,
                }
                for seller in sellers_qs
            ]

            data.append(
                {
                    'id': str(card.id),
                    'name': card.name,
                    'image': card.image_uris,
                    'rarity': card.rarity,
                    'sellers': sellers,
                }
            )

        return JsonResponse({'cards': data, 'total': total_count}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Error interno del servidor: {str(e)}'}, status=500)


@require_get
def cards_by_expansion(request, code):
    try:
        number_start = int(request.GET.get('number-start', 1))
        if number_start < 1:
            raise ValueError('El número de página debe ser mayor que 0')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Parámetro inválido: number-start'}, status=400)

    search_term = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'name')

    cards = Card.objects.filter(set_code__iexact=code)

    if search_term:
        cards = cards.filter(name__icontains=search_term)

    total_count = cards.count()

    if sort_by == 'name':
        cards = cards.order_by('name')
    elif sort_by == 'price':
        cards = cards.order_by('price')
    elif sort_by == 'price_desc':
        cards = cards.order_by('-price')

    start = (number_start - 1) * 20
    end = start + 20
    cards_page = cards[start:end]

    data = []
    for card in cards_page:
        # Al igual que en all_cards: sólo vendedores con quantity > 0
        sellers_qs = CardForSale.objects.filter(card=card, quantity__gt=0).select_related(
            'seller__user'
        )
        sellers = [
            {
                'sellerNickname': sale.seller.user.username,
                'price': float(sale.price),
                'quantity': sale.quantity,
                'id_letter_sale': sale.id,
            }
            for sale in sellers_qs
        ]

        data.append(
            {
                'id': str(card.id),
                'name': card.name,
                'image': card.image_uris,
                'rarity': card.rarity,
                'sellers': sellers,
            }
        )

    return JsonResponse({'cards': data, 'total': total_count}, status=200)


@require_get
def list_expansions(request):
    expansions = (
        Card.objects.values('set_name', 'set_code')
        .exclude(set_name__isnull=True)
        .exclude(set_name='')
        .distinct()
        .order_by('set_name')
    )
    return JsonResponse({'expansions': list(expansions)}, status=200)


@csrf_exempt
def debug_token(request):
    return JsonResponse(
        {
            'received_header': request.headers.get('Authorization', ''),
            'method': request.method,
            'body': request.body.decode('utf-8'),
        }
    )


@csrf_exempt
@auth_required
@require_get
def my_sold_cards(request):
    """
    Devuelve las cartas que el usuario ha vendido,
    basándose en el modelo Purchase donde seller = perfil.
    """
    profile = request.user.profile
    sold_qs = Purchase.objects.filter(seller=profile).select_related('card')

    cards_sold = []
    for p in sold_qs:
        try:
            uris = json.loads(p.card.image_uris or '[]')
            image_url = uris[0] if uris else ''
        except json.JSONDecodeError:
            image_url = p.card.image_uris or ''

        cards_sold.append(
            {
                'id': str(p.id),
                'name': p.card.name,
                'price': float(p.price),
                'quantity': p.quantity,
                'image': request.build_absolute_uri(image_url),
                'sold_at': p.purchased_at.isoformat(),
            }
        )

    return JsonResponse({'cards_sold': cards_sold})


@csrf_exempt
@auth_required
# @require_http_methods(['PATCH', 'DELETE'])
def card_for_sale_detail(request, pk):
    profile = request.user.profile
    try:
        listing = CardForSale.objects.get(pk=pk, seller=profile)
    except CardForSale.DoesNotExist:
        raise Http404('No existe esa carta en tus ventas')

    if request.method == 'PATCH':
        data = json.loads(request.body or '{}')
        if 'quantity' in data:
            listing.quantity = data['quantity']
        if 'price' in data:
            listing.price = data['price']
        listing.save()
        return JsonResponse(
            {
                'id': listing.id,
                'quantity': listing.quantity,
                'price': float(listing.price),
            }
        )

    # DELETE
    listing.delete()
    return JsonResponse({'deleted': True}, status=204)


# views.py
def card_detail(request, card_id):
    # 1) Busca la carta
    card = get_object_or_404(Card, id=card_id)

    # 2) Prepara la URL de la imagen (asumo que image_uris almacena JSON con lista de URLs)
    image_url = None
    if card.image_uris:
        try:
            uris = json.loads(card.image_uris)
            # Toma la primera URL si viene lista, o la propia cadena si no es lista
            if isinstance(uris, list) and uris:
                image_url = uris[0]
            elif isinstance(uris, str):
                image_url = uris
        except json.JSONDecodeError:
            image_url = card.image_uris  # si no es JSON válido, devuélvelo tal cual

    # 3) Serializa los vendedores activos de CardForSale
    sales_qs = CardForSale.objects.filter(card=card)
    sellers = []
    for sale in sales_qs:
        sellers.append(
            {
                'id_letter_sale': sale.id,                   
                'username': sale.seller.user.username,
                'price': float(sale.price),
                'quantity': sale.quantity,
                'listed_at': sale.listed_at.isoformat(),
            }
        )

    # 4) Construye la respuesta para el producto
    card_data = {
        'id': str(card.id),
        'name': card.name,
        'image': image_url,
        'type': card.type_line,
        'rarity': card.rarity,
        'basePrice': float(card.price),
        'sellers': sellers,
    }

    return JsonResponse(card_data, json_dumps_params={'ensure_ascii': False})


# User = get_user_model()
def seller_profile(request, username):
    # 1) Busca el User y su Profile
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    # 2) Recupera todas sus CardForSale
    cards_qs = CardForSale.objects.filter(seller=profile).select_related('card')

    # 3) Serializa los datos para Vue
    context = {
        'profile': {
            'user': {'username': user.username},
            'nickname': profile.nickname,
            'first_name': getattr(profile, 'first_name', ''),  # adapta si lo tienes distinto
            'last_name': getattr(profile, 'last_name', ''),
            'email': user.email,
            'country': profile.country,
            'address': profile.address,
            'phone': profile.phone,
            'bio': profile.bio,
            'avatar_url': profile.avatar_url
            or (profile.avatar_file.url if profile.avatar_file else None),
        },
        'cards_for_sale': [
            {
                'id': sale.card.id,
                'name': sale.card.name,
                'price': float(sale.price),
                'quantity': sale.quantity,
            }
            for sale in cards_qs
        ],
    }

    return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


# User = get_user_model()
def check_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Bearer ') or auth_header.startswith('Token '):
        key = auth_header.split(' ', 1)[1]
    else:
        return JsonResponse({'valid': False, 'detail': 'No token provided'}, status=400)

    try:
        token_obj = Token.objects.select_related('user').get(key=key)
    except Token.DoesNotExist:
        return JsonResponse({'valid': False, 'detail': 'Invalid token'}, status=401)

    user = token_obj.user
    if not user.is_active:
        return JsonResponse({'valid': False, 'detail': 'User inactive'}, status=401)

    return JsonResponse(
        {
            'received_header': request.headers.get('Authorization', ''),
            'method': request.method,
            'body': request.body.decode('utf-8'),
        }
    )


@csrf_exempt
@auth_required
@require_http_methods(['POST'])
def delete_all_cart_items(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=400)

    # Obtener todos los ítems del carrito del usuario
    cart_items = CartItem.objects.filter(user=profile).select_related('card_for_sale')

    if not cart_items.exists():
        return JsonResponse({'info': 'El carrito ya estaba vacío'}, status=200)

    restored = 0
    for item in cart_items:
        sale = item.card_for_sale
        # Devolver stock al vendedor
        sale.quantity += item.quantity
        sale.save()
        restored += 1
        item.delete()

    return JsonResponse(
        {'success': f'{restored} productos eliminados y stock restaurado'}, status=200
    )


@csrf_exempt
@validate_json(
    required_fields=[
        'card-id',
        'nickname',
    ]
)
@auth_required
# @require_http_methods(['POST'])
def delete_cart_sold(request):
    print('🔍 request.body:', request.body)
    print('🔍 request.headers:', request.headers)
    # print("🏷 Received Authorization:", request.META.get('HTTP_AUTHORIZATION'))
    # print("🏷 request.json_data:", request.json_data)

    try:
        card_id = request.json_data['card-id']
        seller_username = request.json_data['nickname']
        # qty             = int(request.json_data['number-cards'])
    except KeyError as e:
        return JsonResponse({'error': f'Falta campo {e.args[0]}'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'number-cards debe ser un entero'}, status=400)

    # Buscar entidades necesarias
    try:
        card = Card.objects.get(id=card_id)
        seller_profile = Profile.objects.get(nickname=seller_username)
        card_for_sale = CardForSale.objects.get(card=card, seller=seller_profile)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Carta no encontrada'}, status=404)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil de vendedor no encontrado'}, status=404)
    except CardForSale.DoesNotExist:
        return JsonResponse({'error': 'Venta no encontrada'}, status=404)

    card_for_sale.delete()

    return JsonResponse({'success': 'Carta retirada de la venta'}, status=200)


@csrf_exempt
@auth_required
@require_post
def buy_for_wallet(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=400)

    # Obtener los ítems del carrito
    cart_items = CartItem.objects.filter(user=profile).select_related('card_for_sale__card')

    if not cart_items.exists():
        return JsonResponse({'error': 'El carrito está vacío'}, status=400)

    # Calcula la cantidad total del carrito
    total_price = 0
    for item in cart_items:
        sale = item.card_for_sale
        # Verificar stock (opcional)
        # if sale.quantity <= item.quantity:
        #     return JsonResponse({
        #         'error': f'Stock insuficiente para {sale.card.name}'
        #     }, status=400)
        # Descontar stock
        # sale.quantity -= item.quantity
        # sale.save()
        # Calcular total
        total_price += item.quantity * sale.price

    # Comprabar que tenga saldo en la cuenta
    if not profile.balance >= total_price:
        return JsonResponse({'error': f'Dinero insuficiente para {sale.card.name}'}, status=400)
    # Se le pone el dinero a los vendedores
    for item in cart_items:
        sale = item.card_for_sale
        Purchase.objects.create(
            buyer=profile,
            seller=sale.seller,
            card=sale.card,
            quantity=item.quantity,
            price=sale.price,
        )
        # Descontar stock
        # sale.quantity -= item.quantity
        sale.seller.balance += item.quantity * sale.price
        sale.save()
        # logic_buyers(sale,profile)

    profile.balance -= total_price
    profile.save()

    cart_items.delete()

    return JsonResponse(
        {
            'success': 'Compra realizada con éxito',
            'total_paid': float(total_price),
            'items': len(cart_items),
        },
        status=200,
    )


@csrf_exempt
@auth_required
@require_post
@validate_json(required_fields=['card-number', 'exp-date', 'cvc'])
def buy_for_card(request):
    user = request.user

    card_number = request.json_data['card-number']
    exp_date = request.json_data['exp-date']
    cvc = request.json_data['cvc']

    # 1) Validar formato de la tarjeta
    card_validation_error = validate_card_data(card_number, exp_date, cvc)
    if card_validation_error:
        return JsonResponse(card_validation_error, status=400)

    # 2) Obtener perfil
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=400)

    # 3) Obtener carrito
    cart_items = CartItem.objects.filter(user=profile).select_related('card_for_sale__card')
    if not cart_items.exists():
        return JsonResponse({'error': 'El carrito está vacío'}, status=400)

    # 4) Calcular total y verificar stock
    total_price = 0
    for item in cart_items:
        sale = item.card_for_sale
        # if sale.quantity < item.quantity:
        #     return JsonResponse(
        #         {'error': f'Stock insuficiente para {sale.card.name}'},
        #         status=400
        #     )
        total_price += item.quantity * sale.price

    # —> **No hacemos comprobación de profile.balance aquí**
    # —> **No restamos nada de profile.balance al final**

    # 5) Crear los registros de Purchase y pagar a los vendedores
    for item in cart_items:
        sale = item.card_for_sale
        Purchase.objects.create(
            buyer=profile,
            seller=sale.seller,
            card=sale.card,
            quantity=item.quantity,
            price=sale.price,
        )
        # sale.quantity -= item.quantity
        # sale.save()

        seller = sale.seller
        seller.balance += item.quantity * sale.price
        seller.save()

        # logic_buyers(sale, profile)

    # 6) Borrar el carrito
    count = cart_items.count()
    cart_items.delete()

    # 7) Devolver respuesta
    return JsonResponse(
        {'success': 'Compra realizada con éxito', 'total_paid': float(total_price), 'items': count},
        status=200,
    )


@csrf_exempt
@auth_required
@require_post
def all_card_sale_for_user(request):
    profile = Profile.objects.get(user=request.user)
    all_card_sale = CardForSale.objects.filter(seller=profile)
    data = []
    for sale in all_card_sale:
        card = sale.card
        # intenta cargar la imagen desde JSON
        try:
            img = json.loads(card.image_uris or '[]')[0]
        except (ValueError, IndexError, TypeError):
            img = ''

        data.append(
            {
                'card_id': str(card.id),
                'name': card.name,
                'price': float(sale.price),
                'quantity': sale.quantity,
                'listed_at': sale.listed_at.isoformat(),
                'rarity': card.rarity,
                'img': request.build_absolute_uri(img),
                'set_name': card.set_name,
            }
        )
    return JsonResponse({'cards': data}, status=200, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@auth_required
@require_post
def all_cards_sold_by_user(request):
    profile = Profile.objects.get(user=request.user)

    purchases = Purchase.objects.filter(seller=profile).select_related('card', 'buyer')

    data = []
    for sale in purchases:
        card = sale.card
        try:
            img = json.loads(card.image_uris or '[]')[0]
        except (ValueError, IndexError, TypeError):
            img = ''

        data.append(
            {
                'card_id': str(card.id),
                'name': card.name,
                'price': float(sale.price),
                'quantity': sale.quantity,
                'purchased_at': sale.purchased_at.isoformat(),
                'rarity': card.rarity,
                'img': request.build_absolute_uri(img),
                'set_name': card.set_name,
                'buyer_nickname': sale.buyer.nickname,  # 👈 útil para mostrar a quién se lo vendiste
                'buyer_nickname': sale.buyer.nickname,
                'buyer_username': sale.buyer.user.username,
            }
        )

    return JsonResponse({'cards': data}, status=200, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@auth_required
@require_post
def all_card_purchased_for_user(request):
    profile = Profile.objects.get(user=request.user)

    purchases = Purchase.objects.filter(buyer=profile).select_related('card', 'buyer')

    data = []
    for sale in purchases:
        card = sale.card
        try:
            img = json.loads(card.image_uris or '[]')[0]
        except (ValueError, IndexError, TypeError):
            img = ''

        data.append(
            {
                'card_id': str(card.id),
                'name': card.name,
                'price': float(sale.price),
                'quantity': sale.quantity,
                'purchased_at': sale.purchased_at.isoformat(),
                'rarity': card.rarity,
                'img': request.build_absolute_uri(img),
                'set_name': card.set_name,
                'buyer_nickname': sale.buyer.nickname,  # 👈 útil para mostrar a quién se lo vendiste
                'seller_nickname': sale.seller.nickname,
                'seller_username': sale.seller.user.username,
            }
        )

    return JsonResponse({'cards': data}, status=200, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@auth_required
@require_get
def wallet_balance(request):
    """
    Devuelve el saldo actual del monedero del usuario logueado.
    """
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=400)

    # Profile.balance es un SmallIntegerField :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}
    return JsonResponse({'balance': float(profile.balance)}, status=200)


@csrf_exempt
@auth_required
@require_post
def delete_account(request):
    try:
        user = request.user
        profile = user.profile  # intenta acceder al perfil relacionado
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=400)

    # Elimina primero el perfil (opcional, ya que se elimina con el user por cascade)
    profile.delete()

    # Luego elimina la cuenta del usuario
    user.delete()

    return JsonResponse({'success': 'Cuenta eliminada correctamente'}, status=200)


@csrf_exempt
@auth_required
@validate_json(required_fields=['card-id', 'name'])  # ajusta según campos que quieras editar
@require_http_methods(['PATCH'])
def edit_card(request):
    profile = request.user.profile

    if profile.role != 'admin':
        return JsonResponse({'error': 'No tienes permisos para editar cartas'}, status=403)

    card_id = request.json_data['card-id']

    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Carta no encontrada'}, status=404)

    # Actualiza campos (agrega más si necesitas)
    card.name = request.json_data.get('name', card.name)
    card.save()

    return JsonResponse({'success': 'Carta actualizada correctamente'}, status=200)


@csrf_exempt
@auth_required
@validate_json(required_fields=['card-id'])
@require_post
def delete_card(request):
    profile = request.user.profile

    if profile.role != 'admin':
        return JsonResponse({'error': 'No tienes permisos para eliminar cartas'}, status=403)

    card_id = request.json_data['card-id']

    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Carta no encontrada'}, status=404)

    card.delete()

    return JsonResponse({'success': 'Carta eliminada correctamente'}, status=200)


# views.py
@csrf_exempt
@auth_required
@require_http_methods(['DELETE'])
def delete_card_for_sale(request, sale_id):
    try:
        profile = request.user.profile
        sale = CardForSale.objects.get(id=sale_id, seller=profile)
        sale.delete()
        return JsonResponse({'success': 'Carta eliminada de las ventas'}, status=200)
    except CardForSale.DoesNotExist:
        return JsonResponse({'error': 'Carta no encontrada o no te pertenece'}, status=404)
