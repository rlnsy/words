from django.test import TestCase
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from .xword.ResponseParser import ResponseParser


class XwordParserTests(TestCase):

    sample_response = None
    parser = None

    def setUp(self):
        url = 'https://www.xwordinfo.com/Crossword'
        info = {'date': '12/24/2018'}
        request = Request(url, urlencode(info).encode())
        response = urlopen(request)
        self.sample_response = response.read().decode('utf-8')
        self.parser = ResponseParser()

    def testClues(self):
        puzzle_o = ResponseParser.parse(self.sample_response)
        num_clues_sample = len(puzzle_o['clues']['down'])
        self.assertGreater(num_clues_sample, 0)
