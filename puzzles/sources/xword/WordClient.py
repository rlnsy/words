from .ResponseParser import ResponseParser
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError
from sources.exceptions import DownloadError

base_url = 'https://www.xwordinfo.com'
puzzle_ext = '/Crossword'


class WordClient:

    @staticmethod
    def download(puzzle_date):
        url = base_url + puzzle_ext
        info = {'date': puzzle_date}
        request = Request(url, urlencode(info).encode())
        try:
            response = urlopen(request)
        except URLError:
            raise DownloadError             # TODO: let internet connection issues propagate to UI
        if response.status == 200:
            puzzle_o = ResponseParser.parse(response.read().decode('utf-8'))
            return puzzle_o
        else:
            raise DownloadError
