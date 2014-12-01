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

def searchSO(term1, term2, limit):
    user_api_key = '5se*FOHNKmiw3H9miisy8w(('
    so = stackexchange.Site(stackexchange.StackOverflow, app_key = user_api_key, impose_throttling = False)
    so.throttle_stop = False
    qs = so.search_advanced(q=term1, tagged=['python'], body=term2, accepted=True)
    ql = list(qs)
    ql.sort(key=lambda x: x.score, reverse=True)
    if limit == None:
        limit = len(ql)
    raw_body = list()
    try:
        for i in range(limit):
            print ql[i].url
            r = so.question(ql[i].id, body=True).body
            raw_body.append(r) 
    except IndexError:
        print "terms are too tight, no pages found"
        os.remove(temp_filename)
        return None
    return raw_body

def getDiff(temp_filename, raw_body):
    if raw_body == None:
        return 
    with open(temp_filename, 'r') as usr_code_fi:
        usr_code = [re.sub('[\n]', '', line).strip(" ") for line in usr_code_fi]
    usr_code_fi.close()
    os.remove(temp_filename)
    print type(raw_body[0])
    query_code = []
    for i in range(len(raw_body)):
        for j in range(50):
            print raw_body[i][j]
        #if "<code>" 
    return usr_code
 
def getSO(fi_name, limit=None, term2="python"): # replace "python" with something relevent to code? blaaaaah
    getDiff(fi_name, searchSO(getErrs(), term2, limit))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='pystack')
    parser.add_argument('temp_file',
            type = str, 
            help = 'filename for the temp file used to get users python code'
            )
    parser.add_argument('search_term',
            type = str, 
            nargs = '?',
            help = 'optional search term string!'
            )
    args = parser.parse_args()
    if args.search_term:
        getSO(fi_name=args.temp_file, term2=args.search_term)
    else:
        getSO(fi_name=args.temp_file, limit=5)

