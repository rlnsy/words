from rest_framework import serializers
from collection.models import Puzzle, Collection


class PuzzleDetailSerializer(serializers.HyperlinkedModelSerializer):

    collection = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='collection-detail',
        lookup_field='name'
    )

    class Meta:
        model = Puzzle
        fields = (
            'title',
            'subtitle',
            'author',
            'editor',
            'day_name',
            'pub_year',
            'num_words',
            'num_blocks',
            'collection'
        )


class PuzzleListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Puzzle
        fields = (
            'id',           # using default pk for now
            'title',
            'pub_year',
        )


class CollectionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'name',
            'long_name',
        )


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'name',
            'long_name',
            'puzzles',
        )
