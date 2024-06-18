from django.urls import path
from . import views

urlpatterns = [
    path('view', views.RoomView.as_view()),
]