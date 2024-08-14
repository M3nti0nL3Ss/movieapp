"""
Tests for models.py
"""

from django.test import TestCase
from core import models


def create_movie(title='Test movie', description='Test movie description'):
    """Create and return a new movie."""
    return models.Movie.objects.create(
            title=title,
            description=description,
        )


class ModelTests(TestCase):
    """Tests for models.py"""

    def test_create_movie(self):
        """Test creating a new movie."""
        movie = models.Movie.objects.create(
            title="Test Movie",
            description="Test Description",
        )
        self.assertEqual(str(movie), "Test Movie")

    def test_create_actor(self):
        """Test creating a new actor."""
        actor = models.Actor.objects.create(
            first_name="Test",
            last_name="Nest",
        )
        self.assertEqual(actor.first_name, "Test")
        self.assertEqual(actor.last_name, "Nest")

    def test_create_review(self):
        """Test creating a new Review."""
        movie = create_movie()
        review = models.Review.objects.create(
            grade=10,
            movie=movie
        )
        self.assertEqual(review.grade, 10)
