from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('cards/', views.card_list, name='card-list'),
    path('cards/random/', views.random_cards, name='random-cards'),
    path('cards/all/', views.all_cards, name='all-cards'),
    path('card/<str:slug>/', views.card_detail, name='card-detail'),
    path('users/login/', views.user_login, name='user-login'),
    path('users/signup/', views.user_signup, name='user-signup'),
    path('users/edit/', views.edit_profile, name='edit-profile'),

    # Estas son las ultimas views que he añadido
    path('users/all-card-sale-for-user/', views.all_card_sale_for_user, name='all-card-sale-for-user'),
    path('users/all-cards-sold-by-user/', views.all_cards_sold_by_user, name='all-cards-sold-by-user'),
    path('users/all-card-purchased-for-user/', views.all_card_purchased_for_user, name='all-card-purchased-for-user'),
    # path('users/profile/', views.edit_profile, name='edit-profile'),
    
    path('users/cart/add/', views.add_cart, name='add-cart'),
    path('users/cart/delete/', views.delete_cart, name='delete-cart'),
    path('users/cart/delete/all/', views.delete_all_cart_items, name='delete-all-cart-items'),
    path('users/cart/delete/delete_cart_sold/', views.delete_cart_sold, name='delete-cart-sold'),


    path("users/sell/", views.sell_card, name="sell-card"),
    path('users/wallet/',views.wallet_balance,name='wallet-balance'),
    path('users/cart/buy-for-wallet/', views.buy_for_wallet, name='buy-for-wallet'),
    path('users/cart/buy-for-card/', views.buy_for_card, name='buy-for-card'),
    path("cards/expansions/", views.list_expansions, name="list-expansions"),
    path('cards/expansion/<str:code>/', views.cards_by_expansion, name='cards-by-expansion'),
    path('users/check-token/', views.check_token, name='check-token'),
    path('users/my-cards-for-sale/', views.my_cards_for_sale, name='my-cards-for-sale'),
    path('cards/<uuid:card_id>/', views.card_detail, name='card-detail'),
    path("users/my-cards-for-sale/<int:pk>/", views.card_for_sale_detail, name="card_for_sale_detail"),
    path("users/my-sold-cards/",views.my_sold_cards, name="my_sold_cards"),
    path("users/debug-token/", views.debug_token, name="debug-token"),
    path('seller/<str:username>/profile/', views.seller_profile, name='seller_profile'),
    path('users/cart/', views.user_cart, name='user_cart'),
    path('cart/<int:pk>/', views.cart_item_detail, name='cart_item_detail'),
    path('users/cart/buy/', views.buy_for_card, name='buy-for-card'),
]
