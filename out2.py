import sys
import re
import stackexchange

def getErrs():
    stderr = []
    for line in sys.stdin.readlines():
        err = re.sub('[\n]', '', line)
        stderr.append(err.strip(" "))
    return stderr[-1]

def parseErrs():
    stderr = getErrs()
    errRoot = stderr[-1]
    if "TypeError" in errRoot:
        print errRoot
    elif "IndexError" in errRoot:
        print errRoot
    elif "NameError" in errRoot:
        print errRoot
    elif "UnboundLocalError" in errRoot:
        print errRoot


if __name__=="__main__":
    parseErrs()