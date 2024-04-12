from django.urls import re_path
from . import views

urlpatterns = [
    re_path('collide', views.collide),
    re_path('matches', views.matches),
    re_path('game_view', views.game),
    re_path('profile', views.profile),
    re_path('gamer', views.gamer),
    re_path('suggestions', views.suggestions)
]
