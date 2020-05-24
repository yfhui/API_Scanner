import threading,requests,time,sys,itertools,string,json
from queue import Queue

#log and analyses the response
def analyseResponse(method,URL,port,status=None,errMsg=""):
    global proxy
    if(status in settings['allowedStatusCodes']):
        #write the result file
        with writeLock:
            result.write(method+"%%"+URL+"%%"+str(status)+"%%"+port+"\n")
    #change the proxy when return with codes
    if settings['proxiesOnChangeMode']:
        if(status in settings['statusCodesChangeProxy']):
            #if there's no more proxies in the list then we don't change the proxy
            if(len(settings['proxiesList'])==0):
                if settings['printErr']:
                    with printLock:
                        print("no more proxies avavilable")
                        return
            #get the first proxy in the list and remove it from list
            proxy = settings['proxiesList'].pop(0)  


#concat the doamin path and port to become URL
def prepareURL(path,port):
    domain = settings['domain']
    #remove the ending "/" if there's one
    if(domain[-1]=="/"):
        domain = domain[:-1]
    #replace the http scheme to https when it's a port 443
    if(port=="443"):
        scheme="https://"
    else:
        scheme="http://"
    #remove the starting "/" on the path
    if(len(path)>0 and path[0]=="/"):
        path = path[1:]
    url = scheme + domain + ":" + port + "/" + path
    return url

#send the requestion with path using global doamin
def sendRequest(path,port="80"):
    URL = prepareURL(path,port)
    for method in settings['HTTPmethods']:
        try:
            if settings['printLog']:
                with printLock:
                    print(method+":"+URL)
            response = getattr(requests,method)(URL,timeout=settings['timeOut'],proxies=proxy)
            analyseResponse(method,URL,port,response.status_code)
        except requests.exceptions.RequestException as e:
            if settings['printErr']:
                with printLock:
                    print(e)

#the search on the word will be extended to some common file names
def extendedSearch(urlWord,port="80"):
    for filename in settings['extendedSearchModeSetting']['commonFileNames']:
        for suffix in settings['extendedSearchModeSetting']['commonFileSuffixs']:
            sendRequest(urlWord+"/"+filename+"."+suffix,port)

#search function that will call differnet functions on different mode
def searchRunner(urlWord,port="80"):
    sendRequest(urlWord,port)
    if(settings['extendedSearchMode']==True):
        extendedSearch(urlWord,port)
    if(settings['versionedSearchMode']==True):
        for l in settings['versionedSearchModeSetting']['verionNameList']:
            sendRequest(urlWord+"/"+l,port)
            if(settings['versionedSearchMode']==True and settings['extendedSearchMode']==True):
                extendedSearch(urlWord+"/"+l,port)

#threader function to search on the urlword
def searchOnWordThreader(urlWord,portQueue):
    while True:
        if(portQueue.empty()):
            break
        port = portQueue.get()
        searchRunner(urlWord,port)
        portQueue.task_done()

#search on a URL word, and handle ports scanning
#threads are created to increase the performance
def searchOnWord(urlWord):
    portQueue = Queue()
    #scann all the possible ports
    if(settings['portScanningMode']==True):
        for port in range(1,65535):    #TCP port start from 1 to 65535
            portQueue.put(str(port))

    #only scan the basic 80 and 443 ports when port scanning mode is off
    if(settings['portScanningMode']==False):
        portQueue.put(str(80))
        if(settings['httpsMode']==True):
            portQueue.put(str(443))

    #create threadsToScanPort number of threads to run
    for _ in range(settings['threadsToScanPort']):
        t = threading.Thread(target=searchOnWordThreader,args=(urlWord,portQueue,))
        t.daemon = True
        t.start()

    #wait until all ports are searched
    portQueue.join()

#threader function to get word from the queue and search on the word
def searchAPIThreader():
    while True:
        if(wordQueue.empty()):
            break
        word = wordQueue.get()
        searchOnWord(word)
        wordQueue.task_done()

#searching on a word list
#threads are created to increase the performance
def searchAPI(wordList):
    #put all the words in to the queue for the thread to run
    for word in wordList:
        wordQueue.put(word)

    #create threadsToScanWord number of threads to run
    for _ in range(settings['threadsToScanWord']):
        t = threading.Thread(target=searchAPIThreader)
        t.daemon = True
        t.start()
    
    #wait until all words are searched
    wordQueue.join()

#generate all the combination of list
def generateWordList(l,size):
    return [''.join(j) for j in itertools.product(l, repeat=size)]

#get the word list 
def getWordList():
    #if now is brute force mode then we generate the wordlist
    if(settings['bruteForceMode']==True):
        #an empty path is also in the bruteforce wordlist
        resultList = [""]
        stringToBruteForce = settings['bruteForceModeSetting']['bruteForceString']
        sizeOfWord = settings['bruteForceModeSetting']['sizeOfWord']
        for x in generateWordList(stringToBruteForce,sizeOfWord):
            resultList.append(''.join(x))
    else:
        #else we read from file
        with open(settings['inputFileName']) as f:
            lines = f.read().splitlines()
            resultList = lines
    return resultList

#read the settings from the file, do not check the correctness of the file
def readSetting():
    global proxy
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    if(settings['bruteForceModeSetting']['bruteForceString']==None):
        settings['bruteForceModeSetting']['bruteForceString']= string.ascii_lowercase+string.ascii_uppercase+string.digits
    if(settings['alwaysUseProxy']):
        if(len(settings['proxiesList'])==0):
            print("no proxies in the proxy list!")
            exit(1)
        else:
            proxy = settings['proxiesList'].pop(0) 
    return settings

#main
if(__name__=='__main__'):
    #read settings from setting.json
    proxy={}                        #proxy that is used(empty means use no proxy)
    settings = readSetting()

    #for multithreading in the scanner on different words
    printLock = threading.Lock()    #lock for printing
    writeLock = threading.Lock()    #lock for writting result to the file
    wordQueue = Queue()             #queue to store on words
                     
    #open a file to output the result
    result = open(settings['outputFileName'], "w")

    #count the program running time
    timeStart = time.time()
    wordList = getWordList()
    searchAPI(wordList)
    print("time used: "+str(time.time()-timeStart))

    #close the result file
    result.close()
