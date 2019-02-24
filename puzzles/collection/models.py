from django.db import models


"""
Puzzle Object Models
"""


class PuzzleCell(models.Model):
    """
    Models a single puzzle cell
    json example:
    {
        "is_block" : false,
        "number" : 29,
        "letter" : "E"
    }
    """
    is_block = models.BooleanField()            # whether or not the cell is a block
    number = models.IntegerField()              # number label on the cell, may be NULL
    letter = models.CharField(max_length=1)     # correct letter, NULL if is_block is true


class PuzzleRow(models.Model):
    """
    Models a row in a puzzle (array of cells)
    """
    cells = models.ManyToManyField(PuzzleCell)  # all cells in the row


class PuzzleGrid(models.Model):
    """
    Grid: represents 2D array of cells (array of rows at top level)
    """
    rows = models.ManyToManyField(PuzzleRow)    # all the rows


class PuzzleClue(models.Model):
    """
    A puzzle clue with an associated grid number and clue content
    json example:
    {
        "num" : 5, "content" : "Cooper of hard rock"
    }
    """
    grid_num = models.IntegerField()
    content = models.CharField(max_length=200)


class ClueSet(models.Model):
    """
    A set of puzzle clues
    """
    set = models.ManyToManyField(PuzzleClue)


class PuzzleClues(models.Model):
    """
    All the necessary clues for a project; across and down sets
    """
    across = models.OneToOneField(ClueSet, on_delete=models.CASCADE, related_name="+")
    down = models.OneToOneField(ClueSet, on_delete=models.CASCADE, related_name="+")


class Puzzle(models.Model):

    """
    Class modeling a crossword puzzle. Structure follows the same serialization
    protocol as source response parsers. Grid and clue lists are represented as JSON Fields.
    """

    collection = models.CharField(max_length=50)    # Original collection
    title = models.CharField(max_length=200)        # Primary puzzle title
    subtitle = models.CharField(max_length=200)     # Secondary title, if applicable
    author = models.CharField(max_length=100)       # Puzzle Author
    editor = models.CharField(max_length=100)       # Puzzle Editor
    pub_day = models.IntegerField()                 # Day of publishing (e.g. 1, 30)
    pub_month = models.IntegerField()               # Month of publishing (e.g. 6, 12)
    pub_year = models.IntegerField()                # Year of publishing (e.g. 1992, 2018)
    day_name = models.CharField(max_length=10)      # Name of publish day (e.g. 'Sunday')
    num_rows = models.IntegerField()                # Number of rows in puzzle grid
    num_columns = models.IntegerField()             # Number of columns (usually the same as num_rows)
    num_word = models.IntegerField()                # Number of words in the puzzle
    num_blocks = models.IntegerField()              # Number of black cells in the puzzle

    grid = models.OneToOneField(PuzzleGrid, on_delete=models.CASCADE, related_name="grid_of")
    clues = models.OneToOneField(PuzzleClues, on_delete=models.CASCADE, related_name="clues_of")

    def __str__(self):
        return self.title
