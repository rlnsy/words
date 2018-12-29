from html.parser import HTMLParser
from enum import Enum
import re

ParserState = Enum('ParserState','init '
                                 'puzzle_title '
                                 'puzzle_subtitle '
                                 'author editor '
                                 'stats')

# regex expressions
non_whitespace = re.compile('\s*\S+\s*')
rows_e = re.compile('Rows: \d*')
cols_e = re.compile('Columns: \d*')
words_e = re.compile('Words: \d*')
blocks_e = re.compile('Blocks: \d*')
num_e = re.compile('\d+')


class ResponseParser(HTMLParser):

    STATS_REQUIRED = 4                          # number of basic stats to be parsed before changing state

    state = ParserState.init                    # current state of the parser

    exit_flag = True                            # indicates whether parser should reset state on next endtag

    stats_parsed = 0

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
    def is_not_whitespace(data):
        return non_whitespace.match(data) is not None

    def parse_stat(self, stat_match, stat_type):
        val = ResponseParser.parse_number(stat_match.group())
        num = str(val)
        if stat_type is 'rows':
            print('Rows: ' + num)
        elif stat_type is 'cols':
            print('Columns: ' + num)
        elif stat_type is 'words':
            print('Words: ' + num)
        elif stat_type is 'blocks':
            print('Blocks: ' + num)
        self.stats_parsed += 1

    def handle_starttag(self, tag, attrs):

        info = self.parse_attrs(attrs)

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

            # TODO: parse puzzle and clues

    def handle_endtag(self, tag):
        if (self.state != ParserState.init) & self.exit_flag:
            self.state = ParserState.init

    def handle_data(self, data):
        if self.state == ParserState.puzzle_title:
            print("Puzzle Title: ", data)
        elif self.state == ParserState.puzzle_subtitle:
            print("Puzzle Subtitle: ", data)
        elif (self.state == ParserState.author) & ResponseParser.is_not_whitespace(data) & (data != 'Author:'):
            print("Author: ", data)
            self.state = ParserState.editor
        elif (self.state == ParserState.editor) & ResponseParser.is_not_whitespace(data) & (data != 'Editor:'):
            print("Editor: ", data)
            self.exit_flag = True
        elif (self.state == ParserState.stats) & ResponseParser.is_not_whitespace(data):
            stat_expressions = [('rows', rows_e), ('cols', cols_e),
                                ('words', words_e), ('blocks', blocks_e)]
            for ex_pair in stat_expressions:
                stat_data = ex_pair[1].search(data)
                stat_type = ex_pair[0]
                if stat_data is not None:
                    ResponseParser.parse_stat(self, stat_data, stat_type)

            if self.stats_parsed is ResponseParser.STATS_REQUIRED:
                self.exit_flag = True


def parse(html):
    parser = ResponseParser()
    parser.feed(html)
