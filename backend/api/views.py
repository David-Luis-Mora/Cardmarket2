# from django.shortcuts import render
from .card_serializers import CardSerializer
from .models import Card

# Create your views here.


def card_list(request):
    card_all = Card.objects.all()
    serializer = CardSerializer(card_all, request=request)
    return serializer.json_response()
