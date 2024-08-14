"""
Views for movies
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from movie import serializers
from core.models import Movie, Actor, Review


class MovieViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.MovieDetailSerializer
    queryset = Movie.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retrieve the movie."""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return serializer class."""
        if self.action == 'list':
            return serializers.MovieSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save()


class ActorViewSet(viewsets.ModelViewSet):
    """Manage actors in the database."""
    serializer_class = serializers.ActorSerializer
    queryset = Actor.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs['movie_pk']
        return Review.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        serializer.save()
