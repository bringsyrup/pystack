import sys
import re
import stackexchange

def getErrs():
    stderr = []
    for line in sys.stdin.readlines():
        #err = re.sub('[\n]', '', line)
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

def searchSO(term1,term2, limit):
    user_api_key = '5se*FOHNKmiw3H9miisy8w(('
    so = stackexchange.Site(stackexchange.StackOverflow, app_key = user_api_key, impose_throttling = False)
    so.throttle_stop = False
    qs = so.search_advanced(q=term1, tagged=['python'], body=term2)
    #for q in qs:
    expanded_q = []
    # counter = 0
    # for q in qs:
    #     print q.url
    #     counter = counter + 1
    # print counter
    for q in qs:
        r = so.question(q.id, body = True, filter = "!b0OfMwwD.s*79x") 
        expanded_q.append(r)
    for i in range(limit):
        q = so.question(qs[i].id, body=True, filter = "!b0OfMwwD.s*79x")
        expanded_q.append(q)
    expanded_q.sort(key=lambda x: x.up_vote_count, reverse=True)
    for i in range(limit):
        print expanded_q[i].url
def getSO(limit):
    searchSO(getErrs(), 'tuple', limit)

if __name__=="__main__":
    getSO(5)
