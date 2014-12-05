import sys
import re
import stackexchange
import os
import argparse
import google

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
        self.temp_file = temp_file
             
    def searchSO(self, term2):
        '''
        called by getSO if StackExchange api is selected
        '''
        user_api_key = '5se*FOHNKmiw3H9miisy8w(('
        so = stackexchange.Site(stackexchange.StackOverflow, app_key = user_api_key, impose_throttling = False)
        so.throttle_stop = False
        if self.trace_err:
            qs = so.search_advanced(q=self.trace_err, tagged=['python'], body=term2, accepted=True)
        else:
            qs = so.search_advanced(q=term2, tagged=['python'], body=term2, accepted=True)
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
            if self.trace_err:
                os.remove(temp_filename)
            return None
        return raw_body

    def getDiff(self, raw_body):
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
        return usr_code

    def searchGoogle(self, term):
        for url in google.search(str(self.trace_err + term), stop=self.limit):
            print url
        return None
     
    def getSO(self, search_term=None): # replace "python" with something relevent to code? blaaaaah
        if self.engine != "google":
            if self.temp_file:
                self.getDiff(self.searchSO(search_term))
            else:
                self.searchSO(search_term)
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
    parser.add_argument('-f', '--file',
            action = 'store_true',
            help = 'if present, indicates whether or not to call getErrs()'
            )
    parser.add_argument('-g', '--google',
            action = 'store_true',
            help = 'search stack overflows for traceback error using Google Search. Else the StackExchange api is used.'
            )

    args = parser.parse_args()

    if args.search_term:
        search_term = args.search_term
    else:
        search_term = "python"
    
    if args.file:
        user_errs = getErrs()
    else:
        user_errs = ""
        args.temp_file = None
        
    if args.google:
        Trace("google", user_errs, 10).getSO(search_term)
    else:
        if args.search_term:
            Trace("stack_exchange", user_errs, None, args.temp_file).getSO(search_term)
        else:
            Trace("stack_exchange", user_errs, 5, args.temp_file).getSO(search_term)

