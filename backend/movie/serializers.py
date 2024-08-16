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


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for actors."""

    class Meta:
        model = Actor
        fields = ['id', 'first_name', 'last_name']
        # read_only_fields = ['id']


class MovieDetailSerializer(MovieSerializer):
    """Serializer for movie detail view."""
    reviews = ReviewSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True)

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['reviews', 'actors']
        # depth = 1

    def create(self, validated_data):
        actors_data = validated_data.pop('actors', [])
        movie = Movie.objects.create(**validated_data)

        for actor_data in actors_data:
            actor_id = actor_data.get('id', None)
            if actor_id:
                # Update existing actor
                actor = Actor.objects.get(id=actor_id)
                for attr, value in actor_data.items():
                    setattr(actor, attr, value)
                actor.save()
                movie.actors.add(actor)
            else:
                # Create a new actor and associate with the movie
                actor = Actor.objects.create(**actor_data)
                movie.actors.add(actor)

        return movie

    def update(self, instance, validated_data):
        actors_data = validated_data.pop('actors', [])
        instance = super().update(instance, validated_data)

        # Handle existing and new actors
        current_actor_ids = [actor.id for actor in instance.actors.all()]
        new_actor_ids = []

        for actor_data in actors_data:
            # Create new actors or update existing ones
            actor_id = actor_data.get('id', None)
            if actor_id:
                # Update existing actor
                if actor_id in current_actor_ids:
                    actor = Actor.objects.get(id=actor_id)
                    for attr, value in actor_data.items():
                        setattr(actor, attr, value)
                    actor.save()
                    new_actor_ids.append(actor_id)
            else:
                # Create a new actor and associate with the movie
                actor = Actor.objects.create(**actor_data)
                instance.actors.add(actor)
                new_actor_ids.append(actor.id)

        # Remove actors that are no longer associated with the movie
        for actor_id in current_actor_ids:
            if actor_id not in new_actor_ids:
                Actor.objects.filter(id=actor_id).delete()

        return instance
