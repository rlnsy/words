from django.test import TestCase
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from .xword.ResponseParser import ResponseParser
from sources.exceptions import AvailabilityError


class XwordParserTests(TestCase):

    url = 'https://www.xwordinfo.com/Crossword'
    info = {'date': '12/24/2018'}
    request = Request(url, urlencode(info).encode())
    response = urlopen(request)

    sample_response = response.read().decode('utf-8')
    parser = ResponseParser()
    puzzle = ResponseParser.parse(sample_response)

    def testCluesNonZero(self):
        num_clues = len(self.puzzle['clues']['across']) + len(self.puzzle['clues']['down'])
        self.assertGreater(num_clues, 0)

    def testCluesNumCorrect(self):
        num_clues = len(self.puzzle['clues']['across']) + len(self.puzzle['clues']['down'])
        self.assertEqual(num_clues, self.puzzle['words'])

    def testUnavailable(self):
        info = {'date': '3/2/2020'}
        request = Request(self.url, urlencode(info).encode())
        response = urlopen(request).read().decode('utf-8')
        self.assertRaises(AvailabilityError, ResponseParser.parse, html=response)
