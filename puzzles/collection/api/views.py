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
    AbstractClueSerializer,
    GridSerializer
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
    serializer_class = PuzzleDetailSerializer  # show all details
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


# /puzzles/<id>/clues/<set>
class PuzzleCluesAPIView(generics.ListAPIView):

    def get_queryset(self):
        puzzle = get_object_or_404(Puzzle, id=self.kwargs['id'])
        if self.kwargs['set'] == 'across':
            set = puzzle.clues.across
        else:
            set = puzzle.clues.down
        return set.items.all()

    serializer_class = ClueDetailSerializer
    permission_classes = [AllowAny]


# /puzzles/date
class PuzzleByDateView(APIView):
    """
    Retrieve a puzzle instance by date and collection parameters
    may add new puzzle to the database
    """
    def get(self, request):
        puzzle = get_puzzle(day=request.query_params['day'], month=request.query_params['month'],
                            year=request.query_params['year'], collection_name=request.query_params['collection'])
        if puzzle is None:
            return Response("ERROR", status=404)
        else:
            serializer = PuzzleDetailSerializer(puzzle, context={'request': request})
            return Response(serializer.data)


# /puzzle/<id>
class PuzzleGridAPIView(APIView):
    def get(self, request, puzzle_id):
        puzzle = get_object_or_404(Puzzle, id=puzzle_id)
        serializer = GridSerializer(puzzle.grid, context={'request': request})
        return Response(serializer.data)
