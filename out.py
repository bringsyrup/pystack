import sys

stderr = []
for line in sys.stdin.readlines():
    stderr.append(line)
print stderr
