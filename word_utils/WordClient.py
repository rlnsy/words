from ResponseParser import ResponseParser
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from word_utils.exceptions import DownloadError

base_url = 'https://www.xwordinfo.com'
puzzle_ext = '/Crossword'


def format_date(day, month, year):
    return str(month) + '/' + str(day) + '/' + str(year)


class WordClient:

    @staticmethod
    def download(puzzle_date):
        url = base_url + puzzle_ext
        info = {'date': puzzle_date}
        request = Request(url, urlencode(info).encode())
        response = urlopen(request)
        if response.status == 200:
            puzzle_o = ResponseParser.parse(response.read().decode('utf-8'))
            return puzzle_o
        else:
            raise DownloadError
