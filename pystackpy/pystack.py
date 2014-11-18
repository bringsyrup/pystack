import sys
import re
import stackexchange
import os
import argparse

def getErrs():
    stderr = []
    for line in sys.stdin.readlines():
        stderr.append(re.sub('[\n]', '', line).strip(" "))
    return stderr[-1]

def getDiff():
    userCode = list()
    with open("pystack.txt.tmp", 'r') as userCodeFi:
        for line in userCodeFi:
            userCode.append(re.sub('[\n]', '', line).strip(" "))
    userCodeFi.close()
    os.remove("pystack.txt.tmp")
    return userCode
           
#def parseErrs():
#    stderr = getErrs()
#    errRoot = stderr[-1]
#    if "TypeError" in errRoot:
#        print errRoot
#    elif "IndexError" in errRoot:
#        print errRoot
#    elif "NameError" in errRoot:
#        print errRoot
#    elif "UnboundLocalError" in errRoot:
#        print errRoot

def searchSO(term1,term2, limit):
    print term1, term2
    user_api_key = '5se*FOHNKmiw3H9miisy8w(('
    so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key, impose_throttling=False)
    so.throttle_stop = False
    qs = so.search_advanced(q=term1, tagged=['python'], body=term2)
    #for q in qs:
    #    r = so.question(q.id, body=True, filter="!b0OfMwwD.s*79x") 
    ql = list(qs)
    ql.sort(key=lambda x: x.score, reverse=True)
    for i in range(limit):
        print ql[i].url

def getSO(limit, term2):
    searchSO(getErrs(), term2, limit)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='pystack')
    parser.add_argument('search_term',
            type = str, 
            nargs = '?',
            help = 'optional search term string!'
            )
    args = parser.parse_args()
    getSO(5, args.search_term)
    
    getDiff()

