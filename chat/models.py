from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Room(models.Model):
    name = models.TextField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
