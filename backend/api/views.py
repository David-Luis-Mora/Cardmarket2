# from django.shortcuts import render
from .card_serializers import CardSerializer
from .models import Card
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Token, Profile
import uuid

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


def card_detail(request, slug):
    try:
        card = Card.objects.get(id=slug)
        serializer = CardSerializer(card, request=request)
        return serializer.json_response()
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    
    if user := authenticate(request, username=username, password=password):
        request.user = user
        token = Token.objects.get(user=user)
        return JsonResponse({'token': token.key}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    

def user_signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not validate_email_unique(email):
        return JsonResponse({'error': 'The email is already registered'}, status=400)

    if not validate_username_unique(username):
        return JsonResponse({'error': 'The username is already registered'}, status=400)
    
    user = User.objects.create_user(username=username, password=password)
    profile = Profile.objects.create(
        user=user,
        name="",
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

def edit_profile(request):
    token_key = request.data.get('token')
    country = request.data.get('country')
    name = request.data.get('name')
    nick = request.data.get('nick')
    address = request.data.get('address')
    phone = request.data.get('phone')
    bio = request.data.get('bio')
    avatar = request.data.get('avatar')
    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Token not found'}, status=404)
    
    profile = Profile.objects.get(key=token.user)
    profile.country = country
    profile.name = name
    profile.nick = nick
    profile.address = address
    profile.phone = phone
    profile.bio = bio
    profile.avatar = avatar
    
    profile.save()

    return JsonResponse({'message': 'Profile updated successfully', 'token': token.key}, status=200)



    
