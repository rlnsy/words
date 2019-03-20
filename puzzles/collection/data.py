from sources.sourcer import Sourcer, format_date
from sources.exceptions import SourceError
from .models import (
    Collection,
    Puzzle,
    PuzzleGrid,
    PuzzleRow,
    PuzzleCell,
    PuzzleClues,
    AbstractClue,
    PuzzleClue,
    ClueSet
)

import logging

logger = logging.getLogger('django')


def find_puzzle(collection, day, month, year):
    """
    Searches for a puzzle in the database following given parameters
    :param collection: collection to in which to look for puzzle
    :param day: puzzle publish day
    :param month: puzzle publish month
    :param year: puzzle publish year
    :return: a Puzzle object fitting the parameters, or None
    """
    logger.info('Finding puzzle...')
    try:
        puzzle = Puzzle.objects.get(collection=collection, pub_day=day, pub_month=month, pub_year=year)
        return puzzle
    except Puzzle.DoesNotExist:
        logger.info('not found')
        return None


def save_clues(info):

    new_clues = PuzzleClues()
    a_set = ClueSet()
    a_set.save()
    d_set = ClueSet()
    d_set.save()
    new_clues.across = a_set
    new_clues.down = d_set
    new_clues.save()

    clue_reg = []  # list of clues to register with puzzle

    def make_new_clue(clue, set):
        # create and save a new puzzle clue

        try:
            clue_abstract = AbstractClue.objects.get(content=clue['content'], answer=clue['answer'])
        except AbstractClue.DoesNotExist:
            # create the new abstract clue
            clue_abstract = AbstractClue(content=clue['content'], answer=clue['answer'])
            clue_abstract.save()

        clue_reg.append(clue_abstract)

        new_clue = PuzzleClue(grid_num=clue['num'], abstract=clue_abstract)
        new_clue.set = set
        new_clue.save()
        return new_clue

    for c in info['clues']['across']:
        new = make_new_clue(c, a_set)
        a_set.items.add(new)

    for c in info['clues']['down']:
        new = make_new_clue(c, d_set)
        d_set.items.add(new)

    return new_clues, clue_reg


def save_grid(info):
    new_grid = PuzzleGrid()
    new_grid.save()
    for row in info['grid']:
        new_row = PuzzleRow()
        new_row.save()
        new_grid.rows.add(new_row)
        for cell in row:
            new_cell = PuzzleCell(is_block=cell['is_block'], letter=cell['letter'])
            if cell['number'] is not None:
                new_cell.number = cell['number']
            else:
                new_cell.number = 0
            if cell['letter'] is not None:
                new_cell.letter = cell['letter']
            else:
                new_cell.letter = ''
            new_cell.save()
            new_row.cells.add(new_cell)
    return new_grid


def save_puzzle(collection, day, month, year):
    """
    Subdivides the puzzle request by collection and activates the appropriate source. Saves a new puzzle
    if download is successful
    :param collection: collection to save puzzle to, also indicates source
    :param day: puzzle publish day
    :param month: puzzle publish month
    :param year: puzzle publish year
    :return: the result of a find() operation with the given parameters (after performing download)
    """

    logger.info('Saving a new puzzle in the database!')

    date = format_date(day, month, year)

    try:
        info = Sourcer.fetch_puzzle(date, collection.name)
    except SourceError:
        return None

    # create the object
    new_puzzle = Puzzle(collection=collection)
    new_puzzle.title = info['title']
    new_puzzle.subtitle = info['title']
    new_puzzle.author = info['author']
    new_puzzle.editor = info['editor']
    new_puzzle.pub_day = info['day']
    new_puzzle.pub_month = info['month']
    new_puzzle.pub_year = info['year']
    new_puzzle.day_name = info['day_name']
    new_puzzle.num_rows = info['rows']
    new_puzzle.num_columns = info['columns']
    new_puzzle.num_words = info['words']
    new_puzzle.num_blocks = info['blocks']
    new_puzzle.grid = save_grid(info)
    new_puzzle.clues, to_add = save_clues(info)
    new_puzzle.save()

    for clue_used in to_add:
        clue_used.puzzles.add(new_puzzle)   # register usage of clue

    new_puzzle.collection.puzzles.add(new_puzzle)   # add to the collection

    return find_puzzle(collection, day, month, year)


def get_puzzle(collection_name, day, month, year):
    """
    Performs a find() for the puzzle with given parameters. If this is unsuccessful, performs a save().
    If the save is unsuccessful, returns None
    """
    try:
        collection = Collection.objects.get(name=collection_name)
    except Collection.DoesNotExist:
        print("No collection matching provided short name")
        return None
    puzzle = find_puzzle(collection, day, month, year)
    if puzzle is None:
        return save_puzzle(collection, day, month, year)
    else:
        return puzzle
