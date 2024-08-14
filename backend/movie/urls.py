from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from movie import views

router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('actors', views.ActorViewSet)

movie_router = DefaultRouter()
movie_router.register(r'reviews', views.ReviewViewSet,
                      basename='movie-reviews')

app_name = 'movie'

urlpatterns = [
    path('', include(router.urls)),
    path('movies/<int:movie_pk>/', include(movie_router.urls)),
]
