from .views import (
    PuzzleDetailAPIView,
    PuzzleListAPIView,
    CollectionAPIView,
    CollectionListAPIView,
    ClueListAPIView,
    ClueDetailAPIView,
    PuzzleCluesAPIView,
    PuzzleByDateView,
    PuzzleGridAPIView
)

from django.urls import path

urlpatterns = [
    path('puzzles', PuzzleListAPIView.as_view(), name='puzzle-list'),
    path('puzzles/<int:pk>', PuzzleDetailAPIView.as_view(), name='puzzle-detail'),
    path('puzzles/date', PuzzleByDateView.as_view(), name='puzzle-date'),
    path('collections', CollectionListAPIView.as_view(), name='collection-list'),
    path('collections/<str:name>', CollectionAPIView.as_view(), name='collection-detail'),
    path('clues', ClueListAPIView.as_view(), name='clue-list'),
    path('clues/<int:pk>', ClueDetailAPIView.as_view(), name='clue-detail'),
    path('puzzles/<int:id>/clues/<str:set>', PuzzleCluesAPIView.as_view(), name='puzzleclues-detail'),
    path('puzzles/<int:puzzle_id>/grid', PuzzleGridAPIView.as_view(), name='puzzlegrid-detail')
]
