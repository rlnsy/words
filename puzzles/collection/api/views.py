from collection.models import Puzzle, Collection

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import (
    PuzzleDetailSerializer,
    PuzzleListSerializer,
    CollectionSerializer,
    CollectionListSerializer
)


class PuzzleDetailAPIView(generics.RetrieveAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleDetailSerializer
    permission_classes = [AllowAny]


class PuzzleListAPIView(generics.ListAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleListSerializer
    permission_classes = [AllowAny]


class CollectionListAPIView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionListSerializer
    permission_classes = [AllowAny]


class CollectionAPIView(generics.RetrieveAPIView):
    lookup_field = 'name'
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
