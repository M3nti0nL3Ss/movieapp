"""
Views for movies
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from movie import serializers
from core.models import Movie


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
