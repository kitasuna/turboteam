from text_functions import *
from sys import argv
from datetime import datetime
from linelog import LineLog
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', required=True, help='File to parse')
    parser.add_argument('-d', '--density', required=False, help='Check the density of a certain word')
    parser.add_argument('-sd', '--start-date', required=False, help='Date to start parsing from. Inclusive.')
    parser.add_argument('-ed', '--end-date', required=False, help='Date to end parsing from. Inclusive.')
    parser.add_argument('--interactive', required=False, action='store_true', help='Run in interactive mode')
    opts = parser.parse_args()
    # stole this from a tutorial
    # leaving it in in case it comes in handy
    #if not (opts.plot_file or opts.csv_file):
    #    parser.error("You have to specify either a --csv-file or --plot-file!")
    #return opts
    return opts

def main():
    daily_tally = 0
    unused_lines = 0
    current_date = False
    daily_lines = {}
    user_lines = {}
    word_count = {}

    # gets our command line args
    opts = parse_args()

    # set up our log file object
    logfile = LineLog(opts.input_file)

    # make sure our dates (if we have them) parse correctly
    if(opts.end_date):
        try:
            end_date = datetime.strptime(opts.end_date, "%Y/%m/%d")
            logfile.set_end_date(end_date)
        except ValueError:
            end_date = None


    # make sure our dates (if we have them) parse correctly
    if(opts.start_date):
        try:
            start_date = datetime.strptime(opts.start_date, "%Y/%m/%d")
            logfile.advance_to(start_date)
        except ValueError:
            start_date = None

    while logfile.current_line < logfile.num_lines:

        l = logfile.get_next_line()
        
        if logfile.current_date != current_date:
            daily_lines[logfile.current_date.strftime('%Y/%m/%d')] = 0
            current_date = logfile.current_date

        if type(l).__name__ == 'Chatline':
            daily_lines[logfile.current_date.strftime('%Y/%m/%d')] += 1

            # Find who wrote this one, if anyone
            user_name = l.user

            #Word count is a dictionary that counts words for each person
            word_count.setdefault(user_name,{})
            line_word_count(l.text, l.user, word_count)
            if user_name in user_lines:
                user_lines[user_name] += 1
            else:
                user_lines[user_name] = 1
        elif type(l).__name__ == 'Badline':
            #print('No match for "', l.text, '"');
            unused_lines += 1

        # Write out the last day
        #if current_date:
        #    daily_lines[current_date] = daily_tally
        
    print('Line count is ' + str(file_len(opts.input_file)))
    print('sum of daily line count is', str(sum(daily_lines.values())))
    print('sum of user line count is', str(sum(user_lines.values())))
    print('unused line count is', unused_lines)
    print("Chat lines per day: " + str(daily_lines))
    print("Chat lines per user: " + str(user_lines))

    
    # Word density!
    if(opts.density):
        for user in word_count:
            print(user + "'s " + opts.density + " density is: " + str(word_density(opts.density,user,word_count)))

    # Lists users to make console input easy
    # for user in word_count:
    print('Users: ' + " | ".join(word_count))

    if(opts.interactive):
        while input('Stay ') != 'no':
            he_says_what_how_much(input('Who? '),input('What? (lowercase) '),word_count)

main()

