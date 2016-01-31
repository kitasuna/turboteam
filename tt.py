# hey fool
import re

def main():
    filename = 'turboteam_mini.txt'
    date_pattern = re.compile('^(\d+/\d+/\d+)')
    dude_pattern = re.compile('^(\d+:\d+\t(.+)\t(.+))')
    current_date = False
    daily_tally = 0;
    daily_tallies = {}
    dude_tallies = {}
    with open(filename, 'r') as f:
        for line in f:
            match = date_pattern.match(line)
            if match:
                if current_date:
                    daily_tallies[current_date] = daily_tally
                current_date = match.group(1)
                daily_tally = 0
            else:
                daily_tally += 1 

                # Find who wrote this one, if anyone
                dude_match = dude_pattern.match(line)
                if dude_match:
                    dude_name = dude_match.group(2);
                    if dude_name in dude_tallies:
                        dude_tallies[dude_name] += 1
                    else:
                        dude_tallies[dude_name] = 1

            # Write out the last day
            if current_date:
                daily_tallies[current_date] = daily_tally
        
        print(daily_tallies)
        print(dude_tallies)

main()
