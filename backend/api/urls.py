from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('cards/', views.card_list, name='card-list'),
    path('cards/all/', views.all_cards, name='all-cards'),
    path('card/<str:slug>/', views.card_detail, name='card-detail'),
    path('users/login/', views.user_login, name='user-login'),
    path('users/signup/', views.user_signup, name='user-signup'),
    path('users/edit/', views.edit_profile, name='edit-profile'),
    path('users/cart/add/', views.add_cart, name='add-cart'),
    path('users/cart/delete/', views.delete_cart, name='delete-cart'),
    path('users/cart/delete/all/', views.delete_all_cart_items, name='delete-all-cart-items'),
    path("users/sell/", views.sell_card, name="sell-card"),
    path("cards/expansions/", views.list_expansions, name="list-expansions"),
    path('cards/expansion/<str:code>/', views.cards_by_expansion, name='cards-by-expansion'),
    path('users/check-token/', views.check_token, name='check-token'),
    path('users/my-cards-for-sale/', views.my_cards_for_sale, name='my-cards-for-sale'),
    path('cards/<uuid:card_id>/', views.card_detail, name='card-detail'),
    # path('users/my-cards-for-sale/<str:card_id>/', views.update_card_for_sale, name='update-card-for-sale'),
    # path('users/my-cards-for-sale/<str:card_id>/delete/', views.delete_card_for_sale, name='delete-card-for-sale'),
    path("users/my-cards-for-sale/<int:pk>/", views.card_for_sale_detail, name="card_for_sale_detail"),
    path("users/my-sold-cards/",views.my_sold_cards, name="my_sold_cards"),
    path("users/debug-token/", views.debug_token, name="debug-token"),
    path('seller/<str:username>/profile/', views.seller_profile, name='seller_profile'),
    path('users/cart/', views.user_cart, name='user_cart'),
    path('cart/<int:pk>/', views.cart_item_detail, name='cart_item_detail'),
]
