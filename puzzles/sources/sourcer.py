from .xword.WordClient import WordClient
from .exceptions import SourceError
from collection.models import Collection
from django.core.exceptions import ObjectDoesNotExist

def format_date(day, month, year):
    return str(month) + '/' + str(day) + '/' + str(year)


class Sourcer:

    @staticmethod
    def fetch_puzzle(puzzle_date, collection):
        """
        Function for unconditionally downloading a puzzle from a given collection which routes to a source
        :return: puzzle object
        :raises SourceError
        """
        try:
            coll = Collection.objects.get(name=collection)
            if coll.name == 'nyt':
                return WordClient.download(puzzle_date)
            else:
                print("Collection name match in database, but no source linked")
                raise SourceError
        except ObjectDoesNotExist:
            print("No collection matching given short name")
            raise SourceError
