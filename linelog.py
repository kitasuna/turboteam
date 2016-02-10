from text_functions import *

class LineLog:
    input_file = ""
    current_date = "2001/01/01"
    content = {}
    current_line = 0
    num_lines = 0

    def __init__(self, input_file = False):
        if(input_file):
            self.input_file = input_file
            self.read_file()

    def advance_to(self, date):
        while self.current_date < date: 
            l = self.get_next_line()
            if (type(l).__name__ == 'Dateline'):
                self.current_date = l.date

    def get_next_line(self):
        line = self.content[self.current_line]
        self.current_line += 1
        return parse_line(line)

    def read_file(self):
        with open(self.input_file, 'r') as f:
            self.content = f.readlines()
        self.num_lines = len(self.content)

