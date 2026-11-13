"""
REST API for cars (Django REST Framework).

    GET    /api/cars/        -> 200 list
    POST   /api/cars/        -> 201 created / 400 invalid   (auth required)
    GET    /api/cars/<id>/   -> 200 detail / 404 not found
    PUT    /api/cars/<id>/   -> 200 updated                 (auth required)
    PATCH  /api/cars/<id>/   -> 200 updated                 (auth required)
    DELETE /api/cars/<id>/   -> 204 no content / 404        (auth required)

Read access is public; writes need authentication. This comes from the
IsAuthenticatedOrReadOnly default set in settings.REST_FRAMEWORK.
"""
from rest_framework import generics

from .models import Car
from .serializers import CarSerializer


class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.select_related("manufacturer")
    serializer_class = CarSerializer


class CarDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.select_related("manufacturer")
    serializer_class = CarSerializer
