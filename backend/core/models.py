from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])

    def __str__(self):
        return self.movie.title
