from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from sources.Sources import Sources, format_date
from exceptions import DatabaseError
from _datetime import datetime

db_client = MongoClient()
db = db_client['words_data']


def find_puzzle(day, month, year, collection):
    puzzle_collection = db['puzzle_collections'][collection]
    search_query = {
        'day': day,
        'month': month,
        'year': year
    }
    try:
        puzzle = puzzle_collection.find_one(search_query)
    except ServerSelectionTimeoutError:
        raise DatabaseError
    return puzzle


def save_puzzle(puzzle, collection):
    try:
        add_time = datetime.now()
        puzzle['date_added'] = add_time
        puzzle_collection = db['puzzle_collections'][collection]
        puzzle['_id'] = format_date(puzzle['day'], puzzle['month'], puzzle['year'])  # using formatted date as key
        ins_id = puzzle_collection.insert_one(puzzle).inserted_id
        print("New puzzle added to %(collection)s on %(date)s with id %(id)s"
              % {'collection': collection, 'date': str(add_time), 'id': str(ins_id)})
    except Exception:
        raise DatabaseError


def get_puzzle(day, month, year, collection):
    """
    Attempts to find precisely dated puzzle in the database. If the puzzle exists, returns it, otherwise makes a call to
    download the puzzle, saves it as a new entry, and returns the result of a new find with the same parameters.
    :param day: puzzle day of publishing e.g. 30
    :param month: puzzle month e.g. 01
    :param year: puzzle year e.g. 2019
    :param collection: collection name e.g. 'nyt'
    :returns: a serializable puzzle object
    :raises: DatabaseError if an error occurs related to saving a new puzzle, or if the new puzzle does not match the
    original query.
    :raises: DownloadError if an error occurred getting a new puzzle from the internet.
    """
    puzzle = find_puzzle(day, month, year, collection)
    if puzzle is None:
        print("Puzzle does not exist in database, downloading...")
        puzzle_date = format_date(day, month, year)
        new_puzzle = Sources.fetch_puzzle(puzzle_date,collection)              # may raise source error
        save_puzzle(new_puzzle, collection)
        puzzle = find_puzzle(day, month, year, collection)
        if puzzle is None:
            print("The download didn't work as expected :(")
            raise DatabaseError
    else:
        print("Found puzzle in database")
    return puzzle
