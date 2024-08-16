"""
Test for the actor API.
"""

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Actor, )

from movie.serializers import ActorSerializer


ACTORS_URL = reverse('movie:actor-list')


def detail_url(actor_id):
    """Create and return an actor detail URL."""
    return reverse('movie:actor-detail', args=[actor_id])


class PublicActorsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        """Test auth is not required for retrieving actor."""

        res = self.client.get(ACTORS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_actors(self):
        """Test retrieving a list of actors."""
        Actor.objects.create(first_name='Kale', last_name='Leez')
        Actor.objects.create(first_name='Vanilla', last_name='Leez')

        res = self.client.get(ACTORS_URL)

        actors = Actor.objects.all().order_by('-id')
        serializr = ActorSerializer(actors, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializr.data)

    def test_update_actor(self):
        """Test updating an actor."""
        actor = Actor.objects.create(first_name='Roberto', last_name='Lez')

        payload = {'first_name': 'dinero', 'last_name': 'lkmlkm'}
        url = detail_url(actor.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actor.refresh_from_db()
        self.assertEqual(actor.first_name, payload['first_name'])
        self.assertEqual(actor.last_name, payload['last_name'])

    def test_delete_actor(self):
        """Test deleting an actor."""
        actor = Actor.objects.create(first_name='Roberto', last_name='Lez')

        url = detail_url(actor.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        actors = Actor.objects.filter(id=actor.id)
        self.assertFalse(actors.exists())
