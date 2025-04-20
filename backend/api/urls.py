from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.card_list, name='card-list'),
    path('card/<str:slug>/', views.card_detail, name='game-detail'),
    path('users/login/', views.user_login, name='user-login'),
    path('users/signup/', views.user_signup, name='user-signup'),
    path('users/edit/', views.edit_profile, name='edit-profile'),
]
