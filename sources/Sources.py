from .xword.WordClient import WordClient
from .exceptions import SourceError


def format_date(day, month, year):
    return str(month) + '/' + str(day) + '/' + str(year)


class Sources:

    @staticmethod
    def fetch_puzzle(puzzle_date, collection):
        """
        Function for unconditionally downloading a puzzle from a given collection which routes to a source
        :return: puzzle object
        """
        try:
            if collection == 'nyt':  # switch machine to divide up sources
                return WordClient.download(puzzle_date)
            else:
                raise SourceError
        except SourceError as se:
            raise se
