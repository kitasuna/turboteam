from text_functions import *
from sys import argv
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', required=True, help='File to parse')
    parser.add_argument('-d', '--density', required=False, help='Check the density of a certain word')
    parser.add_argument('--interactive', required=False, action='store_true', help='Run in interactive mode')
    opts = parser.parse_args()
    # stole this from a tutorial
    # leaving it in in case it comes in handy
    #if not (opts.plot_file or opts.csv_file):
    #    parser.error("You have to specify either a --csv-file or --plot-file!")
    #return opts
    return opts

def main():
    current_date = False
    daily_tally = 0;
    unused_lines = 0;
    daily_lines = {}
    dude_lines = {}
    word_count = {}

    # gets our command line args
    opts = parse_args()

    with open(opts.input_file, 'r') as f:
        for line in f:

            # Figure out of this is a date or a chat entry
            l = parse_line(line)

            if type(l).__name__ == 'Dateline':
                # If current date is already set, reset the tally
                # and set a new date
                if current_date:
                    daily_lines[current_date] = daily_tally
                    current_date = l.date
                    daily_tally = 0
                else:
                    current_date = l.date
            elif type(l).__name__ == 'Chatline':
                daily_tally += 1 

                # Find who wrote this one, if anyone
                dude_name = l.user
                    #Austin fucking around here
                    #Word count is a dictionary that counts words for each person
                word_count.setdefault(dude_name,{})
                line_word_count(l.text, l.user, word_count)
                if dude_name in dude_lines:
                    dude_lines[dude_name] += 1
                else:
                    dude_lines[dude_name] = 1
            else:
                print('No match for "', line, '"');
                unused_lines += 1

        # Write out the last day
        if current_date:
            daily_lines[current_date] = daily_tally
        
        print('Line count is ' + str(file_len(opts.input_file)))
        print('sum of daily line count is', str(sum(daily_lines.values())))
        print('sum of dude line count is', str(sum(dude_lines.values())))
        print('unused line count is', unused_lines)
        print(daily_lines)
        print(dude_lines)

        
        # Fuck density!
        if(opts.density):
            for dude in word_count:
                print(dude + "'s " + opts.density + " density is: " + str(fuck_density(opts.density,dude,word_count)))

        # Lists dudes to make console input easy
        for dude in word_count:
            print(dude)

        if(opts.interactive):
            while input('Stay ') != 'no':
                    he_says_what_how_much(input('Who? '),input('What? (lowercase) '),word_count)
#Commented code prints everything. Ridiculously long and not useful at all.
#for people in word_count:
#           print('***********************' + str(people) + ' says')
#           print(word_count[people].items())

main()

