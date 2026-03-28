from django.db.models import QuerySet
from rest_framework import viewsets

from cinema.models import CinemaHall, Genre, Actor, Movie, MovieSession
from cinema.serializers import CinemaHallSerializer, GenreSerializer, ActorSerializer, MovieSerializer, MovieSessionSerializer, MovieListSerializer, MovieRetrieveSerializer, MovieSessionListSerializer, MovieSessionRetrieveSerializer


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieListSerializer

    def get_serializer_class(self) -> type[MovieListSerializer | MovieRetrieveSerializer | MovieSerializer]:
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieRetrieveSerializer
        return MovieSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("genres", "actors")
        return queryset

class MovieSessionViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self) -> type[MovieSessionListSerializer | MovieSessionRetrieveSerializer | MovieSessionSerializer]:
        if self.action == "list":
            return MovieSessionListSerializer
        if self.action == "retrieve":
            return MovieSessionRetrieveSerializer
        return MovieSessionSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("movie", "cinema_hall")
        return queryset
