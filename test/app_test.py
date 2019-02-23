from urllib.request import urlopen, Request
from urllib.parse import urlencode


def test(day, month, year):
    url = 'http://127.0.0.1:5000/puzzles/nyt'
    params = {
        'day': day,
        'month': month,
        'year': year
    }
    request = Request(url, urlencode(params).encode())
    response = urlopen(request)


def download_year():
    for month in range(1, 12):
        for day in range(1, 30):
            print('%(month)d/%(day)d/2004' % {'day': day, 'month': month})
            test(day, month, 2004)
