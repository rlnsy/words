from .views import (
    PuzzleDetailAPIView,
    PuzzleListAPIView,
    CollectionAPIView,
    CollectionListAPIView,
    ClueListAPIView,
    ClueDetailAPIView,
    PuzzleCluesAPIView,
)

from django.urls import path

urlpatterns = [
    path('puzzle/', PuzzleListAPIView.as_view(), name='puzzle-list'),
    path('puzzle/<int:pk>', PuzzleDetailAPIView.as_view(), name='puzzle-detail'),
    path('collection/', CollectionListAPIView.as_view(), name='collection-list'),
    path('collection/<str:name>/', CollectionAPIView.as_view(), name='collection-detail'),
    path('clue/', ClueListAPIView.as_view(), name='clue-list'),
    path('clue/<int:id>', ClueDetailAPIView.as_view(), name='clue-detail'),
    path('puzzle/<int:id>/clues/', PuzzleCluesAPIView.as_view(), name='puzzleclues-detail'),
]
