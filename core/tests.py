from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from .models import Collision, Gamer, Game
from .serializers import CollisionSerializer, GamerSerializer, GameSerializer
from django.core.cache import cache
import django.db.utils


class FunctionTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.viewed_user = User.objects.create_user(username='vieweduser', email='vieweduser@example.com',
                                                    password='password123')
        self.gamer = Gamer.objects.create(user=self.user)
        self.viewed_gamer = Gamer.objects.create(user=self.viewed_user)
        self.game = Game.objects.create(name='Test Game')
        self.gamer.games.add(self.game)
        self.viewed_gamer.games.add(self.game)

        self.collide_url = reverse('collide')
        self.matches_url = reverse('matches')
        self.profile_url = reverse('profile')
        self.game_url = reverse('game')
        self.gamer_url = reverse('gamer')
        self.suggestions_url = reverse('suggestions')
        self.alter_name_url = reverse('alter_name')
        self.alter_description_url = reverse('alter_description')

    def test_collide(self):
        data = {'viewed_id': self.viewed_user.id, 'acceptation': 'true'}
        response = self.client.post(self.collide_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['viewed_user'], self.viewed_user.id)
        self.assertEqual(response.data['accept'], True)

    def test_matches(self):
        Collision.objects.create(user=self.user, viewed_user=self.viewed_user, accept=True, match=True)
        response = self.client.get(self.matches_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_game(self):
        response = self.client.get(self.game_url, {'id': self.game.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.game.name)

    def test_gamer(self):
        response = self.client.get(self.gamer_url, {'username': self.viewed_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.viewed_user.id)

    def test_suggestions(self):
        response = self.client.get(self.suggestions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_alter_name(self):
        data = {'new_name': 'newtestuser'}
        response = self.client.post(self.alter_name_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Name changed successfully')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newtestuser')

    def test_alter_name_duplicate(self):
        User.objects.create_user(username='newtestuser', email='newtestuser@example.com', password='password123')
        data = {'new_name': 'newtestuser'}
        response = self.client.post(self.alter_name_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Name already exists')

    def test_alter_description(self):
        data = {'new_description': 'New description'}
        response = self.client.post(self.alter_description_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Description changed successfully')
        self.gamer.refresh_from_db()
        self.assertEqual(self.gamer.description, 'New description')
