"""
Tests for movie APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Movie

from movie.serializers import (
    MovieSerializer,
    MovieDetailSerializer
)

MOVIES_URL = reverse('movie:movie-list')


def detail_url(movie_id):
    """Create and return a movie detail URL."""
    return reverse('movie:movie-detail', args=[movie_id])


def create_movie(**params):
    """Create and return a sample movie."""
    defaults = {
        'title': 'Test movie',
        'description': 'Test description for the movie'
    }

    defaults.update(params)

    movie = Movie.objects.create(**defaults)
    return movie


class PublicMovieAPITests(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        """Test auth is not required to call API."""
        res = self.client.get(MOVIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrive_movie(self):
        """Test retrieving a list of movie."""

        res = self.client.get(MOVIES_URL)

        movie = Movie.objects.all().order_by('-id')
        serializer = MovieSerializer(movie, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_movie_detail(self):
        """Test retrieving a movie detail."""
        movie = create_movie()

        url = detail_url(movie.id)
        res = self.client.get(url)
        serializer = MovieDetailSerializer(movie)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie(self):
        """Test creating a movie."""
        payload = {
            'title': 'Test movie',
            'description': 'Test description for the movie'
        }
        res = self.client.post(MOVIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        movie = Movie.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(movie, k), v)
