from flask import Flask, request, jsonify
from flask_api import status
import data
from sources.Sources import format_date
from exceptions import DatabaseError

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to the crosswords server"


@app.route('/puzzles/<collection>', methods=['GET', 'POST'])
def get_puzzle(collection):
    print("Received request for puzzle")
    params = request.form
    day = params['day']
    month = params['month']
    year = params['year']
    if (day is None) or (month is None) or (year is None):
        print("client provided invalid syntax in query")
        return "URL syntax error", status.HTTP_400_BAD_REQUEST
    else:
        date = format_date(day=day, month=month, year=year)
        print("valid date, fetching (%s)..." % date)
        try:
            puzzle = data.get_puzzle(day=int(day), month=int(month), year=int(year), collection=collection)
        except DatabaseError:
            return "Something went wrong with the server :(", status.HTTP_204_NO_CONTENT
        return jsonify(puzzle)
