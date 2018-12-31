from word_utils import parse
from urllib.request import urlopen
import json

def save_response(url, num):
    response = urlopen(url)
    file = open('html/response' + str(num) + '.html', 'w')
    file.write(response.read().decode('utf-8'))
    file.close()

file = open('html/response.html', 'r')
html = file.read()
file.close()

print('Parsing response...')

puzzle_o = parse(html)

puzzle_fp = json.dumps(puzzle_o)

file = open('test.json', 'w')
file.write(puzzle_fp)
file.close()