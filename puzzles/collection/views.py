from django.http import HttpResponse, JsonResponse
from sources.Sources import Sources, format_date
from sources.exceptions import SourceError


def index(request):
    return HttpResponse("Hello. You're at the collections index.")


def get(request, collection_name):
    date = format_date(24, 12, 2018)
    try:
        puzzle = Sources.fetch_puzzle(date, collection_name)
    except SourceError:
        return HttpResponse("ERROR")
    return JsonResponse(puzzle)
