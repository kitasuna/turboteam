# Counts the number of lines in a text file
from sys import argv

script, input_file = argv

# from SilentGhost link- http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

print('Line count is ' + str(file_len(input_file)))

#ALTERNATIVELY
#from Kyle in same post in comments
num_lines = sum(1 for line in open(input_file))
print('Line count is ' + str(num_lines))


