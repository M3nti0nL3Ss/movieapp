from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Review, Movie
from movie.serializers import ReviewSerializer


def get_review_list_url(movie_id):
    """Create and return a reviews list URL for a given movie."""
    return reverse('movie:movie-reviews-list', kwargs={'movie_pk': movie_id})


def detail_url(movie_id, review_id):
    """Create and return a review detail URL."""
    return reverse('movie:movie-reviews-detail',
                   kwargs={'movie_pk': movie_id, 'pk': review_id})


def create_movie(**params):
    """Create and return a sample movie."""
    defaults = {
        'title': 'Test movie',
        'description': 'Test description for the movie'
    }
    defaults.update(params)
    movie = Movie.objects.create(**defaults)
    return movie


class PublicReviewsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_reviews(self):
        """Test retrieving a list of reviews."""
        movie = create_movie()
        Review.objects.create(grade=5, movie=movie)
        Review.objects.create(grade=4, movie=movie)

        url = get_review_list_url(movie.id)
        res = self.client.get(url)

        reviews = Review.objects.all().order_by('-id')
        serializer = ReviewSerializer(reviews, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_review(self):
        """Test updating a review."""
        movie = create_movie()
        review = Review.objects.create(grade=5, movie=movie)

        payload = {'grade': 4}
        url = detail_url(movie.id, review.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.grade, payload['grade'])

    def test_delete_review(self):
        """Test deleting a review."""
        movie = create_movie()
        review = Review.objects.create(grade=5, movie=movie)

        url = detail_url(movie.id, review.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        reviews = Review.objects.filter(id=review.id)
        self.assertFalse(reviews.exists())
