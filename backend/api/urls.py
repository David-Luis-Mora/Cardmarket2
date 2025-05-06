from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.card_list, name='card-list'),
    path('card/<str:slug>/', views.card_detail, name='card-detail'),
    path('users/login/', views.user_login, name='user-login'),
    path('users/signup/', views.user_signup, name='user-signup'),
    path('users/edit/', views.edit_profile, name='edit-profile'),
    path('users/cart/add', views.add_cart, name='add-cart'),
    path('users/cart/delete', views.delete_cart, name='delete-cart'),
    path('users/cart/checkout/', views.delete_cart, name='checkout-cart'),
    path('users/sell/', views.sell_card, name='sell-card'),
    path('cards/expansion/<str:code>/', views.cards_by_expansion, name='cards-by-expansion'),
    path('users/check-token', views.check_token, name='check-token'),
]
