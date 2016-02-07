import re
from sys import argv
import sys

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

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

def main():
    script, filename = argv
    date_pattern = re.compile('^(\d+/\d+/\d+)')
    dude_pattern = re.compile('^(\d+:\d+\t(.+)\t(.+))')
    current_date = False
    daily_tally = 0;
    unused_lines = 0;
    daily_lines = {}
    dude_lines = {}
    word_count = {}
    with open(filename, 'r') as f:
        for line in f:

            # Don't even bother if the line is all whitespace
            if not line.strip():
                unused_lines += 1
                continue

            match = date_pattern.match(line)
            if match:
                if current_date:
                    daily_lines[current_date] = daily_tally
                current_date = match.group(1)
                daily_tally = 0
            else:
                daily_tally += 1 

                # Find who wrote this one, if anyone
                dude_match = dude_pattern.match(line)
                if dude_match:
                    dude_name = dude_match.group(2);
                        #Austin fucking around here
                        #Word count is a dictionary that counts words for each person
                    word_count.setdefault(dude_name,{})
                    line_word_count(line, dude_name, word_count)
                    if dude_name in dude_lines:
                        dude_lines[dude_name] += 1
                    else:
                        dude_lines[dude_name] = 1
                else:
                    print('No match for', line);
                    unused_lines += 1



            # Write out the last day
            if current_date:
                daily_lines[current_date] = daily_tally
        
        print('Line count is ' + str(file_len(filename)))
        print('sum of daily line count is', str(sum(daily_lines.values())))
        print('sum of dude line count is', str(sum(dude_lines.values())))
        print('unused line count is', unused_lines)
        print(daily_lines)
        print(dude_lines)
        
        #Fuck density!
        for dude in word_count:
            print(dude + "'s fuck density is: " + str(fuck_density('fuck',dude,word_count)))
        #Lists dudes to make console input easy
        for dude in word_count:
            print(dude)

        while input('Stay ') != 'no':
                he_says_what_how_much(input('Who? '),input('What? (lowercase) '),word_count)
#Commented code prints everything. Ridiculously long and not useful at all.
#for people in word_count:
#           print('***********************' + str(people) + ' says')
#           print(word_count[people].items())

main()
