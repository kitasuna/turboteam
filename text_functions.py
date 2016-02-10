import re
from collections import namedtuple

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def is_line_date(line):
    pattern = re.compile('^(\d+/\d+/\d+)')
    return pattern.match(line) 

def is_line_chat(line):
    pattern = re.compile('^(\d+:\d+\t(.+)\t(.+))')
    return pattern.match(line) 

def parse_line(line):
    Dateline = namedtuple('Dateline', 'date')
    Chatline = namedtuple('Chatline', 'user text')
    Badline = namedtuple('Badline', 'text')

    l = Badline(line)

    match = is_line_date(line)
    if match:
        l = Dateline(match.group(1)) 

    match = is_line_chat(line)
    if match:
        l = Chatline(match.group(2), match.group(3)) 

    return l

# Takes in a line and a dictionary as follows
# {person's name, {word, word frequency}}
def line_word_count(line, person, word_dict):
    words = line.split()
    for word in words:
        word = word.lower() #makes everything lowercase
        word_dict[person].setdefault(word, 0)
        word_dict[person][word] += 1

    return word_dict

# Pretty self explanatory if I do say so myself
def he_says_what_how_much(he, what, where):
    print( str(he) + ' says "' + str(what) + '" ' + str(where[he].get(what, 'actually, no he dont' )))

# Really it is word density but fuck density sounds infinitely cooler
def fuck_density(word, person, word_dict):
    total_value = 0
    for value in word_dict[person].values():
        total_value += value
    try:
        return word_dict[person][word] / total_value
    except KeyError:
        return 0

# create a sliced version of the file based on start / end dates
def slice_file(start_date, end_date): 
    pass
