from html.parser import HTMLParser
from enum import Enum
import re
from word_utils.exceptions import ParseError

# regex expressions
non_whitespace = re.compile('\s*\S+\s*')
rows_e = re.compile('Rows: \d*')
cols_e = re.compile('Columns: \d*')
words_e = re.compile('Words: \d*')
blocks_e = re.compile('Blocks: \d*')
num_e = re.compile('\d+')
letter_e = re.compile('[A-Z]')
header_date = re.compile('[a-zA-Z]+, [a-zA-Z]+ \d{1,2}, \d{4}') # e.g. Sunday, January 1, 2019
az_block = re.compile('[a-zA-Z]+')
num_block = re.compile('\d+')

month_to_num = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


class ParserState(Enum):
    init = 1
    puzzle_title = 2
    puzzle_subtitle = 3
    author = 4
    editor = 5
    stats = 6
    grid = 7
    grid_item = 8
    header = 9


class ResponseParser(HTMLParser):

    STATS_REQUIRED = 4                          # number of basic stats to be parsed before changing state

    state = ParserState.init                    # current state of the parser

    exit_flag = True                            # indicates whether parser should reset state on next endtag

    stats_parsed = 0

    current_cell = None                         # current cell in which to store data

    puzzle = {
        "collection": 'nyt',
        "title": None,
        "subtitle": None,
        "author": None,
        "editor": None,
        "day": 0,
        "month": 0,
        "year": 0,
        "day_name": None,
        "rows": 0,
        "columns": 0,
        "words": None,
        "blocks": None,
        "grid": [],
        "clues": []
    }

    @staticmethod                               # parse helper for html attributes
    def parse_attrs(pairs):
        attr_dict = {}
        for pair in pairs:
            attr_dict[pair[0]] = pair[1]
        return attr_dict

    @staticmethod                               # extracts a number from a string
    def parse_number(raw_string):
        match = num_e.search(raw_string)
        if match is not None:
            return int(match.group())           # returns int type
        else:
            return None

    @staticmethod
    def parse_date(date_string):
        # takes a date string matching header_date
        # e.g. Sunday, January 1, 2019
        # TODO: make this better

        day__name_match = az_block.match(date_string)
        day_name = day__name_match.group()
        end = day__name_match.end()
        date_string = date_string[end + 1:]
        month_match = az_block.search(date_string)
        month = month_to_num[month_match.group()]
        end = month_match.end()
        date_string = date_string[end + 1:]
        day_match = num_block.search(date_string)
        day = int(day_match.group())
        end = day_match.end()
        date_string = date_string[end + 1:]
        year_match = num_block.search(date_string)
        year = int(year_match.group())

        return day, month, year, day_name

    @staticmethod
    def is_not_whitespace(data):
        return non_whitespace.match(data) is not None

    def parse_stat(self, stat_match, stat_type):
        val = ResponseParser.parse_number(stat_match.group())
        num = str(val)
        if stat_type == 'rows':
            print('Rows: ' + num)
        elif stat_type == 'columns':
            print('Columns: ' + num)
        elif stat_type == 'words':
            print('Words: ' + num)
        elif stat_type == 'blocks':
            print('Blocks: ' + num)
        self.puzzle[stat_type] = val
        self.stats_parsed += 1

    def get_table_size(self):
        count = 0
        for row in self.puzzle['grid']:
            for cell in row:
                count += 1
        return count

    def handle_starttag(self, tag, attrs):

        info = self.parse_attrs(attrs)

        if tag == 'title':
            self.state = ParserState.header

        # elements with id information
        if 'id' in info.keys():

            id = info['id']

            # puzzle title
            if id == 'PuzTitle':
                self.state = ParserState.puzzle_title

            # puzzle subtitle
            elif id == 'CPHContent_SubTitle':
                self.state = ParserState.puzzle_subtitle

            # authors block
            elif id == 'CPHContent_AEGrid':
                self.exit_flag = False
                self.state = ParserState.author

            # puzzle info
            elif id == 'CPHContent_StatsData':
                self.exit_flag = False
                self.state = ParserState.stats

            # actual puzzle grid
            elif id == 'PuzTable':
                self.exit_flag = False
                self.state = ParserState.grid

        # grid tags
        if self.state is ParserState.grid:

            # start of grid row
            if tag == 'tr':
                self.puzzle['grid'].append([])

            elif tag == 'td':           # start item

                self.current_cell = {
                    'is_block': False,
                    'number': None,
                    'letter': None,
                }

                if 'class' in info.keys():
                    if info['class'] == 'black':
                        self.current_cell['is_block'] = True

                self.state = ParserState.grid_item

            # TODO: parse clues

    def handle_endtag(self, tag):
        if (self.state != ParserState.init) & self.exit_flag:
            self.state = ParserState.init
        elif (self.state is ParserState.grid) & (self.get_table_size()
                                                 == self.puzzle['rows'] * self.puzzle['columns']):
            self.exit_flag = True
            self.state = ParserState.init
        elif (self.state is ParserState.grid_item) & (tag == 'td'):
            row_ix = len(self.puzzle['grid']) - 1
            self.puzzle['grid'][row_ix].append(self.current_cell)   # save the cell
            self.state = ParserState.grid

    def handle_data(self, data):
        if self.state == ParserState.header:
            date_ex = header_date.search(data).group()
            day, month, year, day_name = ResponseParser.parse_date(date_ex)
            self.puzzle['day'] = day
            print("Day: ", str(day))
            self.puzzle['month'] = month
            print("Month: ", str(month))
            self.puzzle['year'] = year
            print("Year: ", str(year))
            self.puzzle['day_name'] = day_name
            print("Day Name: ", day_name)
        if self.state == ParserState.puzzle_title:
            self.puzzle['title'] = data
            print("Puzzle Title: ", data)
        elif self.state == ParserState.puzzle_subtitle:
            self.puzzle['subtitle'] = data
            print("Puzzle Subtitle: ", data)
        elif (self.state == ParserState.author) & ResponseParser.is_not_whitespace(data) & (data != 'Author:'):
            self.puzzle['author'] = data
            print("Author: ", data)
            self.state = ParserState.editor
        elif (self.state == ParserState.editor) & ResponseParser.is_not_whitespace(data) & (data != 'Editor:'):
            self.puzzle['editor'] = data
            print("Editor: ", data)
            self.exit_flag = True
        elif (self.state == ParserState.stats) & ResponseParser.is_not_whitespace(data):
            stat_expressions = [('rows', rows_e), ('columns', cols_e),
                                ('words', words_e), ('blocks', blocks_e)]
            for ex_pair in stat_expressions:
                stat_data = ex_pair[1].search(data)
                stat_type = ex_pair[0]
                if stat_data is not None:
                    ResponseParser.parse_stat(self, stat_data, stat_type)

            if self.stats_parsed == ResponseParser.STATS_REQUIRED:
                self.exit_flag = True
        elif (self.state == ParserState.grid_item) & ResponseParser.is_not_whitespace(data):
            num_data = num_e.match(data)
            letter_data = letter_e.match(data)
            if num_data is not None:
                self.current_cell['number'] = int(num_data.group())
            elif letter_data is not None:
                self.current_cell['letter'] = letter_data.group()

    @staticmethod
    def parse(html):
        print("Parsing response...")
        try:
            parser = ResponseParser()
            parser.feed(html)
        except Exception:
            print("An internal error occurred in parsing :(")
            raise ParseError
        print('done.')
        puzzle_o = parser.puzzle
        return puzzle_o
