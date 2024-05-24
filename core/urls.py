from django.urls import re_path, path
from . import views

urlpatterns = [
    path('collide', views.collide),
    path('matches', views.matches),
    path('game_view', views.game),
    path('profile', views.profile),
    path('gamer', views.gamer),
    path('suggestions', views.suggestions),
    path('alter_name', views.alter_name),
]
