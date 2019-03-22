from rest_framework import serializers
from rest_framework.reverse import reverse

from collection.models import (
    Puzzle,
    Collection,
    AbstractClue,
    PuzzleCell,
    PuzzleGrid,
    ClueSet,
    PuzzleClues
)


class GridCellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PuzzleCell
        fields = (
            'is_block',
            'number',
            'letter'
        )


class GridRowSerializer(serializers.Serializer):
    cells = GridCellSerializer(many=True)


class GridSerializer(serializers.Serializer):
    rows = GridRowSerializer(many=True)


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


# class ClueSetSerializer(serializers.Serializer):
#     items = ClueDetailSerializer(many=True)
#
#


class PuzzleCluesSerializer(serializers.Serializer):

    class ClueSetHyperlink(serializers.HyperlinkedRelatedField):

        view_name = 'puzzleclues-detail'
        queryset = ClueSet.objects.all()
        read_only = True
        clue_set = None

        def __init__(self, c_set):
            super().__init__()
            self.clue_set = c_set

        def get_url(self, obj, view_name, request, format):
            set = ClueSet.objects.get(id=obj.pk)
            clue_base = (
                set.origin_across if self.clue_set == 'across'
                else set.origin_down)
            url_kwargs = {
                'id': clue_base.puzzle_of.id,
                'set': self.clue_set
            }
            return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

        def get_object(self, view_name, view_args, view_kwargs):
            lookup_kwargs = {
                'origin_across': Puzzle.objects.get(id=view_kwargs['puzzle_id']).clues
            } if self.clue_set == 'across' else {
                'origin_down': Puzzle.objects.get(id=view_kwargs['puzzle_id']).clues
            }
            return self.queryset.get(**lookup_kwargs)

    across = ClueSetHyperlink(c_set='across')
    down = ClueSetHyperlink(c_set='down')


class PuzzleDetailSerializer(serializers.HyperlinkedModelSerializer):

    collection = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='collection-detail',
        lookup_field='name'
    )

    # TODO: clues hyperlink with custom lookup

    # clues = serializers.HyperlinkedRelatedField(
    #
    # )

    class GridHyperlink(serializers.HyperlinkedRelatedField):

        view_name = 'puzzlegrid-detail'
        queryset = PuzzleGrid.objects.all()
        read_only = True

        def get_url(self, obj, view_name, request, format):
            url_kwargs = {
                'puzzle_id': PuzzleGrid.objects.get(id=obj.pk).puzzle.id
            }
            return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

        def get_object(self, view_name, view_args, view_kwargs):
            lookup_kwargs = {
                'puzzle': Puzzle.objects.get(id=view_kwargs['puzzle_id'])
            }
            return self.queryset.get(**lookup_kwargs)

    # clues = {
    #     'across': None
    #     # 'across': ,
    #     # 'down': CluesHyperlink(c_set='down')
    # }

    clues = PuzzleCluesSerializer()

    grid = GridHyperlink()

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
            'grid',
            'clues'
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
