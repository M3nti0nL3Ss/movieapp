"""
Serializers for movies
"""

from rest_framework import serializers
from adrf.serializers import ModelSerializer as AsyncModelSerializer

from core.models import Movie, Actor, Review


class ReviewSerializer(AsyncModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movie view."""
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']


class MovieDetailSerializer(MovieSerializer):
    """Serializer for movie detail view."""
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['reviews', 'actors']
        depth = 1


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for actors."""

    class Meta:
        model = Actor
        fields = ['id', 'first_name', 'last_name']
        read_only_fields = ['id']
