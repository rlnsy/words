from django.http import HttpResponse
from .data import get_puzzle


def index(request):
    return HttpResponse("COLLECTION")


def by_collection_date(request, collection_name):
    month = request.GET['month']
    day = request.GET['day']
    year = request.GET['year']
    puzzle = get_puzzle(collection_name=collection_name, day=day, month=month, year=year)
    if puzzle is None:
        return HttpResponse("ERROR", status=404)
    else:
        # TODO
        # Stub for view layer
        return HttpResponse("JSON would be here but moving to a proper API")
