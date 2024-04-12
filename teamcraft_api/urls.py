from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    re_path(r'^signin/?$', views.signin),
    re_path(r'^signup/?$', views.signup),
    re_path(r'^token/?$', views.token)
]
