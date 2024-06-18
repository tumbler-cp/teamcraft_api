from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('chats/', include('chat.urls')),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('token', views.token, name='token')
]
