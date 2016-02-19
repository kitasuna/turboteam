from text_functions import *
from datetime import datetime

class LineLog:
    input_file = ""
    current_date = "2001/01/01"
    end_date = "9999/12/31"
    content = {}
    current_line = 0
    num_lines = 0

    def __init__(self, input_file = False):
        self.current_date = datetime.strptime('2001/01/01', '%Y/%m/%d')
        self.end_date = datetime.strptime('9999/12/31', '%Y/%m/%d')
        if(input_file):
            self.input_file = input_file
            self.read_file()

    def advance_to(self, date):
        while self.current_date < date: 
            l = self.get_next_line()

    def get_next_line(self):
        line = self.content[self.current_line]
        self.current_line += 1
        l = parse_line(line)
        if (type(l).__name__ == 'Dateline'):
            self.current_date = datetime.strptime(l.date, '%Y/%m/%d')
            # Kind of a hack-y way to stop getting lines
            if self.current_date > self.end_date:
                self.current_line = self.num_lines + 1
        return l

    def read_file(self):
        with open(self.input_file, 'r') as f:
            self.content = f.readlines()
        self.num_lines = len(self.content)

    def set_end_date(self, end_date):
        self.end_date = end_date

