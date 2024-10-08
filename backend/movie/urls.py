from django.urls import (
    path,
    include,
)

from movie import views

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'actors', views.ActorViewSet)

# Création d'un router imbriqué pour les reviews
movies_router = routers.NestedDefaultRouter(router, r'movies', lookup='movie')
BN = 'movie-reviews'  # For linting
movies_router.register(r'reviews', views.ReviewViewSet, basename=BN)

app_name = 'movie'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(movies_router.urls)),
]
