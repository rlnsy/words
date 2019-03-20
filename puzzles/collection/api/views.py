from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
import logging

from collection.models import (
    Puzzle,
    Collection,
    AbstractClue,
)

from .serializers import (
    PuzzleDetailSerializer,
    PuzzleListSerializer,
    CollectionSerializer,
    CollectionListSerializer,
    ClueDetailSerializer,
    AbstractClueSerializer
)

logger = logging.getLogger('django')

# /puzzles/<id>
class PuzzleDetailAPIView(generics.RetrieveAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleDetailSerializer
    permission_classes = [AllowAny]


# /puzzles
class PuzzleListAPIView(generics.ListAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleListSerializer
    permission_classes = [AllowAny]


# /collections
class CollectionListAPIView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionListSerializer
    permission_classes = [AllowAny]


# /collections/<name>
class CollectionAPIView(generics.RetrieveAPIView):
    lookup_field = 'name'
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]


# /clues
class ClueListAPIView(generics.ListAPIView):
    queryset = AbstractClue.objects.all()
    serializer_class = AbstractClueSerializer
    permission_classes = [AllowAny]


# /clues/<id>
class ClueDetailAPIView(generics.RetrieveAPIView):
    queryset = AbstractClue.objects.all()
    serializer_class = AbstractClueSerializer
    permission_classes = [AllowAny]


# /puzzles/<id>/clues
class PuzzleCluesAPIView(generics.ListAPIView):

    def get_queryset(self):
        return get_object_or_404(Puzzle, id=self.kwargs['id']).clues.down.items.all()

    serializer_class = ClueDetailSerializer
    permission_classes = [AllowAny]

# class PuzzleByDate(APIView):
#     def get(self, request, day, month):
#