from django.core.management.base import BaseCommand
from core.models import Actor, Movie, Review
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Inserts dummy data into the database if not already present'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Check if data already exists
        if Actor.objects.exists() and Movie.objects.exists():
            MESSAGE = 'Dummy data already present. Skipping insertion.'
            self.stdout.write(
                self.style.SUCCESS(MESSAGE))
            return

        # Create 10 actors
        actors = []
        for _ in range(10):
            actor = Actor.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            actors.append(actor)

        # Create 20 movies
        for _ in range(20):
            movie = Movie.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=200)
            )
            # Assign random actors to the movie
            randint = random.randint(1, len(actors))
            movie_actors = random.sample(actors, k=randint)
            movie.actors.set(movie_actors)
            movie.save()

            # Create a review for the movie
            Review.objects.create(
                movie=movie,
                grade=random.randint(1, 5)  # Random grade between 1 and 5
            )
        MESSAGE = 'Dummy data inserted successfully.'
        self.stdout.write(self.style.SUCCESS(MESSAGE))
