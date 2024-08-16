"""
Views for movies
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from movie import serializers
from core.models import Movie, Actor, Review

from asgiref.sync import sync_to_async

from adrf.viewsets import ModelViewSet as AsyncModelViewSet


class MovieViewSet(viewsets.ModelViewSet):
    """View for managing movie APIs."""
    serializer_class = serializers.MovieDetailSerializer
    queryset = Movie.objects.all().order_by('-id')
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
    queryset = Actor.objects.all().order_by("-id")

    def perform_create(self, serializer):
        serializer.save()


class ReviewViewSet(AsyncModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs['movie_pk']
        return Review.objects.filter(movie_id=movie_id).order_by("-id")

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await sync_to_async(serializer.is_valid)()
        # Using sync_to_async for save operation
        # including a sync function wrapper
        await serializer.asave()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)
