#import sys
#print " ".join(sys.argv)

errors = []
with open(".out.txt~", 'r') as outFile:
    for line in outFile:
        errors.append(line)

print errors
