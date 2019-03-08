from .views import (
    PuzzleDetailAPIView,
    PuzzleListAPIView,
    CollectionAPIView,
    CollectionListAPIView,
)

from django.urls import include, path
from django.conf.urls import url

urlpatterns = [
    path('puzzle/', PuzzleListAPIView.as_view(), name='puzzle-list'),
    path('puzzle/<int:pk>', PuzzleDetailAPIView.as_view(), name='puzzle-detail'),
    path('collection/', CollectionListAPIView.as_view(), name='collection-list'),
    path('collection/<str:name>/', CollectionAPIView.as_view(), name='collection-detail'),
]
