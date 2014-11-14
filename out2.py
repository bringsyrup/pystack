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
        
def searchso(term1,term2):
    user_api_key = '5se*FOHNKmiw3H9miisy8w(('
    so = stackexchange.Site(stackexchange.StackOverflow, app_key = user_api_key, impose_throttling = True)
    qs = so.search_advanced(q=term1, tagged=['python'], body=term2)
    for q in qs:
        print(q.id, q.title)

if __name__=="__main__":
    parseErrs()