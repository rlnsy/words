from html.parser import HTMLParser
from enum import Enum
import re

ParserState = Enum('ParserState',
                    'init puzzle_title puzzle_subtitle author editor')

non_whitespace = re.compile('\s*\S+\s*')

def is_not_whitespace(data):
    return non_whitespace.match(data) != None


class ResponseParser(HTMLParser):

    state = ParserState.init        # current state of the parser

    exit_flag = True                # indicates whether parser should
                                    # reset state on next endtag

    def parse_attrs(self, list):
        attr_dict = {}
        for pair in list:
            attr_dict[pair[0]] = pair[1]
        return attr_dict

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

            # TODO: parse puzzle and clues


    def handle_endtag(self, tag):
        if (self.state != ParserState.init) & self.exit_flag:
            self.state = ParserState.init


    def handle_data(self, data):
        if self.state == ParserState.init:
            #print("Encountered some data outside tags: ", data)
            assert True
        elif self.state == ParserState.puzzle_title:
            print("Puzzle Title: ", data)
        elif self.state == ParserState.puzzle_subtitle:
            print("Puzzle Subtitle: ", data)
        elif (self.state == ParserState.author) & is_not_whitespace(data) & (data != 'Author:'):
            print("Author: ", data)
            self.state = ParserState.editor
        elif (self.state == ParserState.editor) & is_not_whitespace(data) & (data != 'Editor:'):
            print("Editor: ", data)
            self.exit_flag = True


def parse(html):
    parser = ResponseParser()
    parser.feed(html)
