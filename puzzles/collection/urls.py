from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:collection_name>', views.get, name='puzzle_get')
]