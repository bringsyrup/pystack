import sys
import re
import stackexchange
import os
import argparse
import google

class Errors(object):

    def __init__(self, temp_file):
        self.temp_file = temp_file

    def getErrs(self): 
        stderr = []
        #return re.sub('[\n]', '', sys.stdin.readlines()[-1]).strip(' ')
        for line in sys.stdin.readlines():
            stderr.append(re.sub('[\n]', '', line).strip(' '))
        return stderr[-1]

    def getCode(self, raw_body):
        '''
        called by getSO if StackExchange api is selected and there's a file. move to Errors class soon
        '''
        if raw_body == None:
            print "No search results"
            return 
        with open(self.temp_file, 'r') as usr_code_fi:
            usr_code = [re.sub('[\n]', '', line).strip(" ") for line in usr_code_fi]
        usr_code_fi.close()
        os.remove(self.temp_file)
        so_code=[]
        for body in raw_body:
            str(body)
            x = body.split("code")
            for b in x:
                b = b.replace('&gt;','')
                #print "-----------"
                if "<pre>" not in str(b) and "</pre>" not in str(b):
                    so_code.append(b)
        return [usr_code, so_code]


class Search(object):

    def __init__(self, engine, trace_err, limit):
        self.engine = engine
        self.trace_err = trace_err
        self.limit = limit
             
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
        if not self.limit:
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


    def searchGoogle(self, term):
        for url in google.search(str(self.trace_err + term), stop=self.limit):
            print url
        return None
     
    def getSO(self, search_term, userErrs=None): 
        if self.engine == "google":
            self.searchGoogle(search_term)
        else:
            if userErrs:
                userErrs.getCode(self.searchSO(search_term))
            else:
                self.searchSO(search_term)



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
        if args.google:
            limit = 10
        else:
            limit = None
    else:
        search_term = "python"
        limit = 10
    
    userErrs = Errors(args.temp_file) 

    if args.file:
        trace_err = userErrs.getErrs()
    else:
        trace_err = ""
        
    userSearch = Search(engine='', trace_err=trace_err, limit=limit)

    if args.google:
        userSearch.engine = "google"
        userSearch.getSO(search_term)
    else:
        userSearch.engine = "stack_exchange"
        if args.search_term:
            userSearch.getSO(search_term)
        else:
            userSearch.getSO(search_term, userErrs=userErrs)

