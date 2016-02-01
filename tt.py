import re
from sys import argv

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def main():
    script, filename = argv
    date_pattern = re.compile('^(\d+/\d+/\d+)')
    dude_pattern = re.compile('^(\d+:\d+\t(.+)\t(.+))')
    current_date = False
    daily_tally = 0;
    unused_lines = 0;
    daily_lines = {}
    dude_lines = {}
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

main()
