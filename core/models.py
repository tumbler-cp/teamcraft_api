from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=127, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='games', blank=True)

    def __str__(self):
        return self.name


class Gamer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Collision(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coll_fr_user')
    viewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coll_fr_viewed_user')
    accept = models.BooleanField()
    match = models.BooleanField()

    class Meta:
        unique_together = ('user', 'viewed_user')