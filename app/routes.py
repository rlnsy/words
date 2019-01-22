from flask import Flask, request, jsonify
import data
from sources.Sources import format_date

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
        return "URL syntax error"  # TODO
    else:
        date = format_date(day=day, month=month, year=year)
        print("valid date, fetching (%s)..." % date)
        puzzle = data.get_puzzle(day=int(day), month=int(month), year=int(year), collection=collection)
        return jsonify(puzzle)
