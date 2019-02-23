import unittest
from urllib.request import urlopen, Request
from urllib.parse import urlencode


class GetPuzzleTests(unittest.TestCase):
    def test_successful(self):
        url = 'http://127.0.0.1:5000/puzzles/nyt'
        params = {
            'day': 22,
            'month': 2,
            'year': 2019
        }
        request = Request(url, urlencode(params).encode())
        response = urlopen(request)
        if response.status == 200:
            print("Get recieved a proper puzzle response")
        else:
            print("Something went wrong with the server")


if __name__ == '__main__':
    unittest.main()
