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

# run the parser
puzzle_o = parse(html)

"""
puzzle_fp = json.dumps(puzzle_o, indent=1)

save the file
file = open('test.json', 'w')
file.write(puzzle_fp)
file.close()
"""

# test parser results
print('Tests:')
# test puzzle dimensions
grid_rows = len(puzzle_o['grid'])
stats_rows = puzzle_o['rows']
grid_cols = len(puzzle_o['grid'][0])
stats_cols = puzzle_o['columns']

print("rows from stats data:" + str(stats_rows))
print("rows from actual grid: " + str(grid_rows))   # should be the same

print("columnss from stats data:" + str(stats_cols))
print("columns from actual grid: " + str(grid_cols))   # should be the same

# test number of blocks
stats_blocks = puzzle_o['blocks']
grid_blocks = 0
for row in puzzle_o['grid']:
    for cell in row:
        if cell['is_block'] is True:
            grid_blocks += 1

print("blocks from stats data:" + str(stats_blocks))
print("blocks from actual grid: " + str(grid_blocks))   # should be the same
