from word_utils import is_not_whitespace, parse
from urllib.request import urlopen

def save_response(url, num):
    response = urlopen(url)
    file = open('html/response' + str(num) + '.html', 'w')
    file.write(response.read().decode('utf-8'))
    file.close()

print('Testing whitespace...')

print(is_not_whitespace(' a  ')) # should be true
print(is_not_whitespace('ab  ')) # should be true
print(is_not_whitespace('    ')) # should be false

file = open('html/response.html', 'r')
html = file.read()
file.close()

print('Parsing response...')

parse(html)
