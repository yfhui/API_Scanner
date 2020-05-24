# What can it do?

* access website and try to find if there's hidden website/api

* if some url of a domain returns 200OK that means it's very possible that it is an api

* you can supply some keywords for the searcher to search or you can use bruteforce mode to search some combination of paths

* there's a chance that the domain will block your ip, automatically switching to other proxise function is provided

# Things you need to know before using it

* you have to provide a list of possible words for the program to access, that means you have to know the domain you want to search, e.g. on domain in Spotify then the possible word list will have [album,song,singer]
* you can write your own program to generate the list of possible words you want
* the output contain list of url that return some positive response, you can write other program to phrase or process it
* make sure the setting file is in correct format, no checker for the format file

# Something special about this program

* extended searching mode: search on some program scripts, not just accessing the directory itself. E.g. domain/api/api.php
* versioned searching mode: searching path will append a versioned path. e.g. domain/v1/api.php. Many public api has this feature.
* http methods: it provides many methods, some api maybe unable to access on "GET" but able to access on "POST". different HTTP accessing methods are provided
* port scanning mode: not just scan the standard 80 port, it also scan all the ports
* https mode: scan both port 443 and 80(if port scanning and https mode is off, then it always search port 80)
* threads: you can adjust the number of threads to scan ports and scan words. If you have a long list of words, but do not do port scanning, then you should set more threads to search on word, and fewer threads to search on port. Vice versa, if you have port scanning activated, you should have more port scanning threads

------

### Setting file explanation
domain = domain that we want to search

inputFileName = the file that contains all the possible word list

portScanningMode = search all the ports

HTTPmethods = HTTP methods to work with

allowedStatusCodes = response that is possible an api will return

httpsMode = search both port 80 and 443

timeOut = request time out time, when request wait excess this time then we will give up on the request

threadsToScanPort = number of threads to scan the ports

threadsToScanWord = number of threads to scan the words

##### total number of threads = threadsToScanPort x threadsToScanWord

versionedSearchMode = search on the version code e.g. doamin/v1/{path}

verionNameList = version name to be searched

bruteForceMode = auto generate some words to search, do not read from file

sizeOfWord = size of the word generated when using brute force

bruteForceString = the characters that will be permutated to generate the word, when it's null, then it's all digits+upper letters and lower case letters

extendedSearchMode = search on common files name beside the path itself, e.g. doamin/path/index.js

commonFileNames = common file name in a server

commonFileSuffixs = common programming language suffix of file

printLog = print the log when searching, i.e. URL that accessing

printErr = print error message when searching

proxiesOnChangeMode = change the proxy when the response status code is some status codes, e.g. 403

alwaysUseProxy = it will use proxy in the list automatically when start, if it's false, we don't use proxy unless it hit the condition that some response status codes are the one in statusCodesChangeProxy

statusCodesChangeProxy = the status code that we will change proxy

proxiesList = proxy that is going to be used in the request                                                           
