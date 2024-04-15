from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    user_pool = models.ManyToManyField(User)


class Message(models.Model):
    text = models.TextField(blank=True)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateField(auto_now=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

