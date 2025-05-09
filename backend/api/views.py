# from django.shortcuts import render
from .card_serializers import CardSerializer
from .models import Card, Profile, CartItem, CardForSale, Purchase, Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from .models import Token, Profile
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import json
from .decorators import require_get,require_post,auth_required,validate_json
from .validator import validate_card_data
from django.views.decorators.http import require_http_methods
import json
from .decorators import auth_required
from django.db.models import Q
from django.contrib.auth import get_user_model
# Create your views here.
import traceback

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
    
def check_token(request):
    token_key = request.headers.get('Authorization', '').replace('Token ', '')
    try:
        token = Token.objects.get(key=token_key)
        return JsonResponse({'valid': True})
    except Token.DoesNotExist:
        return JsonResponse({'valid': False}, status=401)
    
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
@validate_json(required_fields=['firstname','lastname','username','password','email'])
def user_signup(request):
    #data = json.loads(request.body)
    firstname =  request.json_data['firstname']
    lastname =  request.json_data['lastname']
    username =  request.json_data['username']
    password =  request.json_data['password']
    email =  request.json_data['email']

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

    nickname = request.json_data.get("nickname", username)

    profile = Profile.objects.create(
        user=user,
        name=f"{firstname} {lastname}",
        nickname=nickname,
        country='',
        email=email,
        balance=0,
        address='',
        phone='', 
        bio='',
    )


    token = Token.objects.create(user=user)
    return JsonResponse({'token': token.key}, status=200)



@csrf_exempt
@auth_required
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "GET":
        avatar = (
            profile.avatar_url or 
            (request.build_absolute_uri(profile.avatar_file.url) if profile.avatar_file else None)
        )
        return JsonResponse({
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "nickname": profile.nickname,
            "country": profile.country,
            "address": profile.address,
            "phone": profile.phone,
            "bio": profile.bio,
            "avatar": avatar,
        })

    # POST: actualizar datos
    if request.content_type.startswith("multipart"):
        user.username = request.POST.get("username", user.username)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()

        profile.avatar_file = request.FILES.get("avatar_file")
        profile.avatar_url = None  # Se usa imagen, se limpia la URL
        profile.nickname = request.POST.get("nickname", profile.nickname)
        profile.country = request.POST.get("country", profile.country)
        profile.address = request.POST.get("address", profile.address)
        profile.phone = request.POST.get("phone", profile.phone)
        profile.bio = request.POST.get("bio", profile.bio)
        profile.save()

    else:
        data = json.loads(request.body)
        user.username = data.get("username", user.username)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.save()

        profile.avatar_url = data.get("avatar", profile.avatar_url)
        profile.avatar_file = None  # Se usa URL, se limpia imagen
        profile.nickname = data.get("nickname", profile.nickname)
        profile.country = data.get("country", profile.country)
        profile.address = data.get("address", profile.address)
        profile.phone = data.get("phone", profile.phone)
        profile.bio = data.get("bio", profile.bio)
        profile.save()

    avatar = (
        profile.avatar_url or 
        (request.build_absolute_uri(profile.avatar_file.url) if profile.avatar_file else "")
    )
    return JsonResponse({
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "nickname": profile.nickname,
        "country": profile.country,
        "address": profile.address,
        "phone": profile.phone,
        "bio": profile.bio,
        "avatar": avatar,
    })







@csrf_exempt
@validate_json(required_fields=['card-id', 'nickname', 'number-cards'])
@auth_required
@require_http_methods(["POST"])
def add_cart(request):
    # -- 1) Depuración inicial --
    print("🏷 Received Authorization:", request.META.get('HTTP_AUTHORIZATION'))
    print("🏷 request.json_data:", request.json_data)

    # -- 2) Extraer y validar campos obligatorios --
    try:
        card_id         = request.json_data['card-id']
        seller_username = request.json_data['nickname']
        qty             = int(request.json_data['number-cards'])
    except KeyError as e:
        return JsonResponse({'error': f'Falta campo {e.args[0]}'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'number-cards debe ser un entero'}, status=400)

    # -- 3) Buscar Card, Profile del vendedor y CardForSale --
    card = get_object_or_404(Card, id=card_id)
    seller_profile = get_object_or_404(Profile, user__username=seller_username)
    sale = get_object_or_404(CardForSale, seller=seller_profile, card=card)

    # -- 4) Comprobar stock --
    if sale.quantity < qty:
        return JsonResponse({'error': 'Stock insuficiente'}, status=400)

    # -- 5) (Opcional) descontar stock si quieres persistirlo aquí
    # sale.quantity -= qty
    # sale.save()

    # -- 6) Crear o actualizar CartItem --
    # Si el usuario ya tenía ese ítem, aumentamos cantidad
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user.profile,
        card_for_sale=sale,
        defaults={'quantity': qty}
    )
    if not created:
        cart_item.quantity += qty
        cart_item.save()

    # -- 7) Preparar datos de respuesta (incluyendo todos los campos de la carta) --
    # Extraer URL de la imagen (igual que en tu card_detail view)
    try:
        uris = json.loads(card.image_uris or "[]")
        img_url = uris[0] if isinstance(uris, list) and uris else ""
    except json.JSONDecodeError:
        img_url = card.image_uris or ""

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








    
    
# Preguntale a Sanchez si hace falta esta view
# Lo puede hacer a nivel Front nada mas

def delete_cart(request):
    pass




@require_http_methods(["GET"])
@auth_required
def user_cart(request):
    profile = request.user.profile
    items = CartItem.objects.filter(user=profile).select_related("card_for_sale__card")
    data = []
    for ci in items:
        sale = ci.card_for_sale
        card = sale.card
        # extrae la primera URI si está en JSON
        try:
            img = json.loads(card.image_uris or "[]")[0]
        except (ValueError, IndexError):
            img = ""
        data.append({
            "id": ci.id,
            "card": {
                "id":   str(card.id),
                "name": card.name,
                "img":  request.build_absolute_uri(img),
                "price": float(sale.price),
            },
            "quantity": ci.quantity,
        })
    return JsonResponse({"cart": data}, json_dumps_params={"ensure_ascii": False})

@auth_required
@require_http_methods(["PATCH", "DELETE"])
def cart_item_detail(request, pk):
    ci = get_object_or_404(CartItem, pk=pk, user=request.user.profile)
    if request.method == "PATCH":
        payload = json.loads(request.body or "{}")
        ci.quantity = payload.get("quantity", ci.quantity)
        ci.save()
        return JsonResponse({"id": ci.id, "quantity": ci.quantity})
    if request.method == "DELETE":
        ci.delete()
        return JsonResponse({"deleted": True}, status=204)


@csrf_exempt
@auth_required
@require_post
@validate_json(required_fields=['card-id', 'price', 'quantity'])
def sell_card(request):
    print("🔥 Entró a sell_card")
    print("Usuario:", request.user)

    try:
        body = json.loads(request.body)
        card_id = body.get("card-id")
        price = body.get("price")
        quantity = body.get("quantity")

        if not (card_id and price and quantity):
            return JsonResponse({"error": "Faltan campos"}, status=400)

        card = Card.objects.get(id=card_id)

        CardForSale.objects.create(
            card=card,
            seller=request.user.profile, 
            price=price,
            quantity=quantity,
        )

        return JsonResponse({"message": "Carta publicada con éxito"})
    except Card.DoesNotExist:
        return JsonResponse({"error": "Carta no encontrada"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@auth_required
@require_http_methods(["GET"])
def my_cards_for_sale(request):
    profile = request.user.profile
    listings = CardForSale.objects.filter(seller=profile).select_related("card")

    cards = []
    for l in listings:
        try:
            uris = json.loads(l.card.image_uris or "[]")
            img = uris[0] if uris else ""
        except json.JSONDecodeError:
            img = l.card.image_uris or ""
        cards.append({
            "id": l.id,
            "name": l.card.name,
            "quantity": l.quantity,
            "price": float(l.price),
            "image": request.build_absolute_uri(img),
            "listed_at": l.listed_at.isoformat(),
        })

    return JsonResponse({"cards_for_sale": cards})

# @require_http_methods(["PATCH"])
# @auth_required
# def update_card_for_sale(request, card_id):
#     try:
#         data = json.loads(request.body)
#         price = data.get("price")
#         quantity = data.get("quantity")
        
#         card_for_sale = CardForSale.objects.get(card_id=card_id, seller=request.user.profile)

#         if price is not None:
#             card_for_sale.price = price
#         if quantity is not None:
#             card_for_sale.quantity = quantity

#         card_for_sale.save()

#         return JsonResponse({"message": "Carta actualizada correctamente."})
#     except CardForSale.DoesNotExist:
#         return JsonResponse({"error": "Carta no encontrada o no autorizada."}, status=404)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)


# @require_http_methods(["DELETE"])
# @auth_required
# def delete_card_for_sale(request, card_id):
#     try:
#         card_for_sale = CardForSale.objects.get(card_id=card_id, seller=request.user.profile)
#         card_for_sale.delete()
#         return JsonResponse({"message": "Carta eliminada correctamente."})
#     except CardForSale.DoesNotExist:
#         return JsonResponse({"error": "Carta no encontrada o no autorizada."}, status=404)


@require_get
def all_cards(request):
    try:
        number_start = int(request.GET.get('number-start', 1))
        if number_start < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'Invalid number-start'}, status=400)

    search_term = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'name')

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



@require_get
def all_cards(request):
    try:
        number_start = int(request.GET.get('number-start', 1))
        if number_start < 1:
            raise ValueError("El número de página debe ser mayor que 0")
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
            sellers_qs = CardForSale.objects.filter(card=card).select_related('seller')
            sellers = [
                {
                    'sellerNickname': seller.seller.nickname,
                    'price': float(seller.price),
                    'quantity': seller.quantity,
                }
                for seller in sellers_qs
            ]

            data.append({
                'id': str(card.id),
                'name': card.name,
                'image': card.image_uris,
                'rarity': card.rarity,
                'sellers': sellers,
            })

        return JsonResponse({'cards': data, 'total': total_count}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Error interno del servidor: {str(e)}'}, status=500)


@require_get
def cards_by_expansion(request, code):
    try:
        number_start = int(request.GET.get('number-start', 1))
        if number_start < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'Invalid number-start'}, status=400)

    search_term = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'name')

    cards = Card.objects.filter(set_code__iexact=code)

    if search_term:
        cards = cards.filter(name__icontains=search_term)

    total_count = cards.count()
    cards = cards.order_by('name') if sort_by == 'name' else cards.order_by('-price' if sort_by == 'price_desc' else 'price')

    start = (number_start - 1) * 20
    end = start + 20
    cards_page = cards[start:end]

    data = []
    
    for card in cards_page:
        sellers = [
            {
                'sellerNickname': sale.seller.user.username,
                'price': float(sale.price),
                'quantity': sale.quantity,
            }
            for sale in CardForSale.objects.filter(card=card).select_related('seller')
        ]

        data.append({
            'id': str(card.id),
            'name': card.name,
            'image': card.image_uris,
            'rarity': card.rarity,
            'sellers': sellers,
        })

    return JsonResponse({'cards': data, 'total': total_count}, status=200)


    
@require_get
def list_expansions(request):
    expansions = (
        Card.objects
        .values('set_name', 'set_code')
        .exclude(set_name__isnull=True)
        .exclude(set_name='')
        .distinct()
        .order_by('set_name')
    )
    return JsonResponse({'expansions': list(expansions)}, status=200)


@csrf_exempt
def debug_token(request):
    return JsonResponse({
        "received_header": request.headers.get('Authorization', ''),
        "method": request.method,
        "body": request.body.decode('utf-8')
    })
    
    
@csrf_exempt
@auth_required
@require_http_methods(["GET"])
def my_sold_cards(request):
    """
    Devuelve las cartas que el usuario ha vendido,
    basándose en el modelo Purchase donde seller = perfil.
    """
    profile = request.user.profile
    sold_qs = Purchase.objects.filter(seller=profile).select_related("card")

    cards_sold = []
    for p in sold_qs:
        try:
            uris = json.loads(p.card.image_uris or "[]")
            image_url = uris[0] if uris else ""
        except json.JSONDecodeError:
            image_url = p.card.image_uris or ""

        cards_sold.append({
            "id": str(p.id),
            "name": p.card.name,
            "price": float(p.price),
            "quantity": p.quantity,
            "image": request.build_absolute_uri(image_url),
            "sold_at": p.purchased_at.isoformat(),
        })

    return JsonResponse({"cards_sold": cards_sold})

@csrf_exempt
@auth_required
@require_http_methods(["PATCH", "DELETE"])
def card_for_sale_detail(request, pk):
    profile = request.user.profile
    try:
        listing = CardForSale.objects.get(pk=pk, seller=profile)
    except CardForSale.DoesNotExist:
        raise Http404("No existe esa carta en tus ventas")

    if request.method == "PATCH":
        data = json.loads(request.body or "{}")
        if "quantity" in data:
            listing.quantity = data["quantity"]
        if "price" in data:
            listing.price = data["price"]
        listing.save()
        return JsonResponse({
            "id": listing.id,
            "quantity": listing.quantity,
            "price": float(listing.price),
        })

    # DELETE
    listing.delete()
    return JsonResponse({"deleted": True}, status=204)



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
        sellers.append({
            'username': sale.seller.user.username,  # el username real del User
            'price': float(sale.price),
            'quantity': sale.quantity,
            'listed_at': sale.listed_at.isoformat(),
        })

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




User = get_user_model()

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
            'avatar_url': profile.avatar_url or (profile.avatar_file.url if profile.avatar_file else None),
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


from django.contrib.auth import get_user_model
from .models import Token  # tu modelo Token

User = get_user_model()

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

    return JsonResponse({
        "received_header": request.headers.get('Authorization', ''),
        "method": request.method,
        "body": request.body.decode('utf-8')
    })
