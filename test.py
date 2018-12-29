from word_utils import parse
from urllib.request import urlopen

def save_response(url, num):
    response = urlopen(url)
    file = open('html/response' + str(num) + '.html', 'w')
    file.write(response.read().decode('utf-8'))
    file.close()

file = open('html/response2.html', 'r')
html = file.read()
file.close()

print('Parsing response...')

parse(html)
