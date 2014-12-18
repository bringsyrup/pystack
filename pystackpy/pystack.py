import sys
import re
import stackexchange
import os
import argparse
import google

class Errors(object):

    def __init__(self, temp_file):
        self.temp_file = temp_file

    def HarshMethod(self, APIraw):
        #print APIraw
        try:
            usr_code, so_code = self.getCode(APIraw) #so_code is a dictionary {key: val...} ==> {ID: bodyCodeList...}
            #print usr_code, so_code
        except TypeError:
            return None
        return None

    def getErrs(self): 
        stderr = []
        for line in sys.stdin.readlines():
            stderr.append(re.sub('[\n]', '', line).strip(' '))
        return stderr[-1]

    def getCode(self, raw_body):
        '''
        called by search if StackExchange api is selected and there's a file. move to Errors class soon
        '''
        if len(raw_body) < 1:
            print "No search results"
            return None
        else:
            with open(self.temp_file, 'r') as usr_code_fi:
                usr_code = [re.sub('[\n]', '', line).strip(" ") for line in usr_code_fi]
            usr_code_fi.close()
            os.remove(self.temp_file)
            so_code=dict()
            for body in raw_body:
                ln = str()
                x = str(raw_body[body])
                x = x.split("code")
                for b in x:
                    b = b.replace('&gt;','')
                    if "<pre>" not in str(b) and "</pre>" not in str(b) and "p>" not in str(b):
                        ln=ln+str(b)+"\n"
                so_code[body] = ln.split("\n")                
            return usr_code, so_code


class Search(object):

    def __init__(self, engine, trace_err, limit):
        self.engine = engine
        self.trace_err = trace_err
        self.limit = limit

    def filterResults(self, resultlist):
        user_api_key = '5se*FOHNKmiw3H9miisy8w(('
        so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key)
        if len(resultlist) > 0:
            raw_body = dict()
            for result in resultlist:
                raw_body[result] = so.question(result, body=True).body
            return raw_body
        else:
            return None

    def searchGoogle(self, term, SO_filter):
        id_list = list()
        for url in google.search(str(self.trace_err + term), stop=self.limit):
            if SO_filter:
                if "http://stackoverflow.com/questions" in url:
                    id_list.append(url[35:43])
            else:
                print url
        if SO_filter:
            return self.filterResults(id_list)
        #return None


    def search(self, search_term): 
        if self.engine == "google":
            SO_filter = False
        else:
            SO_filter = True
        return self.searchGoogle(search_term, SO_filter)
        #return None

def main():
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
    parser.add_argument('-l', '--limit',
            type=int,
            action = 'store'
            )
    args = parser.parse_args()
    if args.search_term:
        search_term = args.search_term
    else:
        search_term = "python"
    userErrs = Errors(args.temp_file)
    if args.file:
        trace_err = userErrs.getErrs()
    else:
        trace_err = ""
    userSearch = Search(engine='', trace_err=trace_err, limit=args.limit)
    if args.google:
        userSearch.engine = "google"
        userSearch.search(search_term)
    else:
        userSearch.engine = "stack_exchange"
        userErrs.HarshMethod(userSearch.search(search_term)) 
    return None


if __name__=="__main__":
   
    main()
