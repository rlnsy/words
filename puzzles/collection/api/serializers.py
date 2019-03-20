from rest_framework import serializers
from collection.models import (
    Puzzle,
    Collection,
    AbstractClue,
)


class AbstractClueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AbstractClue
        fields = (
            'content',
            'answer',
            'puzzles'
        )


class AbstractClueNestedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AbstractClue
        fields = (
            'content',
            'answer',
        )


class ClueDetailSerializer(serializers.Serializer):
    abstract = AbstractClueNestedSerializer()
    grid_num = serializers.IntegerField()


class ClueSetSerializer(serializers.Serializer):
    items = ClueDetailSerializer(many=True)


class PuzzleCluesSerializer(serializers.Serializer):
    across = ClueSetSerializer(required=True)
    down = ClueSetSerializer(required=True)


class PuzzleDetailSerializer(serializers.HyperlinkedModelSerializer):

    collection = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='collection-detail',
        lookup_field='name'
    )

    # TODO: clues hyperlink

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
            'collection',
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
