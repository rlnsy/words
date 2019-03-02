from django.http import HttpResponse, JsonResponse
from .data import get_puzzle
import json


def index(request):
    return HttpResponse("COLLECTION")


def by_collection_date(request, collection_name):
    month = request.GET['month']
    day = request.GET['day']
    year = request.GET['year']
    puzzle = get_puzzle(collection=collection_name, day=day, month=month, year=year)
    if puzzle is None:
        return HttpResponse("ERROR", status=404)
    else:
        # TODO
        # Stub for view layer
        return JsonResponse(json.loads(puzzle.json), status=200)
