import sys
import re
import stackexchange
import os
import argparse
#import google

def getErrs(): 
    stderr = []
    #return re.sub('[\n]', '', sys.stdin.readlines()[-1]).strip(' ')
    for line in sys.stdin.readlines():
        stderr.append(re.sub('[\n]', '', line).strip(' '))
    return stderr[-1]


class Trace(object):

    def __init__(self, engine, trace_err, limit, temp_file=None):
        self.engine = engine
        self.trace_err = trace_err
        self.limit = limit
        if temp_file != None:
            self.temp_file = temp_file
             
    def searchSO(self, term2):
        '''
        called by getSO if StackExchange api is selected
        '''
        user_api_key = '5se*FOHNKmiw3H9miisy8w(('
        so = stackexchange.Site(stackexchange.StackOverflow, app_key = user_api_key, impose_throttling = False)
        so.throttle_stop = False
        qs = so.search_advanced(q=self.trace_err, tagged=['python'], body=term2, accepted=True)
        ql = list(qs)
        ql.sort(key = lambda x: x.score, reverse=True)
        if self.limit == None:
            self.limit = len(ql)
        raw_body = list()
        try:
            for i in range(self.limit):
                print ql[i].url
                r = so.question(ql[i].id, body=True).body
                raw_body.append(r) 
        except IndexError:
            print "terms are too tight, no pages found"
            os.remove(temp_filename)
            return None
        return raw_body

    def getCode(self, raw_body):
        '''
        called by getSO if StackExchange api is selected
        '''
        if raw_body == None:
            return 
        with open(self.temp_file, 'r') as usr_code_fi:
            usr_code = [re.sub('[\n]', '', line).strip(" ") for line in usr_code_fi]
        usr_code_fi.close()
        os.remove(self.temp_file)
        print type(raw_body[0])
        query_code = []
        for i in range(len(raw_body)):
            for j in range(50):
                return None #standin, duh
            #if "<code>" 
        so_code=[]
        for body in raw_body:
            str(body)
            x = body.split("code")
            for b in x:
                b = b.replace('&gt;','')
                print "-----------"
                if "<pre>" not in str(b) and "</pre>" not in str(b):
                    so_code.append(b)
        return [usr_code, so_code]

    def searchGoogle(self, term):
        for url in google.search(str(self.trace_err + term), stop=self.limit):
            print url
        return None
     
    def getSO(self, search_term): # replace "python" with something relevent to code? blaaaaah
        if self.engine != "google":
            self.getDiff(self.searchSO(search_term))
        else:
            self.searchGoogle(search_term)


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
    parser.add_argument('--google', '-g',
            action = 'store_true',
            help = 'search stack overflows for traceback error using Google Search. Else the StackExchange api is used.'
            )

    args = parser.parse_args()
    if args.search_term:
        search_term = args.search_term
    else:
        search_term = "python"
    if args.google:
        os.remove(args.temp_file)
        Trace("google", getErrs(), 10).getSO(search_term)
    else:
        if args.search_term:
            Trace("stack_exchange", getErrs(), None, args.temp_file).getSO(search_term)
        else:
            Trace("stack_exchange", getErrs(), 5, args.temp_file).getSO(search_term)

