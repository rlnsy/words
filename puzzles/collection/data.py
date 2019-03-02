from .models import Puzzle, PuzzleGrid, PuzzleRow, PuzzleCell, PuzzleClues, ClueSet, PuzzleClue
from django.core.exceptions import ObjectDoesNotExist
from sources.Sources import Sources, format_date
from sources.exceptions import SourceError
import json


def find_puzzle(collection, day, month, year):
    """
    Searches for a puzzle in the database following given parameters
    :param collection: collection to in which to look for puzzle
    :param day: puzzle publish day
    :param month: puzzle publish month
    :param year: puzzle publish year
    :return: a Puzzle object fitting the parameters, or None
    """
    try:
        puzzle = Puzzle.objects.get(collection=collection, pub_day=day, pub_month=month, pub_year=year)
        return puzzle
    except ObjectDoesNotExist:
        return None


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
    if collection == 'nyt':
        date = format_date(day, month, year)
        try:
            info = Sources.fetch_puzzle(date, collection)
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

    new_grid = PuzzleGrid()
    new_grid.save()
    new_puzzle.grid = new_grid

    for row in info['grid']:
        new_row = PuzzleRow()
        new_row.save()
        new_puzzle.grid.rows.add(new_row)
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

    new_clues = PuzzleClues()
    clues_across = ClueSet()
    clues_down = ClueSet()
    clues_across.save()
    clues_down.save()
    for clue in info['clues']['across']:
        new_clue = PuzzleClue(grid_num=clue['num'], content=clue['content'], answer=clue['answer'])
        new_clue.save()
        clues_across.set.add(new_clue)
    for clue in info['clues']['down']:
        new_clue = PuzzleClue(grid_num=clue['num'], content=clue['content'], answer=clue['answer'])
        new_clue.save()
        clues_down.set.add(new_clue)
    new_clues.across = clues_across
    new_clues.down = clues_down
    new_clues.save()

    new_puzzle.clues = new_clues

    new_puzzle.json = json.dumps(info)

    new_puzzle.save()

    return find_puzzle(collection, day, month, year)


def get_puzzle(collection, day, month, year):
    """
    Performs a find() for the puzzle with given parameters. If this is unsuccessful, performs a save().
    If the save is unsuccessful, returns None
    """
    puzzle = find_puzzle(collection, day, month, year)
    if puzzle is None:
        return save_puzzle(collection, day, month, year)
    else:
        return puzzle