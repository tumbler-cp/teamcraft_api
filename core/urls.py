from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('collide', views.collide, name='collide'),
    path('matches', views.matches, name='matches'),
    path('game', views.game, name='game'),
    path('profile', views.profile, name='profile'),
    path('gamer', views.gamer, name='gamer'),
    path('suggestions', views.suggestions, name='suggestions'),
    path('alter_name', views.alter_name, name='alter_name'),
    path('alter_description', views.alter_description, name='alter_description'),
    path('alter_avatar', views.alter_avatar, name='alter_avatar')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
