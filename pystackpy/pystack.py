import sys
import re
import stackexchange
import os
import argparse
import google
import string

class Errors(object):

    def __init__(self, temp_file, limit):
        self.temp_file = temp_file
        self.limit = limit

    def checkimp(self, code = []):
        x = 0
        package = []
        for x in range(len(code) - 1):
            if code[x] == "from":
                if code[x + 2] == "import":
                    package.append(code[x + 1])
            if code[x] == "import":
                if code[x - 2] == "from":
                    continue
                package.append(code[x + 1])
        return package

    def checkif(self, code = [], checklist = []):
        x = 0
        code2 = filter(None, code)
        for x in range(len(code2) - 1):
            splitline = string.split(code2[x])
            a = len(splitline)
            #print code2[x]
            #print splitline
            if not splitline:
                continue
            if splitline[0] == 'if':
                t = list(splitline[a - 1])
                if t[len(t) - 1] == ":":
                    checklist[1] = 2
                    break
            if splitline[0] == "else:":
                checklist[1] = 2
                break
            if splitline[0] == "elif":
                checklist[1] = 2
                break
        return checklist


    def checkcl(self, code = [], checklist = []):
        x = 0
        for x in range(len(code) - 1):
            if code[x] == 'class':
                t = list(code[x + 1])
                if t[len(t) - 1] == ':':
                    checklist[2] = 1
                    break
        return checklist

    def checkfor(self, code = [], checklist = []):
        x = 0 
        for x in range(len(code) - 1):
            if code[x] == "for":
                if code[x + 2] == 'in':
                    checklist[0] = 2
                    break
        return checklist

    def checklist1(self, code = [], checklist = []):
        x = 0 
        for x in range(len(code) - 1):
            if code[x] == "=":
                t = list(code[x + 1])
                if t[0] == '[':
                    checklist[3] = 2
        return checklist

    def checkStructures(self, code = []):
        checklist = [0,0,0,0]
        checklist = self.checkif(code, checklist)
        checklist = self.checkcl(code, checklist)
        checklist = self.checkfor(code, checklist)
        checklist = self.checklist1(code, checklist)
        return checklist

    def checkVal(self, clist = []):
        val = 0
        x = 0
        for x in range(len(clist) - 1):
            val = val + clist[x]
        return val

    def listCode(self, APIcode):
        usr_code, so_code = self.getCode(APIcode)
        list_main = self.checkStructures(usr_code)
        orig_val = self.checkVal(list_main)
        IDsim_list = []
        #sim_list = []
        for key in so_code.keys():
            code = so_code[key]
            list_temp = self.checkStructures(code)
            x = 0
            simVal = 0
            for x in range(len(list_main) - 1):
                if list_main[x] == list_temp[x]:
                    simVal = simVal + 1
            IDsim_list.append((key, simVal))
        return IDsim_list

    def compare(self, APIcode):
        IDlist = self.listCode(APIcode)
        sorted(IDlist, key=lambda sim: sim[1])
        try:
            for x in range(1, self.limit):
                print 'www.stackoverflow.com/questions/' + str(IDlist[-x][0])
        except IndexError:
            pass

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
    userErrs = Errors(args.temp_file, args.limit)
    if args.file:
        trace_err = userErrs.getErrs()
    else:
        trace_err = ""
    userSearch = Search(engine='', trace_err=trace_err, limit=args.limit)
    if args.google:
        userSearch.engine = "google"
        userSearch.search(search_term)
    elif args.search and not args.file:
        userSearch.engine = "google"
        userSearch.search(search_term)
    else:
        userSearch.engine = "stack_exchange"
        userErrs.compare(userSearch.search(search_term)) 
    return None


if __name__=="__main__":
   
    main()
