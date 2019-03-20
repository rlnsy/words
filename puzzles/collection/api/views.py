from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from collection.data import get_puzzle
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


# /puzzles/date
class PuzzleByDateView(APIView):
    """
    Retrieve a puzzle instance by date and collection parameters
    """
    def get(self, request):
        puzzle = get_puzzle(day=request.query_params['day'], month=request.query_params['month'],
                            year=request.query_params['year'], collection_name=request.query_params['collection'])
        if puzzle is None:
            return Response("ERROR", status=404)
        else:
            serializer = PuzzleDetailSerializer(puzzle, context={'request': request})
            return Response(serializer.data)
