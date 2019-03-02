from django.test import TestCase
from .data import save_puzzle, get_puzzle
from .models import Puzzle


class DBModelTests(TestCase):

    def test_save(self):
        puzzle = save_puzzle(collection='nyt', day=24, month=12, year=2018)
        self.assertIsNotNone(puzzle)
        query = Puzzle.objects.get(collection='nyt', pub_day=24, pub_month=12, pub_year=2018)

    def test_info(self):
        query = get_puzzle(collection='nyt', day=24, month=12, year=2018)
        self.assertEqual(query.day_name, 'Monday')
        self.assertEqual(query.title, 'New York Times, Monday, December 24, 2018')
        self.assertEqual(query.author, 'Brendan Emmett Quigley')
        self.assertEqual(query.editor, 'Will Shortz')
        self.assertEqual(query.num_rows, 15)
        self.assertEqual(query.num_words, 72)
        self.assertEqual(query.num_blocks, 40)

    def test_grid(self):
        query = get_puzzle(collection='nyt', day=24, month=12, year=2018)
        rows = query.grid.rows.all()
        self.assertEqual(len(rows), 15)
        sample_cells = rows[0].cells.all()
        self.assertEqual(len(sample_cells), 15)
        cell_normal = sample_cells[5]
        self.assertEqual(cell_normal.number, 5)
        self.assertFalse(cell_normal.is_block)
        self.assertEqual(cell_normal.letter, 'A')
        cell_block = sample_cells[4]
        self.assertEqual(cell_block.number, 0)
        self.assertTrue(cell_block.is_block)
        self.assertEqual(cell_block.letter, '')

    def test_clues(self):
        query = get_puzzle(collection='nyt', day=24, month=12, year=2018)
        clues_down = query.clues.down
        clues_across = query.clues.across
        all_clues = list(clues_across.set.all()) + list(clues_down.set.all())
        self.assertEqual(len(all_clues), query.num_words)
        sample_clue = all_clues[37]
        self.assertEqual(sample_clue.grid_num, 5)
        self.assertEqual(sample_clue.content, 'Rah-rah')
        self.assertEqual(sample_clue.answer, 'AVID')
